# Marker Extraction (Fallback via pdftotext -layout)

*Note: Marker (VikParuchuri/marker) was not available in this environment
(requires torch + heavy vision-transformer weights; not installed per the
"free endpoints only / no heavy install" constraint of this replication wave).
This extraction was produced via `pdftotext -layout` from the arXiv PDF as a
faithful text fallback. The full plain-text extraction of the paper follows.*

**Source:** `paper.pdf` — arXiv:2401.06240v3 (Low & Su, 26 Mar 2026) —
"Quantum eigenvalue processing"

---

                                                                    Quantum eigenvalue processing
                                                                               Guang Hao Low1 and Yuan Su2

                                                                                              Abstract
                                                       Many problems in linear algebra require processing eigenvalues of the input matrices. As
                                                  eigenvalues are different from singular values for non-normal operators, these problems are out
                                                  of reach of the existing quantum singular value algorithm and its descendants.




arXiv:2401.06240v3 [quant-ph] 26 Mar 2026
                                                       We present a Quantum EigenValue Estimation (QEVE) algorithm and a Quantum Eigen-
                                                  Value Transformation (QEVT) algorithm that estimate and transform eigenvalues of high-
                                                  dimensional matrices accessed by a quantum computer through block encoding oracles. We
                                                  focus on input matrices with real spectra and Jordan forms—a broad class of operators that can
                                                  describe non-Hermitian physics and transcorrelated quantum chemistry. However, our technique
                                                  also handles general non-normal matrices with complex eigenvalues, and our method remains
                                                  efficient even when the Jordan basis is ill conditioned.
                                                       Our QEVE estimates an eigenvalue of a diagonalizable matrix using O (ακ/ϵ log(1/p)) queries
                                                  to its block encoding and a unitary preparing the corresponding eigenstate, in terms of error
                                                  ϵ, failure probability p, normalization factor α of the block encoding, and condition number κ
                                                  of its basis transformation. This solves the eigenvalue estimation problem for a broad class of
                                                  non-normal matrices with the Heisenberg-limited scaling, which naturally reduces to the op-
                                                  timal estimation of singular values that has long been known. Our approach is conceptually
                                                  simple, based on reductions to the optimal scaling quantum linear system algorithm, improving
                                                  over prior approaches using differential equation solvers which are polylogarithmic away from
                                                  optimum.
                                                       Our QEVT implements transformations on eigenvalues of the input matrix through the
                                                  Chebyshev and Faber approximations. As these expansions provide a close-to-best uniform
                                                  polynomial approximation of functions over the complex plane, the query complexity of QEVT
                                                  is expected to be nearly optimal. In particular, our eigenvalue algorithm achieves a performance
                                                  comparable to previous singular value transformation results for the special case of Hermitian
                                                  inputs, where eigenvalues coincide with singular values in magnitude.
                                                       As an application, we present a quantum differential equation algorithm based on QEVT,
                                                  whose query complexity scales strictly linear in the evolution time t for an average-case diagonal-
                                                  izable input with imaginary spectra, whereas the best previous approach has a complexity with
                                                  an extra multiplicative polylog(t) factor. We also develop a quantum algorithm for preparing
                                                  the ground state of matrices with real spectra, which reduces to the nearly optimal result for
                                                  Hermitian Hamiltonians from previous work.
                                                       Underlying both QEVE and QEVT is an efficient quantum algorithm for preparing the
                                                  Chebyshev history state through its matrix generating function, encoding Chebyshev polynomi-
                                                  als of the input matrix in quantum superposition, which may be of independent interest. Prior
                                                  to our work, it was known how to efficiently create such a state only for Hermitian inputs. We
                                                  then extend this result to prepare the Faber history state, achieving efficient eigenvalue trans-
                                                  formation over the complex plane. Independently, we develop techniques to generate n Fourier
                                                  coefficients using O(polylog(n)) gates, improving over prior approaches with a cost of Θ(n).
                                                       Our result thus provides a unifying framework for processing eigenvalues of matrices on a
                                                  quantum computer.

                                                This is an enhanced version of the paper entitled Quantum eigenvalue processing presented at the 65th IEEE
                                            Symposium on Foundations of Computer Science [63] and published in the SIAM Journal on Computing [64].
                                                1
                                                  Azure Quantum, Microsoft, Redmond, WA 98052, USA. Now at Google Quantum AI, Venice, CA 90291, USA.
                                                2
                                                  Azure Quantum, Microsoft, Redmond, WA 98052, USA. Now at the AWS Center for Quantum Computing,
                                            Pasadena, CA 91106, USA.


                                                                                                  1
Contents
1 Introduction                                                                                        4
  1.1 Eigenvalue processing . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4
  1.2 Chebyshev history state generation . . . . . . . . . . . . . . . . . . . . . . . . . . . . 5
  1.3 Quantum eigenvalue estimation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9
  1.4 Quantum eigenvalue transformation . . . . . . . . . . . . . . . . . . . . . . . . . . . 10
  1.5 Applications . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13
  1.6 Eigenvalue processing over the complex plane . . . . . . . . . . . . . . . . . . . . . . 15

2 Preliminaries                                                                                        18
  2.1 Notation and terminology . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       18
  2.2 Chebyshev and Fourier expansions . . . . . . . . . . . . . . . . . . . . . . . . . . . .         20
  2.3 Matrix decompositions and transformations . . . . . . . . . . . . . . . . . . . . . . .          25
  2.4 Block encoding . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     31

3 Chebyshev history state generation                                                                   35
  3.1 Matrix Chebyshev generating function . . . . . . . . . . . . . . . . . . . . . . . . . .         35
  3.2 Block encoding implementation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .        39
  3.3 Summary of Chebyshev history state generation . . . . . . . . . . . . . . . . . . . . .          42

4 Quantum eigenvalue estimation                                                                        44
  4.1 Centered modulus and its properties . . . . . . . . . . . . . . . . . . . . . . . . . . .        44
  4.2 Chebyshev state phase estimation . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       46
  4.3 Analysis of imperfect eigenstate . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     50
  4.4 Summary of quantum eigenvalue estimation . . . . . . . . . . . . . . . . . . . . . . .           53

5 Quantum eigenvalue transformation                                                        54
  5.1 Summary of quantum eigenvalue transformation . . . . . . . . . . . . . . . . . . . . 55
  5.2 Summary of quantum eigenvalue transformation, block encoded version . . . . . . . 57

6 Fourier coefficients generation                                                                      59
  6.1 Fourier coefficients generation with frequency domain convolution . . . . . . . . . . .          59
  6.2 Block encoding Riemann integrals . . . . . . . . . . . . . . . . . . . . . . . . . . . .         60
  6.3 Rescaling principle for Riemann integrals . . . . . . . . . . . . . . . . . . . . . . . .        64
  6.4 Summary of Fourier coefficients generation . . . . . . . . . . . . . . . . . . . . . . . .       66

7 Applications                                                                                  69
  7.1 Quantum algorithm for linear differential equations . . . . . . . . . . . . . . . . . . . 69
  7.2 Quantum algorithm for ground state preparation . . . . . . . . . . . . . . . . . . . . 73

8 Eigenvalue processing over the complex plane                                                         77
  8.1 Preliminaries on Faber expansion . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       78
  8.2 Faber history state generation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     81
  8.3 Quantum eigenvalue transformation, Faber version . . . . . . . . . . . . . . . . . . .           86
  8.4 Applications . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .   87

9 Discussion                                                                                           90
A Analysis of Chebyshev-based algorithms                                                        93
  A.1 Matrix exponential bound based on spectral abscissa . . . . . . . . . . . . . . . . . .   93
  A.2 Matrix polynomial bound with Bernstein’s theorem . . . . . . . . . . . . . . . . . . .    94
  A.3 Average-case analysis with Carleson-Hunt theorem . . . . . . . . . . . . . . . . . . .    96

B Analysis of Faber-based algorithms                                                          99
  B.1 Matrix exponential bound based on numerical abscissa . . . . . . . . . . . . . . . . . 99
  B.2 Matrix function bound with Crouzeix-Palencia theorem . . . . . . . . . . . . . . . . 100
  B.3 Matrix function bound based on pseudospectrum . . . . . . . . . . . . . . . . . . . . 103
  B.4 Average-case analysis with Carleson-Hunt theorem . . . . . . . . . . . . . . . . . . . 105
1     Introduction
Many problems in linear algebra can be solved by processing eigenvalues of the input matrix. As
eigenvalues of a non-normal matrix are different from its singular values, such problems are not
approachable by the existing quantum singular value algorithm.
    The goal of this work is to present an algorithmic framework to process eigenvalues of high-
dimensional non-normal matrices on a quantum computer, going beyond previous quantum al-
gorithms targeting at the singular values. We focus on operators with real spectra and Jordan
forms—a broad class of non-normal matrices arising in the study of non-Hermitian physics and
transcorrelated quantum chemistry. However, our method also applies to more general operators
with eigenvalues in the complex plane, with no dependence on the Jordan condition number.
    Within the proposed framework, we develop: (i) a quantum algorithm for estimating eigenvalues
of a non-normal matrix, with the complexity strictly achieving Heisenberg-limited scaling when the
input is diagonalizable with real spectra; (ii) a quantum algorithm for applying arbitrary polynomial
transformations to the input matrix, nearly reproducing previous singular value results when the
input is Hermitian; (iii) a quantum algorithm for solving systems of linear differential equations,
with a strictly linear scaling in the evolution time for an average diagonalizable input matrix with
imaginary spectra; and (iv) a quantum algorithm for ground state preparation, recovering the nearly
optimal scaling from previous work when the inputs are Hermitian Hamiltonians. We summarize
these algorithms in Table 1, explaining how we treat non-normality of the input in each case.
    The core technique underpinning our results is the efficient creation of a history state encoding
Chebyshev polynomials of the input matrix in quantum superposition, with further generalizations
to Faber polynomials for eigenvalue processing over the complex plane. This is in turn achieved
by implementing an operator version of the Chebyshev and Faber generating functions. While the
Chebyshev history state of a Hermitian matrix can be efficiently generated via quantum walk, no
such a mechanism was available for non-normal operators. To our knowledge, our work elucidates
the first connection between quantum computing and the vast field of Faber polynomials, which
provide a nearly-optimal basis for uniform function approximation over the complex domain.
    Our result thus suggests the use of matrix generating functions as a powerful methodology for
solving linear algebraic problems on a quantum computer.

1.1   Eigenvalue processing
Quantum computers can operate quantum systems of exponentially large dimensions with only
polynomially many resources. This feature underlies the exponential speedups found in various
promising applications, including simulating quantum systems [59], solving systems of linear equa-
tions [41], and factoring integers [84]. These computational problems typically have inputs encoded
by matrices such as multi-qubit unitaries and Hamiltonians, and their solutions can be obtained
by processing the exponentially large matrices on a quantum computer using only a polynomial
amount of resources. For quantum simulation, this involves applying the exponential function
H 7→ e−itH to the target Hamiltonian. For solving linear equations, this means implementing the
inverse function A 7→ A−1 on a well-conditioned coefficient matrix. And for factoring integers, this
entails estimating eigenvalues of the modular multiplication operator.
    To directly harness this exponential power of quantum computers, an algorithmic technique
known as the Quantum Singular Value Transformation (QSVT) was proposed [37]. Given the
singular value decomposition A = V ΣU † of the input matrix, QSVT applies polynomial functions
p to the singular values of A in the following manner:
                                 A = V ΣU † 7→ psv (A) = V p(Σ)U † .                             (1)

                                                 4
Notably, this can be realized on a quantum computer with a query complexity that depends on
degree of the polynomial rather than dimensions of the underlying Hilbert space, avoiding an
explicit calculation of the exponentially large basis transformations U and V . As the notion of
singular values plays a fundamental role in linear algebra, QSVT has found a host of applications
in quantum linear algebra and has unified diverse quantum algorithms [18, 29, 55, 67], ranging from
Hamiltonian simulation [61] to fixed-point quantum search [96] and eigenstate filtering [57], while
providing a systematic methodology to implement transformations on singular values with optimal
query complexity [69].
    Closely related to the singular value transformation is the problem of singular value estimation,
whose solution underlies the quantum speedups for factoring integers [84] and elucidating chemical
reactions [52, 93]. Here, an initial state close to a right singular vector |ψj ⟩ of A is given, and
the goal is to estimate the corresponding singular value σj . By generalizing the quantum phase
estimation algorithm, a solution to the singular value estimation can be obtained with an optimal
number of controlled queries to operators encoding the input matrix [15, 37, 48]. In the special
case where A is Hermitian, essentially the same algorithm can be used for eigenvalue estimation,
as eigenvalues and singular values coincide in absolute value.
    However, many problems arising in practice require processing eigenvalues of the input ma-
trix, not its singular values. For a diagonalizable input A, this means performing the polynomial
transformation directly on A, which has the action

                                 A = SΛS −1 7→ p(A) = Sp(Λ)S −1 ,                                  (2)

with an invertible basis transformation S. Such eigenvalue processing problems arise naturally in a
variety of applications, including solving linear differential equations [12], simulating non-Hermitian
physics [4, 9], simulating transcorrelated quantum chemistry [68], and estimating spectral proper-
ties of stochastic matrices [97]. Of course, any singular value processing problem can always be
reformulated as an eigenvalue problem through the Hermitian dilation A 7→ |0⟩⟨1| ⊗ A + |1⟩⟨0| ⊗ A† .
But the converse does not hold for non-normal matrices. In fact, eigenvalue processing appears
far more challenging than singular value processing in many respects: (i) the basis transformation
S is invertible but not necessarily unitary; (ii) eigenvalues are generally complex numbers, unlike
singular values that are real and nonnegative; and (iii) A may only admit the Jordan form decom-
position in general, where the factor Λ is not diagonal. See Section 2.3 for formal definitions of
the singular value, eigenvalue, and Jordan form transformations. Hence, existing singular value
algorithms are not applicable to such eigenvalue problems, and there is no unifying framework to
solve them on a quantum computer with optimal query complexity.

1.2   Chebyshev history state generation
We present a Quantum EigenValue Estimation (QEVE) algorithm and a Quantum EigenValue
Transformation (QEVT) algorithm that estimate and transform eigenvalues of high-dimensional
non-normal matrices accessed by a quantum computer. Our main results and applications are
illustrated diagrammatically in Figure 1 and tabulated in Table 1.
    The common tool underpinning both QEVE and QEVT is an efficient algorithm to prepare a
history state encoding polynomials of the input matrix through the use of generating functions. To
be specific, consider the expansion of a polynomial p with respect to a polynomial basis
                                                  n−1
                                                  X
                                         p(A) =         βj pj (A),                                 (3)
                                                  j=0



                                                   5
            Main techniques                                    Main algorithms                                Applications

       Chebyshev state phase estimator                      Quantum eigenvalue estimator             Quantum differential equation solver



         Faber history state generator



         Fourier coefficients generator                    Quantum eigenvalue transformer             Quantum ground state preparator




Figure 1: A diagrammatic illustration of quantum eigenvalue processing and its applications. See Table 1
for a summary of common treatments of non-normality of the input matrix and query complexity.


where pj are degree-j polynomials, and A is for now assumed to satisfy ∥A∥ = 1 for simplicity (∥·∥
is the spectral norm). Given a block encoding of A (see Section 2.4 for the formal definition), if A is
Hermitian, prior art provides a highly efficient method based on quantum walk for generating pj (A)
that are Chebyshev polynomials of A using only O(j) queries to the block encoding [19, 62]. The
QSVT algorithm in particular allows one to block encode an arbitrary p(A) with query complexity
                                                         
                                         O n ∥p∥max,[−1,1] ,

where ∥p∥max,[−1,1] = maxx∈[−1,1] |p(x)|.
    However, when A is non-normal, the QSVT technique does not apply and previous methods only
allow one to efficiently generate monomials Aj using O(j) queries. Hence if arbitrary polynomials
p(A) or pj (A) of A are desired, previous methods are only able to block encode p(A) by taking a
linear combination of monomials, with a cost scaling like
                                                  
                                          n−1
                                          X
                                   O n       |βj | = O (n ∥β∥1 ) ,                          (4)
                                                            j=0

where βj are coefficients of the monomial       expansion of p. Note that all the terms above add up
constructively, so the result ∥β∥1 = n−1
                                         P
                                            j=0 |β j | can be significantly larger than the desired scaling
with ∥p∥max,[−1,1] . In fact, this cost is exponentially large in n for the differential equation and the
ground state preparation problem to be discussed here.
   Our approach overcomes this exponential complexity of block encoding in a monomial basis
by providing means to directly and efficiently generate a polynomial basis pj (A) of a non-normal
matrix A, where pj may, for instance, includeP          Chebyshev polynomials. Our approach is based
on a matrix version of the generating function ∞              j
                                                         j=0 y pj (x) = g(y, x) of the polynomial basis pj .
Specifically, we introduce the n-by-n lower shift matrix L and aim to implement
                          n−1                            ∞                                                  
                          X
                                    j         A            X
                                                                   j             A                        A
                                 L ⊗ pj                =         L ⊗ pj                    = g L ⊗ I, I ⊗                                   (5)
                                              αA                                 αA                       αA
                           j=0                             j=0

with a complexity polynomial in n (we will incorporate the normalization factor αA of the block
encoding of A hereafter). The above equation follows from the definition of generating function,
along with the substitution y = L ⊗ I and x = I ⊗ αAA . This is then measured to estimate the target
eigenvalue, or is further combined with a subroutine that generates the expansion coefficients βj to
efficiently transform the eigenvalues.
     When the polynomial basis is selected to be Chebyshev polynomials, we have the following
Theorem 1 which will be established in Section 3.

                                                                         6
Theorem 1 (Chebyshev history state generation). Let A be a square matrix with only real eigen-
values, such that A/αA is block encoded by OA with some normalization              factor αA ≥ ∥A∥. Let
Oψ |0⟩ = |ψ⟩ be the oracle preparing the initial state, and Oβe|0⟩ ∝ n−1
                                                                            P
                                                                               k=0 βk − βk+2 )|n − 1 − k⟩
                                                                                  ( e    e
be the oracle preparing the shifting of coefficients βek (k = 0, . . . , n − 1). Then, the quantum state
proportional to
                  n−1          n−1                                       η           n−1         n−1                   
                  X            X                          A                X           X           X                 A
            |0⟩         |l⟩             βek e
                                           Tk+l−n+1                |ψ⟩ +         |s⟩         |l⟩         βek e
                                                                                                            Tk                |ψ⟩   (6)
                                                          αA                                                         αA
                  l=0         k=n−1−l                                      s=1         l=0         k=0

can be prepared with accuracy ϵ and probability 1 − pfail using
                                                                 
                                                    1           1
                              O αU n(η + 1) log          log                                                                        (7)
                                                    ϵ          pfail

queries to controlled-OA , controlled-Oψ , controlled-Oβe, and their inverses, where
                                                                                    
                                                                                A
                                            αU ≥          max          Uj                ,                                          (8)
                                                   j=0,1,...,n−1                αA

is an upper bound on Chebyshev polynomials of the second kind Uj (x), Te k (x) are rescaled Chebyshev
polynomials of the first kind to be defined in Section 2.2, and ∥·∥ denotes the Euclidean norm for
vectors and the spectral norm for operators.

    The output state of our algorithm Eq. (6) resembles those constructed by previous quantum
differential equation algorithms. See [12] for further explanations on how they relate to the history
states commonly used in quantum complexity theory. Specifically, this is a state of three quantum
registers. The third register is the system register holding the input state, on which we perform
the truncated Chebyshev expansion. The first register indicates whether the expansion has shifted
indices, whereas the amount of shifting is further recorded in the second register. Here, the param-
eter η controls the probability of preparing the Chebyshev partial sum. In our applications, we will
adjust the parameter η (choosing either η = 0 or η = 1) as well as the expansion coefficients βek , so
that the resulting history state can be used in QEVE or QEVT respectively.
    The complexity of our algorithm depends onlargest  size of the input operator under the poly-
nomial basis mapping αU ≥ maxj=0,1,...,n−1 Uj αAA , which can be further bounded using prop-
erties of the input matrix A. For instance, if A/αA = SJS −1 has a Jordan form decomposition,
with κS ≥ ∥S∥ S −1 an upper bound on      the Jordan condition number and dmax size of the largest
Jordan block, then αU = O n    dmax −1 κS grows polynomially as a function in n. In particular, we
have αU = O (κS ) if dmax = 1, resulting in the complexity
                                                        
                                                         1
                                      O κS n(η + 1) log                                         (9)
                                                          ϵ

for generating the Chebyshev history state of a diagonalizable input matrix A. As will be explained
in Appendix A, this is essentially a bound based on the spectral abscissa, corresponding to the
analysis [50, Section 3.2] of differential equation solvers. Note however that there exist other
bounds to determine αU each having its own strength and weakness, and there is no unifying
one that completely dominates the others. See Table 1 for more details. For the purpose of
generality, we choose to express the complexity of our algorithm in terms of a general upper bound


                                                                   7
         iℑ(z)                               iℑ(z)                                 iℑ(z)                     iℑ(z)


          i                                      i                                  i                         i

                         ℜ(z)                                  ℜ(z)                                 ℜ(z)                    ℜ(z)
          0         1                            0         1                        0          1             0          1




              (a)                                    (b)                                (c)                       (d)

Figure 2: Illustration of regions in the complex plane that enclose eigenvalues of the input matrices. Subfig-
ure (a) represents the real interval [−1, 1], where functions can be nearly best approximated by truncating
the Chebyshev expansion. Subfigure (b) represents the unit disk, where functions can be nearly best ap-
proximated by truncating the Taylor expansion. Subfigures (c) and (d) represent more general regions in
the complex plane, where functions can be nearly best approximated by truncating the Faber expansion.
Subfigure (c) shows a unit semidisk on the left half-plane, with Faber expansion generated by the Elliott’s
conformal map [23], whereas Subfigure (d) is a smooth deformation of (c).

                          
αU ≥ maxj=0,1,...,n−1 Uj αAA , which can be further refined when our algorithm is applied to a
concrete problem.
   To generate the Chebyshev history state, we use a matrix version of the Chebyshev generating
                              1−y 2
function ∞      je        1
         P
           j=0 y Tj (x) = 2 1−2yx+y 2 :

               n−1                               ∞
                                                                                         I ⊗ I − L2 ⊗ I
                                                                       
               X                    A            X                   A
                     Lj ⊗ e
                          Tj                 =         Lj ⊗ e
                                                            Tj                =                                 ,           (10)
               j=0
                                    αA
                                                 j=0
                                                                     αA           2(I ⊗ I + L2 ⊗ I − 2L ⊗ αAA )

where L is the n-by-n lower shift matrix L = n−2                              n
                                                  P
                                                    k=0 |k + 1⟩⟨k| such that L = 0. When applied
to an ancilla state encoding the Chebyshev coefficients βek , this generates the first term of our
desired history state. The second term can then be generated by repeating the subterm flagged by
|l⟩ = |n − 1⟩ a total number of ∼ ηn times using the runaway padding trick [12].
    The application of the matrix Chebyshev generating function to the initial state can be formu-
lated as solving a system of linear equations with coefficient matrix C = (I ⊗ I + L2 ⊗ I − 2L ⊗ αAA )
                             2
                                 P                        P
                                     n−1 e
and target vector b = I⊗I−L ⊗I      2    βk |n − 1 − k⟩|ψ⟩ ∝ n−1 (βek − βek+2 )|n − 1 − k⟩|ψ⟩, which
                                                     k=0                                      k=0
can in turn be solved by a quantum linear system algorithm. To produce an ϵ-approximate so-
lution state |x⟩ corresponding   to the equation Cx = b, the fastest quantum linear system solver
                          1
                            
makes O αC αC −1 log ϵ queries to the block encoding of C/αC and the unitary preparing the
normalized version of b as a quantum state [24, 27, 65], where αC −1 ≥ C −1 is an upper bound
on size of the inverse operator. The claimed complexity is then established by showing explicitly
how the padded version of (I ⊗ I + L2 ⊗ I − 2L ⊗ αAA ) can be block encoded using 1 query to the
block encoding of A/αA , and by upper bounding condition number of the resulting linear system.
    Chebyshev expansion provides a nearly best uniform polynomial approximation of functions over
the real interval [−1, 1] (Figure 2a). They are thus especially suitable for processing eigenvalues of
matrices with real spectra. As aforementioned, matrices with real eigenvalues and Jordan forms
already constitute a broad class of non-normal matrices that have applications in non-Hermitian
physics [4, 9] and transcorrelated quantum chemistry [68] (complementary to the Hermitian case
of [71]). However, our technique is extendable to handle circular disks by implementing Taylor ex-
pansion (Figure 2b), as well as more general complex regions by implementing Faber expansion [85]


                                                                     8
(Figure 2c and Figure 2d), providing a unified quantum algorithmic framework for eigenvalue pro-
cessing.

1.3   Quantum eigenvalue estimation
The ability to generate the Chebyshev history states allows us to estimate and transform real
eigenvalues of non-normal matrices.
    Recall that although optimal quantum algorithms for the singular value estimation have long
been known, the optimal eigenvalue estimation has remained elusive for non-normal matrices.
Specifically, prior approaches to QEVE work by generating a state of the form
                                          Pn−1      2πil αA
                                            l=0 |l⟩e
                                                          A |ψ⟩
                                                                                                    (11)
                                          Pn−1      2πil αA
                                            l=0 |l⟩e          |ψ⟩
                                                          A




using quantum differential equation algorithms [80, 81]. When |ψ⟩ ≈ |ψj ⟩ is close to an eigenstate
of A with eigenvalue λj , the resulting state (omitting the second register) is close to the Fourier
                       λ
                  2πil α j
state √1n n−1
         P
                e       A |l⟩. Then the standard phase estimation algorithm suffices to estimate λj /αA
           l=0
with accuracy O(1/n) and a constant success probability strictly larger than 1/2, which can be
boosted to at least 1−pfail by repeating O(log(1/pfail )) times and taking the median of measurement
outcomes. Unfortunately, existing quantum differential equation algorithms are not known to be
optimal. For instance, consider a diagonalizable matrix A/αA = S(Λ/αA )S −1 . Then it takes
                                                        κ n 
                                                            S
                                         O κS n polylog                                             (13)
                                                            δ
queries to even produce the Fourier state with accuracy δ. Choosing δ = Θ(1) sufficiently small
and n = Θ(αA /ϵ), one gets a suboptimal quantum algorithm for eigenvalue estimation with cost
                                                                
                                αA κS         α κ 
                                                 A S         1
                            O         polylog         log            .                     (14)
                                  ϵ               ϵ         pfail

   In contrast, our approach starts by generating the following Chebyshev history state:
                                      Pn−1 e  A 
                                         l=0 |l⟩Tl αA |ψ⟩
                                      Pn−1 e  A                                                   (15)
                                         l=0 |l⟩Tl αA |ψ⟩

using only                                           
                                                      1
                                          O κS n log                                                (16)
                                                      δ
queries (for a diagonalizable input), where e
                                            Tl (x) are the rescaled Chebyshev polynomials as above.
To prepare this state, we can use our Theorem 1 with η = 0 and set βek = 1 when k = n − 1 and
βek = 0 otherwise. When |ψ⟩ ≈ |ψj ⟩ is close to an eigenstate     of A with eigenvalue λj , the state
                                                    Pn−1 e  λj                            e 2 λj
                                                                                                     
                                                 1
                                                                               eλ = n−1 T
                                                                                     P
we produce is close to the Chebyshev state q            l=0Tl       |l⟩, where α
                                                                    αA             j      l=0   l   αA
                                                 α
                                                 eλj
is the normalization factor. This state is comparable to the Fourier state used by previous work,
but its generation only takes O (κS n log (1/δ)) queries and is thus significantly faster. It remains
to explain how we estimate λj given copies of such Chebyshev history states.


                                                   9
                                                                                               √
    To this end, we use the observation that our generated
                                                          state has an overlap of Ω (1 − 1/ n) with
                                         Pn−1        λ               Pn−1
the unrescaled Chebyshev state √α1 λ       l=0  Tl αAj |l⟩ = √α1 ϕ     l=0 cos (2πlϕj ) |l⟩, where ϕj =
                                       j                           j
           
            λj
 1
                 and αλj = αϕj = n−1          2
                                    P
2π arccos αA                          l=0 cos (2πlϕj ). Here, cos (2πlϕj ) are periodic trigonometric
functions whose discrete spectra are given by the Kronecker delta functions, so the phase angle ϕj
should be extractable using the Fourier transform. To realize this intuition, we develop a variant
of quantum phase estimation in Theorem 2 for the Chebyshev history state, which may be of
independent interest.
    Given quantum state √1αϕ n−1
                               P
                                  l=0 cos (2πlϕ) |l⟩, the Chebyshev state phase estimation algorithm
outputs a value l ∈ {0, . . . , n − 1} such that nl ≈ ϕ in modular distance. Thus we can use
αA cos 2π nl to estimate λj , and we achieve an accuracy ϵ by setting n = O (αA /ϵ). This fails with
            

a constant probability strictly smaller than 21 . By repeating O (log(1/pfail )) times and taking the
median, the failure probability can be exponentially suppressed to below pfail . We thus have the
following Theorem 3 which we preview here and prove in Section 4.

Theorem 3 (Quantum eigenvalue estimation). Let A be a square matrix with only real eigenvalues,
such that A/αA is block encoded by OA with some normalization factor αA ≥ ∥A∥.      p Suppose that
oracle Oψ |0⟩ = |ψ⟩ prepares an initial state within distance |ψ⟩ − |ψλj ⟩ = O( ϵ/αA /αU ) from
an eigenstate |ψλj ⟩ such that A|ψλj ⟩ = λj |ψλj ⟩, where αU satisfies Eq. (8) with
                                                     α 
                                                        A
                                             n=O           .                                  (20)
                                                       ϵ
Then, the eigenvalue λj can be estimated with accuracy ϵ and probability 1 − pfail using
                                                         
                                         αA           1
                                     O      αU log                                                (21)
                                          ϵ          pfail

queries to controlled-OA , controlled-Oψ , and their inverses.

    The setting in which the above algorithm works is pretty general as it only requires the input
matrix A to have real spectra. As is already explained, there are various methods one can use to
further bound αU . In the case where A/αA = S(Λ/αA )S −1 is diagonalizable, αU = O(κS ) and the
cost of QEVE algorithm becomes
                                                         
                                         αA κS        1
                                     O         log            .                               (22)
                                           ϵ         pfail

The scaling with the inverse precision ∼ αϵA cannot be improved even in the ideal case where
the exact eigenstate is provided. It is closely related [5] to the Heisenberg scaling in quantum
metrology [38, 99], and we will adopt this terminology throughout the remainder of the paper.

1.4   Quantum eigenvalue transformation
Besides the eigenvalue estimation, the availability of the Chebyshev history state also allows us to
apply polynomial functions to the eigenvalues of non-normal matrices. This is formally realized by
the QEVT algorithm in Theorem 4, which we state here and establish in Section 5.

Theorem 4 (Quantum eigenvalue transformation). Let A be a square matrix with only real eigen-
        such that A/αA is
values, P                 block encoded by OA with some normalization factor αA ≥ ∥A∥. Let
          n−1 e e      Pn−1
p(x) = k=0 βk Tk (x) = k=0 βk Tk (x) be the Chebyshev expansion of a degree-(n − 1) polynomial

                                                  10
p. Let Oψ |0⟩ = |ψ⟩ be the oracle preparing the initial state, and Oβe|0⟩ ∝ n−1
                                                                                P
                                                                                  k=0 (βk − βk+2 )|n −1 − k⟩
                                                                                       e e
be the oracle preparing the shifting of coefficients βek (k = 0, . . . , n − 1). Then, the quantum state
                                                                       
                                                                   A
                                                           p       αA       |ψ⟩
                                                                                                           (23)
                                                                   A
                                                           p       αA       |ψ⟩

can be prepared with accuracy ϵ and probability 1 − pfail using
                                                                     
                                  α eT,ψ            α eT,ψ          1
                             O           αU n log            log                                             (24)
                                  αp,ψ              αp,ψ ϵ         pfail
queries to controlled-OA , controlled-Oψ , controlled-Oβe, and their inverses, where αU satisfies Eq. (8)
and
                                      n−1                                   
                                      X            A                            A
               α eT,ψ ≥    max            βek e
                                             Tk−l      |ψ⟩ ,       αp,ψ ≤ p          |ψ⟩            (25)
                        l=0,1,...,n−1              αA                           αA
                                              k=l
are upper bound on the maximum shifted partial sum of the Chebyshev expansion and lower bound
on the transformed state.
    Our QEVT algorithm proceeds by preparing a Chebyshev history state using Theorem 1 with
η = 1, followed by a fixed-point amplitude amplification. The number of amplitude amplification
                                                                                            
                                                                            Pn−1 e e         A
steps is determined by the ratio of the shifted partial sum α eT,ψ ≥ maxl     k=l βk Tk−l αA |ψ⟩
                           
and the desired αp,ψ ≤ p αAA |ψ⟩ . This ratio arises in a similar way as (although is incomparable
to) that of the quantum differential equation solvers [10, 34, 50]. Just like αU , there are multiple
ways one can further bound αT,ψe , which we explain in Appendix A. For now, let us assume that

the input matrix A/αA = S(Λ/αA )S −1 is diagonalizable with some upper bound κS ≥ ∥S∥ S −1
on the condition number to simplify the discussion. 
    To analyze the matrix function n−1        e k−l A , we can then diagonalize A and consider
                                     P
                                       k=l β
                                           ek T
                                                    αA
                            Pn−1 e e
instead the scalar function k=l βk Tk−l (x) for the diagonal entries. For a given l, the shifted
Chebyshev partial sum has a max-norm growing like
             n−1
             X                                             n−1
                                                           X                                           
                    βek T
                        e k−l                 = max                    Tk−l (x) = O ∥p∥max,[−1,1] log(n) .
                                                                    βek e                                    (26)
                                                x∈[−1,1]
              k=l               max,[−1,1]                 k=l
                                    
Thus αT,ψ
      e   = O ∥p∥max,[−1,1] κS log(n) and our QEVT has the query complexity
                                                                                        
                  ∥p∥max,[−1,1] κ2S n       ∥p∥max,[−1,1] κS log(n)
                                                                                         
                                                                                     1
               O                   log                         log (n) log                           (27)
                    p αAA |ψ⟩                   p αAA |ψ⟩ ϵ                         pfail

                                                                                       
in the worst case (for presentational purpose, we have used the actual value of p αAA |ψ⟩ as
opposed to its lower bound). However, we show in Appendix A.3 that this shifted partial sum is
actually smaller with respect to the 2-norm:
                                     v
                n−1
                                     uZ        n−1              2
                X                    u 1       X                                  
                    βek T          =       dx          e k−l (x) = O ∥p∥
                                                   βek T                 max,[−1,1] .     (28)
                        e k−l        t
                 k=l                                −1             k=l
                                   2,[−1,1]


                                                                   11
                                     
This gives α eT,ψ = O ∥p∥max,[−1,1] κS and leads to the complexity
                                                                                                             
                           ∥p∥max,[−1,1] κ2S n                          ∥p∥max,[−1,1] κS
                                                                                                              
                                                                                                          1 
                     O                                  log                         log                      (29)
                              p       A
                                               |ψ⟩                          A
                                                                         p αA |ψ⟩ ϵ                      pfail
                                      αA

when eigenvalues of the input matrix are randomly chosen, so our algorithm has a much better
performance on average. Many recent work have examined the use of randomness in improving
quantum simulation algorithms. However, most of those results have focused on the product-
formula-based algorithms [14, 16, 21, 98]. Our result demonstrates that randomness can also be
useful for speeding up more advanced quantum algorithms, which have many applications to the
quantum simulation problem and beyond.
     We emphasize that the QEVT algorithm as stated above not only solves the eigenvalue trans-
formation problem for non-normal matrices, but actually provides a highly efficient solution, in the
sense that its performance nearly recovers that of the QSVT algorithm for transforming singular val-
ues. Specifically, for polynomial functions p(x) with ∥p∥max,[−1,1] ≤ 1 and diagonalizable matrices,
                                                                                                1
                                                                                                  
we can generate an ϵ-approximate Chebyshev history state with query complexity O κS n log       ϵ ,
                                                                                           2
                                                                                           !
                                                                               p αA |ψ⟩
                                                    A
measuring which produces the quantum state p αA |ψ⟩ with probability Ω               A
                                                                                     κ2S
                                                                                              . This
                                                                                            
is to be compared with the QSVT algorithm that uses n queries and outputs the state psv αAA |ψ⟩
                                       2
with success probability psv αAA |ψ⟩ . By performing an additional fixed-point amplitude am-
plification, we obtain the normalized state
                                                 
                                            psv αAA |ψ⟩
                                                                                              (32)
                                            psv αAA |ψ⟩

using                                                                                           
                                                                                              
                                                               n                          1 
                                       O                                    log                                  (33)
                                                     psv       A
                                                                        |ψ⟩              pfail
                                                               αA

queries to the block encoding, whereas the complexity of QEVT is
                                                                        
                                2
                               κ n
                                                                        
                                                  κS                1 
                      O   S          log              log             .                                      (34)
                            p  A
                                   |ψ⟩        p  A
                                                     |ψ⟩ ϵ         pfail
                                  αA                                      αA

On the common ground where the input matrix is Hermitian, our result has thus naturally re-
covered the complexity of QSVT for transforming singular values, up to a polylogarithmic factor
(independent of n). In particular, this implies a quantum algorithm for solving systems of linear dif-
ferential equations with a strictly linear scaling in time for an average diagonalizable input, as well
as a quantum algorithm for ground state preparation with a nearly optimal combined dependence
on the inverse gap and inverse accuracy, which we discuss in the next subsection.
    Our QEVT algorithm is formulated as a state preparation procedure, where the goal is to
create a quantum state proportional to the transformed input matrix applied to the initial state.
However, by using the quantum linear system solver [37, Corollary 69] in place of [24, 27, 65], it
is fairly straightforward to derive a block encoding version of QEVT. We will not use this in our

                                                                        12
paper, as the block encoding introduces additional normalization factors that ruin our (nearly)
optimal results for solving differential equations and preparing ground states. Nevertheless, we
state this block encoding algorithm as Theorem 5 in Section 5 for completeness, in hoping that it
is useful in scenarios where QEVT serves as a subroutine.
    In the actual circuit
                     Pn−1implementation   of QEVT, we need to implement a shifted version of the
oracle Oβe|0⟩ = 1e         ek |k⟩ preparing Chebyshev expansion coefficients of the target function
                           β
                 ∥β ∥ k=0
in superposition. This state can be prepared using standard circuit techniques with a gate com-
plexity of Θ(n) (although no lower bound is known for this task). However, our truncate order n in
general scales polynomially with the input parameters (such as the evolution time and the inverse
spectral gap), and can lead to a significant gate complexity overhead. We describe an alternative
circuit implementation in Theorem 6 that has gate complexity O(polylog(n)), by re-expressing
the Chebyshev coefficients as Fourier coefficients and performing a cyclic convolution in the fre-
quency domain. For presentational purpose, we defer a formal statement and proof of this result
to Section 6.

1.5   Applications
Differential equations arise naturally in a broad range of scientific disciplines including engineering,
physics, economics, and biology. However, classical differential equation solvers can struggle to
handle problems of large dimensions, which motivates the development of quantum algorithms. To
                                                                                  d
be concrete, consider the system of first-order linear differential equations dt    x(t) = Cx(t), whose
                                         tC
solution is given formally by x(t) = e x(0). When C has purely imaginary eigenvalues, we can
prepare the solution state using QEVT by implementing the function f (x) = e−iαC tx on the matrix
iC/αC (that has real spectra), which can be easily constructed from a block encoding of C/αC . We
establish an equivalent version of this result for A = iC as Theorem 7, whose proof will be given
in Section 7.1.
    Our algorithm proceeds by applying Theorem 4 to the function e−iαA tx truncated at order
                                                                 
                                                          κS
                                n = O αA t + log                       ,                            (37)
                                                     ∥e−itA |ψ⟩∥ ϵ

where A/αA = SJS −1 has a Jordan condition number upper bounded by κS ≥ ∥S∥ ∥S∥−1 . The
                                                                                     −itA |ψ⟩ , as well
complexity of our algorithm depends on the amplitude amplification ratio αT,ψ  e / e

as largest size αU of the block encoded operator under the mapping of polynomial basis. These
two factors arise in a similar way as (although are not directly comparable to) those of previous
differential equation solvers [50]. However, these complexities become comparable when the input
matrix is diagonalizable—a setting relevant for practical applications [4, 68]. Then, we show that
αU = O (κS ) (Appendix A.2), whereas αT,ψ           −itA |ψ⟩ = O (κ ) holds for an average input
                                             e / e                    S
(Appendix A.3). This leads to the strictly linear scaling in the evolution time
                                           κ       κ              
                                2               S           S        1
                          O κS αA t + log           log       log            ,                     (38)
                                               ϵ           ϵ        pfail

shaving off a polylog(t) factor from the best previous result under the same setting. This is
reminiscent of the query complexity improvement of the Chebyshev-based method over the Taylor-
based method for Hamiltonian simulation [61]. However, to achieve this for solving differential
equations, we would need both the new eigenvalue processing technique and the tighter analysis of
Fourier truncation error.


                                                  13
    It is worth noting that previous work proposed anRalternative method to realize QEVT, based
on the contour integration formula: f (A) = 1/(2πi) C dz f (z)(zI − A)−1 , where C is a contour
enclosing all eigenvalues of A [34, 86, 87]. This method requires implementing a discrete version
of the integral coherently on a quantum computer, and its performance depends largely on the
choice of contours. With a circular contour, this method led to a quantum differential equation
algorithm with a quadratic scaling in time [34]. Rigorous analysis of a general contour becomes more
complicated, and it is unclear how much improvement this method offers for other applications.
    More recent work [3] developed a quantum differential equation algorithm whose complexity is
linear in the evolution time, along with additional dependence on an amplitude amplification cost
that can be implicitly time dependent. That result is obtained under the assumption that the input
matrix has a nonpositive numerical abscissa, similar to our Faber-based algorithm (Theorem 11)
to be introduced below. This is however incompatible with the setting of our Theorem 7 where the
input matrix has only imaginary eigenvalues. In fact, a matrix with nonpositive numerical abscissa
has only imaginary eigenvalues, if and only if the matrix is anti-Hermitian (Appendix B.2). Thus the
result of [3] is not immediately useful for applications such as transcorrelated quantum chemistry,
where matrices have real spectra but are not necessarily Hermitian.
    We now turn to our second application: the quantum ground state preparation. In the case
where the input operator is a Hermitian Hamiltonian, this problem has been extensively studied by
previous work such as [36, 73], and can be solved near optimally on a quantum computer [56]. Here,
we extend the scope of previous results by considering non-normal matrices with real eigenvalues,
which are relevant to applications in non-Hermitian physics and transcorrelated quantum chemistry.
Specifically, let A be a matrix with only real eigenvalues and an upper bound κS on its Jordan
condition number, block encoded with a normalization factor αA . Suppose that λ0 is the smallest
eigenvalue of A with the corresponding eigenstate |ψ0 ⟩, and is nondefective and nonderogatory. That
means, there is only one Jordan block in A corresponding to the eigenvalue λ0 , and the size of that
block is 1. Assume further that λ0 is separated from the next eigenvalue λ1 : λ0 ≤ − δ2A < 0 < δ2A ≤
λ1 for some spectral gap δA > 0. Then our goal is to prepare a quantum statePthat ϵ-approximates
the ground state |ψ0 ⟩ up to a global phase, given an initial state |ψ⟩ = γ0 |ψ0 ⟩+ d−1
                                                                                    l=1 γl |ψl ⟩ expanded
in the Jordan basis. We achieve this using Theorem 8, which is established in Section 7.2.
    Our algorithm proceeds by applying Theorem   r 4 to               function 1 − Erf (cx) = 1 −
                                                               the error
                                                                     
      cx        2
√2       dy e−y with a rescaling factor c = O αδAA log αδAA |γκ0S|ϵ
    R
  π 0
                                                                         truncated at order

                                                                        
                                                 αA           αA κS
                                     n=O            log                        .                        (40)
                                                 δA           δA |γ0 |ϵ

Similar as above, we will describe the algorithm in its full generality, keeping factors like αU and α eT,ψ
that can be further refined in concrete problems. For instance,    if the input matrix is diagonalizable,
                                                       αA         κS
then we show that αU = O(κS ) and n = O δA log |γ0 |ϵ , whereas the amplification ratio
   
O |γκS0 | holds on average (with an additional log(n) for the worst-case input). This gives the
query complexity                   2                                  
                                     κS αA       2    κS             1
                                O            log              log            .                           (41)
                                    |γ0 | δA         |γ0 |ϵ         pfail
Thus when the input matrix A is Hermitian, our result recovers the nearly optimal ground state
preparation result [56] up to a logarithmic factor. However, our algorithm is more general in that
it applies to non-normal matrices with real eigenvalues whose ground states are still well defined.



                                                     14
                       iℑ(z)                                     iℑ(w)
                                             Ψ(w)

                           i                                       i
                       E                                               D
                                          ℜ(z)                                    ℜ(w)
                        0        1                                 0       1



                                              Φ(z)

Figure 3: Illustration of the unit disk D, the target region E, and the exterior Riemann mappings Ψ, Φ
associated with the definition of Faber polynomials.


1.6   Eigenvalue processing over the complex plane
To simplify the analysis of algorithms, we have so far focused on the case where input matrices have
only real eigenvalues from [−1, 1]. In this case, we develop techniques to efficiently generate the
Chebyshev history states, and our result is comparable to previous results for processing singular
values. However, our techniques are applicable to more general matrices whose eigenvalues are
enclosed by regions in the complex plane, thereby providing a quantum linear algebraic framework
far more versatile than QSVT.
    The core idea behind this generalization is to create the polynomial basis for a nearly-best
uniform approximation over the target eigenvalue enclosing region. This is in turn achieved by
passage from known polynomial basis for the real interval [−1, 1] or the unit disk D, with the help
of conformal maps. To be specific, consider a compact region E that includes eigenvalues of the
input matrix. Under reasonable mathematical assumptions, there exists a unique conformal map

                                     Φ : E c → Dc ,    Φ(z) = w,                                 (42)

known as the exterior Riemann map, that sends the complement of E conformally onto the exterior
of the unit disk D = {|w| ≤ 1} and satisfies Φ(∞) = ∞, Φ′ (∞) = limz→∞ Φ(z) z   = ζ > 0, with
inverse
                                Ψ : Dc → E c ,     Ψ(w) = z,                               (43)
where complement is taken with respect to the extended complex plane C ∪ {∞}. This implies
that Φ has a Laurent expansion in some neighborhood of ∞ as Φ(z) = ζz + ζ0 + ζz1 + zζ22 + · · · and
for the same reason Ψ(w) = ςw + ς0 + ςw1 + wς22 + · · · . Then the jth Faber polynomial Fj (z) for
the region E is defined as the polynomial part of the Laurent series of Φj (z). See Figure 3 for an
illustration of regions and conformal maps relevant to the definition of Faber polynomials.
    Faber polynomials provide a general methodology for constructing polynomial expansions that
encompass Chebyshev and Taylor expansions as     √ special cases. For instance, using the Joukowsky
               w+w−1
map Ψ(w) =        2   and its inverse Φ(z) = z + z 2 − 1, one can re-express Chebyshev polynomials
Tj (x) = cos(j arccos(x)) = Fj (x) as Faber polynomials over the real interval [−1, 1]. Similarly,
                                                                           (z−z0 )j
using the affine map Φ(z) = z−z    ρ , one can identify power functions
                                     0
                                                                             ρj
                                                                                    = Fj (z) as Faber
polynomials for the disk {|z − z0 | ≤ ρ}. The significance of Faber polynomials however is that they
provide a nearly-best uniform approximation of functions over the complex plane [85, Page 190].
Thus, by generating Faber polynomials in quantum superposition, one expects to obtain efficient

                                                  15
quantum algorithms for matrices with complex eigenvalues, going beyond the Chebyshev-based
algorithms discussed above.
    To realize this idea, we use a matrix version of the Faber generating function
                   n−1                                 ∞
                                                                                                   Ψ′ (L−1 ) ⊗ I
                                                                                   
                   X
                           j              A            X
                                                              j                 A
                         L ⊗ Fj                    =         L ⊗ Fj                       =                           ,                         (44)
                   j=0
                                          αA
                                                       j=0
                                                                                αA             LΨ(L−1 ) ⊗ I − L ⊗ αAA

where L is the n-by-n lower shift matrix. Note that the Laurent series of wΨ(w−1 ) is actually a
power series and so LΨ(L−1 ) is well defined, despite the fact that L itself is not invertible. Similar
to the Chebyshev case, we aim to bundle the numerator with a subroutine that prepares the
Faber coefficients, and invert the denominator using a quantum linear system solver. The technical
challenge, however, is that we need to implement operators such as Ψ′ (L−1 ) and LΨ(L−1 ) through
efficient block encodings. We overcome this by using the Fourier expansions

 Ψ′ (eiω ) = ς − ς1 e−2iω − 2ς2 e−3iω + · · · ,                     e−iω Ψ(eiω ) = ς + ς0 e−iω + ς1 e−2iω + ς2 e−3iω + · · · (45)

This allows us to invoke Theorem 6 to efficiently generate the Fourier coefficients, thereby producing
the desired block encoding. We summarize our result for generating the Faber history states in
Theorem 9, which will be previewed below and further discussed in Section 8.
Theorem 9 (Faber history state generation). Let A be a square matrix such that A/αA is block
encoded by OA with some normalization factor αA ≥ ∥A∥. Suppose that eigenvalues of A/αA are
enclosed by a Faber region E with associated conformal maps Φ : E c → Dc , Ψ : Dc → E c and
Faber polynomials
         Pn−1       Fn (z). Let Oψ |0⟩ = |ψ⟩ be the oracle preparing the initial state, and Oβ |0⟩ ∝
  ′  −1
Ψ (Ln ) k=0 βk |n−1−k⟩ be the oracle preparing the shifting of coefficients β. Then, the quantum
state proportional to
                   n−1          n−1                                                 η            n−1         n−1                   
                   X            X                                 A                   X            X           X                 A
             |0⟩         |l⟩              βk Fk+l−n+1                      |ψ⟩ +            |s⟩          |l⟩         βk Fk                |ψ⟩
                                                                  αA                                                             αA
                   l=0         k=n−1−l                                                s=1          l=0         k=0

can be prepared with accuracy ϵ and probability 1 − pfail using
                                                                  
                                                    1            1
                              O αF′ n(η + 1) log          log
                                                    ϵ           pfail
queries to controlled-OA , controlled-Oψ , controlled Oβe, and their inverses, where
                                                                                              
                                                                                F′j       A
                                                                                          αA
                                                       αF′ ≥ max
                                                                  j=1,...,n           j

is an upper bound on the derivative of Faber polynomials.
    With an additional fixed-point amplitude amplification, we obtain the Faber-based quantum
eigenvalue transformation algorithm in Theorem 10, previewed below. As an application, we de-
velop a quantum differential equation algorithm in Theorem 11 for general coefficient matrices by
implementing Faber polynomials over a compact set (such as the one shown in Figure 2d) on the
left half of the complex plane. We also show in Theorem 12 how to estimate leading eigenvalues
(eigenvalues of maximum absolute value) by directly implementing the Taylor expansion. How-
ever, the success probability of our algorithm would decay drastically when applied to non-leading
eigenvalues, which is partially addressed by the more recent method from [1].

                                                                           16
             Algorithm                                        Query complexity                                                         Measure of non-normality
     Quantum eigenvalue estimator                                            
                                                             O αAϵκS log pfail
                                                                          1
                                                                                                                                       Jordan condition number
            (Theorem 3)                                                                            !                            !
   Quantum eigenvalue transformer            ∥p∥max,[−1,1] κ2S              ∥p∥max,[−1,1] κS
                                                                                                                
                                                                                                                     1
                                                                                                                            
                                         O                   n log                                  log         pfail              Jordan condition number
           (Theorem 4)                         p αA |ψ⟩                       p αA |ψ⟩ ϵ
                                                      A                              A
  Quantum differential equation solver                                                                            
                                          O κ2S αA t + log κϵS log κϵS log pfail      1
                                                                          
                                                                                                                                       Jordan condition number
            (Theorem 7)
   Quantum ground state preparator                2
                                                    κ
                                                                                
                                              O |γS0 | αδAA log2 |γκ0S|ϵ log pfail
                                                                              1
                                                                                                                                       Jordan condition number
            (Theorem 8)                                                      !              !
   Quantum eigenvalue transformer           ∥p∥max,∂E             ∥p∥max,∂E
                                                                                    
                                                                                        1
                                                                                          
                                         O            n log                log pfail                                            Numerical range/pseudospectrum
          (Theorem 10)                         A
                                                 p    αA
                                                           |ψ⟩        A
                                                                              p   αA
                                                                                         |ψ⟩ ϵ

  Quantum differential equation solver           
                                                       αA t
                                                                            
                                                                                   αA t
                                                                                                       
                                                                                                             1
                                                                                                                    
                                             O       ∥etA |ψ⟩∥
                                                               polylog          ∥etA |ψ⟩∥ϵ
                                                                                                  log       pfail                   Numerical range/pseudospectrum
           (Theorem 11)
    Quantum eigenvalue estimator                                 
                                                                      αA
                                                                                     
                                                                                          1
                                                                                                 
                                                           O         λmax ϵ κS log       pfail                                         Jordan condition number
           (Theorem 12)

Table 1: Summary of common measures of non-normality and the corresponding complexity of quantum
eigenvalue processing algorithms. The Jordan condition number, introduced in Section 2.3, is a commonly
used measure of non-normality in numerical linear algebra [90, Page 444]. However, this measure is not
suitable for problems with ill-conditioned Jordan basis. Alternatively, we can apply Faber approximations
over the numerical range/pseudospectrum of the input matrix, to be formalized in Appendix B.2 and Ap-
pendix B.3 respectively, which leads to query complexity independent of the Jordan condition number. See
the relevant theorem statements for definitions of the remaining scaling parameters.


Theorem 10 (Quantum eigenvalue transformation, Faber version). Let A be a square matrix
such that A/αA is block encoded by OA with some normalization factor αA ≥ ∥A∥. Suppose that
eigenvalues of A/αA are enclosed by a Faber region E with associated                         c    c
       c      c
                                                            Pn−1 conformal maps Φ : E → D ,
Ψ : D → E and Faber polynomials Fn (z). Let p(z) =             k=0 βk Fk (z) be the Faber expansion
of a degree-(n − 1) polynomial p. Let Oψ |0⟩ = |ψ⟩ be the oracle preparing the initial state, and
                   Pn−1
Oβ |0⟩ ∝ Ψ′ (L−1
               n )  k=0 βk |n − 1 − k⟩ be the oracle preparing the shifting of coefficients β. Then,
the quantum state                              
                                            p αAA |ψ⟩
                                               
                                            p αAA |ψ⟩
can be prepared with accuracy ϵ and probability 1 − pfail using
                                                                    
                                  αF,ψ             αF,ψ            1
                             O         αF′ n log            log
                                  αp,ψ             αp,ψ ϵ         pfail
queries to controlled-OA , controlled-Oψ , controlled Oβe, and their inverses, where
                      
                  F′j αAA                            n−1
                                                     X            
                                                                  A
                                                                                       
                                                                                       A
 αF′ ≥ max                  , αF,ψ ≥       max           βk Fk−l       |ψ⟩ , αp,ψ ≤ p     |ψ⟩
        j=1,...,n     j                l=0,1,...,n−1              αA                   αA
                                                                           k=l

are upper bound on the derivative of Faber polynomials, upper bound on the shifted Faber partial
sum and lower bound on the transformed state respectively.
   For the purpose of generality, we will express the complexity of Faber-based algorithms using
upper bounds like
                                
                            F′j αAA                             n−1
                                                                X            
                                                                             A
           αF′ ≥ max                 ,     αF,ψ ≥    max            βk Fk−l     |ψ⟩ .       (46)
                  j=1,...,n     j                 l=0,1,...,n−1              αA
                                                                                                             k=l


                                                                         17
Similar to αU and αT,ψ
                    e   in the Chebyshev case, these parameters can be further upper bounded when
the Faber algorithms are applied to a concrete problem. Specifically, we consider the case where
the target region E contains the numerical range of the input matrix, which generalizes previous
bounds for differential equation solvers based on the numerical abscissa [50, Section 3.1]. A similar
bound can be obtained when the pseudospectrum of the input matrix is enclosed by E. Intuitively,
one can view “numerical range” and “pseudospectrum” as two common relaxations of the notion
of eigenvalues. These relaxations provide useful tools for bounding the size of matrix functions.
Indeed, as will be explained in Appendix B, our resulting bounds are independent of the Jordan
condition number κS and therefore do not suffer from an ill-conditioned Jordan basis transformation
that can arise in the Chebyshev case. See Table 1 for a summary of common treatments of non-
normality of input matrices and the corresponding complexity of quantum eigenvalue processing
algorithms.
    We summarize in Section 2 preliminaries required to understand our results, and include in
Section 9 a brief summary of our work and a collection of questions for future work.


2     Preliminaries
In this section, we present prerequisites that are necessary to understand our results on eigenvalue
processing. We begin in Section 2.1 with an introduction of notation and terminology to be used
throughout this paper. The next two subsections, Section 2.2 and Section 2.3, summarize back-
ground material from mathematical analysis and linear algebra respectively. We also formally define
in Section 2.3 the eigenvalue transformation and the singular value transformation of a square ma-
trix. A reader who has a sufficient background on these topics may proceed to Section 2.4, where
we introduce the block encoding framework of quantum algorithms, on which our results are based.

2.1    Notation and terminology
We use lowercase Latin and Greek alphabets to represent vectors defined               on a discrete
                                                                                                     set and
functions defined on a continuum. For instance, we often write β = β0 β1 · · · to represent
coefficients of a polynomial expansion and f : [−1, 1] → C to denote the target function for the
eigenvalue transformation. To quantify the size of such vectors and functions, we useq          the ℓ1 -norm
         P∞                                     R1                                                P∞           2
∥β∥1 = j=0 |βj | and L1 -norm ∥f ∥1,[−1,1] = −1 dx |f (x)|, the Euclidean norm ∥β∥ =                 j=0 |βj |
                            qR
                                1            2
and L2 -norm ∥f ∥2,[−1,1] =     −1 dx |f (x)| , and the max-norm ∥β∥max = supj=0,1,... |βj | and L∞ -
norm ∥f ∥max,[−1,1] = supx∈[−1,1] |f (x)|, dropping the underlying discrete set from the subscript
of a vector norm if it is clear from the context. We will occasionally compute norms for anony-
                                                   P∞           −ij(·)
mous functions. For instance, when writing             j=0 βj e                 , we are computing L2 -norm
qR                                                                     2,[−π,π]
    π            2                         P∞         −ijω . We use the Dirac notation |ψ⟩ to denote a
    −π dω |g(ω)| of the function g(ω) =       j=0 βj e
vector only when it has unit length ∥|ψ⟩∥ = 1 with respect to the Euclidean norm.
    On the other hand, matrices and operators are represented by uppercase Latin and Greek letters
in our paper, and their size is typically quantified by the operator norm ∥·∥ (also known as the
spectral norm). This notation of the operator norm is compatible with that of the Euclidean norm,
as their values coincide for a vector when treated as a mapping from a one-dimensional space.
Example notation of matrices includes: the input matrix of a quantum algorithm A , the diagonal
factor of an eigendecomposition Λ, the Jordan form of a matrix J and the corresponding basis
transformation S, the diagonal factor of a singular value decomposition Σ, the identity matrix I, and


                                                      18
the lower shift matrix L with 1 on the first lower diagonal and 0 elsewhere. When necessary,
                                                                                   Pn−2      we will
use subscripts to represent dimensions of the matrix. For instance, we have Ln = k=0 |k + 1⟩⟨k|.
    We can obtain a block matrix B by stacking up submatrices Bjk :
                                                            
                                               B11 · · · B1n
                                      B =  ...      ..   ..  .                               (47)
                                             
                                                      .    . 
                                                Bn1 · · · Bnn

We require that partition of the rows is the same as that of the columns, so that the block structure
is respected under matrix multiplication. In the case where all Bjk ∈ Cd×d are d-by-d matrices, we
can treat B ∈ Cn×n ⊗ Cd×d as acting on the tensor product space Cn ⊗ Cd , writing
                                                  
                                    B11 · · · B1n        n
                             B =  ...     ..   ..  = X |j⟩⟨k| ⊗ B .                            (48)
                                  
                                            .    .                   jk
                                   Bn1 · · · Bnn       j,k=1


We will slightly abuse the notation and sometimes use the above representation even when not all
Bjk are of the same size. We give a bound in the following lemma on the spectral norm of a block
matrix, using a generalized notion of max row and column sum norms defined for block matrices.

Lemma 1 (Spectral norm bound for block matrices). For dj -by-dk matrices Bjk ∈ Cdj ×dk ,
                                
                   B11 · · · B1n     v                  v
                                     u         n        u         n
                  ..    ..   ..  ≤ u       X          u        X
                  .      .    .    t  max       ∥Bjk ∥ max
                                                        t            ∥Bjk ∥.                     (49)
                                       1≤k≤n               1≤j≤n
                  Bn1 · · · Bnn               j=1                k=1


Proof. The claimed bound follows from [44, 5.6.P21] and a direct verification that
                                       n
                                       X                             n
                                                                     X
                                max          ∥Bjk ∥ ,        max           ∥Bjk ∥                (50)
                               1≤k≤n                         1≤j≤n
                                       j=1                           k=1

are valid matrix norms for matrices with the underlying block structure [44, 5.6.P55].

    We use boldface symbols to denote functions and operations having specific meanings. For
instance, we write Tj (x) for Chebyshev polynomials of the first kind (T    e j (x) for their rescaled
version), Uj (x) for Chebyshev polynomials of the second kind, Jj (t) for Bessel functions of the
                                                                                   Rx        2
first kind, Ij (k) for modified Bessel functions of the first kind, Erf (x) = √2π 0 dy e−y for the
error function, and Fj (z) for Faber polynomials, to be introduced in Section 2.2 and Section 8.1
respectively. In analyzing the Fourier expansion, we write H(·) for the Hilbert transform, S(−n,n) (·)
for the nth partial sum of the Fourier expansion, and S∗ (·) for the Fourier maximal function, to
be defined in Section 2.2. We denote the rank of an operator by Rank(·), kernel of an operator
by Ker(·), and image of an operator by Im(·), to be used in Section 2.3 and Section 2.4. We
use Floor(·)     denote the largest integer not exceeding a real number, and CModq (x) = x −
                to
          x+ q
         
q Floor q 2 ∈ [− 2q , 2q ) to denote the centered modulus of x modulo q (see Section 4.1), reserving
Modq (·) ∈ [0, q) for the regular modulo-q operation. We write O(·) or ≲ to mean asymptotically
less than, Ω(·) or ≳ to mean asymptotically more than, and Θ(·) or ∼ to represent quantities
having the same asymptotic scaling, using o(1) to denote a positive number that approaches zero
as some parameter grows.

                                                        19
    Finally, we use calligraphic uppercase letters to represent sets. For instance, we denote the
set of qth-power integrable functions over [−1, 1] by Lq ([−1, 1]) (Section 2.2), a finite-dimensional
Hilbert space by G or H (Section 2.4), the ball centered at x with radius δ by D(x, δ) (the unit
disk being D), the target region enclosing eigenvalues of the input operator by E (Section 8.1),
the numerical range of an operator by W(·) (Appendix B.2), and the δ-pseudospectrum by Sδ (·)
(Appendix B.3). We denote the number of elements in a finite set S by #S, introduce the indicator
function IndS (·) for a given set S, and define the distance of subsets E1 and E2 in a Hilbert space by
Dist(E1 , E2 ) = inf x1 ∈E1 ,x2 ∈E2 ∥x1 − x2 ∥. We adopt standard notations for number systems, writing
Z for integers, Q for rational numbers, R for real numbers, and C for complex numbers, and we
use superscripts like Cd and Cd×d to denote sets of vectors and matrices of the given dimensions.

2.2    Chebyshev and Fourier expansions
We begin this subsection by motivating the use of Chebyshev and Fourier expansions. Let A be
a diagonalizable matrix with only real eigenvalues, i.e., A = SΛS −1 where Λ is a real diagonal
matrix. Given a real analytic function fe : R → C and quantum state |ψ⟩, the goal of QEVT is to
                                            fe(A)|ψ⟩
produce a state that approximates                     .   For the purpose of developing quantum algorithms,
                                           ∥fe(A)|ψ⟩∥
however, the input matrix A needs to be properly normalized as A/αA with αA ≥ ∥A∥, before it
can be accessed by a quantum computer (we will make this point clearer in Section 2.4). Therefore,
the problem of eigenvalue transformation should be reformulated as applying the rescaled function
f (·) = fe(αA (·)) to the block encoded operator A/αA , approximately producing the state
                                                
                                             f αAA |ψ⟩
                                                       .                                   (51)
                                             f αAA |ψ⟩

     For most problems of interest, we cannot directly implement the target function on a quantum
computer. Instead, we aim to implement a polynomial p(x) that approximates the rescaled function
f (·) = fe(αA (·)). The above discussion suggests that this approximation should be made over the
real interval [−1, 1]. In this case, Chebyshev polynomials provide a nearly optimal solution to the
uniform polynomial approximation problem, which we briefly review in the following.
     We define the Chebyshev polynomials of the first kind over the real interval [−1, 1] as

                                 Tj (x) := cos(j arccos(x)).                                  (52)
                                                             j k  j−k (θ) 1 − cos2 (θ) k/2 , which
                                                 P                                   
Note that by setting θ = arccos(x), cos(jθ) =       0≤k≤j k i cos
                                                   k is even
                         j k j−k         2 k/2 . Thus Chebyshev polynomials defined above are
                 P                       
implies Tj (x) =   0≤k≤j k   i x   1 − x
                        k is even
indeed polynomialP functions, jand the definition can be extended naturally to all R. Now consider
the power series ∞ j=0 Tj (x)y generated by the Chebyshev polynomials. Assuming |y| < 1, we use
the substitution θ = arccos(x) again to get the generating function
                                                                        1
      ∞
      X                 ∞
                        X                  ∞ ijθ
                                           X e + e−ijθ                1−yeiθ
                                                                             + 1−ye1 −iθ          1 − yx
                  j                  j                          j
            Tj (x)y =         cos(jθ)y =                        y =                        =                 .   (53)
                                                      2                       2                1 + y 2 − 2yx
      j=0               j=0                j=0

It is sometimes convenient to rescale the first Chebyshev polynomial by a factor of 12 :
                                              (
                                                Tj (x),   j ≥ 1,
                                   Tj (x) = 1
                                    e                                                                            (54)
                                                2 T0 (x), j = 0.

                                                           20
In this case, we have the alternative generating function
                         ∞                         ∞
                         X
                               e j (x)y j = 1 +
                                                   X                        1 − y2
                               T                         Tj (x)y j =                    .           (55)
                                            2                          2(1 + y 2 − 2yx)
                         j=0                       j=1

We also define Chebyshev polynomials of the second kind as
                                                   sin((j + 1) arccos(x))
                                     Uj (x) :=                            ,                         (56)
                                                       sin(arccos(x))
which has the generating function for |y| < 1
                                      ∞
                                      X                           1
                                            Uj (x)y j =                      .                      (57)
                                                            1 + y 2 − 2yx
                                      j=0

The two kinds of Chebyshev polynomials are related as the solutions of the Pell equation T2j (x) −
(x2 − 1)U2j−1 (x) = 1.
    Chebyshev polynomials are orthogonal in the sense that
                                                    
                        Z 1                         0,
                                                           j ̸= k,
                                            dx        π
                            Tj (x)Tk (x) √       = 2,       j = k ̸= 0,                       (58)
                         −1                1 − x2 
                                                      π,    j = k = 0.
                                                    

Thus, if a function has a Chebyshev expansion, the expansion coefficients must be uniquely deter-
mined:                                        (2 R1
                        ∞                                           dx
                                                      Tj (x)f (x) √1−x   ,  j ≥ 1,
                           βj Tj (x) ⇒ βj = π1 R−1
                       X                                               2
               f (x) =                              1               dx
                                                                                             (59)
                                                 π −1 T0 (x)f (x) 1−x2 ,    j = 0.
                                                                  √
                       j=0
For notational convenience, we sometimes rescale the first coefficient and define
                                           (
                                            βj ,    j ≥ 1,
                                     βej =                                                          (60)
                                            2β0 , j = 0,
so that we can rewrite the expansion as
                                             ∞
                                             X                   ∞
                                                                 X
                                   f (x) =         βj Tj (x) =         βej T
                                                                           e j (x).                 (61)
                                             j=0                 j=0

    As aforementioned, Chebyshev expansion provides a nearly best uniform polynomial approxima-
tion of functions over the real interval [−1, 1]. Specifically, for a continuous function with the Cheby-
shev expansion f (x) = ∞
                          P                                                         Pn−1
                             j=0 βj Tj (x), the maximum truncation error f −           j=0 βj Tj
                                                                                               max,[−1,1]
is larger by a factor at most 4 + π42 ln(n − 1) than the error achieved by the (unique) best degree-
(n − 1) polynomial [89]. Moreover, the error of approximating a Lipschitz function f by the first
n terms of its Chebyshev expansion decreases rapidly with n. For differentiable functions where
f, f ′ , . . . , f (ν−1) are absolutely continuous with a uniformly bounded variation, the error decays
polynomially like f − n−1                          −ν
                                P
                                  j=0 βj Tj = O(n ). For functions f analytic in [−1, 1] that are ana-
lytically continuable to the ellipse with foci ±1 and major and minor semiaxis lengths summing
to ρ > 1, the approximation error decays geometrically like f − n−1                         −n ). Entire
                                                                        P
                                                                          j=0 βj Tj = O(ρ
analytic functions may converge even faster. Here, we bound the error of truncating Chebyshev
expansion of the exponential function and the error function, which will be useful in analyzing the
quantum differential equation algorithm and the ground state preparation algorithm respectively.

                                                          21
Proposition 2 (Chebyshev expansion of exponential function P     [61]). Given τ > 0, the complex
exponential function e −iτ x has the Chebyshev expansion e−iτ x = ∞j=0 βj Tj (x), where
                                                 (
                                                  2ij Jj (τ ),               j ≥ 1,
                                            βj =                                                             (62)
                                                  J0 (τ ),                   j = 0,

with Jj (t) Bessel functions of the first kind. Truncated at order n,

                                            n−1
                                            X                                           eτ n 
                               e−iτ (·) −          βj Tj (·)                     =O                 .        (63)
                                                                                           2n
                                            j=0
                                                                   max,[−1,1]

Proposition 3R (Chebyshev expansion of error function [60, 94]). Given
                                                                 P∞ c > 0, the error function
           2  cx    −u2
Erf (cx) = π 0 du e
          √             has the Chebyshev expansion Erf (cx) = j=0 βj Tj (x), where

                                   2
                          
                           2ce√− c2         j−1
                                                               2                2 
                                                                c                  c
                                   (−1) 2              I j−1            + I j+1            ,    j is odd,
                   βj =        j π                       2
                                                                2            2
                                                                                   2                         (64)
                          0,                                                                   j is even,

with Ij (c) modified Bessel functions of the first kind. Truncated at order n,

                               n−1                                                     2 m 
                               X                                       c     n2
                                                                           − 2m
                                                                                      2
                                                                                   − c2  ec
                Erf (c(·)) −          βj Tj (·)                    =O    e      +e                           (65)
                                                                       n                 2m
                                j=0
                                                   max,[−1,1]

for all m = Ω(c2 ) sufficiently large.

   Now let us apply the substitution θ = arccos(x) and re-express the Chebyshev expansion as
                         ∞
                                                ( Rπ
                                                  2
                        X                             cos(jθ)f (cos(θ))dθ,   j ≥ 1,
           f (cos(θ)) =     βj cos(jθ),   βj = π1 R0π                                      (66)
                        j=0                      π 0 f (cos(θ))dθ,           j = 0.

We thus see that the Chebyshev expansion of f (x) is closely related to the Fourier expansion of the
even function f (cos(θ)), the latter of which has been extensively studied in previous literature. In
what follows, we review a collection of results from Fourier analysis that are most relevant to our
work, referring the reader to [2, 92] for a comprehensive treatment of this subject in the context of
signal processing. We focus on the exponential form of the Fourier expansion for convenience, but
it is straightforward to reformulate all the results in the trigonometric form.
     Consider a function g : [−π, π] → C and periodically extend its domain to the entire R. Due
to the orthogonality of e−ijω over the interval [−π, π], if g has a Fourier expansion, the expansion
coefficients must be uniquely determined as:
                                      ∞                                           Z π
                                      X
                                                  −ijω                        1
                       g(ω) =               ξj e               ⇒        ξj =            dω g(ω)eijω .        (67)
                                                                             2π    −π
                                  j=−∞

In engineering, the coefficients ξj are often thought of as a signal in the time domain, and g(ω)
is then the discrete time Fourier transform of ξj in the frequency domain. We do not explicitly
use this terminology hereafter, but it is useful to have this time-frequency correspondence in mind


                                                                   22
when analyzing properties of the Fourier expansion. By the unitarity of the expansion, we have
the Parseval-Plancherel identity:
                       ∞                                                 Z π
                       X                    1                 1
                                2        2
                             |ξj | = ∥ξ∥ =    ∥g∥22,[−π,π] =                    dω |g(ω)|2 .    (68)
                                           2π                2π            −π
                      j=−∞

   Supposing that g(ω) can be Fourier expanded with coefficients {ξj }∞  j=−∞ , we would like to find
the function to which the shifted coefficients {ξj−k }∞
                                                      j=−∞   correspond.  A simple calculation yields
that
                         X∞                  X∞
                               ξj−k e−ijω =       ξj e−i(j+k)ω = e−ikω g(ω).                     (69)
                         j=−∞                        j=−∞

Thus a shift in the time domain corresponds to a phase shift in the frequency domain. Addi-
tionally, we may take the derivative in the frequency domain when appropriate, which yields the
correspondence
                                      ∞
                                     X                  d
                                          jξj e−ijω = i g(ω).                              (70)
                                                       dω
                                       j=−∞

Now suppose that functions g(ω) and h(ω) can be Fourier expanded as g(ω) = ∞               −ijω and
                                                                              P
         P∞                                                                      j=−∞ ξj e
h(ω) = j=−∞ ζj e−ijω , respectively. Then the function corresponding to the pointwise product
coefficients {ξj ζj }∞
                     j=−∞ can be obtained from the frequency domain convolution:

                              ∞                             Z π
                              X
                                              −ijω      1
                                    ξj ζj e          =            du g(u)h(ω − u).              (71)
                                                       2π    −π
                             j=−∞

The right-hand side of the above equation is sometimes known as the cyclic convolution of periodic
functions g and h.
   As an application of the frequency domain convolution, let us consider the one-sided Fourier
expansion
                                                 X∞
                                     H(g)(ω) =
                                      e             ξj e−ijω                                  (72)
                                                            j=0

and its relation to the two-sided Fourier expansion g(ω) = ∞           −ijω . Note that the one-sided
                                                          P
                                                             j=−∞ ξj e
expansion can be obtained by multiplying the discrete Heaviside step function in the time domain,
which corresponds to
                               ∞                        ∞
                              X              1         X
                                 e−ijω =           + π     δ (ω − 2πk)                           (73)
                                          1 − e−iω
                              j=0                                 k=−∞

in the frequency domain, where δ (·) is the Dirac delta function. Thus, by the frequency domain
convolution theorem,
                                                              ∞
                           Z π                                                !
                         1                        1          X
              H(g)(ω)
              e       =        du g(ω − u)              +π        δ (u − 2πk)
                        2π −π                  1 − e−iu
                                                            k=−∞
                           Z π                                       ∞
                                                                                           (74)
                         1          g(ω − u) 1 π
                                                  Z                  X
                      =        du            +        du g(ω − u)        δ (u − 2πk).
                        2π −π       1 − e−iu    2 −π
                                                                                 k=−∞




                                                        23
For the second term, we have
                Z π                 ∞                          ∞ Z π−2πk
            1                       X                      1 X
                      du g(ω − u)          δ (u − 2πk) =                 du g(ω − 2πk − u)δ (u)
            2    −π                                        2      −π−2πk
                                    k=−∞                     k=−∞                                      (75)
                                                           1 π                    1
                                                             Z
                                                         =      du g(ω − u)δ (u) = g(ω),
                                                           2 −π                   2

whereas
                                         1        1    i      u
                                               =    −     cot                                          (76)
                                      1 − e−iu    2 2          2
for the first term. So altogether, the one-sided expansion has the spectrum
                                                         Z π
                                       i             1                 1
                          H(g)(ω) = − H(g)(ω) +
                          e                                   du g(u) + g(ω)                           (77)
                                       2            4π −π              2

in the frequency domain, where
                                                      Z π
                                                                              ω−u
                                                                                   
                                               1
                                    H(g)(ω) =               du g(u) cot                                (78)
                                              2π       −π                      2

is the Hilbert transform of the 2π-periodic function g.
    The following Riesz inequality asserts that L2 -norm does not increase under the Hilbert trans-
form.

Lemma 4 (Riesz inequality [49, (6.167)]). For g ∈ L2 ([−π, π]), its Hilbert transform
                                          Z π
                                                            ω−u
                                                                  
                                        1
                          H(g)(ω) =           du g(u) cot                                              (79)
                                       2π −π                   2

satisfies
                                           ∥H(g)∥2,[−π,π] ≤ ∥g∥2,[−π,π] ,                              (80)
                        qR
                           π           2
where ∥g∥2,[−π,π] =        −π dω |g(ω)| .

    Finally, we consider the growth of Fourier Ppartial sum as a function of the truncate order.
Specifically, given a Fourier expansion g(ω) = ∞  j=−∞ ξj e
                                                            −ijω and J a collection of indices, we

define SJ (ω) = j∈J ξj e−ijω . So for instance,
                 P

                                            n−1
                                            X                                       n−1
                                                                                    X
                       S(−n,n) (g)(ω) =            ξj e−ijω ,     S[0,n) (g)(ω) =         ξj e−ijω .   (81)
                                          j=−n+1                                    j=0

Note that these partial sums correspond to the pointwise multiplication of ξj with rectangular
window functions. Thus, by the frequency domain convolution theorem,
                                                                                     nω
                                                                                         
                                      1 − e−inω
                      Z π                             Z π
                    1                              1                     (n−1)ω sin
                                                                       −i 2           2
   S[0,n) (g)(ω) =        du g(ω − u)           =         du g(ω − u)e                     ,
                   2π −π              1 − e−iω    2π −π                          sin ω2
                                                                                                  
                                                                                           (2n−1)ω
                    1
                      Z π
                                              1−e −i(2n−1)ω    1
                                                                 Z π                sin       2
 S(−n,n) (g)(ω) =         du g(ω − u)ei(n−1)ω        −iω
                                                            =        du g(ω − u)              ω
                                                                                                 .
                   2π −π                        1−e           2π −π                     sin 2
                                                                                                   (82)

                                                            24
Note that while L∞ -norm of the Dirichlet kernel
                                          n
                                                              sin (n + 12 )ω
                                                                               
                                          X
                                                     −ijω
                               Dn (ω) =          e          =                                     (83)
                                                                  sin ω2
                                                                         
                                          j=−n

is given by
                                      ∥Dn ∥max,[−π,π] = 2n + 1,
its L1 -norm scales like
                                                      4
                                  ∥Dn ∥1,[−π,π] =       log (n) + O(1).                          (84)
                                                     π2
We thus see that in the worst case, the Fourier partial sums grow like ∼ log n as well: in particular,
if g ∈ L∞ ([−π, π]), we have
                                                                             
                                                                4
            S[0,n) (g) max,[−π,π] , S(−n,n) (g) max,[−π,π] =      log n + O(1) ∥g∥max,[−π,π] .   (85)
                                                               π2
However, the scaling of the partial sum can be much smaller on average. In fact, we have the
following highly nontrivial result due to Carleson and Hunt.

Lemma 5 (Carleson-Hunt theorem [28, Theorem 12.8] and [88]). Given g ∈ L2 ([−π, π]), its Fourier
maximal operator
                            S∗ (g)(ω) = sup S(−n,n) (g)(ω) .                                (86)
                                             n=0,1,...

satisfies
                                  ∥S∗ (g)∥2,[−π,π] ≤ c ∥g∥2,[−π,π]                                (87)
                                                   qR
                                                        π          2
for some universal constant c, where ∥g∥2,[−π,π] =     −π dω |g(ω)| .


2.3    Matrix decompositions and transformations
We now introduce common classes of matrices and their decompositions relevant to our work, based
on which we define transformations of these matrices. We refer the reader to [6, 44, 75] for a more
comprehensive coverage of matrix analysis and linear algebra.
   We say a square matrix A is diagonalizable if A = SΛS −1 for some invertible matrix S and
diagonal matrix Λ. In this case, A = SΛS −1 is called the eigendecomposition of A. Diagonalizable
matrices arise in a variety of practical applications [4, 68], and they are especially easy to handle
because, up to a change of basis, their actions are described by scalar multiplications by eigenvalues.
But not all
         matrices
                    are diagonalizable. For instance, if we are restricted to Q or R, then matrices
           0 1
such as            cannot be diagonalized due to the lack of rational or real eigenvalues. Even
          −1 0
complex matrices can be non-diagonalizable if they fail to satisfy the following criterion.

Proposition 6 (Eigendecomposition). The following statements hold for a matrix A ∈ Cd×d :

   1. (Uniqueness of eigenvalues): The diagonal matrix
                                                                      
                                        λ0
                                           λ1                         
                                   Λ=                                  ∈ Cd×d                   (88)
                                                                      
                                                 ..
                                                   .                  
                                                                λd−1

                                                      25
      satisfies A = SΛS −1 for some invertible matrix S ∈ Cd×d , if and only if

                                   #{λl | λl = λ} = d − Rank(A − λI)                               (89)

      for all λ ∈ C.

  2. (Equivalence of eigenbasis): Invertible matrices S, T ∈ Cd×d satisfy A = SΛS −1 = T ΛT −1
     for some diagonal matrix
                                                              
                                   λ0 Id0
                                          λ1 Id1              
                            Λ=                                 ∈ Cd×d                   (90)
                                                              
                                                  ..
                                                    .         
                                                          λs−1 Ids−1

      with the same eigenvalue λl grouped together as λl Idl ∈ Cdl ×dl (λl are pairwise distinct), if
      and only if S and T are related by
                                                                
                                             R0
                                                R1              
                                     T =S                                                      (91)
                                                                
                                                      ..         
                                                        .       
                                                               Rs−1

      for some invertible matrices Rl ∈ Cdl ×dl [44, Theorem 1.3.27].

    For a diagonalizable matrix A with eigendecomposition A = SΛS −1 , if a scalar function f (x)
is defined at all eigenvalues of A, we can simply let the eigenvalue transformation be
                                                                         
                                              f (λ0 )
                                                     f (λ1 )             
                      f (A) = Sf (Λ)S −1 = S 
                                                                           −1
                                                                          S .              (92)
                                             
                                                              ..
                                                                .        
                                                                    f (λd−1 )

This is indeed well defined. As eigenvalues and their multiplicities are determined by the rank
condition Eq. (89), we can simultaneously permute the diagonal entries of Λ and f (Λ) so that the
same values are collected together. Then, diagonal blocks λl Idl and f (λl )Idl are all multiples of the
identity matrix, which are invariant under the transformations Rl (·)Rl−1 from Eq. (91).
    In general, a complex square matrix admits the Jordan form decomposition A = SJS −1 , where
S is an invertible matrix and J is only block diagonal. Its existence and uniqueness are formally
asserted by the following proposition.

Proposition 7 (Jordan form decomposition). The following statements hold for a matrix A ∈
Cd×d :




                                                  26
1. (Existence): There exist an invertible matrix S ∈ Cd×d and a block diagonal matrix
                                                                     
                              J(λ0 , d0 )
                                         J(λ1 , d1 )                 
                        J =                                           ∈ Cd×d ,
                                                                     
                                                      ..
                                                        .            
                                                                           J(λs−1 , ds−1 )
                                                                      
                                λl
                               1                                                            (93)
                                      λl                              
                                                                       
                               0      1      λl                       
                                                                        ∈ Cdl ×dl ,
                                                                      
                                ...
                 J(λl , dl ) = 
                                        0      1
                                                     ..
                                                          .            
                                                                      
                                ..    ..     ..     ..                
                               .         .      .    . λl             
                                 0     ··· ···       0 1 λl

  such that A = SJS −1 .

2. (Uniqueness of Jordan form): The block diagonal matrix J from Eq. (93) satisfies A = SJS −1
   for some invertible matrix S ∈ Cd×d , if and only if
                                                                                  
           #{J(λl , dl ) | λl = λ, dl ≥ k} = Rank (A − λI)k−1 − Rank (A − λI)k            (94)

  for all λ ∈ C and positive integer k [44, Lemma 3.1.18].

3. (Equivalence of Jordan basis): Invertible matrices S, T ∈ Cd×d satisfy A = SJS −1 = T JT −1
   for some Jordan form
                                                                    
                            Jeds0 (λ0 )
                                        Jeds1 (λ1 )
                                                                    
                                                                      ∈ Cd×d
                                                                    
                      J =                          ..                                    (95)
                          
                                                      .             
                                                                     
                                                         Jed (λg−1 )   sg−1



  where blocks with the same eigenvalue λl are grouped together as Jedsl (λl ) ∈ Cdsl ×dsl (λl are
  pairwise distinct), if and only if S and T are related by
                                           e                                     
                                            R0
                                              R
                                               e1                                 
                                       T =S                                                 (96)
                                                                                 
                                                              ..                  
                                                                  .              
                                                                           R
                                                                           eg−1

                               el ∈ Cdsl ×dsl with Toeplitz-type block structures [35, Theorem
  for some invertible matrices R
  3.2].

Given a matrix A with Jordan form decomposition A = SJS −1 , if a scalar function f (x) is




                                                     27
analytic at all eigenvalues of A, we let the Jordan form transformation be
                                                                                                                     
                                    f (J(λ0 , d0 ))
                                                   f (J(λ1 , d1 ))                                                    
          f (A) = Sf (J)S −1 = S 
                                                                                                                        −1
                                                                                                                       S ,
                                   
                                                                    ..
                                                                      .                                               
                                                                                                    f (J(λs−1 , ds−1 ))
                         f (λl )
                                                                                                     
                       f ′ (λl )                f (λl )                                                                       (97)
                       (2)                                                                              
                       f (λl )
                                                 f ′ (λl )   f (λl )
                                                                                                          d −1
                                                                                                          X f (r) (λl ) r
                                                                                                             l
                           2!                                                                           
    f (J(λl , dl )) = 
                            ..              f (2) (λl )                    ..                           =             Ldl .
                             .                  2!          f ′ (λl )           .                              r!
                                                                                                            r=0
                             ..                   ..           ..          ..             ..            
                      
                              .                        .          .             .            .          
                                                                                                         
                          f (dl −1) (λl )                                f (2) (λl )
                             (dl −1)!              ···         ···           2!         f ′ (λl ) f (λl )

In other words, we need not only the function f itself, but also its higher derivatives: at least,
f should be sufficiently smooth at λl to match largest size of the λl -Jordan blocks. The validity
of this matrix function definition can be seen as follows. We permute the Jordan blocks so that
blocks with the same eigenvalue λl are grouped together as Jedsl (λl ) ∈ Cdsl ×dsl . By the above
equivalence result, we can without loss of generality restrict ourselves within each Jedsl (λl ), since
this is the only place where one has freedom to choose the basis transformation. We thus have
Jedsl (λl ) = R           e−1 from Eq. (96), which implies L
              el Jed (λl )R                                ed = R   el L
                                                                       ed R e−1 for the blocked lower shift
                    sl      l                                  sl        sl  l
                                                        P  dsl −1 f (λl ) r
                                                                   (r)
matrix Ld = Jd (λl ) − λl Id . This means that
            e
           sl
                     e
                     sl                     sl                           L is also invariant under the
                                                                         e
                                                                                       r=0    r!    ds
                                                                                                       l
action of R     e−1 , from which validity of the definition is justified.
          el (·)R
                 l
    If a matrix A ∈ Cd×d has only real spectra, we order its eigenvalues increasingly and write

                             λmin (A) = λ0 (A) ≤ λ1 (A) ≤ · · · ≤ λd−1 (A) = λmax (A).                                          (98)

Otherwise, we assign an arbitrary ordering to the eigenvalues λl (A) if A has complex spectra.
We drop the dependence on A when the underlying matrix is clear from the context. We call an
eigenvalue λ nonderogatory if there is only one λ-Jordan block, and nondefective if all λ-Jordan
blocks have
            size
               one. When both conditions are satisfied, we have the Jordan form decomposition
          λ 0 −1
A = S           S , where the bottom right Je has no eigenvalue λ. In solving the ground state
          0 Je
preparation problem, we will assume that the ground state energy is both nondefective and non-
derogatory to simplify our analysis of the algorithm. We will use a similar notation for singular
values (to be introduced below):

                   0 ≤ σmin (A) = σ0 (A) ≤ σ1 (A) ≤ · · · ≤ σd−1 (A) = σmax (A) = ∥A∥ .

   Now, we consider matrix decompositions involving unitary transformations, i.e., we consider
A = U ΛU † with Λ diagonal and U unitary. It is well known in linear algebra that such a spectral
decomposition exists when and only when A is normal.

Proposition 8 (Spectral decomposition). The following statements hold for a normal matrix A ∈
Cd×d (AA† = A† A):




                                                                         28
  1. (Existence): There exist a unitary matrix U ∈ Cd×d and a diagonal matrix
                                                           
                                        λ0
                                           λ1              
                                  Λ=                        ∈ Cd×d                            (99)
                                                           
                                                 . .
                                                    .      
                                                       λd−1

     such that A = U ΛU † .

  2. (Uniqueness of eigenvalues): The diagonal matrix Λ from Eq. (99) satisfies A = U ΛU † for
     some unitary matrix U ∈ Cd×d , if and only if

                                  #{λl | λl = λ} = d − Rank(A − λI)                            (100)

     for all λ ∈ C.

  3. (Equivalence of orthonormal eigenbasis): Unitary matrices U, V ∈ Cd×d satisfy A = U ΛU † =
     V ΛV † for some diagonal matrix
                                                                 
                                  λ0 Id0
                                        λ1 Id1                   
                            Λ=                                    ∈ Cd×d                (101)
                                                                 
                                                 . .
                                                    .            
                                                       λs−1 Ids−1

     with the same eigenvalue λl grouped together as λl Idl ∈ Cdl ×dl (λl are pairwise distinct), if
     and only if U and V are related by
                                                                
                                           W0
                                               W1               
                                   V =U                                                      (102)
                                                                
                                                      ..         
                                                        .       
                                                              Ws−1

     for some unitary matrices Wl ∈ Cdl ×dl [44, Theorem 2.5.4].
    Spectral decomposition offers a useful perspective that differentiates a normal matrix from a
general one. This can be understood as follows. For a square matrix A, we introduce its Jordan
condition number as inf J,S ∥S∥ S −1 , where the minimization is over all possible Jordan form
decompositions A = SJS −1 . Since the factor J is unique up to a permutation of diagonal blocks, it
suffices to only minimize over the basis transformations inf S ∥S∥ S −1 . We then have that Jordan
condition number of a matrix is always ≥ 1, and the matrix is normal if and only if it is diago-
nalizable with Jordan conditon number = 1 [33, Condition 72]. In fact, Jordan condition number
serves as a commonly used measure of nonnormality in numerical linear algebra [90, Page 444],
and it may be nearly optimally bounded by separating the spectrum of input matrix into a disjoint
union of eigenvalues [7, Section 5.3]. This perspective can be useful in analyzing our eigenvalue
algorithms. For instance, we bound the runtime of our Chebyshev-based algorithms in Appendix A
using known upper bounds κS on the Jordan condition number, with the understanding that this
condition number approaches 1 when the target matrix is close to normal. This treatment is sim-
ilar to previous analysis of differential equations [50, Section 3.2] based on the spectral abscissa.
However, we also show in Appendix B that complexity of the Faber-based algorithms can be inde-
pendent of the Jordan condition number, which avoids the issue with a potentially ill-conditioned

                                                 29
Jordan basis similar to previous work [50, Section 3.1] based on the numerical abscissa. See Table 1
for more details.
    Below we list subclasses of normal matrices that we will commonly refer to in this work. They
all admit the spectral decomposition, with eigenvalues belonging to different subsets of the complex
plane.
  1. Normal matrices: N N † = N † N , if and only if ∥N |ψ⟩∥ = N † |ψ⟩ for all ∥|ψ⟩∥ = 1, if and
     only N has a spectral decomposition.

  2. Unitary matrices: U U † = U † U = I, if and only if ∥U |ψ⟩∥ = U † |ψ⟩ = 1 for all ∥|ψ⟩∥ = 1, if
     and only if U has a spectral decomposition with all eigenvalues |λl | = 1.

  3. Hermitian matrices: HH † = H 2 , if and only if H † = H, if and only if ⟨ψ|H|ψ⟩ ∈ R for all
     ∥|ψ⟩∥ = 1, if and only if H has a spectral decomposition with
                                                                  all eigenvalues λl ∈R. The
                                                                          †
                                                                                     †
                                                                              H − H†
                                                                            
     first characterization can be proved by showing the trace Tr H − H                 = 0.

  4. Anti-Hermitian matrices: KK † = −K 2 , if and only if K † = −K, if and only if ⟨ψ|K|ψ⟩ ∈ iR
     for all ∥|ψ⟩∥ = 1, if and only if K has a spectral decomposition
                                                                   with all  eigenvalues λl ∈ iR
                                                                          †
                                                                                      †
                                                                              K + K†
                                                                            
     purely imaginary. The first characterization follows from Tr K + K                    = 0.

  5. Positiv semidefinite matrices: P = CC † for some matrix C, if and only if ⟨ψ|P |ψ⟩ ≥ 0 for all
     ∥|ψ⟩∥ = 1, if and only if P has a spectral decomposition with all eigenvalues λl ≥ 0.

  6. Orthogonal projection matrices: Π = GG† for some isometry G† G = I, if and only if Π2 = Π
     and ∥Π|ψ⟩∥ ≤ 1 for all ∥|ψ⟩∥ = 1, if and only if Π has a spectral decomposition with all
     eigenvalues λl = 0, 1. See [75, Theorem 10.5] or [44, Corollary 3.4.3.3] for a proof of the
     second characterization.
    Finally, we introduce the singular value decomposition, which simplifies the action of a matrix
with two orthonormal bases. We will only introduce this decomposition for a square matrix, to
facilitate a direct comparison with the eigendecomposition. Nevertheless, it is fairly straightforward
to extend the following discussion to an arbitrary non-square matrix.
Proposition 9 (Singular value decomposition). The following statements hold for a matrix A ∈
Cd×d :
  1. (Existence): There exist unitary matrices U, V ∈ Cd×d and a diagonal matrix
                                                           
                                        σ0
                                            σ1             
                                  Σ=                        ∈ Cd×d                            (103)
                                                           
                                                 . .
                                                    .      
                                                       σd−1

     with nonnegative entries σl ≥ 0, such that A = V ΣU † .

  2. (Uniqueness of singular values): The diagonal matrix Σ from Eq. (103) with nonnegative
     entries satisfies A = V ΣU † for some unitary matrices U, V ∈ Cd×d , if and only if
                                                                     
                               #{σl | σl = σ} = d − Rank A† A − σ 2 I                    (104)

     for all σ ≥ 0.

                                                 30
                                                                    e , Ve ∈ Cd×d satisfy A =
  3. (Equivalence of singular vector basis): Unitary matrices U, V, U
     V ΣU † = Ve ΣU
                  e † for some diagonal matrix
                                                           
                                    0d0
                                        σ1 Id1             
                              Σ=                            ∈ Cd×d                      (105)
                                                           
                                                ..
                                                  .        
                                                          σs−1 Ids−1

      with the same singular value σl grouped together as σl Idl ∈ Cdl ×dl (σl are pairwise distinct),
      if and only if V and Ve , U and U e are related by
                                                                                     
                      W0,left                                 W0,right
                             W1                                      W1              
            Ve = V                              ,     U = U                                    (106)
                                                                                     
                                   ..                 e                     ..        
                                     .                                        .      
                                         Ws−1                                        Ws−1

      for some unitary matrices W0,left , W0,right ∈ Cd0 ×d0 , Wl ∈ Cdl ×dl [44, Theorem 2.6.5].
    Let us now define the singular value transformation of matrices, which is central to the QSVT
algorithm to be introduced in the next subsection. Specifically, suppose we are given a function
f (x) satisfying a parity constraint, i.e., we have either f (x) = −f (−x) for all x (odd parity) or
f (x) = f (−x) for all x (even parity). Our goal is to apply f to the singular values of the target
matrix A. Assuming A is a square matrix and has the singular value decomposition A = V ΣU † ,
our singular value transformation is then defined as
                                                                                          
                                                           f (σ0 )
                V f (Σ)U † ,      f is odd,                       f (σ1 )                
      fsv (A) =                                   f (Σ) =                                 .  (107)
                                                                                          
                                                                            ..
                U f (Σ)U † ,      f is even,                                 .           
                                                                                 f (σd−1 )
We claim that the above transformation is mathematically well defined. Indeed, as singular values
and their multiplicities are determined by the rank condition Eq. (104), we can simultaneously
permute the diagonal entries of Σ and f (Σ) so that the same values are collected together. Then,
diagonal blocks σl Idl and f (σl )Idl are all multiples of the identity matrix, which are invariant under
the unitary conjugation Wl (·)Wl† from Eq. (106). In the case where f is an odd function, we have an
                                                       †
additional transformation of the form W0,left (·)W0,right   . But this corresponds to the block with the
zero singular value, and so the result is always the zero matrix when mapped by an odd function:
               †                  †
W0,left f (0)W0,right = W0,left 0W0,right = 0. We thus conclude that the singular value transformation
fsv (·) is indeed well defined in all the cases.

2.4   Block encoding
In this subsection, we review basic facts about block encoding and quantum algorithms developed
within this framework, on which our eigenvalue processing results are based.
    We will define the block encoding in its full generality using unitaries and isometries. We
say an operator G : G → H is an isometry if G† G = I. By definition, G is injective and G† is
surjective, whereas GG† is an orthogonal projection on H with kernel Ker(GG† ) = Ker(G† ) and
image Im(GG† ) = Im(G). We thus have the Hilbert space embedding
                                            G      †
                                         G−
                                          −
                                          ↽⇀
                                           −− Im(GG ) ⊆ H.                                         (108)
                                            G†


                                                   31
Choosing any two orthonormal bases that respect this embedding, we have the matrix representa-
tion                                  
                                      I
                                               G† = I 0 .
                                                         
                                G=        ,                                              (109)
                                      0
Examples of isometries include: (i) unitaries U ; (ii) quantum states |ψ⟩; (iii) tensor product G1 ⊗G2 ,
if G1 and G2 are both isometries; and (iv) composition G2 G1 , if G1 and G2 are both isometries
and the composition makes sense.
    Now given Hilbert spaces G0 , G1 and H, we say an operator A : G0 → G1 is block encoded by
isometries G0 : G0 → H, G1 : G1 → H, and a unitary U : H → H, if

                                             A = G†1 U G0 .                                       (110)

Choosing bases with respect to the orthogonal decompositions H = Im(G0 G†0 ) k Ker(G0 G†0 ) =
Im(G1 G†1 ) k Ker(G1 G†1 ), we have the matrix representation
                                                     
                                                  A ∗
                                          U=            ,                              (111)
                                                  ∗ ∗

where A is exhibited as the top-left block of U ; hence the name block encoding. Note that this is
essentially a unitary dilation problem, and it is mathematically feasible if and only if ∥A∥ ≤ 1 [44,
2.7.P2]: if the norm condition is satisfied, we can simply let [40]
                                                       √
                                                      − I − AA†
                                                                 
                                         √   A
                                  U=                                .                          (112)
                                           I − A† A      A†

However, when a block encoding is realized by quantum circuits, additional normalization factors
will likely be introduced.
    Specifically, to block encode a square matrix on a system register using quantum circuits, we
can prepare states |G0 ⟩, |G1 ⟩ on an ancilla register and perform a unitary U acting jointly on
the ancilla and the system register. Then, the operator block encoded by this circuit is given by
(⟨G1 | ⊗ I) U (|G0 ⟩ ⊗ I). For a given operator A on the system register, we need to introduce a
normalization factor αA so that A/αA can be properly encoded. Our above discussion suggests
that αA ≥ ∥A∥ is a prerequisite for the existence of a block encoding. But the corresponding
construction typically requires an explicit computation of the singular value decomposition of A,
which is prohibitive for high-dimensional input matrices. So the strict inequality αA > ∥A∥ often
holds in practice.
    In developing our eigenvalue algorithms, we sometimes assume that the input matrix can be
block encoded with a normalization factor α ≥ 2 ∥A∥. We note that the block-encoding-based
model covers a host of input matrices with sparsity constraints or linear-combination-of-unitary
expansions [37, 62]. If a normalization factor satisfies 2 ∥A∥ > αA ≥ ∥A∥, we can block encode a
rescaling constant
             √              √                             √             √
               α + αA ⟨0| + α − αA ⟨1|                      α + αA |0⟩ + α − αA |1⟩   αA
                         √              (|0⟩⟨0| − |1⟩⟨1|)            √              =       (113)
                           2α                                          2α             α

with α > αA and artificially increase the normalization factor to meet the desired assumption [11,
Appendix A.2]. This rescaling of normalization factor from αA to α > αA has no query overhead.
    The block-encoding framework allows quantum computers to efficiently perform arithmetic op-
erations on the input matrices, including linear combinations, multiplications, and tensor products.


                                                  32
Moreover, there exists the QSVT technique to apply polynomial functions to the singular values
of a block encoded matrix [37]. We briefly explain the idea of taking linear combination of block
encodings as well as the algorithm of QSVT, which we compare with our main result QEVT on
transforming eigenvalues.
    Suppose we have Aj /αAj block encoded by |0⟩ ⊗ I and Uj for j = 0, 1, . . . , n − 1, and we want
to implement the linear combination n−1
                                        P
                                          j=0 βj Aj for some coefficients βj ≥ 0. Here, the choice of
the reference state |0⟩ is without loss of generality, as any state preparation can be absorbed into
the definition of Uj . Then, we define
                                               n−1 q                                                  n−1
                               1               X                                                      X
                 |G⟩ = qP                           βj αAj |j⟩|0⟩,                           U=             |j⟩⟨j| ⊗ Uj ,   (114)
                             n−1
                             k=0 βk αAk j=0                                                           j=0


so that                                                                        Pn−1
                                                                                   j=0 βj Aj
                               (⟨G| ⊗ I) U (|G⟩ ⊗ I) = Pn−1                                           .                     (115)
                                                                                k=0 βk αAk
This block encoding consists of a state preparation subroutine that can be implemented using Θ(n)
gates [83], as well as an operator selection subroutine that can be realized by generating all binary
strings of length ∼ log(n) with gate complexity Θ(n) [20, Appendix G.4]. The normalization factor

                               n−1
                               X                     n−1
                                                     X                                 n−1
                                                                                       X
                                     βj αAj ≥                   βj ∥Aj ∥ ≥                   β j Aj                         (116)
                               j=0                   j=0                               j=0

                                    Pn−1
is larger than the spectral norm      j=0 βj Aj as expected. But in fact, this normalization factor
can be exponentially large if the above construction is directly applied to implement the polynomial
expansion Eq. (3) for eigenvalue processing. We overcome this catastrophe by developing efficient
methods for generating polynomial basis, including the Chebyshev basis for matrices with real
eigenvalues, and the Faber basis for matrices with complex eigenvalues.
    As for the singular value transformation, consider a polynomial p with max-norm ∥p∥max,[−1,1] =
maxx∈[−1,1] |p(x)| ≤ 1. Then the QSVT algorithm implements a block encoding of the transformed
             
matrix psv αAA with a query complexity proportional to the degree n of p. When performed on
                                                  
an input state |ψ⟩, QSVT outputs the state psv αAA |ψ⟩ with success probability
                                                                             2
                                                                A
                                                 psv                     |ψ⟩       .                                        (117)
                                                                αA
                                                
                                           A
                                     psv       |ψ⟩
Obtaining the normalized state           αA                   with a success probability 1 − pfail would cost an
                                           A
                                     psv α     |ψ⟩
                                           A                    !
                                                           
additional factor of O        1      log           1
                                                                  queries to the block encoding.
                          psv αA |ψ⟩                pfail
                               A                                                    
   In contrast, our goal is to apply polynomial functions to the eigenvalues like p αAA . If the input
matrix is not normal, this problem is out of reach of the QSVT algorithm and its descendants. But
otherwise, we achieve a complexity comparable to that of QSVT for Hermitian matrices. Suppose
that the input matrix A is diagonalizable with a condition number κS of the basis transformation.
Then in the worst case, our QEVT algorithm ϵ-approximates a Chebyshev history state using

                                                                 33
                                                                                                      
                                                                                                  A
O(κS n log(1/ϵ)) queries to the block encoding of A/αA , which if measured will produce p         αA       |ψ⟩
with probability
                                                          2
                                                         
                                                 A
                                          p αA |ψ⟩ 
                                       Θ                   .                                     (118)
                                             κ2S log2 (n)
                                            
                                         A
                                     p       |ψ⟩
So obtaining the normalized state      αA         would require a fixed-point amplitude amplification
                                         A
                                     p α     |ψ⟩
                                         A                                 !
                                                                        
                                                    κS log(n)      1
with an additional query complexity of O                A
                                                              log pfail     . Furthermore, we show that
                                                     p   αA
                                                              |ψ⟩
QEVT can achieve a better performance on average: we can shave off the additional log(n) factor
from the above expressions when eigenvalues of the input matrix are randomly chosen. Therefore,
under the common assumption where the input matrix is Hermitian (which holds if and only if it is
diagonalizable with real eigenvalues and κS = 1 [33, Condition 72]), our QEVT naturally recovers
QSVT. In particular, this yields a quantum algorithm for solving linear differential equations on the
imaginary axis with a strictly linear scaling in the evolution time, improving over the best previous
result under the same setting.
    Finally, we introduce several quantum algorithms within the block encoding framework which
will be used as subroutines in eigenvalue processing. This includes an optimal scaling quantum
linear system solver (to be used in Section 3 and Section 8 to generate the Chebyshev and Faber
history states), a block encoded quantum linear system solver (to be used in Section 5.2 to realize
the block encoded version of QEVT), and a block encoding amplifier (to be used in Section 8 to
block encode the matrix Faber generating function).

Lemma 10 (Optimal scaling quantum linear system algorithm [24, 27, 65]). Let C be a matrix
such that C/αC is block encoded by OC with some normalization factor αC ≥ ∥C∥. Let Ob be the
oracle preparing the initial state |b⟩. Then the quantum state

                                                    C −1 |b⟩
                                                                                                   (119)
                                                   ∥C −1 |b⟩∥

can be prepared with accuracy ϵ and probability 1 − pfail using
                                                               
                                                  1           1
                                O αC αC −1 log        log                                          (120)
                                                  ϵ          pfail

queries to controlled-OC , controlled-Ob , and their inverses, where αC −1 ≥ C −1 is an upper bound
on norm of the inverse matrix.

Remark. Unless otherwise stated, we will choose a sufficiently large (but constant) success proba-
bility when invoking the quantum linear system solver as a subroutine, and boost the probability
at the very end of the entire quantum algorithm.

Lemma 11 (Block encoding inversion [37, Corollary 69]). Let C be a matrix such that C/αC is
block encoded by OC with some normalization factor αC ≥ ∥C∥. Then the operator

                                                     C −1
                                                                                                   (121)
                                                    2αC −1



                                                         34
can be block encoded with accuracy ϵ using
                                                     
                                                      1
                                      O αC αC −1 log                                         (122)
                                                      ϵ

queries to the controlled-OC and its inverse, where αC −1 ≥ C −1 is an upper bound on norm of
the inverse matrix.

Lemma 12 (Block encoding amplification [60, Theorem 2]). Let C be a matrix such that C/α is
block encoded by OC with some normalization factor α. Then given any αC ≥ ∥C∥, the operator

                                                    C
                                                                                             (123)
                                                   2αC
can be block encoded with accuracy ϵ using
                                                          
                                                  α        1
                                        O           log                                      (124)
                                                 αC        ϵ

queries to the controlled-OC and its inverse.

Remark. In the interesting regime where α ≫ 2αC , this rescaling decreases the normalization from
α to 2αC and necessarily
                          incurs a query overhead as above. Note also that this is lower than the
                            
complexity O ααC log ααC ϵ      stated in [37, Theorem 30] by a logarithmic factor, which results
from a looser 
              error analysis.
                           In the proof of [37, Theorem 30], the constructed odd polynomial pℜ
                α
has degree O αC log αC ϵ α
                                and actually approximates the linear function f (x) = ααC x on the
           αC αC
domain [− 2α , 2α ] with additive error
                                                               α ϵ
                                                                 C
                                 ∥pℜ − f ∥max,[− αC , αC ] = O       .
                                                 2α 2α           α
This is tighter than what was claimed in [37]:

                                  ∥pℜ − f ∥max,[− αC , αC ] = O(ϵ).
                                                     2α   2α



3     Chebyshev history state generation
In this section, we present our main technique—a quantum algorithm that efficiently generates
Chebyshev history states for non-normal input matrices. This is achieved using a matrix version of
the Chebyshev generating function, which is overviewed in Section 3.1. We then present a quantum
circuit implementing the matrix Chebyshev generating function in Section 3.2, together with an
explicit normalization factor for the block encoding. With the help of a quantum linear system
solver, we obtain the desired quantum algorithm for creating the Chebyshev history state, which
we summarize as Theorem 1 and analyze in Section 3.3.

3.1   Matrix Chebyshev generating function
As is discussed in Section 1.2, the main insight of our approach is to efficiently create a history
state, encoding a polynomial basis of the input matrix in quantum superposition, even when the



                                                    35
input matrix is not Hermitian or normal. For Chebyshev polynomials, this is accomplished by
using the following matrix version of the generating function:
                                                                                             
                                          I
                                                         0           0            · · ·  0
                                        2                                      ..     .. 
                                   T1 A                 I
                                                                     0                .   .
                                            αA          2                                    
             n−1
                                                                                          .
                             
             X             A                                                 . ..    .. 
                                                                                              
                 Lj ⊗ T         =  T2 αAA           T1 αAA           I
                      ej          
                           αA                                         2                       
                                          ..                                               .. 
                                                                                             
             j=0                                        ..          ..            ..              (125)
                                                           .            .             .
                                  
                                  
                                          .                                    .
                                                                                              
                                    Tn−1 αAA           ···       T2 αAA       T1 αAA     I
                                                                                         2
                                   ∞                                            2
                                                                     I ⊗I −L ⊗I
                                                      
                                  X                 A
                                =      Lj ⊗ e Tj          =                2 ⊗ I − 2L ⊗ A )
                                                                                                ,
                                                    αA       2(I ⊗ I  +   L             α
                                  j=0                                                       A


where the input matrix is block encoded as A/αA and L = n−2
                                                               P
                                                                   k=0 |k + 1⟩⟨k| is the n-by-n lower
shift matrix such that Ln = 0. Eq. (125) follows from Eq. (55) by substituting x = I ⊗ αAA and
y = L ⊗ I. This substitution is valid because L has zero eigenvalues only, whereas both sides of
Eq. (55) have the same derivatives at y = 0 of any order. See [43, Chapter 6] or [42, Chapter 2] for
a complete mathematical justification.
Pn−1Now consider the problem of eigenvalue processing. Given a target Chebyshev expansion
   k=0 βk Tk , we apply the matrix generating function to the initial state
                          Pn−1 e                            (
                            k=0 βk |n  − 1 − k⟩              βk ,     k ̸= 0,
                                                |ψ⟩,  βek =                                     (126)
                                    βe                       2β0 ,    k = 0.

Up to a normalization factor, we obtain
                     
                           n−1
    n−1                                       ! n−1    k                    
    X
         j        A        X                       X X                        A
       L ⊗ Tj
            e                 βk |n − 1 − k⟩|ψ⟩ =
                               e                      βk
                                                      e    |n − 1 − k + j⟩Tj
                                                                          e      |ψ⟩
                 αA                                                           αA
    j=0                     k=0                         k=0          j=0
                                                        n−1            n−1                             
                                                        X              X                           A
                                                    =          βek             |l⟩T
                                                                                  e l+k−n+1                 |ψ⟩    (127)
                                                                                                   αA
                                                        k=0          l=n−1−k
                                                        n−1           n−1                              
                                                        X             X                            A
                                                    =          |l⟩             βek T
                                                                                   e k+l−n+1                |ψ⟩.
                                                                                                   αA
                                                         l=0         k=n−1−l

If we now measure the first register and get the outcome l = n − 1, the second register will have
the desired state proportional to
                            n−1                 n−1        
                            X          A          X          A
                                βk T
                                e  ek       |ψ⟩ =     βk Tk      |ψ⟩.                       (128)
                                       αA                    αA
                             k=0                       k=0

However, we will also get unwanted components for l = 0, . . . , n − 2, leading to a failure of the
algorithm.
    To boost the success probability, we use the runaway padding trick [12] to repeat the desired
state ηn times. This can be understood via the following formula for inverting lower block matrices.
Lemma 13 (Lower block matrix inversion). For invertible square matrices A11 and A22 ,
                                   −1 
                                               A−1
                                                               
                         A11 0                   11         0
                                       =                          .                                                (129)
                         A21 A22          −A−1        −1
                                              22 A21 A11   A−1
                                                             22


                                                  36
   In our case, we let

                                                          I      0    ···    ···  ···    0
                                                                                             
                                              2A                     ..     ..   ..      .. 
                                             − α                I       .      .    .     .
                                              A
                                                                             ..   ..       .. 
                                                                                              
                                                              − α2A             .    .
                                             
                            2             A   I                       I                    .
            A11 = In ⊗ I + Ln ⊗ I − 2Ln ⊗   =                    A
                                                                                  ..     .. 
                                                                                                 (130)
                                          αA 
                                              0                I     −2A
                                                                              I      .    .
                                                                      αA
                                              ..
                                                                                             
                                                               ..     ..     ..   ..          
                                              .                  .     .       .    .   0
                                                                                   2A
                                               0               ···     0      I − αA     I

corresponding to the denominator of the matrix Chebyshev generating function, so that from
Eq. (57),
                                                                              
                                        U0 αAA         0        ···         0
                                           
                                               A
                                                       
                                                          A     ..          ..   
                                        U          U               .         .
                                                                                
                                                     0 αA
                       1               1 αA
                                                                                
    −1
   A11 =                             =                                           . (131)
                                                                                 
                    2             A
          In ⊗ I + Ln ⊗ I − 2Ln ⊗ αA        .
                                            ..        . ..      . ..
                                      
                                                                           0    
                                                                                 
                                                                       
                                       Un−1 αAA       ···    U1 αAA     U0 αAA

Here, we have used subscripts to explicitly represent dimensions of the identity and the lower shift
matrix on the ancilla register. Now we take the ηn-by-n block matrix
                                                                      
                                                        0 0 · · · −I
                                                      0 0 · · · 0 
                           A21 = |0⟩⟨n − 1| ⊗ (−I) =  . . .        ..  .                    (132)
                                                                      
                                                        . .
                                                      . . .  .      . 
                                                          0 0 ···     0
                                                           −1
Thus the action of −A21 A−111 is to copy the last row of A11 to the first row while padding the
remaining rows with zeros. Now we simply need to copy the first row of −A21 A−1 11 to the remaining
rows, which can be achieved by setting
                                                                                        
                                I    0    0 ··· 0                 I 0       0 ··· 0
                             −I I        0 · · · 0             I I       0 · · · 0
                                                                                        
                              0 −I I . . . 0
                                                                               . .   .. 
    A22 = (Iηn − Lηn ) ⊗ I =                          ⇒ A−1  = I I
                                                                           I         . . . (133)
                              ..                           22    .. . . . . . . .. 
                                    .. .. ..       .. 
                              .
                                      .    .   . .  
                                                                 .
                                                                        .    .       . . 
                                         ..                                .. ..
                                0 ···       . −I I                I ···       .       . I

We will bundle the numerator of the Chebyshev generating function

                                              In ⊗ I − L2n ⊗ I
                                      B11 =                                                       (134)
                                                     2
with the state preparation subroutine and discuss it later in Section 6.
   To summarize, after the padding, the denominator of the matrix Chebyshev generating function




                                                 37
becomes
                 Pad(A) = |0⟩⟨0| ⊗ A11 + |1⟩⟨0| ⊗ A21 + |1⟩⟨1| ⊗ A22
                                                                          
                                                   2                    A
                        = |0⟩⟨0| ⊗ In ⊗ I + Ln ⊗ I − 2Ln ⊗
                                                                        αA
                          + |1⟩⟨0| ⊗ |0⟩⟨n − 1| ⊗ (−I) + |1⟩⟨1| ⊗ (Iηn − Lηn ) ⊗ I
                              I       0     ··· ··· ···             0       0 ··· ···
                                                                                               
                           2A              ..       ..     ..      ..      ..   ..     .. 
                          − α        I          .        .      .   .       .    .      . 
                           A
                                                     .      .        .       .    .      .. 
                                                                                                
                           I
                          
                                   − αA2A
                                              I         . .    . .   .
                                                                     .       .
                                                                             .    .
                                                                                  .       .                    (135)
                                                            .        .       .    .       .. 
                                                                                               
                          
                           0         I    −2A
                                                      I        . .   .
                                                                     .       .
                                                                             .    .
                                                                                  .        . 
                                            αA
                              .                                              .    .        .. ,
                                                                                               
                        = .        . .     . .      .  .   .  .             .    .
                                         .       .        .      .
                          
                           .                                  2A
                                                                    0        .    .         .  
                           0
                                   ···       0       I − αA I              0 · · · · · ·      
                           0
                                   ·  · ·  ·  · ·     0     0     −I       I    0    ·     · · 
                                                                                                
                                                                                     .. 
                           0
                                   ···     ··· ···          0      0 −I I                    .
                              ..      ..      ..       ..     ..     ..    .. .. ..
                               .       .       .        .      .      .        .    .         .
which has inverse
                                                                                                        
                                       A
                              U0       αA           0          ···
                                                                0 ···         0                     ···
                                                          .... ..        ..                      .. 
                        U1 αAA       U0 αAA                      .
                                                                  . .          .                       . 
                                                                                                          
                             ..                                   .. ..                                .. 
                                                                                                          
                                        ..                     ..
                                            .                     .
                       
                              .                          0  . .                                     . 
                       
                                                                                                        
            Pad(A)−1 = Un−1 αAA        ···     U1 αAA   U0 αAA 0 ···                               · · · .   (136)
                       
                                                                                                    
                       Un−1 αAA        ···     U1 αAA   U0 αAA I 0                                 · · ·
                                                                                                          
                                                                                                          
                       Un−1 A
                                                                                              .. 
                                                U1 αAA   U0 αAA                                          .
                       
                                αA     ···                     I I                                        
                            ..           ..        ..       ..  .. ..                               ..
                             .            .         .        .   . .                                     .

The numerator
                          Pad(B) = |0⟩⟨0| ⊗ B11 + |1⟩⟨1| ⊗ Iηn ⊗ I
                                             In − L2n                                         (137)
                                       = |0⟩⟨0| ⊗     ⊗ I + |1⟩⟨1| ⊗ Iηn ⊗ I
                                                 2
will be bundled with the initial state, which is now augmented with an additional ancilla |0⟩:
                                               Pn−1 e
                                                    βk |n − 1 − k⟩
                                            |0⟩ k=0                |ψ⟩.                                         (138)
                                                        βe

Here, we have slightly abused the notation and used |0⟩⟨0|, |0⟩⟨1|, and |1⟩⟨1| to index matrix blocks
with different sizes.




                                                        38
   Ignoring the normalization factor, we obtain
                                      n−1
                                                                          !
                                      X
      Pad(A)−1 Pad(B) |0⟩                   βek |n − 1 − k⟩|ψ⟩
                                      k=0
                                                                                                           n−1
                                                                                                                                        !
                                                                                                           X
       |0⟩⟨0| ⊗ A−1                     −A−1      −1
                                                                    + |1⟩⟨1| ⊗ A−1
                                                                                          
  =              11 + |1⟩⟨0| ⊗            22 A21 A11                            22               |0⟩B11            βek |n − 1 − k⟩|ψ⟩       (139)
                                                                                                           k=0
          n−1          n−1                                          η             n−1         n−1                    
          X            X                            A                 X             X           X                  A
  = |0⟩         |l⟩             βek T
                                    e k+l−n+1                 |ψ⟩ +           |s⟩         |l⟩         βek T
                                                                                                          ek                |ψ⟩,
                                                    αA                                                             αA
          l=0         k=n−1−l                                         s=1           l=0         k=0

which pads the original state
                n−1                                                                  n−1
                                           !                                                                                            !
                X                                         In ⊗ I − L2n ⊗ I           X
 A−1
  11 B11              βek |n − 1 − k⟩|ψ⟩       =                                         βek |n − 1 − k⟩|ψ⟩
                k=0
                                                 2(In ⊗ I + L2n ⊗ I − 2Ln ⊗ αAA ) k=0
                                                                       
                                                   n−1                     n−1
                                                                                                 !
                                                   X               A       X
                                               =      Ljn ⊗ Tej              βek |n − 1 − k⟩|ψ⟩                                           (140)
                                                                  αA
                                                     j=0                                        k=0
                                                   n−1              n−1                                   
                                                   X                X                                 A
                                               =          |l⟩                 βek T
                                                                                  e k+l−n+1                    |ψ⟩
                                                                                                      αA
                                                    l=0         k=n−1−l

as desired. This can alternatively be understood using the fact that
                                          I
                                                                                                                              
                                                    0      ···     0                                           0 ··· ···
                                          2              .         ..                                          .. ..    .. 
                                                              ..
                                              A     I
                                      T1
                                              αA    2                .                                           . .      . 
                                           .
                                            ..     .  ..   .  ..                                                .. ..    .. 
                                                             0                                                 . .      . 
                                                                                                                             
                                              
                                                 A              A   I
                                                                                                                             
               Pad(A)−1 Pad(B) = Tn−1  αA  · · · T1  αA  2                                                0 · · · · · ·               (141)
                                     
                                                                                                                              
                                                                   I
                                                                                                                              
                                     Tn−1 A       · · · T1 αAA                                                I 0 · · ·
                                               αA                  2                                                         
                                                         
                                                                    I                                                  .. 
                                      n−1 αAA     · · · T1 αAA                                                             .
                                     T                                                                        I I
                                                                    2                                                         
                                           ..        ..      ..     ..                                         .. .. . .
                                                                                                                             
                                            .         .       .      .                                          . .         .

pads the original matrix Chebyshev generating function Eq. (125).
    Note that there is no need to worry about the normalization factor of the initial or the output
state, simply because such a factor is automatically canceled out by the quantum linear system
solver Lemma 10 which outputs a normalized quantum state. However, we must consider the
normalization factor for block encoding Pad(A) as that will affect the condition number of the
linear system. We discuss this issue in the next subsection.

3.2    Block encoding implementation
Our goal is to invert the denominator of the padded matrix Chebyshev generating function Pad(A)
in Eq. (135) using the optimal quantum linear system algorithm Lemma 10. The complexity of
this inversion further depends on the specific way in which we perform the block encoding. So in
this subsection, we describe a block encoding of the padded matrix Pad(A) with an efficient circuit
implementation.

                                                                       39
   Let us first simplify Pad(A) as
                                                                
                                                              A
            Pad(A) = |0⟩⟨0| ⊗ In ⊗ I + L2n ⊗ I − 2Ln ⊗
                                                              αA
                       − |1⟩⟨0| ⊗ |0⟩⟨n − 1| ⊗ I + |1⟩⟨1| ⊗ (Iηn − Lηn ) ⊗ I
                    = (|0⟩⟨0| ⊗ In ⊗ I + |1⟩⟨1| ⊗ Iηn ⊗ I) + |0⟩⟨0| ⊗ L2n ⊗ I
                                                                                         
                                        2A
                      − |0⟩⟨0| ⊗ Ln ⊗        + |1⟩⟨0| ⊗ |0⟩⟨n − 1| ⊗ I + |1⟩⟨1| ⊗ Lηn ⊗ I
                                        αA
                    = Iη+1 ⊗ In ⊗ I + |0⟩⟨0| ⊗ L2n ⊗ I                                                        (142)
                                                              
                                        2A
                      − |0⟩⟨0| ⊗ In ⊗       + |1⟩⟨1| ⊗ Iηn ⊗ I
                                        αA
                        · (|0⟩⟨0| ⊗ Ln ⊗ I + |1⟩⟨0| ⊗ |0⟩⟨n − 1| ⊗ I + |1⟩⟨1| ⊗ Lηn ⊗ I)
                    = Iη+1 ⊗ In ⊗ I + |0⟩⟨0| ⊗ L2n ⊗ I
                                                        η
                                                                                 !
                                           2A X                                                   
                       −     |0⟩⟨0| ⊗ In ⊗    + |s⟩⟨s| ⊗ In ⊗ I                        L(η+1)n ⊗ I ,
                                           αA
                                                     s=1
where we have slightly abused the Dirac notation  to represent block matrices of different sizes and
applied the matrix equality |1⟩⟨1| ⊗ Iηn = ηs=1 |s⟩⟨s| ⊗ In . Alternatively, we can understand the
                                            P
above simplification through a direct matrix computation. For instance, if n = 3 and η = 1,
                                    
       I                                  I                        0
                                                                                  
   − 2A      I                       I                    0 0
    αA                                                                           
               2A
                                                                                  
    I      − α     I                         I           
                                                            +
                                                                 I    0  0         
                                    =
               A
                                                                                   
                   −I I                             I                        0
                                                                                
                                                                               
                        −I I                           I                       0 
                                                          
                                   
                             −I I                         I                       0
                                            2A                                              (143)
                                                                        0
                                                                                        
                                             αA
                                                2A                  I 0
                                                 αA
                                                                                     
                                                      2A
                                                                     I 0             
                                                                                        
                                        −            α                                 .
                                                       A
                                                                     
                                                                              I 0
                                                                     
                                                          I                          
                                                                                        
                                                                                 I 0 
                                                                    
                                                              I     
                                                                   I                I 0
Then we need to block encode the lower shift matrix L, and further combine it with A/αA by
applying matrix arithmetics within the block encoding framework.
   Without loss of generality, let us consider an n-by-n lower shift matrix Ln . To block encode Ln
and its jth power (for j = 0, 1, . . . , n − 1)
                                    n−2
                                    X                                    n−1−j
                                                                          X
                             Ln =         |k + 1⟩⟨k|,            Ljn =           |k + j⟩⟨k|,                  (144)
                                    k=0                                   k=0
we enlarge the Hilbert space and consider the cyclic shift operator
                    2n−2
                     X
            X2n =          |k + 1⟩⟨k| + |0⟩⟨2n − 1|,
                     k=0
                    2n−1−j                   2n−1                                2n−1
                                                                                                              (145)
             j
                      X                       X                                   X
            X2n =            |k + j⟩⟨k| +            |k + j − 2n⟩⟨k| =                  |Mod2n (k + j)⟩⟨k|.
                     k=0                    k=2n−j                               k=0


                                                            40
The operator X2n is unitary and can be used to block encode Ln , as long as we “zero out” some of
its redundant entries. This is achieved by the following comparing operation
                                               n−1
                                               X                     2n−1
                                                                      X
                                CMP2n,2 =            |k⟩⟨k| ⊗ I2 +            |k⟩⟨k| ⊗ X2 ,                              (146)
                                               k=0                      k=n

whose action is to flag an ancilla qubit (using the regular Pauli gate X) when the given register
overflows. Note that when n is a power of 2, this is simply a CNOT gate with the most significant
bit of k as the control and the ancilla qubit as the target. Our observation is that the cyclic shift
operator X2n and the lower shift operator Ln are equivalent, up to the action of the comparator.

Lemma 14 (Lower shift matrix block encoding). For integers j = 0, 1, . . . , n − 1, it holds
                                                      j
               Ljn = (I2n ⊗ ⟨0|) CMP2n,2 (I2n ⊗ |0⟩) X2n (I2n ⊗ ⟨0|) CMP2n,2 (I2n ⊗ |0⟩) .                               (147)

Proof. Note that
                                                                               n−1
                                                                               X
                                 (I2n ⊗ ⟨0|) CMP2n,2 (I2n ⊗ |0⟩) =                   |k⟩⟨k|.                             (148)
                                                                               k=0

Therefore,
                                                      j
                   (I2n ⊗ ⟨0|) CMP2n,2 (I2n ⊗ |0⟩) X2n  (I2n ⊗ ⟨0|) CMP2n,2 (I2n ⊗ |0⟩)
                                                                               
                      n−1
                      X                 2n−1
                                         X                            n−1
                                                                      X
                 =       |k1 ⟩⟨k1 |       |Mod2n (k2 + j)⟩⟨k2 |      |k3 ⟩⟨k3 |
                       k1 =0              k2 =0                                      k3 =0                               (149)
                                X
                 =                             |Mod2n (k2 + j)⟩⟨k2 |.
                         k2 =0,...,n−1
                     Mod2n (k2 +j)=0,...,n−1

For j, k2 = 0, 1, . . . , n − 1, it always holds k2 + j ≤ 2n − 2, which then implies

          X                                                X                                 n−1−j
                                                                                              X
                           |Mod2n (k2 +j)⟩⟨k2 | =                       |k2 +j⟩⟨k2 | =               |k2 +j⟩⟨k2 | = Ljn , (150)
     k2 =0,...,n−1                                     k2 =0,...,n−1                         k2 =0
 Mod2n (k2 +j)=0,...,n−1                              k2 +j=0,...,n−1

as claimed.

    The above construction can be understood through a direct matrix calculation. For instance,
if n = 3 and j = 1, we have

                                                 0              1 1
                                                                          
                                           1 0               1 
                  0 0 0       1        0        
                                                 1 0
                                                                           
                1 0 0 =  1
                                                                         1 
                                          0                              .           (151)
                                                      1 0         0       
                  0 1 0             1        0                           
                                                          1 0  0 
                                                              1 0          0

Note that the result not only works for Ln but also its powers In , Ln , . . . , Ln−1
                                                                                  n . This general version
will be used in Section 6 to construct an efficient circuit that creates n Fourier coefficients with only




                                                           41
∼ polylog(n) gates. Alternatively, we can also realize the block encoding as the linear combination
                    n−1−j                     n−1−j                  n−1
                     X                     1+1 X                 1−1 X
            Ljn =           |k + j⟩⟨k| =            |k + j⟩⟨k| +         |k + j − n⟩⟨k|
                                            2                     2
                     k=0                         k=0                        k=n−j
                                                                                                        (152)
                          n−1                         n−1
                                                                                                 !
                 1        X                           X
               =                |Modn (k + j)⟩⟨k| +         (−1)Indn−j≤k≤n−1 (k) |Modn (k + j)⟩⟨k| ,
                 2
                          k=0                         k=0

with the indicator function Indn−j≤k≤n−1 (k) implemented by inequality testings [78], exemplified
by the matrix computation
                                                           
                           0 0 0            0 0 1       0 0 −1
                          1 0 0 = 1 1 0 0 + 1 0 0  .                               (153)
                                      2
                           0 1 0            0 1 0       0 1 0
In any case, let us focus on j = 1 for now and conclude that the n-by-n lower shift matrix Ln can
be block encoded with normalization factor 1.
    To complete the block encoding of Pad(A) in Eq. (142), we consider the rewriting
                         η                                              η
                                                                                             !
                  2A X                        3                   A    X
    |0⟩⟨0| ⊗ In ⊗     +     |s⟩⟨s| ⊗ In ⊗ I =     |0⟩⟨0| ⊗ In ⊗      +      |s⟩⟨s| ⊗ In ⊗ I
                  αA                          2                  αA
                        s=1                                            s=1
                                                                           η
                                                                                                !      (154)
                                                1                   A    X
                                              +      |0⟩⟨0| ⊗ In ⊗     −       |s⟩⟨s| ⊗ In ⊗ I .
                                                2                  αA
                                                                          s=1
                                                                                 Pη                     
This means we can implement the block encoding of |0⟩⟨0| ⊗ In ⊗ α2A        A
                                                                              +      s=1 |s⟩⟨s| ⊗ In ⊗ I   /2
with normalization factor 2. Putting it altogether, we conclude that Pad(A)/4 can be block encoded
with a normalization factor of 4, using one query to the controlled block encoding of A/αA .

3.3    Summary of Chebyshev history state generation
We now summarize the quantum algorithm for generating the Chebyshev history state.

   1. Construct a block encoding of the lower shift matrix L using Lemma 14.
   2. Combine L and the input matrix A to construct Pad(A)/4 of Eq. (142) within the block
      encoding framework.
   3. Invoke the quantum linear system algorithm Lemma 10 with Pad(A)/4
                                                                             as the coefficient ma-
                                                                                                   
                                                                             q
                     1 Pn−1 e                                                 Pn−1 e             2
      trix, and |0⟩ α e k=0 (βk −βk+2 )|n−1−k⟩|ψ⟩ as the initial state αβe =
                                 e
                                                                                 k=0 |βk − βk+2 |
                                                                                            e        .
                      β


Theorem 1 (Chebyshev history state generation). Let A be a square matrix with only real eigen-
values, such that A/αA is block encoded by OA with some normalization                factor αA ≥ ∥A∥. Let
                                                                            1 Pn−1 e
Oψ |0⟩ = |ψ⟩ be the oracle preparing the initial state, and Oβe|0⟩ = α e k=0 (βk − βek+2 )|n − 1 − k⟩ be
                                                                             β
                                                                                       q
                                                                                         Pn−1 e             2
the oracle preparing the shifting of coefficients βek (k = 0, . . . , n−1) with αβe =       k=0 |βk − βk+2 | .
                                                                                                      e
Then, the quantum state
                                                     Pη           Pn−1 Pn−1 e e  A 
    |0⟩ n−1
       P         Pn−1                       A
         l=0 |l⟩   k=n−1−l βk Tk+l−n+1 αA |ψ⟩ +           s=1 |s⟩      l=0 |l⟩  k=0 βk Tk αA |ψ⟩
                           e e
         r                                                                                          , (155)
            Pn−1 Pn−1                                  2            Pn−1 e e  A          2
                                                A
                      k=n−1−l βk Tk+l−n+1 αA |ψ⟩           + ηn         k=0 βk Tk αA |ψ⟩
                                e e
               l=0


                                                            42
can be prepared with accuracy ϵ and probability 1 − pfail using
                                                                 
                                                   1            1
                              O αU n(η + 1) log          log            ,                                                   (156)
                                                   ϵ           pfail

queries to controlled-OA , controlled-Oψ , controlled-Oβe, and their inverses, where
                                                                                      
                                                                                  A
                                               αU ≥        max           Uj                ,                                (157)
                                                        j=0,1,...,n−1             αA

is an upper bound on Chebyshev polynomials of the second kind Uj (x).

Proof. The analysis of Section 3.2 shows that Pad(A)/4 can be block encoded with 1 query to the
controlled block encoding of A/αA (i.e., the controlled-OA ). The quantum linear system algorithm
of Lemma 10 outputs a state ϵ-close to
            P                              
                  n−1 e
      4           k=0 (βk −βk+2 )|n−1−k⟩
                           e                                       P                        
    Pad(A)   |0⟩           αβe           |ψ⟩    Pad(A)  −1 Pad(B) |0⟩   n−1 e
                                                                            β |n − 1 − k⟩|ψ⟩
                                                                        k=0 k
            P                               =                    P                         ,
                  n−1 e                                                 n−1 e
      4           k=0 (βk −βk+2 )|n−1−k⟩
                           e
                                                Pad(A)  −1 Pad(B) |0⟩       β |n − 1 − k⟩|ψ⟩
    Pad(A) |0⟩             αe     β
                                         |ψ⟩                            k=0 k

                                                                                                                            (158)
which follows from the fact that
               n−1
               X                         n−1
                                         X                         n−1
                                                                   X                           n−1
                                                                                               X
 (In − L2n )         βek |n − 1 − k⟩ =         βek |n − 1 − k⟩ −         βek |n + 1 − k⟩ =        (βek − βek+2 )|n − 1 − k⟩, (159)
               k=0                       k=0                       k=2                         k=0

under the convention βen = βen+1 = · · · = 0. This is exactly the padded Chebyshev history state
because of Eq. (139).
   We have the norm bound on the inverse padded matrix

                             Pad(A)−1 = O ((η + 1)nαU ) ,                          (160)
                                             
for any upper bound αU ≥ maxj=0,1,...,n−1 Uj αAA on Chebyshev polynomials of the second
kind, which follows from Lemma 1 and the matrix representation of Pad(A)−1 in Eq. (136). The
claimed complexity now follows from Eq. (120).

Remark. For the purpose of generality, we have expressed the complexity of our algorithm in terms
of αU , which shares a similar spirit with recent results on solving linear differential equations [50].
This analysis can be further refined when the algorithm is applied in a concrete setting. For
instance, if the input matrix has the Jordan form decomposition A/αA = SJS −1 with upper
bound κS ≥ ∥S∥ ∥S∥−1 on the Jordan      condition number and size dmax of the largest Jordan block,
then it holds αU = O ndmax −1 κS provided that αA ≥ 2 ∥A∥, which is always achievable per the
                                   

rescaling technique of Eq. (113). In particular, we have αU = O (κS ) for diagonalizable matrices
and the complexity becomes                               
                                                           1
                                      O κS n(η + 1) log          .                                (161)
                                                           ϵ
See Appendix A.2 for more details.
   The generation of Chebyshev historyqstate relies on preparation of the shifted coefficients
 1   n−1 e                                  Pn−1 e
                                                |βk − βek+2 |2 . This is an n-dimensional quantum
   P
αβe     (βk − βek+2 )|n − 1 − k⟩ with α e =
      k=0                                           β           k=0


                                                                   43
state, and can thus be prepared using the conventional approach [83] with gate complexity Θ(n).
However, our n typically scales polynomially with the input parameters, leading to a considerable
overhead. Fortunately, this overhead is avoidable for both QEVE and QEVT. For the eigenvalue
estimation, we set βek = 0 if k ̸= n − 1, so this is actually a 2-dimensional state which can be pre-
pared with O(1) gates. For the eigenvalue transformation, we can treat βek as the coefficients from
a truncated Fourier expansion and coherently implement a convolution in the frequency domain,
which has a cost of O (polylog(n)). See Section 4 and Section 6 for further details.
    Finally, note that the query complexity of initial state preparation can be improved using the
block preconditioning technique of [65].


4     Quantum eigenvalue estimation
With the Chebyshev history state at our disposal, we now present a solution to the quantum
eigenvalue estimation problem. We start by introducing the centered modulus together with its
properties in Section 4.1 which is useful for our algorithmic analysis. We develop a variant of phase
estimation in Section 4.2 to extract the phase information from a Chebyshev state, establishing
Theorem 2. This essentially solves the eigenvalue estimation problem when the input state is
an exact eigenstate. We then consider the general case of imperfect eigenstate in Section 4.3.
Finally, we state and analyze the quantum eigenvalue estimation algorithm in Section 4.4, obtaining
Theorem 3.

4.1    Centered modulus and its properties
In our analysis of the eigenvalue estimation algorithm, we will make extensive use of the centered
modulus which we now introduce. Fixing a positive number q > 0, every real number x ∈ R can
be uniquely written as
                                                         q       q
                                x = kq + r,     k ∈ Z, − ≤ r < .                             (162)
                                                         2       2
Indeed, the fact that such an expansion exists follows by taking

                                     x + 2q                        x + 2q
                                                                       
                        k = Floor             ,   r = x − qFloor                             (163)
                                       q                             q

with Floor(·) the largest integer not exceeding the input. As for the uniqueness, assume that
k1 q + r1 = k2 q + r2 , which implies (k1 − k2 )q = r2 − r1 . Now the requirement −q < r2 − r1 =
(k1 − k2 )q < q forces that k1 = k2 and r1 = r2 . We can thus well define

                                                         x + 2q
                                                                h
                                                                       q q
                         CModq (x) = r = x − qFloor              ∈ − ,                     (164)
                                                             q         2 2

as the centered modulus of x modulo q, which is basically x modulo q with offset − 2q .
    In the following, we include a list of properties of the centered modulus which are useful for our
analysis.

Lemma 15 (Properties of centered modulus). The following properties hold for the centered mod-
ulus:

    1. Periodicity: CModq (x + lq) = CModq (x) for l ∈ Z.

    2. Boundedness: |CModq (x)| ≤ |x|.

                                                 44
  3. Negation: |CModq (−x)| = |CModq (x)|.

  4. Positive scaling: CModq (cx) = cCModq/c (x) for c > 0.

  5. Triangle inequality: |CModq (x + y)| ≤ |CModq (x)| + |CModq (y)|.

Proof. Periodicity directly follows from definition of the centered modulus. To see the second
property, note that |CModq (x)| ≤ 2q always holds true. So if |x| ≥ 2q , there is nothing to prove.
But the remaining case |x| < 2q means that CModq (x) = x, so the claimed bound holds in both
cases. For the third property, note that
                         q      q                                               q      q
 x = kq+r,       k ∈ Z, − ≤ r <         ⇒     −x = (−k)q+(−r),         −k ∈ Z, − < −r ≤ . (165)
                         2      2                                               2      2
Thus if x ̸= (k − 12 )q, we have CModq (−x) = −CModq (x). But on the other hand if x = (k − 21 )q,
we have CModq (−x) = − 2q = CModq (x), so the claimed equality holds in both cases. The
positive scaling property follows from the observation that
        q                       q      q                                       q      q
   x = k + r,        k ∈ Z, −      ≤r<        ⇒     cx = kq + cr,      k ∈ Z, − ≤ cr < .         (166)
        c                       2c     2c                                      2      2
To prove the triangle inequality, assume that
                                                                  q        q
                        x = jq + r, y = kq + s,        j, k ∈ Z, − ≤ r, s < .                    (167)
                                                                  2        2
Then, we have

  |CModq (x + y)| = |CModq (r + s)| ≤ |r + s| ≤ |r| + |s| = |CModq (x)| + |CModq (y)| ,          (168)

which completes the proof.

    Although absolute value of the centered modulus is not a valid norm due to the potential
change of modulus     in the rescaling, it does induce a natural distance metric |CModq (x − y)| for
the interval − 2q , 2q under the periodic boundary condition. In particular, it satisfies the following
            

defining properties of a distance metric:

  1. Nonnegativity: |CModq (x − y)| ≥ 0.

  2. Positivity: |CModq (x − y)| = 0 if and only if CModq (x) = CModq (y).

  3. Symmetry: |CModq (x − y)| = |CModq (y − x)|.

  4. Triangle inequality: |CModq (x − y)| ≤ |CModq (x − z)| + |CModq (z − y)|.

    Centered modulus can be used to significantly simplify reasonings about trigonometric functions.
In particular, we will use the following two inequalities in analyzing the eigenvalue estimation
algorithm:

Lemma 16 (Trigonometric bounds with centered modulus). The following bounds on trigonometric
functions hold:

  1. |sin(x)| ≥ π2 |CModπ (x)|.

  2. |cos(x) − cos(y)| ≤ |CMod2π (x − y)|.


                                                  45
Proof. To prove the first inequality, we assume that x = kπ + r for k ∈ Z and − π2 ≤ r < π2 . Then,

                                                            2      2
                     |sin x| = |sin(kπ + r)| = |sin(r)| ≥     |r| = |CModπ (x)| .                 (169)
                                                            π      π
The second inequality follows from the fact that

   |cos(x) − cos(y)| = ℜ(eix − eiy ) ≤ eix − eiy = ei(x−y) − 1
                                              Z CMod2π (x−y)                                      (170)
                     = eiCMod2π (x−y) − 1 =                  dθ ieiθ ≤ |CMod2π (x − y)| ,
                                                 0

where ℜ is the real part of a complex number.

4.2   Chebyshev state phase estimation
Recall that in the eigenvalue estimation problem, we are given a matrix A with only real eigenvalues,
which has an eigenstate |ψλ ⟩ corresponding to the eigenvalue λ, such that A|ψλ ⟩ = λ|ψλ ⟩. Our goal
is to estimate λ assuming that the input state |ψ⟩ is sufficiently close to |ψλ ⟩.
    We start by preparing a Chebyshev state encoding the target eigenvalue in the phase of the
coefficients. Specifically, we invoke Theorem 1 with η = 0 and
                                             (
                                              1,    k = n − 1,
                                       βek =                                                   (171)
                                              0,    k ̸= n − 1.

This allows us to prepare the following version of the Chebyshev history state
                                       Pn−1 e  A 
                                         l=0 |l⟩Tl αA |ψ⟩
                                       Pn−1 e  A                                                (172)
                                         l=0 |l⟩Tl αA |ψ⟩

with accuracy δ using                                
                                                      1
                                          O αU n log                                              (173)
                                                      δ
queries to the oracle OA that block encodes A/α
                                               A and the oracle Oψ that prepares the initial state
|ψ⟩. The complexity reduces to O κS n log 1δ for diagonalizable matrices with upper bound κS
on the Jordan condition number.
    The state we prepare is close to
             Pn−1      
                        λ
               j=0 T j αA |j⟩        1 X
                                        n−1                      n−1
                                                              1 X ei2πjϕ + e−i2πjϕ
                               =  √       cos(2πjϕ)|j⟩ =  √                       |j⟩,      (174)
             Pn−1
                   T    λ
                            |j⟩      αϕ                       αϕ            2
               j=0   j   αA               j=0                        j=0

             1
where ϕ = 2π   arccos αλA and αϕ is the corresponding normalization factor. In light of the rescaling
trick in Eq. (113), we may assume αA ≥ 2 ∥A∥ without loss of generality, which implies αλA ∈ − 12 , 12
                                                                                                      

and                                                   
                                                   1 1
                                             ϕ∈     ,    .                                      (175)
                                                   6 3
In the following, we develop a variant of the quantum phase estimation algorithm for estimating
the unknown ϕ given a Chebyshev state as above. For presentational purpose, we will first assume

                                                     46
that the input state is exactly the eigenstate and the Chebyshev history state can be prepared
perfectly. The general case will be handled in the next subsection.
   Let us first analyze the normalization factor αϕ . We have
                   n−1                   n−1                                  n−1
                   X                     X   cos(4πjϕ) + 1         n 1 X  i4πjϕ          
            αϕ =         cos2 (2πjϕ) =                         =    +     e      + e−i4πjϕ .                            (176)
                                                    2              2 4
                   j=0                   j=0                                   j=0

Since ei4πϕ ̸= 1 by our assumption,
                    n 1 1 − ei4πnϕ 1 − e−i4πnϕ
                                                      
              αϕ = +                    +
                    2 4 1 − ei4πϕ           1 − e−i4πϕ
                            −i2πnϕ
                                      − ei2πnϕ i2π(n−1)ϕ ei2πnϕ − e−i2πnϕ −i2π(n−1)ϕ
                                                                                     
                    n 1 e
                  = +                         e         +                e                 (177)
                    2 4        e−i2πϕ − ei2πϕ             ei2πϕ − e−i2πϕ
                    n 1 sin(2πnϕ)
                  = +                 cos((n − 1)2πϕ).
                    2 2 sin(2πϕ)
                                         √                                               √
Note that because ϕ ∈ 61 , 13 , we have 23 ≤ sin(2πϕ) ≤ 1, which implies αϕ − n2 ≤ 1√3 = 33 and
                            
                                                                                                                  2 2
                                               "  √     √ #
                                              n    3 n   3
                                         αϕ ∈   −   , +     .                                                           (178)
                                              2   3 2   3

We formulate this observation in terms of properties of Chebyshev polynomials as follows.
Lemma 17 (ℓ2 -norm bounds for Chebyshev polynomials). For any x ∈ − 21 , 12 , it holds that
                                                                            

                                       √     n−1            √
                                   n     3 X 2           n    3
                                     −     ≤     Tj (x) ≤ +     ,
                                   2    3                2   3
                                             j=0
                                   √                        √                                                           (179)
                                             n−1
                               n     3 3 X e2            n    3 3
                                 −     − ≤       Tj (x) ≤ +      − .
                               2    3    4               2   3    4
                                                   j=0
                                                                   Pn−1 −i 2πjl
   Applying the quantum Fourier transform F |j⟩ = √1n               l=0 e
                                                                            n |l⟩, we obtain


                     n−1                           n−1                                 n−1
               1 X                 1 X ei2πjϕ + e−i2πjϕ 1 X −i 2πjl
             F√    cos(2πjϕ)|j⟩ = √                    √   e n |l⟩
                αϕ                  αϕ         2         n
                     j=0                            j=0                                l=0
                                                                                                                        (180)
                                                         n−1
                                                         X n−1
                                             1               X
                                                                       i2πj(ϕ− nl )        −i2πj(ϕ+ nl )
                                                                                                           
                                          = √                      e                  +e                       |l⟩.
                                           2 αϕ n
                                                         l=0 j=0

Because ϕ ∈ 61 , 31 and nl ∈ [0, 1), the first summation is degenerate when ϕ = nl , whereas the
                  

second summation is degenerate when ϕ = n−l                              l
                                              n . For the case where ϕ = n ,
                                 n−1
                            1 X                 1
                          F√    cos(2πjϕ)|j⟩ = √     (n|l⟩ + n|n − l⟩) .                                                (181)
                             αϕ               2 αϕ n
                                  j=0

Here, the normalization factor is
                                n 1 sin 2πn nl
                                                            
                                                            l   n
                            αϕ = +         l
                                               cos (n − 1)2 ϕ = .                                                      (182)
                                2 2 sin 2π n                n   2

                                                         47
So we actually obtain the state
                                            1
                                            √ (|l⟩ + |n − l⟩) ,                                                  (183)
                                             2
from which the phase/eigenvalue can be recovered deterministically. A similar analysis applies to
ϕ = n−l
     n .
   Assuming this is not the case hereafter, we have
                    n−1                          n−1 n−1
              1 X                 1    XX          l               l
                                                                       
            F√    cos(2πjϕ)|j⟩ = √         ei2πj(ϕ− n ) + e−i2πj(ϕ+ n ) |l⟩
               αϕ               2 αϕ n
                    j=0                          l=0 j=0
                                                 n−1
                                                                                                       !
                                         1       X         1 − ei2π(nϕ−l)         1 − e−i2π(nϕ+l)
                                      = √                                l    +                    l       |l⟩
                                       2 αϕ n              1 − ei2π(ϕ− n )        1 − e−i2π(ϕ+ n )
                                                 l=0                                                             (184)
                                                 n−1
                                         1       X        sin π(nϕ − l) iπ(n−1)(ϕ− l )
                                      = √                                 e         n
                                       2 αϕ n
                                                 l=0
                                                           sin π(ϕ − nl )
                                                                                             
                                                               sin π(nϕ + l) −iπ(n−1)(ϕ+ l )
                                                           +                  e          n    |l⟩.
                                                               sin π(ϕ + nl )

In other words,
                                     n−1                                n−1
                                1 X                 1    X
                              F√    cos(2πjϕ)|j⟩ = √       αl |l⟩,                                               (185)
                                 αϕ               2 αϕ n
                                      j=0                               l=0

where
                                                      !
                  sin2 π(nϕ − l) sin2 π(nϕ + l)
                                                                                               
        2                                                             1               1
     |αl | ≤ 2                    +                       ≤2                   +                 .               (186)
                  sin2 π(ϕ − nl )   sin2 π(ϕ + nl )             sin2 π(ϕ − nl ) sin2 π(ϕ + nl )
                                                                |     {z      } |     {z      }
                                                                      α21,l                α22,l


   Let us see that we can approximately recover the eigenvalue if l is close to ±Floor(nϕ) in
centered modulus. Indeed,
                                                    1                           n1 − 1
        |CModn (l ± Floor(nϕ))| ≤ n1 − 1 ⇔            |CModn (l ± Floor(nϕ))| ≤
                                                    n                             n
                    l ± Floor(nϕ)       n1 − 1
                                                                  
                                                                 l         n1
  ⇔      CMod1                       ≤           ⇒     CMod1       ±ϕ ≤
                           n              n                      n          n
                                                                            
                 l                                l                          l         2πn1
  ⇒      cos 2π       − cos(2πϕ) ≤ CMod2π 2π ± 2πϕ ≤ 2π CMod1                  ±ϕ ≤
                 n                                n                          n          n
                      
                     l          2παA n1
  ⇒      αA cos 2π       −λ ≤           ,
                     n             n
                                                                                         (187)
where in the second line we have used the fact that
                                ±nϕ ∓ Floor(nϕ)         nϕ − Floor(nϕ)
                                                
                                                                          1
                      CMod1                          ≤                 ≤ .               (188)
                                        n                     n           n

We now set
                                                n = n0 n1 .                                                      (189)



                                                      48
To ensure that the eigenvalue is estimated to accuracy ϵ, it suffices to take
                                          2παA                             2παA
                                               ≤ϵ          ⇒        n0 ≥        .                                       (190)
                                           n0                                ϵ
                                                     2 and α2 , which we then use to analyze the
   In the following, we will derive tail bounds for α1,l     2,l
success probability of the algorithm. To this end, we consider those l whose centered modulus to
±Floor(nϕ) is larger than some threshold value n1 − 1. We have
       1                 X
                                            2
                                           α1,l
     2αϕ n
             |CModn (l−Floor(nϕ))|>n1 −1
       1                 X                    1
 =
     2αϕ n
             |CModn (l−Floor(nϕ))|>n1 −1
                                         sin π(ϕ − nl )
                                               2

       1                X                            1
 ≤
     2αϕ n                                4
                                                  CModπ (π(ϕ − nl ))
                                                                             2                                          (191)
             |CModn (l−Floor(nϕ))|>n1 −1 π 2
       1                 X                             1
 =                                                                  2
     8αϕ n                                  CMod1 (ϕ − nl )
             |CModn (l−Floor(nϕ))|>n1 −1
       1                 X                                                        1
 ≤                                                                                                              2 .
     8αϕ n
                                                                                         
                                                               Floor(nϕ)−l                      nϕ−Floor(nϕ)
             |CModn (l−Floor(nϕ))|>n1 −1       CMod1                n            − CMod1             n

Since
                              nϕ − Floor(nϕ)       nϕ − Floor(nϕ)
                                             
                                                                   1
                      CMod1                     ≤                 ≤ ,
                                    n                    n         n
                                                                                                                        (192)
                                Floor(nϕ) − l
                                             
                                                  1
                        CMod1                   = |CModn (Floor(nϕ) − l)| ,
                                     n            n
this implies that
                         1                 X
                                                                  2
                                                                 α1,l
                       2αϕ n
                               |CModn (l−Floor(nϕ))|>n1 −1
                       n                 X                          1
                    ≤                                                                                                   (193)
                      8αϕ
                          |CModn (l−Floor(nϕ))|>n1 −1
                                                      (|CModn (Floor(nϕ) − l)| − 1)2
                            ∞               Z ∞
                       n X 1            n               1       n
                    ≤             2
                                    ≤              dx 2 =               .
                      4αϕ       j      4αϕ n1 −2       x   4αϕ (n1 − 2)
                            j=n1 −1

Similarly,
                              1                    X
                                                                         2            n
                                                                        α2,l ≤                .                         (194)
                            2αϕ n                                                4αϕ (n1 − 2)
                                     |CModn (l+Floor(nϕ))|>n1 −1




                                                               49
     Now, our success probability can be lower bounded as
                                                                   
                      l                                  l        2παA n1
       P αA cos 2π        − λ ≤ ϵ ≥ P αA cos 2π              −λ ≤
                      n                                 n           n
                                                                             
     ≥ P |CModn (l − Floor(nϕ))| ≤ n1 − 1 OR |CModn (l + Floor(nϕ))| ≤ n1 − 1
                                                                                  
     = 1 − P |CModn (l − Floor(nϕ))| > n1 − 1 AND |CModn (l + Floor(nϕ))| > n1 − 1
             1             X                             1           X
                                          |αl |2 ≥ 1 −                          2    2
                                                                                         
     = 1−                                                                    α1,l + α2,l
           4αϕ n                                       2αϕ n
                    |CModn (l−Floor(nϕ))|>n1 −1                         |CModn (l−Floor(nϕ))|>n1 −1
                              AND                                                 AND
                    |CModn (l+Floor(nϕ))|>n1 −1                         |CModn (l+Floor(nϕ))|>n1 −1
              1                X
                                                   2         1                X
                                                                                                  2
     ≥ 1−                                         α1,l −                                         α2,l
            2αϕ n                                          2αϕ n
                    |CModn (l−Floor(nϕ))|>n1 −1                    |CModn (l+Floor(nϕ))|>n1 −1
               n
     ≥ 1−              ,
          2αϕ (n1 − 2)
                                                                                                        (195)
where the failure probability is further upper bounded as
            n                n                  n1                  n1
                    ≤     √          =      √          ≤      √          .
       2αϕ (n1 − 2)    n− 2 3
                               (n − 2)    n − 2 3
                                                   (n − 2)    n − 2 3
                                                                       (n − 2)                          (196)
                                 3      1              1        3n0    1             1    3         1


This is ≤ 0.433 for n1 ≥ 5. In other words, we can choose n1 sufficiently large to succeed with a
probability strictly greater than 21 . The success probability can then be boosted to at least 1 − pfail
using the median amplification by repeating the algorithm O (log(1/pfail )) times. We summarize
the core idea of this analysis as follows:

Theorem 2 (Chebyshev state phase estimation). Given Chebyshev state √1αϕ n−1
                                                                                  P
                                                                                     l=0 cos (2πlϕ) |l⟩
          1 1
with ϕ ∈ 6 , 3 , there exists a quantum algorithm that uses one copy of the state and outputs a
value l ∈ {0, . . . , n − 1} satisfying
                                                       
                                                   l          n1
                                        CMod1        ±ϕ ≤        ,                               (197)
                                                  n            n

with probability at least
                                                         n1
                                            1−         √         .                                    (198)
                                                       2 3
                                                   n1 − 3 (n1 − 2)

The algorithm performs a quantum Fourier transform followed by a measurement in the computa-
                                                                     5√
tional basis. For n1 ≥ 5, the success probability is at least 1 − 15−2  3
                                                                          ≈ 0.566 strictly larger than
1
2.


4.3     Analysis of imperfect eigenstate
In describing the Chebyshev state phase estimation algorithm, we have assumed that a perfect
eigenstate is given a prior. In this subsection, we discuss how this assumption can be relaxed to
allow for imperfect eigenstates, which is more common in practical applications.
    Specifically, the error comes from the following three sources:

     1. the quantum linear system solver we use only outputs an approximate solution state;


                                                           50
  2. the initial state |ψ⟩ only approximates an eigenstate |ψλ ⟩; and

  3. the output state from the linear system solver corresponds to the rescaled Chebyshev poly-
     nomials T
             e j , which approximates that of the regular Chebyshev polynomials Tj .

The first error is easy to analyze. If |ψ⟩ is the input and |φ⟩ is the output state of the quantum
linear system solver, then we have
                                        Pn−1 e  A 
                                          j=0 |j⟩Tj αA |ψ⟩
                                |φ⟩ − P                       ≤ ϵlin                        (199)
                                          n−1         A
                                          j=0 |j⟩Tj αA |ψ⟩
                                                 e

where ϵlin is the accuracy of the linear system algorithm.
    The second error is essentially the error of solving linear equations with an imperfect initial
state. This can be analyzed as follows.

Lemma 18. Let C and C
                    e be invertible matrices of the same size. It holds that

                      e −1 − C −1 = −C
                      C              e −1 (C
                                           e − C)C −1 = −C −1 (C     e −1 .
                                                               e − C)C                            (200)

Corollary 19 (Quantum linear system with perturbation). Let C and C  e be invertible matrices of
the same size, acting on (normalized) quantum states |ψ⟩ and | e
                                                              ψ⟩. We have

                                  2 C −1 |ψ⟩ e − |ψ⟩     e −1 C −1 C
                                                       2 C              e−C
          e −1 |ψ⟩
          C     e     C −1 |ψ⟩
                   −            ≤                    +                      .                     (201)
          e −1 |ψ⟩
          C     e    ∥C −1 |ψ⟩∥        ∥C −1 |ψ⟩∥            ∥C −1 |ψ⟩∥

Proof. We use the triangle inequality to upper bound the left-hand side as

       C −1 |ψ⟩    e −1 |ψ⟩
                   C      e          C −1 |ψ⟩   e −1 |ψ⟩
                                                C     e      e −1 |ψ⟩
                                                             C     e     e −1 |ψ⟩
                                                                         C      e
                 −             ≤              −           +            −                  .       (202)
      ∥C −1 |ψ⟩∥   e −1 | e
                   C     ψ⟩         ∥C −1 |ψ⟩∥ ∥C −1 |ψ⟩∥   ∥C −1 |ψ⟩∥   e −1 | e
                                                                         C     ψ⟩

For the first term, we have

                            C −1 |ψ⟩   e −1 |ψ⟩
                                       C     e     C −1 |ψ⟩ − C
                                                              e −1 |ψ⟩
                                                                    e
                                     −           =                     ,                          (203)
                           ∥C −1 |ψ⟩∥ ∥C −1 |ψ⟩∥       ∥C −1 |ψ⟩∥

whereas the second term can be further bounded similarly as

     e −1 | e
     C     ψ⟩   e −1 | e
                C     ψ⟩                       1         1              C −1 |ψ⟩ − C
                                                                                   e −1 | e
                                                                                         ψ⟩
              −               = C  e −1 e
                                      |ψ⟩           −              ≤                          .   (204)
       −1
    ∥C |ψ⟩∥                                   −1
                                            ∥C |ψ⟩∥                          ∥C −1 |ψ⟩∥
                e −1 |ψ⟩
                C      e                              e −1 |ψ⟩
                                                      C     e

                            ∥C −1 |ψ⟩−Ce−1 |ψ⟩
                                            e∥
Thus, it remains to analyze         −1
                                ∥C |ψ⟩∥
                                               .
   For the denominator, one can further bound
                                                                 1
                   1 = CC −1 |ψ⟩ ≤ ∥C∥ C −1 |ψ⟩         ⇒               ≤ ∥C∥ .                   (205)
                                                             ∥C −1 |ψ⟩∥



                                                51
But we will keep it for the time being, as C −1 |ψ⟩ represents size of the solution vector, which we
may have direct knowledge about in applications. As for the numerator,

                  C −1 |ψ⟩ − C
                             e −1 | e
                                   ψ⟩ ≤ C −1 |ψ⟩ − C −1 | e
                                                         ψ⟩ + C −1 | e   e −1 | e
                                                                    ψ⟩ − C     ψ⟩
                                                                                                                  (206)
                                                 ≤ C −1            e + C −1 − C
                                                            |ψ⟩ − |ψ⟩         e −1 .

The claimed bound now follows from the proceeding lemma.

    In applications where C e −1 is unknown, we may remove its dependence using a strategy similar
to that for proving [45, Proposition 5.7.7]. Note that our above perturbation analysis is more general
than is needed here, as it bounds the error of quantum linear system where the coefficient matrix
and the input state can both be imperfect. This general bound will be used later in Section 8.2
to analyze complexity of generating the Faber history state. For the time being, let us assume
that the input state
                    has distance   ∥|ψ⟩ − |ψλ ⟩∥ ≤ ϵinit to a true eigenstate. By Lemma 17, we have
 Pn−1 e          A              √
    j=0 |j⟩Tj αA |ψλ ⟩ = Θ( n), which implies

               Pn−1                                Pn−1                     
                                  A                                       A
                  j=0 |j⟩Tj                |ψ⟩            j=0 |j⟩Tj                |ψλ ⟩        √
                         e                                        e
                                  αA                                      αA                                 
               Pn−1                             − P                                    =O       nαU ϵinit ,   (207)
                                  A                  n−1                  A
                  j=0 |j⟩Tj                |ψ⟩            j=0 |j⟩Tj                |ψλ ⟩
                         e                                       e
                                  αA                                      αA

where the second term further simplifies to
                      Pn−1 e  A                  Pn−1 e  λ 
                         j=0 |j⟩Tj αA |ψλ ⟩         j=0 Tj αA |j⟩|ψλ ⟩
                      Pn−1 e  A                = P                    .                                       (208)
                                                    n−1 e    λ
                         j=0 |j⟩ T j αA   |ψ λ ⟩    j=0 T j αA  |j⟩|ψ λ ⟩

    Finally, we analyze the error of performing eigenvalue estimation on the rescaled Chebyshev
state as opposed to the regular Chebyshev state. This is handled by the following bound.

Corollary 20 (Distance between rescaled and regular Chebyshev states). For any x ∈ − 12 , 12 , it
                                                                                           

holds that
   Pn−1 e           Pn−1                      3                  1
    j=0 Tj (x)|j⟩    j=0 Tj (x)|j⟩
                                                                           
                                              8                  2       1
   qP             − qP             ≤q     √ q       √       +q     √ =O √     . (209)
      n−1 e 2          n−1 2
                           T  (x)     n     3   n     3   3    n    3     n
          T
      k=0 k   (x)      k=0 k          2 −  3    2 −  3  − 4    2 − 3

Proof. We use the triangle inequality to get
            Pn−1 e           Pn−1
             j=0 Tj (x)|j⟩     j=0 Tj (x)|j⟩
            qP             − qP
               n−1 e 2            n−1 2
               k=0 Tk (x)         k=0 Tk (x)
            Pn−1 e           Pn−1 e             Pn−1 e            Pn−1
             j=0 Tj (x)|j⟩     j=0 Tj (x)|j⟩      j=0 Tj (x)|j⟩    j=0 Tj (x)|j⟩
          ≤ qP             − qP               + qP              − qP                                              (210)
               n−1 e 2            n−1 2              n−1 2           n−1 2
               k=0 Tk (x)         k=0 Tk (x)         k=0 Tk (x)      k=0 Tk (x)
            qP              qP
              n−1 2             n−1 e 2
              k=0 Tk (x) −      k=0 Tk (x)         1
          =       qP                        + qP 2          .
                        n−1 2                    n−1 2
                           T
                        k=0 k (x)                    T
                                                 k=0 k  (x)


                                                             52
Here, the numerator of the first term can be further bounded by
             v              v
             un−1           un−1             Z Pn−1 T2 (x)            3
             uX             uX                   k=0    k     1
             t      2
                   Tk (x) − t         2
                                   Tk (x) = P
                                    e                      du √ ≤ qP 8          .              (211)
                                                n−1 e 2
                                                k=0 Tk (x)
                                                             2 u    n−1 e 2
               k=0             k=0                                      T
                                                                    k=0 k   (x)

The claimed bound now follows from Lemma 17.

    Putting it altogether, we finally obtain that output state of the quantum linear system algorithm
|φ⟩ has error at most
                        Pn−1       
                                     λ
                               T j αA |j⟩|ψλ ⟩                 √
                                                                                    
                           j=0                                                   1
                 |φ⟩ − P                         = ϵlin + O nαU ϵinit + O √          .        (212)
                           n−1
                               Tj λ |j⟩|ψ ⟩                                        n
                            j=0    αA          λ


4.4   Summary of quantum eigenvalue estimation
We now summarize the quantum algorithm for estimating eigenvalues.
  1. If necessary, rescale the input block encoding using Eq. (113), so that αA ≥ 2 ∥A∥.
  2. Invoke the Chebyshev state generation algorithm Theorem 1 with η = 0, coefficients βek from
     Eq. (171), and a state |ψ⟩ close to the target eigenstate.
  3. Perform the quantum Fourier transform and measure in the computational basis.
  4. Perform the median amplification to boost the success probability.
Theorem 3 (Quantum eigenvalue estimation). Let A be a square matrix with only real eigenvalues,
such that A/αA is block encoded by OA with some normalization factor αA ≥ ∥A∥.      p Suppose that
oracle Oψ |0⟩ = |ψ⟩ prepares an initial state within distance |ψ⟩ − |ψλj ⟩ = O( ϵ/αA /αU ) from
an eigenstate |ψλj ⟩ such that A|ψλj ⟩ = λj |ψλj ⟩, where αU satisfies Eq. (157) with
                                                     α 
                                                        A
                                             n=O           .                                 (213)
                                                       ϵ
Then, the eigenvalue λj can be estimated with accuracy ϵ and probability 1 − pfail using
                                                         
                                         αA           1
                                     O      αU log                                             (214)
                                          ϵ          pfail
queries to controlled-OA , controlled-Oψ , and their inverses.
Proof. Assume that the input matrix A/αA is block encoded with normalization factor αA ≥ 2 ∥A∥,
that the input state |ψ⟩ = |ψλj ⟩ is the exact eigenstate, and that the quantum linear system solver
makes no error, while ignoring the distinction between T0 (x) = 1 and T      e 0 (x) = 1 . Then the
                                                                                       2
Chebyshev state phase estimation of Section 4.2 (in particular, Theorem 2) shows that we can get
a measurement outcome l ∈ {0, . . . , n − 1} satisfying
                                                 
                                                l           2παA n1
                                    αA cos 2π       − λj ≤                                     (215)
                                               n               n
with probability at least
                                                       n1
                                        1−          √            .                           (216)
                                               n1 − 2 3 3 (n1 − 2)

                                                     53
For n1 ≥ 5, the success probability is at least 1 − 15−25√
                                                           3
                                                             ≈ 0.566 strictly larger than 12 . We can
then choose                                       α 
                                                      A
                                             n=O                                                (217)
                                                     ϵ
so that the target eigenvalue λj is estimated with accuracy ϵ.
    Now consider the general case. The analysis of Section 4.3 shows that output of the quantum
linear system solver is close to the ideal Chebyshev state with Euclidean distance at most
                                            √
                                                                
                                                             1
                                  ϵlin + O nαU ϵinit + O √         .                            (218)
                                                               n

But for two quantum states with distance ∥|φ1 ⟩ − |φ2 ⟩∥ ≤ δ, if we apply a unitary U followed by
an orthogonal projection Π, the amplitudes differ at most

                        |∥ΠU |φ1 ⟩∥ − ∥ΠU |φ2 ⟩∥| ≤ ∥ΠU |φ1 ⟩ − ΠU |φ2 ⟩∥ ≤ δ,                    (219)

which implies difference of the probabilities

                    ∥ΠU |φ1 ⟩∥2 − ∥ΠU |φ2 ⟩∥2 ≤ 2 |∥ΠU |φ1 ⟩∥ − ∥ΠU |φ2 ⟩∥| ≤ 2δ.                 (220)

Thus if we have δ = O(1) sufficiently small, we still guarantee a success probability strictly larger
than 21 in the Chebyshev state phase estimation, even after accounting for the success probability
of the quantum linear system solver (Lemma 10), which can then be boosted using the median
                                                                                    √
amplification. To achieve this, we let ϵlin = O(1) sufficiently small, ϵinit = O(1/( nαU )) sufficiently
small, and n = Ω(1) sufficiently large. However, we already have the stronger requirement n =
Θ (α
   pA /ϵ) to achieve the desired accuracy in the Chebyshev state phase estimation, so ϵinit =
O( ϵ/αA /αU ). Our proof is now complete with the claimed complexity from Theorem 1.

Remark. The complexity of our algorithm depends on size αU of the input matrix under Chebyshev
polynomials of the second kind. See the remark succeeding Theorem 1 for more discussions about
this parameter. When the input matrix is diagonalizable with a known upper bound κS on its
Jordan condition number, we have αU = O(κS ) and the complexity becomes
                                                         
                                         αA κS        1
                                    O          log            .                          (221)
                                           ϵ         pfail

This achieves the so-called Heisenberg scaling [38, 99] in quantum metrology and is provably optimal
for the eigenvalue estimation.
    In the actual circuit implementation, we need to prepare a quantum state Oβe|0⟩ = α1e n−1
                                                                                          P
                                                                                            k=0 (βk −
                                                                                                  e
                                                                                        β
                                                                               q
                                                                                 Pn−1 e             2
βek+2 )|n − 1 − k⟩ encoding the shifted coefficients with normalization αβe =       k=0 |βk − βk+2 | .
                                                                                              e
                                                                                            |0⟩−|2⟩
For eigenvalue estimation, we have all βek = 0 except βen−1 = 1. The resulting state √            2
                                                                                                    is
2-dimensional, and can be prepared with O(1) cost.
    Finally, note that the query complexity of initial state preparation can be improved using the
block preconditioning technique of [65].


5    Quantum eigenvalue transformation
In this section, we use the Chebyshev history state to construct a quantum algorithm that trans-
forms eigenvalues of a high-dimensional input matrix. With all the technical preliminaries already

                                                  54
in place, we describe this algorithm and analyze its complexity in Theorem 4 of Section 5.1. We also
describe a variant of the algorithm in Theorem 5 of Section 5.2 based on a block encoded quantum
linear system solver, which can be useful when QEVT is used as a subroutine in desigining other
quantum algorithms.

5.1    Summary of quantum eigenvalue transformation
We now summarize the quantum algorithm for transforming eigenvalues.

   1. Invoke the ChebyshevP
                          state generation algorithm Theorem 1 with η = 1, coefficients βek from
      the expansion p(x) = n−1
                            k=0 βk Tk (x), and input state |ψ⟩.
                                e e

   2. Perform a fixed-point amplitude amplification on part of the state flagged by the ancilla |1⟩.

Theorem 4 (Quantum eigenvalue transformation). Let A be a square matrix with only real eigen-
values, such
        P that    A/αA isP block encoded by OA with some normalization factor αA ≥ ∥A∥. Let
p(x) = n−1k=0 β T
              ek e k (x) =  n−1
                            k=0 βk Tk (x) be the Chebyshev expansion of a degree-(n −P1) polyno-
mial p. Let Oψ |0⟩ = |ψ⟩ be the oracle preparing the initial state, and Oβe|0⟩ = α e n−1
                                                                                   1
                                                                                       k=0 (βk −
                                                                                            e
                                                                                                             β

       q − 1 − k⟩ be the oracle preparing the shifting of coefficients βk (k = 0, . . . , n − 1) with
βek+2 )|n                                                              e
          Pn−1 e           2
αβe =      k=0 |βk − βk+2 | . Then, the quantum state
                     e
                                                                  
                                                              A
                                                      p       αA       |ψ⟩
                                                                                                               (222)
                                                              A
                                                      p       αA       |ψ⟩

can be prepared with accuracy ϵ and probability 1 − pfail using
                                                                     
                                  α eT,ψ            α eT,ψ          1
                             O           αU n log            log                                                 (223)
                                  αp,ψ              αp,ψ ϵ         pfail
queries to controlled-OA , controlled-Oψ , controlled-Oβe, and their inverses, where αU is defined in
Eq. (157) and
                                        n−1                                                     
                                        X                     A                               A
               αT,ψ ≥      max                βek T
                                                  e k−l                |ψ⟩ ,   αp,ψ ≤ p                |ψ⟩       (224)
                                                              αA                              αA
                e
                        l=0,1,...,n−1
                                        k=l

are upper bound on the maximum shifted partial sum of the Chebyshev expansion and lower bound
on the transformed state.

Proof. With η = 1, the Chebyshev history state from Theorem 1 reads
                                                    Pn−1 Pn−1 e e  A 
      |0⟩ n−1
         P         Pn−1                  A
           l=0 |l⟩  k=n−1−l βk Tk+l−n+1 αA |ψ⟩ + |1⟩    l=0 |l⟩  k=0 βk Tk αA |ψ⟩
                            e e
         r                                                                        .                              (225)
           Pn−1 Pn−1                             2                       2
                                          A              P  n−1        A
                     k=n−1−l βk Tk+l−n+1 αA |ψ⟩      +n     k=0 βk Tk αA |ψ⟩
                             e e                                e e
              l=0


Applying the fixed-point amplitude amplification on the ancilla state |1⟩ then produces a quantum
state close to               Pn−1 e e  A                  
                                                             A
                                   β T
                                k=0 k k αA     |ψ⟩       p  αA |ψ⟩
                             Pn−1 e e  A           =                                     (226)
                                                             A
                                   β T
                                k=0 k k αA     |ψ⟩       p  αA   |ψ⟩

                                                              55
as desired.
     To achieve a success probability at least 1 − pfail , we take a number of amplification steps scaling
like
       r                                                                                            
            Pn−1 Pn−1                                   2      Pn−1 e e  A         2
                                                 A
                                  β T
                                  ek e k+l−n+1 αA    |ψ⟩    + n        β T
                                                                    k=0 k k αA    |ψ⟩              
              l=0      k=n−1−l                                                                 1 
     O                             r                                                    log         
                                         Pn−1 e e  A          2                             pfail 
                                       n    k=0 βk Tk αA |ψ⟩
                             
             αT,ψ         1
     =O            log            ,
              e

             αp,ψ        pfail
                                                                                                      (227)
where αT,ψe   defined in Eq. (224) is an upper bound on the shifted partial sum of the Chebyshev
expansion. To achieve a total accuracy ϵ, we require each preparation of the Chebyshev history
state to have error at most O (αp,ψ ϵ/αT,ψ   e ). The claimed complexity now follows from Theorem 1

and the above analysis.

Remark. The complexity of our algorithm depends on parameters such as αU and αT,ψ
                                                                                e , the former

of which has already been discussed in the remark succeeding Theorem 1. The parameter α eT,ψ
denotes maximum size of the shifted Chebyshev expansion, and it can be further upper bounded
in terms of the Jordan condition number. For instance, if A/αA = SJS −1 is the Jordan form
decomposition of the input matrix, with an upper bound κS ≥ ∥S∥ ∥S∥−1 on the Jordan condition
number
       and dmax size of the largest
                                    Jordan block, then we show in Appendix A.2 that α e
                                                                                         T,ψ =

O κS ndmax −1 log(n) ∥p∥max,[−1,1] . In particular, we have αT,ψ  e   = O κS log(n) ∥p∥max,[−1,1] for
diagonalizable matrices, leading to the complexity
                                                                                       
                  ∥p∥max,[−1,1] κ2S n       ∥p∥max,[−1,1] κS log(n)
                                                                                        
                                                                                    1
              O                    log                         log(n) log                (228)
                      p αAA |ψ⟩                 p αAA |ψ⟩ ϵ                        pfail

for a worst-case input. However, we further show that the log(n) factors can be shaved off
                                                                                
                         ∥p∥max,[−1,1] κ2S n       ∥p∥max,[−1,1] κS
                                                                                 
                                                                             1
                     O                    log                  log                           (229)
                           p A |ψ⟩                  p A |ψ⟩ ϵ               pfail
                                 αA                      αA

when running the algorithm on an average input matrix (Appendix A.3). Specifically, if the dis-
tribution of eigenvalues
                        of A does not depend on the target polynomial degree n, then the vector
         Pn−1 e e        A
norm       k=l βk Tk−l αA |ψ⟩ admits an upper bound independent of n. This is reminiscent of
the fact that Fourier expansions can converge much faster on average, and is made rigorous by the
Carleson-Hunt inequality from Lemma 5.
    The circuit implementation of QEVT requires preparing the state Oβe|0⟩ = α1e n−1
                                                                                         P
                                                                                           k=0 (βk −
                                                                                                e
                                                                                       β
                              q
                                Pn−1 e            2
βek+2 )|n − 1 − k⟩ with αβe =     k=0 |βk − βk+2 | encoding shifted coefficients from the Chebyshev
                                            e
expansion. We show how such a state can be prepared using O (polylog(n)) gates in Section 6,
improving over the standard state preparation method with complexity Θ(n).
    Finally, note that the query complexity of initial state preparation can be improved using the
block preconditioning technique of [65].



                                                    56
5.2    Summary of quantum eigenvalue transformation, block encoded version
We now summarize a variant of the quantum eigenvalue transformation algorithm with a block
encoding output.
  1. Construct a block encoding of Pad(A)/4 as in Section 3.2 with η = 1.

  2. Invoke the block encoding version of quantum linear system solver Lemma 11 with Pad(A)/4
     as the input.
                                                                 q
                            1 Pn−1 e                               Pn−1 e            2
  3. Prepare the state |0⟩ α e k=0 (βk −βk+2 )|n−1−k⟩ with αβe =
                                        e
                                                                     k=0 |βk − βk+2 | . Unprepare
                                                                               e
                             β

     the state |1⟩ √1n n−1
                      P
                        k=0 |k⟩.

  4. Amplify the block encoding using Lemma 12.
Theorem 5 (Quantum eigenvalue transformation, block encoded version). Let A be a square matrix
with only real eigenvalues, such that A/αAPis block encoded by OA with some normalization factor
                        Pn−1                n−1
αA ≥ ∥A∥. Let p(x) = k=0 βk Tk (x)
                               e e
                                       =  k=0 βk Tk (x) be the Chebyshev expansion of a degree-n
                                                 A
polynomial p. Then for any αp ≥ p                αA     , the operator
                                                                      
                                                                  A
                                                          p       αA
                                                                                                                             (230)
                                                              2αp
can be block encoded with accuracy ϵ using
                                   √                                                              √           !        !
               ∥p(cos) sin∥2,[−π,π] nαU                             ∥p(cos) sin∥2,[−π,π]              nαU              1
           O                            nαU log                                                                   log        (231)
                           αp                                                        αp ϵ                              ϵ

queries to controlled-OA and its inverse, where αU satisfies Eq. (157)
Proof. Applying Lemma 11 to Pad(A)/4, we get a block encoding of

                                                        Pad(A)−1
                                                                                                                             (232)
                                                        2αPad(A)−1
                                                                                             Pn−1 e
with αPad(A)−1 = O (αU n). Together with the preparation of |0⟩ α1e                           k=0 (βk − βk+2 )|n − 1 − k⟩ and
                                                                                                        e
                                                                  β

unpreparation of |1⟩ √1n n−1
                        P
                          k=0 |k⟩, we obtain the block encoding

                n−1                                n−1
                             !                                                      !
            1 X                  Pad(A)−1       1 X e
       ⟨1| √    ⟨k| ⊗ I                    |0⟩         (βk − βek+2 )|n − 1 − k⟩ ⊗ I
             n                   2αPad(A)−1    αβe
                k=0                                k=0
                                 n−1                                    n−1
                                           !                                                    !
                 1               X
                                                       −1
                                                                        X
       =√                    ⟨1|    ⟨k| ⊗ I Pad(A) Pad(B) |0⟩               βek |n − 1 − k⟩ ⊗ I                              (233)
            nαPad(A)−1 αβe
                                   k=0                                                      k=0
                                                                                                                  
                                                                                                              A
                             n−1                  n−1         n−1                                     p
                                             !                                              !
                 1           X                    X           X                 A                             αA
       =√                          ⟨k| ⊗ I              |l⟩         βek e
                                                                       Tk                ⊗I       =
            nαPad(A)−1 αβe                                                      αA                     αp,pre
                             k=0                  l=0         k=0

with
                                                 αPad(A)−1 αβe     √     
                                   αp,pre =          √         = O αU nαβe ,                                                 (234)
                                                       n

                                                               57
where the first equality follows from Eq. (159) and Eq. (137), and the second equality follows from
Eq. (139).
   We now claim that Euclidean norm of the shifted coefficients scales like
                               v
                               un−1                                         
                               uX
                         αβe = t     |βek − βek+2 |2 = O ∥p(cos) sin∥2,[−π,π] .               (235)
                                 k=0

Here the Chebyshev coefficients are shifted in the time domain, so the target function will have a
phase shift in the frequency domain. Indeed, a direct calculation shows that

                                  2 π
                                    Z
                      βj − βj+2 =
                       e   e            dθ p(cos(θ)) (cos(jθ) − cos((j + 2)θ))
                                  π 0
                                    Z π
                                  4
                                =       dθ p(cos(θ)) sin(θ) sin((j + 1)θ)                    (236)
                                  π 0
                                    Z π
                                  2
                                =       dθ p(cos(θ)) sin(θ) sin((j + 1)θ).
                                  π −π

Thus, βej − βej+2 can be seen as the Fourier coefficients of the odd function 2p(cos θ) sin θ. Invoking
Parseval’s theorem with the convention that βen = βen+1 = · · · = 0, we have
                  v
                  u∞                     s Z
                  uX                      1 π
           αβe = t     |βek − βek+2 |2 =        dθ 4 |p(cos θ) sin θ|2 ∼ ∥p(cos) sin∥2,[−π,π] .   (237)
                                          π −π
                   k=0

The theorem now follows from Lemma 12.

Remark. For a discussion about the scaling of αU , see the remark succeeding Theorem 1. This
block encoding version of the eigenvalue transformation algorithm (Theorem 5) underperforms the
state version (Theorem 4) for the differential equation problem and the ground state preparation
problem to be considered in Section 7. This is because both versions have a similar gate complexity
to generate the Chebyshev history state. But the block encoding algorithm introduces an additional
normalization factor αp,pre , which needs to be further amplified. It is for this reason that Theorem 5
will not be used in the remainder of the paper. However, the block-encoded version can become
useful when QEVT is invoked as a subroutine in designing other quantum algorithms. The scaling
O(n1.5 ) with degree of the target polynomial is improved to O(n) by recent work [65] through block
preconditioning.
    To implement this algorithm with quantum circuits, we need to prepare the state α1e n−1
                                                                                             P
                                                                                               k=0 (βk −
                                                                                                    e
                                                                                          β

βek+2 )|n − 1 − k⟩ encoding the shifted Chebyshev coefficients. As discussed in the remark succeed-
ing Theorem 4, this state can be prepared using the technique from Section 6. However, unlike
Theorem 4, we only need to prepare this state once to get the preamplified block encoding. Hence,
the cost of the state preparation is much less than that for inverting Pad(A)/4, so it may also be
acceptable to prepare this state using the conventional approach [83].
    Finally, the normalization factor ∥p(cos) sin∥2,[−π,π] corresponds to the L2 -norm of the phase
shifted function p(cos(θ)) sin(θ) evaluated in the frequency domain. We assume that this norm can
be efficiently computed to arbitrary precision on a classical computer as is often the case; otherwise,
we can replace it with a known upper bound αp(cos) sin ≥ ∥p(cos) sin∥2,[−π,π] . Asymptotically, this




                                                  58
is better than the more familiar ∥p∥max,[−1,1] since
                          sZ                                   s Z
                             π                                          π
                                                      2
 ∥p(cos) sin∥2,[−π,π] =             dθ |p(cos θ) sin θ| =       2           dθ |p(cos θ)|2 sin2 θ
                               −π                                   0
                          s                                                                             (238)
                                 Z −1             p                                     
                     =      −2          dx |p(x)|2 1 − x2 = O ∥p∥2,[−1,1] = O ∥p∥max,[−1,1] .
                                    1


6     Fourier coefficients generation
In this section, we describe an efficient quantum circuit for generating n Fourier coefficients, encoded
by the amplitudes of a quantum state. This state can be prepared using standard circuit techniques
with a gate complexity of Θ(n). However, our truncate order n in general scales polynomially with
the input parameters (such as the evolution time and the inverse spectral gap), and can lead to a
significant overhead. Our new result has gate complexity O(polylog(n)).
    We begin by introducing the problem in Section 6.1, explaining how the generation of Fourier
coefficients can be achieved with a frequency domain convolution. Such a convolution is given by
a Riemann integral, which we implement using the circuit described in Section 6.2. However, due
to presence of the Dirichlet kernel, integrand of the convolution changes dramatically throughout
the entire domain, which can be costly to implement directly. We apply a rescaling principle
for Riemann integrals to significantly reduce the implementation cost in Section 6.3. Finally, we
summarize the quantum circuit for generating the Fourier coefficients as Theorem 6 and analyze it in
Section 6.4. The generation of Chebyshev coefficients follows immediately as Chebyshev expansions
can be reformulated as Fourier expansions through a change of variables.

6.1   Fourier coefficients generation with frequency domain convolution
Let g be a 2π-periodic function with the Fourier expansion
                     ∞
                     X
            g(ω) =            ξj e−ijω = · · · + ξ−2 e2iω + ξ−1 eiω + ξ0 + ξ1 e−iω + ξ2 e−2iω + · · ·   (239)
                     j=−∞

Then the problem of generating Fourier coefficients is to construct a block encoding for the operator
                                                                
                                               ξ0
                                n−1          ξ1
                                X                     ξ0         
                                    ξj Lj =  .                  ,                             (240)
                                                                
                                             ..     .. ..
                                        j=0
                                                        .   .    
                                                     ξn−1 · · ·         ξ1     ξ0

where {ξj }n−1
            j=0 are the first n Fourier coefficients with nonnegative indices, and L is the n-by-n
lower shift matrix.
   There are a number of places in the paper where we need an efficient quantum circuit for
generating Fourier coefficients. For instance, in the Chebyshev eigenvalue transformation algorithm,
we need to prepare an initial state of the following form encoding the shifted Chebyshev coefficients
                                                                   v
                             n−1                                   un−1
                          1  X                                     uX
                Oβe|0⟩ =        (βek − βek+2 )|n − 1 − k⟩,   αβe = t     |βek − βek+2 |2 .     (241)
                         αβe
                                k=0                                                  k=0



                                                          59
This can be achieved by treating the Chebyshev expansion as a Fourier expansion, and applying the
                                                    P            n−1 e
                                                                 j=0 βj |j⟩
above block encoding to |0⟩. This generates the state         , which can be shifted to the desired
                                                       ∥βe∥
form by applying (I − L)/2 followed by a further amplitude amplification. On the other hand, for
the Faber-based algorithm to be discussed in Section 8.2, we need to block encode operators such
as
                                    Ψ′ (L−1 ),    LΨ(L−1 ),                                   (242)
where both functions have Laurent expansions with only nonnegative powers (they are purely power
series expansions):

        Ψ′ (w−1 ) = ς − ς1 w2 − 2ς2 w3 + · · ·        wΨ(w−1 ) = ς + ς0 w + ς1 w2 + ς2 w3 + · · ·         (243)

To handle this, we take w → e−iω and turn the above Laurent expansions into Fourier expansions

 Ψ′ (eiω ) = ς − ς1 e−2iω − 2ς2 e−3iω + · · ·     e−iω Ψ(eiω ) = ς + ς0 e−iω + ς1 e−2iω + ς2 e−3iω + · · · (244)

Thus we can invoke our circuit with respect to the Fourier expansions of Ψ′ (eiω ) and e−iω Ψ(eiω )
and obtain the desired block encoding.
   The key idea behind our approach is to generate the Fourier coefficients using a frequency
domain convolution. To be more specific, recall from Lemma 14 that for j = 0, 1, . . . , n − 1,
                                                      j
               Ljn = (I2n ⊗ ⟨0|) CMP2n,2 (I2n ⊗ |0⟩) X2n (I2n ⊗ ⟨0|) CMP2n,2 (I2n ⊗ |0⟩) .                (245)

Here,Pthe cyclic shift operator X2n can be P diagonalized by the quantum Fourier transform F2n =
                2π
       2n−1 −i 2n                        †             2π
√1
 2n    l,m=0 e
                   lm
                      |l⟩⟨m| as F2n X2n F2n = 2n−1
                                               m=0 e
                                                    −i 2n m
                                                            |m⟩⟨m| = Z2n , resulting in
                                               
                                             †     j
      Ljn = (I2n ⊗ ⟨0|) CMP2n,2 (I2n ⊗ |0⟩) F2n   Z2n (F2n (I2n ⊗ ⟨0|) CMP2n,2 (I2n ⊗ |0⟩)) .             (246)

Thus for each diagonal element of Z2n labeled by m = 0, 1, . . . , 2n − 1, we need to implement
                                       2π             2π                           2π
                           ξ0 + ξ1 e−i 2n m + ξ2 e−2i 2n m + · · · + ξn−1 e−(n−1)i 2n m .                 (247)

Comparing Eq. (239) and Eq. (247), we arrive at the integral representation

              2π             2π                           2π      1
                                                                    Z π       mπ     1 − e−niu
  ξ0 + ξ1 e−i 2n m + ξ2 e−2i 2n m + · · · + ξn−1 e−(n−1)i 2n m =        du g      −u                      (248)
                                                                 2π −π          n      1 − e−iu

from the frequency domain convolution theorem. The circuit implementation of such a Riemann
integral will be discussed in the next subsection.

6.2    Block encoding Riemann integrals
Suppose we have a function h : [a, b] → C with max-norm ∥h∥max,[a,b] that is µh -Lipschitz continuous
such that |h(z) − h(w)| ≤ µh |z − w| for all z, w ∈ [a, b]. Our goal here is to construct a block
encoding of the Riemann integral
                                             Rb
                                              a dx h(x)
                                                              .                                 (249)
                                         (b − a) ∥h∥max,[a,b]
   This is achieved by approximating the integral with a Riemann sum which can then be im-
plemented using standard techniques. Here we include a description of this block encoding for
completeness. To this end, let us first describe the oracular access model for the input function

                                                           60
h. We assume that the input register takes nin values, and two output registers take (nAbs + 1)
and nArg values, holding the absolute value and argument of h respectively. Then we introduce the
oracles                                                        
                                                   h a + b−a
                                                          nin s      
                      OAbs |s, 0⟩ = s, Floor nAbs                 ,
                                                    ∥h∥max,[a,b]
                                                                                      (250)
                                                   Arg h a + b−a nin s     
                      OArg |s, 0⟩ = s, Floor nArg                        .
                                                           2π

Here, we segment [a, b] into nin subintervals labeled by s = 0, 1, . . . , nin −1, so that a+ b−a s approx-
                                                                                            nin
imately represents a general number from [a, b]. The absolute value h a + b−a          nin s  is normalized
                                                              !
                                                         h a+ b−a s
by the max-norm ∥h∥max,[a,b] , so that Floor nAbs ∥h∥ nin           = 0, 1, . . . , nAbs can be held by the
                                                     max,[a,b]
                                                                  
first output register. Similarly, the argument Arg h a + b−a   nin s    ∈ [0, 2π) is normalized by 2π,
                                  !
                      Arg h a+ b−a
                               n
                                   s
so that Floor nArg           2π
                                  in
                                         = 0, 1, . . . , nArg − 1 can be represented in the second output

register. Note that the value of max-norm ∥h∥max,[a,b] can often be efficiently computed to arbi-
trary precision on a classical computer. But our method still works if the exact value of max-norm
is replaced by its upper bound αh,max ≥ ∥h∥max,[a,b] . We now implement the block encoding as
follows.

Lemma 21 (Block encoding Riemann integrals). Let h : [a, b] → C be a µh -Lipschitz function with
max-norm ∥h∥max,[a,b] . Suppose that its absolute value and argument are provided by the oracles
                                                                 
                                                     h a + b−a
                                                           nin  s      
                        OAbs |s, 0⟩ = s, Floor nAbs                 ,
                                                      ∥h∥max,[a,b]
                                                                                               (251)
                                                                   b−a
                                                     Arg h a + nin s        
                        OArg |s, 0⟩ = s, Floor nArg                       ,
                                                            2π

with an nin -value input register, and (nAbs + 1)- and nArg -value output registers respectively. Then,
the normalized integral
                                              Rb
                                               a dx h(x)
                                                                                                  (252)
                                          (b − a) ∥h∥max,[a,b]
can be block encoded with accuracy δ by setting nin = O(µh (b − a)/(∥h∥max,[a,b] δ)), nAbs , nArg =
O(1/δ), using 2 queries to OAbs and 1 query to OArg , together with
                                                            !!
                                              µh (b − a)
                                   O log                                                      (253)
                                             ∥h∥max,[a,b] δ

two-qubit gates.

Proof. We perform the block encoding as follows:



                                                    61
1. We prepare a uniform superposition state
                                                         in n −1
                                                    1    X
                                                   √        |s⟩                                              (254)
                                                     nin
                                                                s=0

  for nin sufficiently large. This has gate complexity O(log(nin )).

2. We apply the oracle OAbs . This has query complexity 1.

3. We introduce the uniform superposition state

                                                       1    X−1
                                                           nAbs
                                                  √             |x⟩                                          (255)
                                                      nAbs
                                                                x=0

  and test the inequality                                              
                                                        h       a + b−a
                                                                    nin s
                                     Floor nAbs                             ≤ x.                           (256)
                                                         ∥h∥max,[a,b]

  The state of the entire system becomes
                     v                       
                                                              v                           
                                                                                                       
                                   h a+ b−a                                    h a+ b−a
                      u                                      u          
                      u                 nin
                                            s                 u                     nin
                                                                                        s
          nin −1     u Floor nAbs ∥h∥                        u     Floor nAbs ∥h∥                     
      1    X                          max,[a,b]                                   max,[a,b]
                                                                                                             (257)
                     t                                       t                                        
     √           |s⟩                             |ϕ 0 ⟩|0⟩ +   1 −                           |ϕ 1 ⟩|1⟩
       nin s=0       
                               nAbs                                        nAbs
                                                                                                       
                                                                                                       


   for some auxiliary states |ϕ0 ⟩ and |ϕ1 ⟩. This has gate complexity O(log(nAbs )).

4. We apply the oracle OArg . This has query complexity 1.
5. We prepare a phase gradient state over nArg values, and add the argument to it with gate
   complexity O(log(nArg )) [77, Appendix A]. Omitting unnecessary registers, we obtain
                                                                 
         1
             nin −1
              X             2π                 Arg h a + b−a   nin
                                                                   s
        √           exp i      Floor nArg                             |s⟩
          nin s=0          nArg                            2π
               v                                             v                                         
                                                                                                             (258)
                                                                                        
                                  h a+ b−a                                      h a+ b−a
                  u                                          u           
                  u                    nin
                                           s                  u                      nin
                                                                                         s
               u Floor nAbs ∥h∥                              u      Floor nAbs ∥h∥                     
               t                    max,[a,b]                t                    max,[a,b]            
             ⊗                                  |ϕ 0 ⟩|0⟩ +    1 −                            |ϕ 1 ⟩|1⟩.
               
                               nAbs                                          nAbs
                                                                                                        
                                                                                                        



6. We introduce an ancilla register in state |0⟩ and swap out outcome of the inequality test
                                                             
       1
           nin −1
            X             2π                 Arg h a + b−a nin
                                                               s
      √           exp i      Floor nArg                           |s⟩
        nin s=0          nArg                          2π
             v                                            v                                           
                                                                                                             (259)
                                                                                     
                                h a+ b−a s                                   h a+ b−a
                u                                         u            
                                                                                      s
             u Floor nAbs ∥h∥ nin                                                nin
                u                                          u
                                                           u      Floor nAbs ∥h∥                       
             t                    max,[a,b]               t                    max,[a,b]              
           ⊗                                |ϕ0 ⟩|0, 0⟩ + 1 −                             |ϕ1 ⟩|0, 1⟩
                                                                                                       .
                             nAbs                                        nAbs                         




                                                       62
  7. Finally, we reverse the first four steps. This is described by the bra vector (omitting unnec-
     essary registers)
                              v                       
                                                                          v                          
                                                                                                                     
                                            h a+ b−a                                      h a+ b−a
                               u                                         u         
                               u                 nin
                                                     s                    u                    nin
                                                                                                   s
                    nin −1    u Floor nAbs ∥h∥                           u    Floor nAbs ∥h∥                        
                1    X        t               max,[a,b]                  t                  max,[a,b]               
               √          ⟨s|                             ⟨ϕ 0 |⟨0, 0| +  1 −                           ⟨ϕ1 |⟨1, 0| .
                 nin s=0      
                                        nAbs                                          nAbs                          
                                                                                                                     

                                                                                                                                     (260)

   The above procedure allows us to block encode
                                                                                                                               !
                                                                                                                         b−a
                                                                             h a+     s
                                                                  Floor nAbs ∥h∥ nin
                                                         
             in −1                                     b−a
         1
            nX
                           2π              Arg  h  a + nin s                    max,[a,b]
                   exp i      Floor nArg                     
        nin               nArg                     2π                     nAbs
             s=0
                                                         !
                                                                       h a+ b−a
                                                                            n
                                                                                s
                                                 Floor nAbs ∥h∥
                                                                               in
                in −1
               nX                                                         max,[a,b]
         1
                              
  (1)                    iArg h a+ b−a s
  ≈                     e          n      in
                                                                                                                                     (261)
        nin                                       nAbs
                s=0
                                                      
          nin −1                    h a + b−a s
  (2) 1
                       
                  iArg h a+ b−a  s             nin
           X
  ≈              e           nin
      nin                               ∥h∥max,[a,b]
           s=0
                              
          nin −1 h a + b−a s              Rb
       1 X                                 a dx h(x)
                         nin      (3)
   =                              ≈                        .
      nin          ∥h∥max,[a,b]       (b − a) ∥h∥max,[a,b]
                s=0

                                                                                        1
It is easy to see that the first error is at most n2π
                                                   Arg
                                                       and the second error is at most nAbs . So our
remaining task is to bound the third error, which comes from discretizing the Riemann integral as
a Riemann sum.
    We discretize the integral as
                        Z b                     in −1 Z a+ b−a (s+1)
                                               nX                                      in −1
                                                                                      nX
                                                                                               b−a       b−a
                                                                                                              
                                                            nin
                              dx h(x) =                                 dx h(x) ≈                   h a+      s .                    (262)
                         a                              a+ b−a s                                nin       nin
                                                s=0        nin                         s=0

Since h is µh -Lipschitz, within each subinterval the error contribution is at most
 Z a+ b−a (s+1)                                    Z a+ b−a (s+1)
                                        b−a                                     b−a         (b − a)2
                                            
         nin                                            nin
                        dx h(x) − h a +      s   ≤                dx µh x − a −      s = µh          .
   a+ b−a
      n
          s                              nin        a+ b−a s                     nin
                                                                                nin
                                                                                              2n2in
         in
                                                                                                                                     (263)
So altogether,
                                                           
                                     in −1 h
                                    nX             a + b−a
                                                       nin s
                                                                         Rb
                               1                                          a dx h(x)                   µh (b − a)
                                                                 −                             ≤                     .               (264)
                              nin              ∥h∥max,[a,b]          (b − a) ∥h∥max,[a,b]          2nin ∥h∥max,[a,b]
                                    s=0

                                                                                µh (b−a)
The proof is now complete by choosing nin , nAbs , nArg such that n2π , 1 ,
                                                                   Arg nAbs 2nin ∥h∥
                                                                                                                               = O(δ).
                                                                                                                   max,[a,b]




                                                                          63
6.3   Rescaling principle for Riemann integrals
Now that we have the quantum circuit for implementing Riemann integrals, it is tempting to apply
it directly to the frequency domain convolution in Eq. (248). However, this would result in a
gate complexity scaling linear in n, same as that of the standard approach for state preparation.
The underlying reason is that our convolution in Eq. (248) is essentially defined with respect to
the Dirichlet kernel, whose function value changes dramatically over the domain of interest. In
particular, L∞ -norm of the Dirichlet kernel grows like Θ(n) which determines the block encoding
normalization factor as per Lemma 21, although its L1 -norm only scales like Θ(log(n)).
    Our idea to overcome this catastrophe is to use the following rescaling principle for Riemann
integrals.

Lemma 22 (Rescaling principle for Riemann integrals). Let h : [a, b] → C and α : [a, b] → R>0 be
continuous. Then the primitive function
                                               Z t
                                      α1 (t) =     dτ α(τ )                                (265)
                                                        a

is positive, continuously differentiable, and monotonically increasing on [a, b], such that

                                             h α1−1 (s)                   h α1−1 (s)
                   Z b           Z α1 (b)               Z ∥α∥                      
                                                               1,[a,b]
                       dt h(t) =          ds            =             ds            .          (266)
                    a             0          α α1−1 (s)    0              α α1−1 (s)

Proof. This is just a change of variables with s = α1 (t).

    A similar rescaling principle was previously introduced for simulating time-ordered integra-
tors [13]. Here, we use this technique to improve the circuit implementation of scalar Riemann
integrals. To this end, we choose α(τ ) ∼ |h(τ )| so that absolute value of the rescaled integrand

                                   h α1−1 (s)     h α1−1 (s)
                                                           
                                               ∼            =1                                 (267)
                                   α α1−1 (s)     h α1−1 (s)

is almost uniform, over the rescaled interval of length
                                            Z b                Z b
                    a1 (b) = ∥α∥1,[a,b] =         dτ α(τ ) ∼         dτ |h(τ )| = ∥h∥1,[a,b] .   (268)
                                             a                  a

This technique thus helps “flatten out” a function whose instantaneous value may change dramat-
ically over the domain.
    Toward generating the Fourier coefficients via Eq. (248), we further simplify the frequency
domain convolution as

          1
            Z π       mπ      1 − e−niu    1
                                                Z π        mπ      n−1 sin nu 
                du g      −u              =          du g      − u e− 2 iu          2
         2π −π          n       1 − e−iu    2π −π            n                sin u2
                                               Z π                                         (269)
                                             1 2          mπ      
                                                                      −(n−1)iv sin (nv)
                                          =         dv g       − 2v e                   .
                                            π −π            n                   sin (v)
                                                        2


We will break the integral into the following 4 parts:




                                                       64
       π
1. [0, 2n ]: In this case, we have the integral
                                                     π
                                           1                     mπ                            sin (nv)
                                               Z
                                                    2n
                                                                            
                                                         dv g          − 2v e−(n−1)iv                    .                  (270)
                                           π    0                 n                              sin (v)

   The L∞ -norm of the integrand multiplied by length of the interval is bounded by

      π 1        mπ               sin (nv)    1                   nv  π
          max g      − 2v e−(n−1)iv          ≤    ∥g∥max,[−π,π] max 2v = ∥g∥max,[−π,π] .
      2n π v       n                 sin (v)   2n                v
                                                                     π
                                                                        4
                                                                                    (271)
     π π
2. [ 2n , 2 ]: In this case, we have the integral
                                               Z π               mπ
                                           1        2
                                                                                  sin (nv)
                                                         dv g       − 2v e−(n−1)iv          .                               (272)
                                           π        π             n                 sin (v)
                                                   2n


   In this case, the instantaneous absolute value of the integrand changes dramatically, and we
   need to rescale the integral by letting
                                              v = es ,                                     (273)
   so that
       Z π                                            Z π
     1 2         mπ        
                               −(n−1)iv sin (nv)    1 ln 2            mπ                          s
                                                                                          s sin (ne )
           dv g       − 2v e                     =           ds es g      − 2es e−(n−1)ie              .
    π π            n                     sin (v)    π ln π              n                    sin (es )
        2n                                                2n
                                                                                                  (274)
   After the rescaling, the L∞ -norm of the integrand multiplied by length of interval is now
   bounded by
                      π                                                            s
                                  π1                                     s sin (ne )
                                                    mπ        
                      ln − ln            max es g         − 2es e−(n−1)ie
                         2       2n π s               n                      sin (es )
                                                                                                  (275)
                           ln(n)                       es     ln(n)
                       ≤         ∥g∥max,[−π,π] max 2 s =             ∥g∥max,[−π,π] .
                             π                   s
                                                      πe
                                                                2

3. [− π2 , − 2n
             π
                ]: In this case, we have
         Z −π                                                               Z π
    1            2n
                              mπ      
                                               −(n−1)iv sin (nv)      1              2
                                                                                                 mπ             sin (nv)
                      dv g          − 2v e                          =                    dv g       + 2v e(n−1)iv          . (276)
    π     − π2                 n                            sin (v)   π              π            n                sin (v)
                                                                                    2n


   We then proceed as in the second case.
      π
4. [− 2n , 0]: In this case, we have
         Z 0                                                                         π
     1                    mπ
                                            −(n−1)iv sin (nv)         1                          mπ              sin (nv)
                                                                            Z
                                                                                    2n
                                                                                                       
                  dv g             − 2v e                           =                    dv g       + 2v e(n−1)iv          . (277)
     π       π
          − 2n                n                             sin (v)   π         0                 n                sin (v)

   We then proceed as in the first case.

By taking a linear combination of the above integrals, we can block encode
                1
                  Rπ        mπ
                                     1−e−niu          1
                                                         Rπ        mπ
                                                                           1−e−niu
               2π −π du g    n − u 1−e−iu             2π −π du g     n − u 1−e−iu
                                                  =    π
                                                                                   .                                       (278)
         2 π4 ∥g∥max,[−π,π] + ln(n) ∥g∥                   2 + ln(n) ∥g∥max,[−π,π]
                                2       max,[−π,π]


                                                                       65
If we perform the block encoding for each quantum value m = 0, 1, . . . , 2n − 1 with the same
normalization factor, we obtain
                                         Pn−1      j
                                           j=0 ξj Z2n
                                   π
                                                           ,                             (279)
                                    2 + ln(n) ∥g∥max,[−π,π]

which block encodes                          Pn−1       j
                                                j=0 ξj Ln
                                        π
                                                                                                (280)
                                        2 + ln(n)       ∥g∥max,[−π,π]
per the analysis of Section 6.1. We analyze the complexity of this circuit in more detail in the next
subsection.

6.4   Summary of Fourier coefficients generation
We now summarize the circuit for generating Fourier coefficients.

  1. Implement the four rescaled convolutions of Section 6.3 using Lemma 21, controlled by the
     quantum value m = 0, 1, . . . , 2n − 1 from an ancilla register.

  2. Take a linear combination to block encode Eq. (279).

  3. Construct a block encoding of Eq. (280) using Eq. (246).

Theorem 6 (Fourier  P∞ coefficients    generation). Let g be a 2π-periodic function having the Fourier
expansion g(ω) = j=−∞ ξj e       −ijω , with max-norm ∥g∥max,[−π,π] of the function value and maximum
derivative ∥g ′ ∥max,[−π,π] . Suppose that the absolute value and argument of g are provided by the
oracles                                                                   
                                                        g mπ n + π  −  2π
                                                                      nin s     
                  OAbs |m, s, 0⟩ = m, s, Floor nAbs
                                                                                ,
                                                            ∥g∥max,[−π,π]
                                                                                            (281)
                                                       Arg g mπ  n   +  π − 2π
                                                                            nin s     
                  OArg |m, s, 0⟩ = m, s, Floor nArg                                 ,
                                                                    2π

with 2n-value register holding |m⟩, nin -value register holding |s⟩, and (nAbs + 1)- and nArg -value
output registers respectively. Then the operator
                                             Pn−1       j
                                                j=0 ξj Ln
                                        π
                                                                                                (282)
                                        2 + ln(n)       ∥g∥max,[−π,π]

can be block encoded to accuracy ϵ by setting size of the registers nAbs , nArg = O(1/ϵ) and nin =
   ∥g′ ∥
          max,[−π,π] n log(n)
                                          
                                n2 log(n)
O        ∥g∥             ϵ    +     ϵ       , using O(1) queries to OAbs and OArg , together with
          max,[−π,π]


                                              ∥g ′ ∥max,[−π,π] n
                                                                        !!
                                                                n2
                               O polylog                      +                                  (283)
                                              ∥g∥max,[−π,π] ϵ    ϵ

two qubit gates.




                                                    66
Proof. The query complexity and normalization factor of the block encoding are already analyzed in
Section 6.3. To establish the gate complexity, we begin with the four convolutions from Section 6.3.
Consider first the integral
                                Z π
                              1 2n         mπ                sin (nv)
                                     dv g      − 2v e−(n−1)iv           .                     (284)
                              π 0            n                  sin (v)
We have already shown that L∞ -norm of the integrand is bounded by
                 1  mπ                   sin (n(·))             n
                   g    − 2(·) e−(n−1)i(·)                       ≤ ∥g∥max,[−π,π] ,            (285)
                 π    n                      sin (·) max,[0, π ]  2
                                                                2n

                                  π
whereas length of the interval is 2n . For the Lipschitz constant, we take the derivative of the
integrand
                                                                                           
                                                                              n−1
             1 d      mπ                 sin(nv)      1       d  mπ          X
    µ = max        g      − 2v e−(n−1)iv            = max          g      − 2v       e−i2jv 
         v   π dv      n                   sin(v)      π   v  dv       n
                                                                                     j=0

                                 n−1                            n−1
       1         ′ mπ
                             X
                                      −i2jv
                                                   mπ      X
     = max −2g           − 2v       e       − i2g      − 2v      je−i2jv
       π v           n                               n
                                j=0                          j=0
                                            
     = O n g ′ max,[−π,π] + n2 ∥g∥max,[−π,π] .
                                                                                              (286)
Moreover, the integrand has absolute value
                  1  mπ                  sin (nv)   1  mπ       sin (nv)
                    g      − 2v e−(n−1)iv           =   g    − 2v                             (287)
                  π     n                   sin (v)   π    n         sin (v)
and argument
                                        
         1  mπ     
                       −(n−1)iv sin (nv)
                                                       mπ              
  Arg      g    − 2v e                     = Mod2π Arg g     − 2v − (n − 1)v .                (288)
         π    n                  sin (v)                   n
Invoking Lemma 21 with additional arithmetics to compute the trigonometric and exponential
functions, this integral can be implemented to accuracy O(ϵ) with gate complexity

                                             ∥g ′ ∥max,[−π,π]
                                                                  !!
                                                                1
                               O polylog                      +      .              (289)
                                           n ∥g∥max,[−π,π] ϵ ϵ

  Now, consider the rescaled convolution
  Z π                                        Z π
 1 2        mπ      
                        −(n−1)iv sin (nv)   1 ln 2          mπ                          s
                                                                                s sin (ne )
      dv g      − 2v e                    =        ds es g      − 2es e−(n−1)ie              . (290)
 π π          n                   sin (v)   π ln π            n                    sin (es )
     2n                                              2n

We have already shown that L∞ -norm of the integrand is bounded by
                                                         (·)         ∥g∥max,[−π,π]
                                                             
             1 (·)  mπ              −(n−1)ie(·) sin ne 
                                 
                             (·)
               e g      − 2e       e                               ≤               ,          (291)
             π        n                           sin e (·)
                                                               π π
                                                                          2
                                                          max,[ln 2n ,ln 2 ]

whereas length of the interval is ln π2 − ln 2n
                                             π
                                                = ln n. Denoting the integrand by h(s), we have
                               d         d      d       d
                                  h(s) =    h(v) v(s) =    h(v)es                             (292)
                               ds        dv     ds      dv

                                                67
from the chain rule. Thus the Lipschitz constant has the scaling
                                                                         s
                                                                           
                              1 d     s
                                          mπ
                                                   s
                                                     
                                                       −(n−1)ies sin (ne )
                     µ = max         e g      − 2e e
                          s   π ds          n                     sin (es )                           (293)
                                                                             
                       = O n log(n) g ′ max,[−π,π] + n2 log(n) ∥g∥max,[−π,π] .

Moreover, the integrand has absolute value

               1 s  mπ                           s                            s
                                        s sin (ne )    1 s  mπ      s sin (ne )
                                                                     
                 e g    − 2es e−(n−1)ie              =   e g    − 2e                                  (294)
               π      n                    sin (es )   π      n         sin (es )

and argument
                                                s
                                                  
             1 s  mπ     s
                            
                              −(n−1)ies sin (ne )
       Arg     e g    − 2e e
             π      n                    sin (es )                                                    (295)
                    mπ                                                      
     = Mod2π Arg g         − 2es − (n − 1)es + Arg (sin (nes )) − Arg (sin (es )) .
                        n
Invoking Lemma 21 with additional arithmetics to compute the trigonometric and exponential func-
                   π
tions (for s ∈ [ln 2n , ln π2 ]), this integral can be implemented to accuracy O(ϵ) with gate complexity

                                                    n ∥g ′ ∥max,[−π,π] n2
                                                                          !!
                                     O polylog                        +      .                     (296)
                                                    ∥g∥max,[−π,π] ϵ     ϵ

This completes the proof since analysis of the remaining two convolutions proceeds in a similar way
as above.

Remark. Although we have only constructed the circuit to generate Fourier coefficients in the
exponential-form expansion, the construction can be trivially adapted to other settings such as the
trigonometric form. For instance, suppose we have
                    ∞
                    X                        ∞
                                             X
           g(ω) =          ξj e−ijω = ξ0 +         ((ξj + ξ−j ) cos(jω) + (−iξj + iξ−j ) sin(jω)) ,   (297)
                    j=−∞                     j=1

                              Pn−1               j
and we want to implement        j=0 (ξj + ξ−j ) L , with the first coefficient rescaled. Because

                                                       ∞
                                                       X
                                g(ω) + g(−ω) =               (ξj + ξ−j ) e−ijω ,                      (298)
                                                      j=−∞

it suffices for us to invoke the above circuit with the even function g(ω) + g(−ω).
    We can thus apply this to generate the Chebyshev coefficients, since Chebyshev expansion can
be recast as a Fourier expansion of an even function     in the trigonometric form, as per Eq. (66).
                                                      Pn−1
Specifically, given a Chebyshev expansion p(x) = j=0 βej T     e j (x) of a degree-(n − 1) polynomial,
                        Pn−1 e j                                                                     
we can block encode j=0 βj Ln /α with some normalization factor α = O ∥p∥max,[−1,1] log(n) .
When applied to |0⟩, this gives the Chebyshev coefficient state n−1
                                                                     P
                                                                        j=0 βj |j⟩/ β with probability
                                                                            e         e
     2
  βe /α2 . We can then subtract n−1 and negate the quantum register to get n−1
                                                                                  P
                                                                                     j=0 βj |n−1−j⟩/ β
                                                                                         e           e




                                                        68
with the same probability. By a further application of (In − Ln )/2 through block encoding, we
obtain the shifted Chebyshev coefficients
                                      Pn−1 e
                                       k=0 (βk − βk+2 )|n − 1 − k⟩
                                                 e
                                                                                                       (299)
                                                  αβe
            q                                             
              Pn−1 e             2                                                     2    2
for αβe =        k=0 |βk − βk+2 | = O ∥p(cos) sin∥2,[−π,π] , with success probability αβe/α . Typi-
                           e
cally, this ratio can be computed exactly on a classical computer, so the success probability can be
boosted exactly to unity using                                 !
                                          ∥p∥max,[−1,1] log(n)
                                     O                                                         (300)
                                          ∥p(cos) sin∥2,[−π,π]
steps of amplitude amplification. Altogether, this gives the gate complexity

                                              ∥p′ ∥max,[−1,1] n
                                                                                                  !!
           ∥p∥max,[−1,1] log(n)                                            ∥p∥max,[−1,1] n2
       O                          polylog                            +                                 (301)
           ∥p(cos) sin∥2,[−π,π]             ∥p(cos) sin∥2,[−π,π] ϵ       ∥p(cos) sin∥2,[−π,π] ϵ

to prepare the shifting of Chebyshev coefficients, fulfilling the requirement of QEVT in Theorem 4.
See the remark succeeding Theorem 5 for further discussions on the scaling of ∥p(cos) sin∥2,[−π,π] .


7     Applications
We now apply QEVT to solve linear differential equations in Section 7.1 and prepare ground states
in Section 7.2. For both applications, the underlying idea is to implement truncated Chebyshev
expansions that approximate the target functions, similar to previous QSVT-based results [56,
61, 62]. However, the challenge here is that our input matrices are no longer Hermitian or even
diagonalizable. So to establish the claimed complexities in Theorem 7 and Theorem 8, we will
develop more general error bounds for truncating Chebyshev expansions of matrix functions, which
may be of independent interest.

7.1   Quantum algorithm for linear differential equations
We first consider the homogeneous linear differential equations
                                             d
                                                x(t) = Cx(t),                                          (302)
                                             dt
whose solution is given by
                                             x(t) = etC x(0).                                          (303)
When C has only imaginary eigenvalues, we can use QEVT to implement the function e−iαC tx on
a block encoding of iC/αC , which can be easily constructed from a block encoding of C/αC . For
presentational purpose, we change the variable to A = iC and describe our result as to implement
e−iαA tx on a block encoding of A/αA .
   Suppose that the matrix exponential function has the (rescaled) Chebyshev expansion e−itA =
P∞ e e  A 
  j=0 βj Tj αA . We wish to choose the truncate order n sufficiently large so that the error
                        
 e−itA − n−1            A
          P
            j=0 β  T
                 ej e j αA   is at most ϵ. The problem can then be solved by implementing the
truncated series using QEVT. When A is Hermitian, we can use Proposition 2 to get an n scaling


                                                    69
like n = O αA t + log 1ϵ , which leads to the optimal Hamiltonian simulation results from previous
                         

work [61, 62]. In the general case where A is not diagonalizable, Proposition 2 is no longer applicable,
and we instead develop the following bound for truncating matrix exponentials.
Lemma 23 (Chebyshev truncation of matrix exponentials). Let A               e be a matrix with eigenvalues
                                   1 1                                −1
belonging to the real interval [− 2 , 2 ]. Suppose that A = SJS has a Jordan form decomposition
                                                            e
with upper bound κS ≥ ∥S∥ ∥S∥−1 on the        P Jordan     condition number and size dmax of the largest
Jordan block. Given τ > 0, let e−iτ x = ∞       j=0 β
                                                    ej T
                                                       e j (x) be the Chebyshev expansion of the complex
exponential function e−iτ x . Then,
                                     n−1
                                                                     edmax τ n
                                     X                                    
                             −iτ A
                           e       −       βj Tj A = O κS                         .                  (304)
                                 e         e  e   e
                                                                       2n
                                                   j=0

Proof. We start with the triangle inequality estimate
                                        n−1
                                        X              ∞
                                                         X          ∞
                                                                      X                     
                         e−iτ A −                    e =
                                                  ej A
                                              βej T        βej T  e ≤
                                                               ej A     βej              T
                                                                                         ej A
                                                                                            e .              (305)
                                  e

                                        j=0                         j=n          j=n

Here, the Chebyshev expansion coefficients are given by Bessel functions of the first kind as βej =
2ij Jj (τ ), which are bounded by
                                                          2  τ j
                                      βej = 2 |Jj (τ )| ≤          .                         (306)
                                                          j! 2
                                                             
It remains to analyze size of the matrix polynomial e     Tj A e .
     In Corollary 31 of Appendix A, we will derive a general bound for matrix polynomial functions
that reads                                                                  !
                                                  j dmax −1
                                                     
                            ∥pj (C)∥ = O κS √                 ∥pj ∥max,[a,b] ,               (307)
                                                   δ
where pj is a degree-j polynomial and eigenvalues of C are all contained in [a+δ, b−δ]. The prefactor
of the bound only depends on dmax and [a, b] which we treat as constant, and is independent of the
polynomial degree j and the margin δ.
     We now apply this bound to the rescaled Chebyshev polynomials e     Tj ( e
                                                                              A). To this end, we set
[a, b] = [−1, 1], which contains all eigenvalues of A, and is constant-distance gapped from [− 12 , 12 ]
                                                    e
that also encloses the eigenvalues. We have
                                                                    
                                 dmax −1 e
                                                        = O κS j dmax −1 = O κS djmax .
                                                                                        
             Tj A = O κS j
              e    e                      Tj                                                    (308)
                                                                max,[−1,1]

Thus, there exists a constant c for which
                                  n−1               ∞                         ∞ 
                                                                         cκS X edmax τ j
                                                                                      
                      −iτ A
                                  X               X 1  τ j     j
                  e           −         βj Tj A ≤ c            κS dmax ≤ √               ,                   (309)
                          e             e  e  e
                                                      j! 2                 2π     2j
                                  j=0                         j=n                      j=n

                                               √          j
                                                          j             √  j
where we have used the bound                       2πj    e     ≤ j! ≤ e j ej . Assuming n ≥ edmax τ , we continue
the calculation to get
                       n−1                    ∞  
                                  cκS edmax τ n X 1 j−n 2cκS edmax τ n
                       X                                        
          −iτ A
         e        −     βj Tj A ≤ √                    = √             .                                     (310)
              e         e  e  e
                                    2π   2n         2      2π   2n
                    j=0                         j=n

The claimed bound is now established.

                                                                      70
   The above bound essentially quantifies the error of Chebyshev truncation for producing an
unnormalized solution state. The effect of normalization is considered by the following bound,
which follows from a similar reasoning as in Corollary 19.
Lemma 24 (Quantum state transformation with perturbation). Let C and C   e be invertible matrices
of the same size, acting on (normalized) quantum states |ψ⟩ and | e
                                                                 ψ⟩. We have

                        C|
                        e ψ⟩
                           e    C|ψ⟩    2 ∥C∥ |ψ⟩
                                               e − |ψ⟩     e−C
                                                         2 C
                             −        ≤                +         .                         (311)
                        C|
                        e ψ⟩
                           e   ∥C|ψ⟩∥        ∥C|ψ⟩∥       ∥C|ψ⟩∥

Proof. We use the triangle inequality to upper bound the left-hand side as

                 C|ψ⟩    C|
                         e ψ⟩
                            e             C|ψ⟩   C|
                                                 e ψ⟩
                                                    e     C|
                                                          e ψ⟩
                                                             e    C|
                                                                  e ψ⟩
                                                                     e
                       −            ≤          −       +        −                  .       (312)
                ∥C|ψ⟩∥   C|
                         e ψ⟩
                            e            ∥C|ψ⟩∥ ∥C|ψ⟩∥   ∥C|ψ⟩∥   C|
                                                                  e ψ⟩
                                                                     e

For the first term, we have

                                C|ψ⟩   C|
                                       e ψ⟩
                                          e    C|ψ⟩ − C|
                                                      e ψ⟩
                                                         e
                                     −       =             ,                               (313)
                               ∥C|ψ⟩∥ ∥C|ψ⟩∥     ∥C|ψ⟩∥

whereas the second term can be further bounded similarly as

                C|
                e ψ⟩
                   e    C|
                        e ψ⟩
                           e                     1       1           C|ψ⟩ − C|
                                                                            e ψ⟩
                                                                               e
                      −             = C|
                                      e ψ⟩
                                         e            −          ≤                     .   (314)
               ∥C|ψ⟩∥   C|
                        e ψ⟩
                           e                   ∥C|ψ⟩∥   C|
                                                        e ψ⟩
                                                           e           ∥C|ψ⟩∥

The claimed bound then follows from
      C|ψ⟩ − C| e ≤ C|ψ⟩ − C|ψ⟩
             e ψ⟩                  e − C|
                             e + C|ψ⟩     e ≤ ∥C∥ |ψ⟩ − |ψ⟩
                                       e ψ⟩              e + C −C
                                                                e .                        (315)



Theorem 7 (Quantum differential equation algorithm). Let A be a square matrix with only real
eigenvalues, such that A/αA is block encoded by OA with some normalization factor αA ≥ ∥A∥.
Suppose that A/αA = SJS −1 has a Jordan form decomposition with upper bound κS ≥ ∥S∥ ∥S∥−1
on the Jordan condition number. Let Oψ |0⟩ = |ψ⟩ be the oracle preparing the initial state.
    Then, applying Theorem 4 to the function e−iαA tx truncated at order
                                                           κ 
                                                               S
                                     n = O αA t + log                                       (316)
                                                              ϵ
produces the state
                                                e−itA |ψ⟩
                                                                                            (317)
                                              ∥e−itA |ψ⟩∥
with accuracy ϵ and probability 1 − pfail . The algorithm uses
                                                                                 
                        α eT,ψ                 κ 
                                                   S            α eT,ψ          1
                    O          αU αA t + log            log              log                (318)
                        αexp,ψ                    ϵ           αexp,ψ ϵ         pfail
queries to controlled-OA , controlled-Oψ , and their inverses, where αU satisfies Eq. (157), αT,ψ
                                                                                              e

satisfies Eq. (224), and
                                        αexp,ψ ≤ e−itA |ψ⟩                                  (319)
is a lower bound on size of the solution vector.

                                                   71
Proof. There are two sources of error, one from Chebyshev truncation of the matrix exponential
function, and the other from the application of QEVT. Most of our 
                                                                  effort will be spent on choosing
                                                                                     Pn−1 e e    A
                                   −itA                                               j=0 βj Tj αA |ψ⟩
the truncate order n, such that ∥ee−itA |ψ⟩
                                        |ψ⟩∥
                                             approximates                            Pn−1 e e  A       to accuracy ϵ/2. We
                                                                                      j=0 βj Tj α  |ψ⟩
                                                                                                 A
know from the perturbation bound of Lemma 24 that
                           Pn−1 e e  A              −itA −
                                                             Pn−1 e e  A 
              e −itA |ψ⟩        β  T
                             j=0 j j αA   |ψ⟩     2 e          j=0 βj Tj αA
                         −                      ≤                           .                                          (320)
            ∥e−itA |ψ⟩∥                                     ∥e−itA |ψ⟩∥
                           Pn−1 e e    
                                βj Tj A |ψ⟩
                                         j=0             αA

Furthermore, Lemma 23 implies that the numerator has the scaling
                                         n−1
                                                                              edmax αA t n
                                                                                     
                              −itA
                                         X                   A
                          e          −          βej T
                                                    ej                 = O κS               ,                          (321)
                                                             αA                  2n
                                         j=0

as long as αA ≥ 2 ∥A∥, which can always be satisfied using the rescaling trick of Eq. (113). It
remains to analyze 1/ e−itA |ψ⟩ .
    We have from Eq. (205) that

                                                     n−1
                                                                                           edmax αA t n
                                                                                                  
                      1                  itA
                                                     X                     A
                               ≤ e              =            βej T
                                                                 ej                 + O κS               .             (322)
               ∥e−itA |ψ⟩∥                                                 αA                 2n
                                                     j=0

Here, the first term is a degree-(n − 1) matrix polynomial function, which can be bounded again
using Corollary 31 from Appendix A as
                                                                     
                 n−1                               n−1
                 X           A                       X
                     βej e
                        Tj         = O κS ndmax −1      βej T
                                                            ej       
                             αA
                                                                      
                j=0                                                         j=0
                                                                                         max,[−1,1]
                                                                                     eαA t n                           (323)
                                                                                        
                                               = O κS dnmax   e−iαA t max,[−1,1] +
                                                                                      2n
                                                                     n 
                                                                  eαA t
                                               = O κS dnmax 1 +                  .
                                                                    2n
    To approximate with
                      accuracy ϵ/2, it thus suffices to choose a truncate order n scaling like
                  κS
n = O αA t + log ϵ . We now apply QEVT with accuracy ϵ/2 as well. The claimed complexity
follows from Theorem 4.

Remark. Methods for bounding αU and α eT,ψ are discussed in the remarks succeeding Theorem 1
and Theorem 4, whereas a bound for 1/αexp,ψ is given in the above proof. For diagonalizable
coefficient matrices with purely imaginary spectra, we show in Appendix A.2 and Appendix A.3
                             αT,ψ
that αU = O(κS ), and that αexp,ψ  = O (κS log(n)) in the worst case. But the log(n) factor can be
                               e


shaved off for an average input, resulting in the complexity
                                            κ      κ             
                               2                 S         S        1
                          O κS αA t + log           log      log                             (324)
                                                ϵ         ϵ        pfail
strictly linear in the evolution time.
    In the circuit implementation, we use Theorem 6 to prepare the shifted Chebyshev coefficients;
see the remark succeeding that theorem. To this end, we need to implement the oracle for the

                                                                      72
complex exponential function, which can be achieved in a standard way using a classical reversible
computation. Moreover, we have ∥f ∥max,[−1,1] = O(1) and ∥f (cos) sin∥2,[−π,π] = Ω(1) for the
exponential function f (x) = e−iαA tx . Therefore, the gate complexity for preparing the shifted
Chebyshev coefficients is polylogarithmic in the input parameters.
    It is unclear whether our method can be used to solve differential equations with time-dependent
coefficients. This is somewhat reminiscent of the limitation that Chebyshev-based approach [61] is
not directly applicable to the quantum simulation of time-dependent Hamiltonians. Note however
that the above algorithm can be adapted to solve an inhomogeneous linear differential equation
dx(t)                                                            tC     etC −I
 dt = Cx(t)+b, which has the exact solution given by x(t) = e x0 + C b. After the substitution
A = iC, we consider the Chebyshev expansion of both
                                                                      n−1
                                                                      X
                                                        −iαA tx
                                         f (x) = e                ≈         βj Tj (x)                       (325)
                                                                      j=0

and
                                                                          n−1
                                       e−iαA tx − 1 X
                                g(x) =             ≈     ξj Tj (x).                      (326)
                                         −iαA x
                                                     j=0

We can truncate f and g at order n = O αA t + log 1δ as both functions can be extended to be
                                                      

analytic on the entire complex plane. Then, we use the Chebyshev generating function as before
to generate a state proportional to
                                 n−1                                    n−1                   
                                 X                 A                      X                 A
                           |0⟩         βj Tj                |x0 ⟩ + |1⟩         ξj Tj                |b⟩.   (327)
                                                   αA                                       αA
                                 j=0                                      j=0
                                                                                   q
Finally, we perform amplitude amplification toward the state (∥x0 ∥ |0⟩ + ∥b∥ |1⟩)/ ∥x0 ∥2 + ∥b∥2 in
the first register.
   Note that the query complexity of initial state preparation can be improved using the block
preconditioning technique of [65].

7.2      Quantum algorithm for ground state preparation
As a second application, we present a quantum algorithm that prepares the ground state of an
input matrix with real eigenvalues.
   Let A be the input matrix with only real eigenvalues and block encoded as A/αA . Suppose
that the Jordan form decomposition A/αA = SJS −1 holds with upper bound κS ≥ ∥S∥ S −1 on
the Jordan condition number and size dmax of the largest Jordan block. To simplify the analysis,
we assume that λ0 is the smallest eigenvalue of A with eigenstate |ψ0 ⟩ that is nondefective and
nonderogatory. In other words, there is only one Jordan block correponding to λ0 , and size of that
block is 1. Then our goal is to approximately prepare |ψ0 ⟩, given an initial trial state expanded in
the Jordan basis as
                                                      d−1
                                                      X
                                     |ψ⟩ = γ0 |ψ0 ⟩ +     γl |ψl ⟩.                             (328)
                                                                      l=1

       Following previous conventions [56], we assume that λ0 is separated from the next eigenvalue
λ1 :
                                                        δA     δA
                                           λ0 ≤ −          <0<    ≤ λ1                                      (329)
                                                         2      2

                                                                73
with some spectral gap δA > 0. Here, we have placed λ0 and λ1 on different sides of the origin,
which is without loss of generality as we can always shift and rescale the input block encoding [56].
In practice, it is also natural to consider quantum algorithms for preparing an arbitrary eigenstate
as opposed to the ground state, but such an extension is fairly straightforward and will not be
discussed here.
    As is to be expected, we will solve the ground state preparation problem by applying QEVT to
implement a truncated Chebyshev expansion. In the special case where the input is Hermitian, this
route was pursued by previous work [56] with QSVT. In that case, the input matrix can be unitarily
diagonalized and one only needs to find a Chebyshev truncation for the scalar error function as in
Proposition 3. However, such a truncation result is not applicable here per se, because our matrices
are not necessarily Hermitian (or even diagonalizable). Instead, we prove the following bound for
truncating matrix functions.

Lemma 25 (Chebyshev truncation of matrix sign functions). Let A           e be a matrix with eigenvalues
belonging to [− 12 , −2δ]    e 1 ]. Suppose that A
                       e ∪ [2δ,                       e = SJS −1 has a Jordan form decomposition with
                                 2
upper bound κS ≥ ∥S∥ S      −1     on the Jordan condition number and size dmax of the largest Jordan
                          1−Erf (cx)
                                      = ∞
                                          P
block. Given c > 0, let                         βej e
                                                   Tj (x) be the Chebyshev expansion of the (shifted and
                               2           Rj=0
                                             x        2
rescaled) error function Erf (x) = √π 0 du e−u . Then,
                                        2

                                                    !dmax −1                                                          
     I − Sgn A
             e        n−1                     n                  e   −c2 δ
                                                                           e2
                                                                                    c       n2       c    2
                                                                                                                  2
                                                                                                                  ec
                                                                                                                     m !
                                                                                                       − c2
                      X
                                                                                          − 2m
                  −         βej T
                                ej A
                                   e = O κS    p                               +     e          +     e                 ,
           2          j=0                         δe                    cδe         n                n            2m
                                                                                                                         (330)
with the sign function                           
                                                 −1,
                                                                 x < 0,
                                         Sgn(x) = 0,              x = 0,                                                 (331)
                                                 
                                                  1,              x > 0.
                                                 

Proof. Similar to the proof of Lemma 23, we will also be using the matrix polynomial bound Corol-
lary 31 derived in Appendix A.     However, the challenge is that we need to handle
                                Pn−1                                              Pn−1 two  different
polynomials here: we have 1 − j=0 βj Tj (x) over the interval [−1, −δ], and − j=0 βj Tj (x) over
                                        e  e                           e               e  e
the interval [δ,
              e 1]. Therefore, we will separate Jordan blocks of A
                                                                 e accordingly, based on intervals to
which the eigenvalues belong.
    Let us start with the estimate
                           
                 I − Sgn A e     n−1
                                 X                                   n−1
                                                        I − Sgn (J) X e e
                               −     βj Tj A ≤ κS
                                      e  e    e                      −     βj Tj (J) .          (332)
                       2                                     2
                                   j=0                                                    j=0


Note that by our assumption, all eigenvalues of A e belong to [− 1 , −2δ]      e 1 ], whereas the sign
                                                                       e and [2δ,
                                                                 2                2
function is analytic on larger intervals [−1, −δ]
                                               e and [δ,e 1]. Thus, the above matrix functions are
indeed well defined as per Eq. (97).
    We now collect all Jordan blocks with negative eigenvalues into J− and those with positive
eigenvalues into J+ (size of J− and J− sums up to that of J). This gives

                            n−1                 n−1                 n−1
               I − Sgn (J) X e e                X                   X
                          −     βj Tj (J) ≤ I −     βej T
                                                        e j (J− ) +     βej T
                                                                            e j (J+ ) .                                  (333)
                    2
                                j=0                      j=0                              j=0



                                                   74
Invoking Corollary 31, we obtain
                                                                                        
                    n−1
                                                 !dmax −1              n−1
                    X                       n                          X
               I−       βej T
                            e j (J− ) = O               1−       βej T              ,
                                                                      ej             
                                           p
                    j=0                      δe               j=0
                                                                         max,[−1,−δ]
                                                                                  e
                                                                                            (334)
                    n−1
                                                !dmax −1 n−1
                    X                       n            X
                            e j (J+ ) = O  p
                        βej T                                βej T          .
                                                                ej         
                    j=0                      δe          j=0             e   max,[δ,1]

The claim now follows from the Chebyshev truncation bounds for the scalar error and sign func-
tions [60, 94].

Theorem 8 (Quantum ground state preparation algorithm). Let A be a square matrix with only
real eigenvalues, such that A/αA is block encoded by OA with some normalization factor αA ≥ ∥A∥.
Suppose that A/αA = SJS −1 has a Jordan form decomposition with upper bound κS ≥ ∥S∥ ∥S∥−1
on the Jordan condition number. Let eigenvalues of A be ordered nondecreasingly, with λ0 the
smallest one with eigenstate |ψ0 ⟩, which is nondefective and nonderogatory satisfying the condition

                                              δA     δA
                                     λ0 ≤ −      <0<    ≤ λ1                                  (335)
                                               2      2
for some spectral gap δA > 0. Let Oψ |0⟩ = |ψ⟩ be the oracle preparing the initial state with the
Jordan basis expansion
                                                   d−1
                                                   X
                                  |ψ⟩ = γ0 |ψ0 ⟩ +     γl |ψl ⟩.                            (336)
                                                           l=1

 Then,
      r applying      Theorem   4 to the error function 1 − Erf (cx) with a rescaling factor c =
                       
O αδAA log αδAA |γκ0S|ϵ    truncated at order

                                                                     
                                              αA           αA κS
                                   n=O           log                                          (337)
                                              δA           δA |γ0 |ϵ

produces the ground state |ψ0 ⟩ with accuracy ϵ, probability 1 − pfail , and the global phase factor
γ0 / |γ0 |. The algorithm uses
                                                                                 
                            α eT,ψ    αA       αA κS             α eT,ψ           1
                        O          αU    log               log             log                 (338)
                            |γ0 |     δA       δA |γ0 |ϵ         |γ0 | ϵ         pfail

queries to controlled-OA , controlled-Oψ , and their inverses, where αU satisfies Eq. (8) and αT,ψ
                                                                                               e

satisfies Eq. (224).

Proof. If 2 ∥A∥ > αA ≥ ∥A∥, we first rescale the input block encoding by a factor of 2 using the
trick of Eq. (113). So in what follows, we will assume αA ≥ 2 ∥A∥ without loss of generality. This
rescaling may increase the Jordan condition number by 2dmax −1 [44, Corollary 3.1.21] which we
treat as constant. The eigenvalues of the block encoded matrix now satisfy the condition
                      1  λ0     δA      δA   λ1         λd−1  1
                     − ≤    ≤−     <0<     ≤    ≤ ··· ≤      ≤ .                              (339)
                      2  αA    2αA     2αA   αA          αA   2



                                                  75
   We then apply Lemma 25 to get
                                                                                    !dmax −1                                                                 
                  A
   I − Sgn        αA
                               n−1            
                                                  A
                                                       
                                                                                 n                   e   −c2 δ
                                                                                                             e2
                                                                                                                       c       n2       c        2
                                                                                                                                                         2
                                                                                                                                                         ec
                                                                                                                                                            m !
                                                                                                                                              − c2
                               X
                                                                                                                             − 2m
                           −         βej T
                                         ej                = O κS               p                                 +     e          +     e                     ,
          2                    j=0
                                                  αA                              δe                      cδe          n                n                2m
                                                                                                                                                                  (340)

where
                                                                                   δA
                                                                             δe =     .                                                                           (341)
                                                                                  4αA
From the perturbation bound of Lemma 24,
                                                                                                                  
                                                                                                               A
                                                                                                 I−Sgn        αA           Pn−1 e e  A 
                                                                                             2                         −    j=0 βj Tj αA
                        
                     A
                                                                        
        I−Sgn            Pn−1 e e     A
                          j=0 βj Tj αA |ψ⟩
                    αA                                                                                   2
            2      |ψ⟩
                     − P                                                             ≤                                                                  .   (342)
        I−Sgn αA          n−1 e e     A                                                                         I−Sgn αA
               A
                   |ψ⟩    j=0 β j Tj  αA |ψ⟩                                                                                  A
                                                                                                                                    |ψ⟩
            2                                                                                                          2


Note that denominator of the above bound is exactly |γ0 |, because
                          
                I − Sgn αAA             I − Sgn (J) −1
                              |ψ⟩ = S                S |ψ⟩ = ∥|ψ0 ⟩γ0 ∥ = |γ0 | .                                                                                 (343)
                      2                       2

To see the second equality, we permute the Jordan blocks and Jordan basis so that eigenvalues are
ordered increasingly. Then, we have
                                                                                 
                                                                              γ0
                                          I − Sgn (J)
                                                                  |ψ⟩ = S  ...  ,
                                   
             S = |ψ0 ⟩ · · · |ψd−1 ⟩ ,                = |0⟩⟨0|,                            (344)
                                                                                 
                                               2
                                                                             γd−1
from which the above calculation is justified.
   Our goal now is to choose parameters c, m, n so that Chebyshev truncation of the matrix
                                                                                         sign
function in Eq. (340) has an error at most ϵe. We will make sure that n = Ω(c) and c = Ω 1e , so
                                                                                         δ
the error scaling simplifies to
                                                               2 m 
                                     demax    −c2 δe2      n2
                                                         − 2m    ec
                              O κS n        e         +e      +                            (345)
                                                                 2m
                  −3
for demax = 3dmax
               2     = O(1). Let us first try
          s                                                                                                      s                  
        1         1            2          1     1        1                                                                        1   1     1
   c∼      log       ,   m ∼ c + log          ∼     log     ,                                                 n∼           m log     ∼ log       ,
        δ
        e         ϵe                      ϵe    δ
                                                e 2      ϵe                                                                       ϵe  δ
                                                                                                                                      e     ϵe
                                                                                                                                               (346)
which ensures that                                                                             m
                                                                                         ec2
                                                                             2
                                                                                     
                                                                        n
                                                       −c2 δe2        − 2m
                                                   e             +e              +                  = O (e
                                                                                                         ϵ) .                                                     (347)
                                                                                         2m
However, we have an additional factor due to the non-Hermitian nature of the input matrix, which
contributes to an asymptotic scaling of
                                                       
                                 demax    κS    demax  1       κS
                            κS n       ∼ e log            ≲ e √ .                          (348)
                                        δedmax         ϵe  δedmax ϵe

                                                                                  76
Hence to compensate for this contribution, we choose
                                                   
                                             1      κS
                                    n=Θ        log      .                                         (349)
                                             δ
                                             e       δe
                                                     eϵ

    Finally, we take the normalization into account and set

                                             ϵe = Θ (|γ0 | ϵ) .                                   (350)

The proof is now complete by noting that
                           
                   I−Sgn αA
                       2
                            A
                              |ψ⟩         S I−Sgn(J)
                                               2     S −1 |ψ⟩          |ψ0 ⟩γ0      γ0
                                      =                           =              =       |ψ0 ⟩.   (351)
                                                                      ∥|ψ0 ⟩γ0 ∥   |γ0 |
                           
                   I−Sgn αA
                                          S I−Sgn(J) S −1 |ψ⟩
                        2
                            A
                                |ψ⟩            2




Remark. For a discussion on the scaling of αU and αT,ψ    e , see the remarks succeeding Theorem 1 and

Theorem 4. For input matrices that are diagonalizable with real spectra, we show in Appendix A.2
that αU = O(κS ), and that α eT,ψ = O(κS log(n)) in the worst case where the log(n) factor can be
dropped for an average input (Appendix A.3), resulting in the complexity

                                   αA κ2S
                                                                      
                                                2    κS              1
                             O              log               log            .                   (352)
                                   δA |γ0 |         |γ0 | ϵ         pfail

Note that we have also removed a factor of αδAA from inside of a logarithmic factor, due to the fact
that dmax = 1 in Eq. (340). Anyway, our result naturally reduces to the nearly optimal ground
state preparation result from previous work [56] in the special case where the input matrix is a
Hermitian Hamiltonian.
    The complexity of our algorithm depends on the expansion coefficient γ0 of the initial trial
state under the Jordan basis. This is compatible with previous work [56] that uses the notion of
initial overlap, because the basis is orthonormal when the input matrix is Hermitian. We have
also explicitly worked out the global phase factor γ0 / |γ0 |, and adopted the Euclidean distance
as the accuracy metric of the output state. This necessarily implies that our output state has
a large overlap/fidelity with the true ground state in the language of [56], since the inequality
|⟨ψ0 |φ2 ⟩| ≥ |⟨ψ0 |φ1 ⟩| − ∥|φ1 ⟩ − |φ2 ⟩∥ holds for arbitrary quantum states |ψ0 ⟩, |φ1 ⟩, |φ2 ⟩.
    For a circuit implementation of the shifted Chebyshev coefficients preparation, see Theorem 6
and the succeeding remark. To this end, we need to implement the oracle for the error function
Erf , which can be achieved by translating the efficient classical algorithm from [17]. Moreover, we
have ∥f ∥max,[−1,1] = O(1) and ∥f (cos) sin∥2,[−π,π] = Ω(1) for the rescaled error function, assuming
the spectral gap is at most constant. Therefore, the gate complexity for preparing the shifted
Chebyshev coefficients is polylogarithmic in the input parameters.
    Finally, note that the query complexity of initial state preparation can be improved using the
block preconditioning technique of [65].


8    Eigenvalue processing over the complex plane
We have so far focused on quantum eigenvalue algorithms for input matrices with real spectra.
In this section, we show that many of these results can be carried over to the complex plane.

                                                    77
This is achieved using the Faber expansion that provides a nearly optimal polynomial basis for
approximation over a compact set of the complex plane, the preliminaries of which will be reviewed
in Section 8.1. We then describe efficient quantum algorithms for generating the Faber history
state in Theorem 9 of Section 8.2, and for transforming eigenvalues of input matrices with complex
spectra in Theorem 10 of Section 8.3. Finally, we present in Section 8.4 a quantum algorithm for
solving differential equations with general coefficient matrices (Theorem 11), as well as a quantum
algorithm for estimating leading eigenvalues (Theorem 12).

8.1   Preliminaries on Faber expansion
Suppose that we have an input matrix whose eigenvalues are enclosed by a subset E of the complex
plane. When the matrix has only real spectra, we may choose E to be a closed real interval, and
approximate functions over E using the Chebyshev expansion. But here, we relax this assumption
to handle more general operators with complex eigenvalues.
    Specifically, we require E to be a nonempty simply connected compact set in the complex plane
with a simply closed (or Jordan curve) boundary, which we refer to as a Faber region. By the
Riemann mapping theorem, there exists a unique function, known as the exterior Riemann map,

                                   Φ : E c → Dc ,       Φ(z) = w,                             (353)

which sends the complement of E conformally onto the exterior of the unit disk D = {|w| ≤ 1} and
satisfies the conditions
                                                              Φ(z)
                          Φ(∞) = ∞,           Φ′ (∞) = lim         = ζ > 0.                   (354)
                                                        z→∞    z
Here, the complement is taken with respect to the extended complex plane C ∪ {∞}. This implies
that Φ has its Laurent expansion in some neighborhood of ∞ as
                                                       ζ1  ζ2
                                  Φ(z) = ζz + ζ0 +        + 2 + ···                           (355)
                                                       z   z
Then the nth Faber polynomial Fn (z) for the domain E is taken to be the polynomial part of the
Laurent expansion of Φn (z). We let the inverse of Φ be

                             Ψ : Dc → E c ,      Ψ(w) = Φ−1 (w) = z,                          (356)

which maps the exterior of the unit disk D conformally onto the complement of E, with the Laurent
expansion
                                                     ς1    ς2
                                  Ψ(w) = ςw + ς0 + + 2 + · · ·                               (357)
                                                     w w
for |w| > 1. By the Carathéodory’s theorem, the maps Φ and Ψ can be extended continuously to
the boundaries ∂E and ∂D respectively. See Figure 3 for an illustration of these definitions, and
references [66, 85] for more introductory material on Faber polynomials.
    By restricting E to be special subsets of the complex plane, one can recover familiar examples
of polynomial basis for nearly best uniform approximation of functions. For instance, consider first
the case where E = [−1, 1]. Then we have
                                                          
                                                 1       1
                                        Ψ(w) =       w+                                      (358)
                                                 2      w



                                                  78
                                                         √
as the Joukowsky √  map, which has inverse Φ(z) = z + z 2 − 1 with the branch of square root
                      2                         √
satisfying limz→∞ zz −1 = 1. This means z − z 2 − 1 has no polynomial part in its Laurent ex-
                                                                                     √        n
pansion, so the polynomial part of Φn (z) is the same as the polynomial part of z + z 2 − 1 +
      √       n
   z − z 2 − 1 . But the nth Chebyshev polynomial of the first kind satisfies the equality Tn (x) =
 1
        √       n       √       n                                              √       n
      x +   x 2−1    +  x −   x 2−1      for  x ∈  R.  We  thus  conclude that    z +   z 2−1     +
2     √       n
   z − z 2 − 1 is a degree-n polynomial itself, and that Fn (z) = 2Tn (z) for n ≥ 1, or

                                                 Fn (z) = 2T
                                                           e n (z)                                          (359)
for all nonnegative integers n. As another example, consider the case where E is just the unit disk
D = {|w| ≤ 1} itself. Then we have
                                            Ψ(w) = w                                          (360)
and the inverse Φ(z) = z both as identity maps, so
                                                   Fn (z) = z n                                             (361)
are the power functions. But the significance of Faber polynomials is that they provide a uni-
fying approach for function approximations over compact subsets of the complex plane, of which
Chebyshev polynomials and power series are two special cases.
    The generating functions for Faber polynomials and their derivatives have the form [26, 79]
               ∞                                            ∞
               X
                            j     Ψ′ (y −1 )                X F′j (z)                      1
                     Fj (z)y =                  ,                         y j−1 =                       ,   (362)
                               y (Ψ(y −1 ) − z)                       j             y (Ψ(y −1 ) − z)
               j=0                                           j=1

for |y| < 1. This is reminiscent of the generating functions
                 ∞                                             ∞
                 X
                       e j (x)y j =        1 − y2              X                          1
                       T                               ,              Uj (x)y j =                   ,       (363)
                                      2(1 + y 2 − 2yx)                              1 + y 2 − 2yx
                 j=0                                           j=0

for Chebyshev polynomials of the first and second kind, where Te ′ (x) = T′ (x) = jUj−1 (x) for
                                                                 j          j
j ≥ 1. In ourFaber algorithms,   we will implement a matrix version  of the  generating function
                         Ψ′ (L−1 )⊗I
P∞ j             
               A
   j=0 L ⊗ Fj αA   = LΨ(L−1 )⊗I−L⊗ A . The challenge here is that we need to handle operators
                                            αA

like Ψ′ (L−1 ) and LΨ(L−1 ) which need not have finite Taylor expansions, unlike the Chebyshev
case. We overcome this difficulty by reformulating it as a problem of generating Fourier coefficients,
which we solve using techniques we develop in Section 6.
    Given a function analytic over a Faber region in the complex plane, we may expand the function
into a series of Faber polynomials associated with that region. This is formalized by the following
lemma.
Lemma 26. Let E be a Faber region with the corresponding conformal maps Φ : E c → Dc , Ψ :
Dc → E c and Faber polynomials Fn (z). For any function f : C → C analytic on E, the following
statements hold:
  1. (Existence [85, Page 52]): There exists an expansion
                                                            ∞
                                                            X
                                                  f (z) =          βj Fj (z)                                (364)
                                                            j=0

     converging uniformly on the entire E.

                                                        79
  2. (Uniqueness [85, Page 109]): For any expansion f (z) = ∞
                                                            P
                                                              j=0 βj Fj (z) converging uniformly
     on the entire E,
                                                     Z 2π
                            1         f (Ψ(w))     1
                              Z                                               
                                                              −ijθ         iθ
                      βj =         dw          =          dθ e     f   Ψ(e    )  ,         (365)
                           2πi ∂D        wj+1     2π 0

     where ∂D = {|w| = 1} is the unit circle.

Moreover, if f is analytic on a region containing Ψ(r∂D) (r ≥ 1) and its interior, then the Faber
coefficients can also be computed with the rescaled contour:
                                                       Z 2π
                          1          f (Ψ(w))       1
                            Z                                                     
                                                                 −ijθ         iθ
                    βj =         dw            =             dθ e     f   Ψ(re   )   .      (366)
                         2πi r∂D        wj+1      2πrj 0
    Finally, we consider the size of Faber polynomials Fj over the Faber region E, which is useful
for bounding the complexity of our quantum algorithms. Applying Cauchy’s integral formula to
the Faber generating function, we have

                                           1             wj Ψ′ (w)
                                             Z
                                 Fj (z) =             dw                                    (367)
                                          2πi (1+δ)∂D    Ψ(w) − z

                                                                                           (1+δ)∥Ψ′ ∥
for any z ∈ E and δ > 0, which implies ∥Fj ∥max,E ≤ cδ (1 + δ)j for constant cδ = Dist(Ψ((1+δ)∂D),E)
                                                                                          max,(1+δ)∂D


independent of j, and hence                 q
                                    lim sup j ∥Fj ∥max,E ≤ 1.                                   (368)
                                       j→∞

This estimate holds for an arbitrary Faber region E. But under additional assumptions of the
region, it is possible to get a tighter estimate. For instance, if the boundary ∂E is of bounded total
rotation, we have the following integral representation of Faber polynomials

                                             1 2π ijφ
                                               Z
                                      iθ
                              Fj (Ψ(e )) =          e dφ v(φ, θ), j ≥ 1,                        (369)
                                             π 0

where v(φ, θ) = Arg Ψ(eiφ ) − Ψ(eiθ ) is an angular function with the jump at φ = θ equal to the
                                          

exterior angle of ∂E at θ. From this, we obtain the following bound on the maximum size of Faber
polynomials [85, Page 182] [31]
                                                                         Z 2π
                                                                   1                           V(∂E)
  ∥Fj ∥max,E = ∥Fj ∥max,∂E = Fj Ψ(ei(·) )                  ≤ max                |dφ v(φ, θ)| ≤         , (370)
                                              max,[0,2π]    θ∈[0,2π] π    0                        π

where the first equality follows from the maximum modulus principle, and the last inequality follows
from a bound due to Radon. Here, V(∂E) is the variation or total rotation of the curve ∂E. It is
known that V(∂E) ≤ 4π if E is simply connected, and that V(∂E) ≥ 2π always holds, with the
equality V(∂E) = 2π if and only if E is convex [32, Page 147]. Thus, we have

                                           ∥Fj ∥max,E ≤ 2                                                (371)

for a convex Faber region, which is reminiscent of the familiar bound

                                         ∥Tj ∥max,[−1,1] ≤ 1                                             (372)

for Chebyshev polynomials.

                                                  80
8.2     Faber history state generation
Suppose that the input matrix is block encoded as A/αA with some normalization factor αA ≥ ∥A∥,
whose eigenvalues are enclosed by a Faber region E. Denote the corresponding conformal maps as
Φ : E c → Dc , Ψ : Dc → E c and the Faber polynomials as Fn (z). As aforementioned, the main idea
behind our approach is to use a matrix Faber generating function of the form
               n−1                             ∞
                                                                                   Ψ′ (L−1 ) ⊗ I
                                                                    
               X
                      j           A            X
                                                      j           A
                     L ⊗ Fj                =         L ⊗ Fj                =                          .   (373)
               j=0
                                  αA
                                               j=0
                                                                  αA           LΨ(L−1 ) ⊗ I − L ⊗ αAA

This follows from Eq. (362) by substituting z = I ⊗ αAA and y = L ⊗ I. This substitution is
mathematically valid because L has zero eigenvalues only, whereas both sides of Eq. (362) have
the same derivatives at y = 0 of any order. See [43, Chapter 6] or [42, Chapter 2] for a complete
mathematical justification. Note that the Laurent series of Ψ′ (w) and wΨ(w−1 ) only contains
terms with nonnegative exponents, so operator functions Ψ′ (L−1 ) and LΨ(L−1 ) are well defined
even though the lower shift matrix L is not invertible per se.
   Now consider the problem   of eigenvalue processing. Toward implementing a truncated Faber
expansion of the form n−1
                      P
                         k=0 k Fk , we apply the matrix generating function to the initial state
                            β
                                               Pn−1
                                                 k=0 βk |n − 1 − k⟩
                                                                           |ψ⟩.                           (374)
                                                          ∥β∥

Similar to the Chebyshev case, we obtain up to a normalization factor
                     
   n−1                    n−1
                                             ! n−1      n−1                 
    X
         j        A       X                       X       X                   A
       L ⊗ Fj               βk |n − 1 − k⟩|ψ⟩ =    |l⟩         βk Fk+l−n+1     |ψ⟩.                     (375)
                 αA                                                           αA
      j=0                     k=0                                 l=0          k=n−1−l

If we now measure the first register and get the outcome l = n − 1, the second register will have
the desired state proportional to
                                       n−1        
                                       X          A
                                           βk Fk      |ψ⟩.                                  (376)
                                                  αA
                                                 k=0

However, we will also get unwanted components for l = 0, . . . , n − 2, leading to a failure of the
algorithm.
    To boost the success probability, we use the runaway padding trick to repeat the desired state
ηn times. This can again be understood via the formula in Lemma 13 for inverting lower block
matrices. Specifically, we let
                                                                                  A
                                       A11 = Ln Ψ(L−1
                                                   n ) ⊗ I − Ln ⊗                    ,                    (377)
                                                                                  αA
which corresponds to the denominator of the generating function. Here, we have used subscripts
to explicitly represent dimensions of the matrices. Now we take
                                                                    
                                                       0 0 · · · −I
                                                     0 0 · · · 0 
                           A21 = |0⟩⟨n − 1| ⊗ (−I) =  . . .      ..  .                (378)
                                                                    
                                                      .. .. ..    . 
                                                                       0 0 ···           0


                                                            81
and set
                                                                                          
                               I   0         0    ··· 0           I 0          0 ··· 0
                             −I I           0    · · · 0       I I         0 · · · 0
                                                                                          
                                                 ..                             . . .. 
    A22 = (Iηn − Lηn ) ⊗ I =  0 −I
                                             I       . 0 ⇒ A = I I
                                                             −1             I        . .  .   (379)
                              ..                             22
                                  ..         .. ..       .        ... . . . . . . . . . ... 
                                                      . .. 
                                                                                           
                              .
                                    .          .                                          
                                             ..                              .     .
                               0 ···            . −I I            I · · · .. .. I

We will bundle the numerator of the generating function

                                         B11 = Ψ′ (L−1
                                                    n )⊗I                                         (380)

with the state preparation subroutine and handle it later.
   To summarize, after the padding, denominator of the matrix Faber generating function becomes

                   Pad(A) = |0⟩⟨0| ⊗ A11 + |1⟩⟨0| ⊗ A21 + |1⟩⟨1| ⊗ A22
                                                                   
                                              −1                  A
                          = |0⟩⟨0| ⊗ Ln Ψ(Ln ) ⊗ I − Ln ⊗
                                                                αA
                            + |1⟩⟨0| ⊗ |0⟩⟨n − 1| ⊗ (−I) + |1⟩⟨1| ⊗ (Iηn − Lηn ) ⊗ I
                                                    0     0    0 ··· 0
                                                                             
                            
                             L Ψ(L−1 ) ⊗ I         0     0    0 · · · 0
                                                      ..  ..   ..    ..   .. 
                                                                              
                             n         n
                             −L ⊗ A                   .   .    .     .    .  
                                                                                                  (381)
                                     n    αA                                 
                            
                                                   0     0    0 · · · 0     
                                                   0     0    0 · · · 0
                          = 0 0 · · · 0 −I I                                  .
                                                                             
                                                         0    0 · · · 0     
                            0 0 · · · 0 0 −I I                0 · · · 0     
                            
                                                                   ..     .. 
                            0 0 · · · 0 0
                                                   0    −I    I        .   .
                             .. .. .. ..      ..    ..  .. .. ..             
                            . . . .            .     .      .    .     . 0
                              0 0 ··· 0 0           0 · · · 0 −I I

The numerator
                          Pad(B) = |0⟩⟨0| ⊗ B11 + |1⟩⟨1| ⊗ Iηn ⊗ I
                                                                                                  (382)
                                   = |0⟩⟨0| ⊗ Ψ′ (L−1
                                                   n ) ⊗ I + |1⟩⟨1| ⊗ Iηn ⊗ I

will be bundled with the state preparation which is now augmented with an additional ancilla state
                                       Pn−1
                                             βk |n − 1 − k⟩
                                    |0⟩ k=0                 |ψ⟩.                            (383)
                                               ∥β∥

   Using the matrix generating function
                                                 
             Xn        F′j αAA     X∞          F′j αAA           1
                Lj−1 ⊗           =      Lj−1 ⊗         =                                          (384)
             j=1
                           j
                                       j=1
                                                   j     LΨ(L ) ⊗ I − L ⊗ αA
                                                             −1
                                                                                        A




                                                    82
for the derivative of Faber polynomials, we have
                                                                                                                          
                              F′1 αAA       0                                ···                 0           0 ··· ···
                             A                                                                                   
                             F′2 α                                        ..                   ..         .... ..
                            
                                 2
                                     A
                                        F′1 αAA                                    .               .          . .  .
                                                                                                                    
                                 .        ..                                ..                               .... ..
                             ..             .                                   .           0              . .  .
                                                                                                                   
                             ′ A                                            
                                                                                  A
                                                                       F′2
                                                                                                                    
                             Fn αA                                                          ′
                                                                                                
               Pad(A)−1 =                                                                         A
                                                                                 αA
                                                                                                                    
                             n          ···                                2            F1 αA     0 · · · · · · .                  (385)
                             ′ A                                                     
                                                                                  A
                                                                       F′2
                                                                                                                    
                             Fn αA                                                             
                                           ···                                   αA
                                                                                           F′1 αAA   I 0 · · ·
                                                                                                                    
                             n                                            2
                            
                                                                                                                   
                             F′ A                                     F′2        A
                                                                                                             .. 
                                                                                                                  
                             n αA
                                 n        ···                                2
                                                                                 αA
                                                                                           F′1 αAA   I I          .
                                  ..        ..                                ..                ..   .. .. . .
                                                                                                                   
                                   .         .                                 .                 .    . .         .

This implies
                                                                                                                                 
                                              A
                                     F0       αA              0   0 ···                ···              0                    ···
                                                             .. ..                ..               ..                     .. 
                         F1 αAA      F0 αAA                       . .                    .              .                      . 
                                                                                                                                   
                             ..                                    .. ..                                                        .. 
                                                                                                                                   
                                        ..                                             ..
                                            .                                             .
                        
                              .                          0  . .                                                              . 
                        
                                                                                                                                 
      Pad(A)−1 Pad(B) = Fn−1 αAA       ···     F1 αAA   F0 αAA   0 ···                                                      · · ·     (386)
                        
                                                                                                                                    
                                                                                                                             
                        Fn−1 αAA       ···     F1 αAA   F0 αAA   I 0                                                        · · ·
                                                                                                                                   
                                                                                                                                   
                        Fn−1 A
                                                                                                                       .. 
                                                F1 αAA   F0 αAA                                                                   .
                        
                                αA     ···                       I I                                                               
                              ..         ..        ..       ..      .. ..                                                    ..
                               .          .         .        .       . .                                                          .

as desired.
    Let us now consider circuit implementation of block encoding Eq. (381). To this end, we bundle
−Ln ⊗ αAA with the two blocks at the bottom to get
                            
                          A
          |0⟩⟨0| ⊗ Ln ⊗ −      + |1⟩⟨0| ⊗ |0⟩⟨n − 1| ⊗ (−I) + |1⟩⟨1| ⊗ (Iηn − Lηn ) ⊗ I
                          αA
               n−1                       nη+n−1                  nη+n−1                                                                 (387)
               X                    A      X                       X
       = −           |k⟩⟨k − 1| ⊗      −        |k⟩⟨k − 1| ⊗ I +        |k⟩⟨k| ⊗ I.
                                    αA
               k=1                             k=n                                         k=n

Here, the first two terms can be rewritten as
                         n−1                 nη+n−1                                        nη+n−1
                                                                                   !                                     !
                         X              A      X                                             X
                     −         |k⟩⟨k| ⊗    +        |k⟩⟨k| ⊗ I                                         |k⟩⟨k − 1| ⊗ I                   (388)
                                        αA
                         k=0                           k=n                                  k=1

and can thus be block encoded with normalization factor 1, using Lemma 14. The third term is
reexpressed as
                            nη+n−1
                              X 1 + (−1)Ind[0,n−1] (k)
                                                       |k⟩⟨k| ⊗ I,                     (389)
                                            2
                                       k=0

with the indicator function Ind[0,n−1] (k) = 1 if and only if 0 ≤ k ≤ n − 1, and can also be block
encoded with normalization factor 1.

                                                                  83
   We already know from Section 6 that Ln Ψ(L−1
                                             n ) can be block encoded as

                                            Ln Ψ(L−1 )
                                         π
                                                  n                                          (390)
                                         2 + ln(n) αΨ,max
for any upper bound on maximum value of the conformal map over the unit circle
                                   αΨ,max ≥ (·)−1 Ψ(·) max,∂D ,                               (391)

with a normalization factor scaling like ∼ log(n) (·)−1 Ψ(·) max,∂D . To prevent this logarithmic
overhead from ruining the query complexity, we perform a uniform amplification of the block
encoding as in Lemma 12. This gives
                                           Ln Ψ(L−1n )
                                                                                             (392)
                                               2αΨ
for any upper bound on the spectral norm
                                       αΨ ≥ Ln Ψ(L−1
                                                  n ) .                                       (393)
By taking a final linear combination, we can thus block encode
                                               Pad(A)
                                                       .                                      (394)
                                               2αΨ + 2
    We see that the dependence on αΨ comes from the necessity of block encoding Ln Ψ(L−1     n ) in
implementing the matrix Faber generating function. It is obvious that αΨ = O(1) when Ψ has a
finite Laurent expansion. This happens for instance in the generation of Chebyshev history states,
where Ψ(w) = 21 w + w1 is the Joukowsky map containing only two terms. Even when Ψ has an
infinite Laurent expansion, αΨ can still be constant. For instance, if ∂E = Ψ(∂D) is an analytic
curve, then by the generalized Schwarz reflection principle, Ψ can be analytically continued across
the unit circle ∂D [51, Page 299]. Therefore, the Laurent series of Ψ converges absolutely on ∂D,
implying a constant value of αΨ as well. In fact, the scaling αΨ = O(1) holds in general. This can
be proved using the Crouzeix-Palencia theorem (Lemma
                                                      33 of Appendix B), together with the fact
that the numerical range of Ln is the disk cos n+1 D [91], whereas the function (·)Ψ((·)−1 ) is
                                                   π

analytic on {|w| < 1} and can be extended continuously to the entire D:
                Ln Ψ(L−1            −1                      −1
                      n ) ≲ (·)Ψ((·) ) max,W(Ln ) = (·)Ψ((·) ) max,cos( π )D
                                                                               n+1
                                                                                              (395)
                                        −1
                            ≤ (·)Ψ((·)       ) max,D = O(1).
Note that constant prefactor of the above analysis can be tightened using von Neumann’s inequal-
ity [76, Proposition 1] and [43, 1.6.P26]. It is for this reason that the dependence on αΨ will be
dropped in the asymptotic analysis of Faber-based algorithms.
Theorem 9 (Faber history state generation). Let A be a square matrix such that A/αA is block
encoded by OA with some normalization factor αA ≥ ∥A∥. Suppose that eigenvalues of A/αA are
enclosed by a Faber region E with associated conformal maps Φ : E c → Dc , Ψ : Dc → E c and
Faber polynomials Fn (z). Let Oψ |0⟩ = |ψ⟩ be the oracle preparing the initial state, and Oβ |0⟩ =
          Pn−1                           Pn−1
Ψ′ (L−1
      n )
                                  ′  −1
            k=0 βk |n − 1 − k⟩/ Ψ (Ln )   k=0 βk |n − 1 − k⟩ be the oracle preparing the shifting of
coefficients β. Then, the quantum state
                                                 Pη         Pn−1 Pn−1           
    |0⟩ n−1
        P         Pn−1                   A                                         A
          l=0 |l⟩   k=n−1−l βk Fk+l−n+1 αA |ψ⟩ +      s=1 |s⟩  l=0 |l⟩  k=0 βk Fk αA |ψ⟩
          r                                                                                    (396)
             Pn−1 Pn−1                             2        Pn−1               2
                                            A                               A
                l=0    k=n−1−l βk Fk+l−n+1 αA |ψ⟩      + ηn     k=0 βk Fk αA |ψ⟩


                                                  84
can be prepared with accuracy ϵ and probability 1 − pfail using
                                                                  
                                                    1            1
                              O αF′ n(η + 1) log          log                                           (397)
                                                    ϵ           pfail

queries to controlled-OA , controlled-Oψ , controlled Oβe, and their inverses, where
                                                                                 
                                                                   F′j       A
                                                                             αA
                                       αF′ ≥ max                                                        (398)
                                                 j=1,...,n               j

is an upper bound on the derivative of Faber polynomials.

Proof. The analysis proceeding the above theorem shows that one can block encode Pad(A)/(2αΨ +
2) with an arbitrary precision using only 1 query to OA . The quantum linear system algorithm of
Lemma 10 then outputs a state ϵ-close to
                                              
               Ψ′ (L−1
                          Pn−1
   2αΨ +2            n )       βk |n−1−k⟩                           P                         
  Pad(A) |0⟩ ∥Ψ′ (L−1
                           k=0
                          Pn−1              |ψ⟩    Pad(A) −1 Pad(B) |0⟩  n−1
                                                                             β  |n − 1 − k⟩|ψ⟩
                     n )   k=0 β k |n−1−k⟩∥                              k=0  k
                                               =                  P                          .
                 ′ (L−1 )
                          Pn−1                                           n−1
   2αΨ +2      Ψ     n         βk |n−1−k⟩          Pad(A) −1 Pad(B) |0⟩      β  |n − 1 − k⟩|ψ⟩
  Pad(A) |0⟩ ∥Ψ′ (L−1                       |ψ⟩
                           k=0
                          Pn−1                                           k=0 k
                     n )   k=0 βk |n−1−k⟩∥
                                                                                             (399)
This is exactly the padded Faber history state.
    We have the norm bound on the inverse padded matrix

                                    Pad(A)−1 = O ((η + 1)nαF′ )                                         (400)
                                                         
                                                      A
                                           F′j       αA
for any upper bound αF′ ≥ maxj=1,...,n            j            on the derivative of Faber polynomials (normal-

ized by the degrees), which follows from Lemma 1 and the matrix representation of Pad(A)−1 in
Eq. (385). The claimed complexity now follows from Eq. (120).

Remark. For the purpose of generality, we have expressed the complexity of our algorithm in terms
of αF′ . This analysis can be further refined when the algorithm is applied in a concrete setting.
For instance, if the Faber region E encloses the numerical range W(A/αA ) or the pseudospectrum
Sδ (A/αA ) with a sufficiently smooth boundary ∂E, then it holds αF′ = O(1). This extends pre-
vious analysis of quantum differential equation algorithms [50] based on the notion of numerical
abscissa, which avoids the issue with a ill-conditioned Jordan basis that could potentially arise in
the Chebyshev case. See Appendix B.2 and Appendix B.3 for more details.
    In the circuit implementation of this algorithm, we need to choose the precision with which
Eq. (390) is block encoded. This can be determined as follows. We first invoke Corollary 19 to see
that the padded Faber history state has accuracy ∼ ϵ, as long as Eq. (394) is block encoded with
                   ϵ
accuracy ∼ (η+1)nα     α . This is satisfied as long as we block encode Eq. (392) using Lemma 12
                     F′ Ψ
with the same asymptotic accuracy. Up to a polylogarithmic factor, we can then block encode
Eq. (390) with accuracy ∼ (η+1)nαϵ ′ αΨ,max . However, the specific choice of block encoding accuracy
                                   F
does not change the query complexity of the algorithm, and its contribution to the gate complexity
is only polylogarithmically as per Theorem 6.
    Finally, note that the query complexity of initial state preparation can be improved using the
block preconditioning technique of [65].


                                                              85
8.3   Quantum eigenvalue transformation, Faber version
Now that we have an efficient quantum algorithm for preparing the Faber history state, we let the
padding parameter η = 1 and further perform a (fixed-point) amplitude amplification to solve the
eigenvalue transformation problem. This is formally stated as follows.

Theorem 10 (Quantum eigenvalue transformation, Faber version). Let A be a square matrix
such that A/αA is block encoded by OA with some normalization factor αA ≥ ∥A∥. Suppose that
eigenvalues of A/αA are enclosed by a Faber region E with associated                         c     c
       c      c
                                                              Pn−1 conformal maps Φ : E → D ,
Ψ : D → E and Faber polynomials Fn (z). Let p(z) =              k=0 βk Fk (z) be the Faber expansion
of a degree-(n − 1) polynomial p. Let Oψ |0⟩ = |ψ⟩ be the oracle preparing the initial state, and
                    Pn−1                    ′  −1
                                                   Pn−1
Oβ |0⟩ = Ψ′ (L−1n )   k=0 βk |n − 1 − k⟩/ Ψ (Ln )    k=0 βk |n − 1 − k⟩ be the oracle preparing the
shifting of coefficients β. Then, the quantum state
                                                
                                              p αAA |ψ⟩
                                                                                             (401)
                                              p αAA |ψ⟩

can be prepared with accuracy ϵ and probability 1 − pfail using
                                                                    
                                  αF,ψ             αF,ψ            1
                             O         α ′ n log            log                                              (402)
                                  αp,ψ F           αp,ψ ϵ         pfail

queries to controlled-OA , controlled-Oψ , controlled Oβe, and their inverses, where αF′ satisfies
Eq. (398) and
                                        n−1                                                   
                                        X                   A                               A
               αF,ψ ≥      max                βk Fk−l                |ψ⟩ ,   αp,ψ ≤ p                |ψ⟩ .   (403)
                        l=0,1,...,n−1                       αA                              αA
                                        k=l

are upper bound on the shifted Faber partial sum and lower bound on the transformed state respec-
tively.

Proof. This follows from a similar reasoning as that for Theorem 4.

Remark. For a discussion on the scaling of αF′ , see the remark succeeding Theorem 9. The parame-
ter αF,ψ denotes maximum size of the shifted Faber expansion, which can be further upper bounded
in terms of the max-norm of the polynomial p. For instance, if the numerical range W(A/αA ) ⊆ E
or the pseudospectrum Sδ (A/αA ) ⊆ E is contained       in the Faber
                                                                   region, then we prove in Ap-
pendix B.2 and Appendix B.3 that αF,ψ = O log(n) ∥p∥max,∂E . Furthermore, we can shave off
the log(n) factor (albeit picking up the Jordan condition number κS ) when running
                                                                                     the algorithm
                                                                                            
on an average diagonalizable input matrix (Appendix B.4), giving αF,ψ = O κS ∥p∥max,∂E .
    In the circuit implementation, we need to prepare a quantum state encoding the Faber expansion
coefficients. This can be realized using Theorem 6 in a similar way as in the Chebyshev case. This
is because in computing the Faber coefficients Eq. (365), we can perform a contour integral along
the unit circle, which can be reformulated as the generation of Fourier coefficients after a change
of variable.
    Finally, note that the query complexity of initial state preparation can be improved using the
block preconditioning technique of [65].



                                                             86
8.4   Applications
We now apply the Faber eigenvalue processing algorithm to solve linear differential equations and
estimate leading eigenvalue of the input matrix.
                                                           d
    Consider a system of linear differential equations dt     x(t) = Ax(t), whose solution is given by
         tA
x(t) = e x(0). We assume that a block encoding of A/αA is given as input, and that the numerical
range W(A/αA ) ⊆ E is enclosed by a Faber region. This consideration is a generalization of previous
analysis of differential equation algorithms based on the notion of numerical abscissa [50], which
avoids the stability issue that could arise in transforming the Jordan
                                                                       basis. Then, we write the Faber
                                          tA
                                                 P∞            A
expansion of the matrix exponential e = j=0 βj Fj αA and aim to choose a truncate order
n sufficiently large to achieve a target accuracy. We prove the following matrix Faber truncation
bound by adapting previous results [8, 70, 72] to our setting.

Lemma 27 (Faber truncation of matrix exponentials). Let A      e be a matrix, such that its numerical
range W(A) is enclosed by a Faber region E with associated P
           e                                                 conformal maps Φ : E c → Dc , Ψ : Dc →
E and Faber polynomials Fn (z). Given τ > 0, let e = ∞
  c                                                     τ z
                                                               j=0 βj Fj (z) be the Faber expansion of
                                      τ z
the complex exponential function e . Assume that E is convex and symmetric with respect to the
real axis, lying on the left half of the complex plane (ℜ(E) ≤ 0). Then,

                                                          n−1                 ζ n 
                                                          X                  e τ
                                                eτ A −            βj Fj A
                                                                        e =O                                                        (404)
                                                    e
                                                                                n
                                                          j=0


for n = Ω(τ ) sufficiently large, where ζ = Ψ′ (∞) > 0 is the capacity of the Faber region.

Proof. We start with the estimate

                                                 n−1
                                                 X                        n−1
                                                                            X
                                        eτ A −                 e ≲ eτ (·) −
                                                         βj Fj A                βj Fj                               ,               (405)
                                            e

                                                   j=0                                        j=0
                                                                                                            max,E

which follows from the Crouzeix-Palencia theorem Lemma 33 from Appendix B. Using the convexity
of E and evaluating the Faber coefficients with a circular contour of radius r > 1,

                          n−1
                          X                             ∞
                                                        X                          ∞
                                                                                   X
              τ (·)
          e           −         βj Fj           =             β j Fj           ≤         |βj | ∥Fj ∥max,E
                          j=0                           j=n                        j=n
                                        max,E                          max,E
                                                        ∞              Z 2π
                                                        X       1                                     
                                                ≤2                             dθ e−ijθ exp τ Ψ(reiθ )                              (406)
                                                               2πrj     0
                                                        j=n
                                                                                   ∞                                      1 n
                                                                                                                            
                                                          τ (·)
                                                                                   X 1              τ (·)                 r
                                                ≤2 e                                          =2 e                              .
                                                                  max,Ψ(r∂D)             rj                  max,Ψ(r∂D) 1 − 1
                                                                                   j=n                                        r

Assuming n > τ , let us choose
                                                                            n
                                                                       r=     > 1,                                                  (407)
                                                                            τ
so that
                                             n−1
                                             X                                                 n  τ n
                                    eτ A −                 e ≲ eτ (·)
                                                    β j Fj A                                              .                         (408)
                                        e
                                                                                    max,Ψ(r∂D) n − τ n
                                             j=0



                                                                            87
   Because E is convex and symmetric relative to the real axis, we have

                                         eτ (·)                = eτ Ψ(r) .                      (409)
                                                  max,Ψ(r∂D)

Now, by [8, Eqs. (4.4) and (4.5)],
                                                                            
                                    1                                        1
  |Ψ(r) − Ψ(1) − ζ (r − 1)| ≤ ζ 1 −                 ⇒    Ψ(r) ≤ Ψ(1) + ζ r −     ≤ Ψ(1) + ζr,   (410)
                                    r                                        r
where ζ = Ψ′ (∞) > 0 is the capacity. This implies

                                       eτ (·)                ≤ eτ Ψ(1)+ζn .                     (411)
                                                max,Ψ(r∂D)

Combining with the estimate from the previous paragraph, we obtain
                                                n
                          n−1            n eζ τ ,             Ψ(1) ≤ 0,
                                    e ≲ n−τ  n
                          X
                   eτ A −     βj Fj A                                                           (412)
                      e
                                                   ζ+Ψ(1)
                                                            n
                                           n e           τ
                                                               , Ψ(1) > 0.
                          j=0               n−τ      n

This establishes the claimed bound. Note that requirements on the convexity, symmetry, and
nonpositiveness of ℜ(E) can be relaxed along similar lines of [8, 72].

Theorem 11 (Quantum differential equation algorithm, Faber version). Let A be a square matrix,
such that A/αA is block encoded by OA with some normalization factor αA ≥ ∥A∥. Suppose that
the numerical range W(A/αA ) is enclosed by a Faber region E, which is convex and symmetric
with respect to the real axis, lying on the left half of the complex plane (ℜ(E) ≤ 0), with associated
conformal maps Φ : E c → Dc , Ψ : Dc → E c and Faber polynomials Fn (z). Let Oψ |0⟩ = |ψ⟩ be the
oracle preparing the initial state.
    Then, applying Theorem 10 to the function eαA tz (t > 0) truncated at order
                                                                  
                                                              1
                                     n = O αA t + log                                            (413)
                                                           αexp,ψ ϵ
produces the state
                                                 etA |ψ⟩
                                                                                                (414)
                                               ∥etA |ψ⟩∥
with accuracy ϵ and probability 1 − pfail . The algorithm uses
                                                                                
                      αF,ψ                        1               αF,ψ             1
                 O         α ′ αA t + log                  log              log                 (415)
                     αexp,ψ F                  αexp,ψ ϵ          αexp,ψ ϵ         pfail
queries to controlled-OA , controlled-Oψ , and their inverses, where αF′ satisfies Eq. (398), αF,ψ
satisfies Eq. (403) and
                                          αexp,ψ ≤ etA |ψ⟩                                   (416)
is a lower bound on size of the solution vector.
Proof. This is proved in a similar way as Theorem 7.

Remark. See the remaks succeeding Theorem 9 and Theorem 10 for a discussion on thescaling of
αF′ and αF,ψ . In particular, we have both αF′ = O(1) and αF,ψ = O log(n) ∥p∥max,∂E satisfied
for a region of the form Figure 2d, which is a smooth deformed version of the Elliott semidisk
Figure 2c. See the discussion at the end of Appendix B.2 for more details. Finally, note that the
query complexity of initial state preparation can be improved using techniques of [65].

                                                        88
    We now explain how our techniques can be applied to estimate leading eigenvalues of an input
matrix. These leading eigenvalues play an important role in classical linear algebraic algorithms as
they largely determine the behavior of algorithms involving matrix power iterations.
    Specifically, given matrix A, let |ψθ ⟩ be an eigenstate of A with eigenvalue λmax eiθ , i.e., A|ψθ ⟩ =
λmax eiθ |ψθ ⟩. Here, λmax > 0 is the largest absolute value of eigenvalues of A which is known a priori,
and our goal is to estimate the phase angle θ. The underlying idea for solving this problem is to
generate the Faber history state corresponding to the disk λmax D. In this case, Faber polynomials
are given by power functions, and one can directly implement the power series
                         n−1                           ∞
                         X               Aj            X              Aj                      1
                               Ljn ⊗               =         Ljn ⊗           =                            (417)
                         j=0           λjmax           j=0           λjmax                          A
                                                                                     In ⊗ I − Ln ⊗ λmax

without invoking the full power of the Faber mechanism.
    Suppose that the input matrix is block encoded as A/αA with some normalization factor αA ≥
∥A∥ ≥ λmax . Then, using the fact that the n-by-n lower shift matrix Ln can be block encoded with
normalization factor 1 (Lemma 14), we can take the tensor product and obtain a block encoding
of Ln ⊗ αAA . By taking a further linear combination using the ancilla state
                                                        q
                                                              αA
                                                             λmax |0⟩ + |1⟩
                                                             q                   ,                        (418)
                                                                  αA
                                                                 λmax + 1

                       In ⊗I−Ln ⊗ λ A
we can block encode             αA
                                    +1
                                         max
                                               .
                               λmax
    We now invert the block encoded matrix using the optimal scaling quantum linear system
solver Lemma 10 with the initial state |0⟩|ψ⟩. We have

               αA                               n−1                        n−1
                                                                             X Aj
              λmax + 1                                     Aj
                                                                
                                       αA        X                  αA
                       A
                                   =        +1       Ljn ⊗ j   ≤        +1        j
        In ⊗ I − Ln ⊗ λmax            λmax                λmax     λmax
                                                 j=0                         j=0 λmax                     (419)
                                                 
                                            αA
                                   ≤ nκS        +1 ,
                                           λmax
where κS is the Jordan condition number of A. Thus, to generate an ϵlin -approximation of the
history state, the query complexity of the algorithm is asymptotically
                                                           
                                          αA             1
                                    O         nκS log           .                       (420)
                                         λmax           ϵlin
Note that the query complexity of initial state preparation can be improved using the block pre-
conditioning technique of [65]. Assuming the input state |ψ⟩ = |ψθ ⟩ is the exact eigenstate, we then
obtain              αA
                   λmax
                        +1                Pn−1 j         j
              In ⊗I−Ln ⊗ λ A
                               |0⟩|ψθ ⟩         Ln ⊗ A     |0⟩|ψθ ⟩       n−1
                                            j=0      λ j               1 X ijθ
                    αA
                           max
                                        = P            max
                                                                    =√        e |j⟩|ψθ ⟩.       (421)
                   λmax
                        +1                  n−1 j
                                                L  ⊗  Aj
                                                           |0⟩|ψ  ⟩     n
              In ⊗I−Ln ⊗ λ A   |0⟩|ψθ ⟩     j=0  n     j        θ         j=0
                                                                        λmax
                             max

The phase angle θ can now be estimated using the standard quantum phase estimation.
Theorem 12 (Quantum eigenvalue estimation, leading eigenvalues). Let A be a square matrix, such
that A/αA is block encoded by OA with some normalization factor αA ≥ ∥A∥. Assume that A/αA =

                                                                  89
SJS −1 has a Jordan form decomposition with upper bound κS ≥ ∥S∥ ∥S∥−1 on the Jordan condition
number. Suppose that oracle Oψ |0⟩ = |ψ⟩ prepares an initial state within distance ∥|ψ⟩ − |ψθ ⟩∥ =
         √
O (λmax ϵ/(αA κS )) from an eigenstate such that A|ψθ ⟩ = λmax eiθ |ψθ ⟩, where λmax > 0 is the
largest absolute value of eigenvalues of A. Assume that the numerical range W(A) is enclosed by
the disk λmax D. Then, there exists a quantum algorithm that outputs a value θe with accuracy in
centered modulus                                    
                                       CMod2π θe − θ ≤ ϵ                                    (422)

and probability 1 − pfail , using                                         
                                               αA                    1
                                      O                κS log                                   (423)
                                              λmax ϵ                pfail
queries to controlled-OA , controlled-Oψ , and their inverses.

Proof. Assume that the input state |ψ⟩ = |ψθ ⟩ is the exact eigenstate, and that the quantum linear
system solver makes no error. Then the standard phase estimation allows us to estimate θ with
an accuracy ϵ (in centered modulus) and a constant probability strictly larger than 1/2, for some
choice of                                           
                                                    1
                                          n=O           .                                     (424)
                                                    ϵ
   Now consider the general case, where the quantum linear system solver has accuracy ϵlin and
the initial state has distance ∥|ψ⟩ − |ψθ ⟩∥ = ϵinit to the true eigenstate. Then Corollary 19 implies
that the output state is close to the Fourier state Eq. (421) with Euclidean distance at most

                                                √
                                                                 
                                                         αA
                                     ϵlin + O      nκS       ϵinit .                             (425)
                                                        λmax

The remaining analysis proceeds in a similar way as in Theorem 3.

Remark. Note that the above query complexity is expressed in terms of the Jordan condition
number, although this can be improved by a tighter estimate of Aj . If we were to impose the
assumption on the numerical range W(A) ⊆ λmax D, we would find the leading eigenvalue λmax eiθ
on the boundary of W(A). Consequently, A can be unitarily block diagonalized separating λmax eiθ
away from the remaining spectra [43, Theorem 1.6.6]. The problem can then be directly solved by
QSVT, and there is no need to invoke the above eigenvalue estimation algorithm.


9    Discussion
In this work, we have developed quantum algorithms to estimate and transform eigenvalues of high-
dimensional matrices accessed by a quantum computer. Our eigenvalue estimation algorithm is
provably optimal in the inverse accuracy and failure probability for a diagonalizable input, whereas
our eigenvalue transformation algorithm achieves an average performance comparable to previous
results for singular value transformation. As immediate applications, we present a quantum differ-
ential equation solver for matrices with imaginary spectra achieving a strictly linear time scaling
for an average diagonalizable input, as well as a ground state preparation algorithm for matrices
with real spectra nearly optimal in the combined scaling with the inverse spectral gap and inverse
accuracy. We have extended the results to more general matrices with complex eigenvalues, obtain-
ing a new differential equation solver and a quantum algorithm for estimating leading eigenvalues.
Our work thus provides a unified toolbox for processing eigenvalues of non-normal matrices on


                                                        90
quantum computers—a practical problem that is out of reach of the pre-existing quantum singular
value algorithm and its descendants.
    Our main technical contribution is a method to efficiently generate the Chebyshev history state,
which encodes Chebyshev polynomials of the input matrix in quantum superposition. Prior to our
work, it was known how to create such a state for Hermitian inputs via discrete-time quantum walk,
but no such a mechanism was available for non-normal operators. Our new approach employs a
matrix version of the Chebyshev generating function, which is then implemented using the optimal
scaling quantum linear system solver. As Chebyshev polynomials provide a close-to-best minimax
approximation for functions defined over a real interval, the query complexity of our solution is
expected to be nearly optimal. However, our methodology is by no means restricted to only the
Chebyshev expansion. We show how to estimate leading eigenvalues by generating a power series of
the input matrix. More generally, we present an efficient quantum algorithm to generate a history
state of Faber polynomials that provide a nearly optimal basis for function approximations on
compact subsets of the complex plane, of which Chebyshev polynomials and power series are two
special cases.
    When the initial state is prepared close to an eigenstate, the Chebyshev history state we produce
contains information about the corresponding eigenvalue in the phase of coefficients. We have
developed a Chebyshev phase estimation algorithm that estimates the phase (and thus eigenvalue
of the target matrix) with an asymptotically optimal query complexity. However, it is plausible
that alternative methods exist that can extract the phase from a Chebyshev state with a better
performance in practice. It would also be useful to consider a setting where the initial state is an
arbitrary superposition of eigenstates, which is relevant for applications such as period finding. We
leave a detailed analysis of this case as a subject for future work.
    Recent work developed an alternative approach for implementing functions of non-normal ma-
trices based on contour integrals [34, 86, 87]. That approach requires a coherent implementation
of the discretized integral on a quantum computer, and its complexity depends largely on the
choice of contours. With a circular contour, that method gives a differential equation solver whose
complexity has a quadratic dependence on the evolution time [34]. In contrast, our approach im-
plements the Chebyshev expansion of the target function with a predetermined truncate order, and
is conceptually quite different. However, contour integrals have appeared in our analysis of Faber
polynomials, suggesting a deeper connection between our approach and the contour integral method
from previous work. It would also be of interest to construct quantum eigenvalue algorithms with
fewer queries to the initial state preparation, on which the recent technique of linear combination
of Hamiltonian simulation [3] may provide insight.
    We have shown that our eigenvalue transformation algorithm achieves a better performance
for a random choice of input matrix. This speedup in turn follows from the fact that Fourier
series converges faster on average—a powerful result known as the Carleson-Hunt theorem. This
complements many recent work that explored the use of randomness in speeding up quantum
simulation algorithms [14, 16, 21, 98]. Most of those results have focused on improvement of the
product-formula algorithm and its variants. Our work demonstrates that randomness can also be
used to speed up more advanced quantum algorithms through the faster convergence of Fourier
expansion, which has applications to quantum simulation and beyond.
    For the purpose of generality, we have expressed the complexity of our algorithms in terms of
various matrix functions, with the understanding that these functions can be bounded differently
for different problems (see Table 1 for a summary of results). In the Chebyshev case, we have
further derived bounds for input matrices having Jordan forms, generalizing previous analysis of
differential equation algorithms based on the spectra abscissa [50, Section 3.2]. This introduces a
dependence on the Jordan condition number κS , which is a common measure of nonnormality in

                                                 91
numerical linear algebra [90, Page 444] and can be upper bounded using techniques from [7]. It
seems possible to establish a query lower bound for solving differential equations in terms of κS , by
analyzing the speed at which a non-Hermitian Hamiltonian evolves quantum states [9], though the
details remain to be worked out. In the Faber case, we have derived bounds assuming numerical
range or pseudospectrum are enclosed by the Faber region, extending previous differential equation
analysis based on the notion of numerical abscissa [50, Section 3.1].
    We emphasize again that this is not the only way to analyze our algorithms. For instance,
one can also apply the Jordan-form analysis in the Faber case, obtaining a dependence on the
Jordan condition number. The reverse direction is however not very interesting: numerical range
is enclosed by a real interval, if and only if the matrix itself is Hermitian, per the characterizations
from Section 2.3, whereas the pseudospectrum is an open set that can never be enclosed by the
real interval. Anyway, it could be fruitful for future work to establish stronger bounds on matrix
functions, which would have a direct influence on the performance of our eigenvalue algorithms.
    The output of our QEVT algorithm is a quantum state proportional to the transformed input
matrix applied to the initial state. By measuring copies of this state and post-processing the
measurement outcomes, one can learn and make predictions about properties of the input matrix.
However, it is plausible that more efficient methods exist that bypass this two-step procedure and
target directly at properties of high-dimensional non-normal matrices. Our algorithm also maintains
a considerable amount of coherence to produce the output state in quantum superposition. But
this resource requirement may be relaxed using recent methods developed for Hermitian eigenvalue
estimation and transformation [30, 58]. On a different note, we have also studied an alternative
version of QEVT where the input matrix is transformed as a block encoding, which may be useful
when QEVT is invoked as a subroutine in designing other quantum algorithms.
    As further developments unfold, we hope the work initiated here will reveal the potential of
quantum computers in processing non-normal operators, opening up applications that were previ-
ously unexplored.


Acknowledgements
Y.S. thanks Yu Tong for helpful discussions.




                                                  92
A     Analysis of Chebyshev-based algorithms
In this appendix, we analyze the Chebyshev-based eigenvalue algorithms in more detail. Specifically,
we review previous bounds for matrix exponentials in Appendix A.1 based on the spectral abscissa.
We show in Appendix A.2 how this analysis can be generalized for a polynomial function with
the help of Bernstein’s theorem. Finally, we bound the average complexity of our algorithms in
Appendix A.3 using the Carleson-Hunt theorem.

A.1    Matrix exponential bound based on spectral abscissa
We begin by reviewing a bound on norm of the matrix exponential function used in the analysis
of quantum differential equation algorithms [50] [53, Appendix D]. Given a square input matrix
C, our goal is to bound eτ C for τ > 0. Assuming that C has the Jordan form decomposition
C = SJS −1 , we have eτ C ≤ κS eτ J with any upper bound κS ≥ ∥S∥ S −1 on the Jordan
condition number.
    We know from Eq. (97) that eτ J contains only diagonal blocks of the form
                                                                                             
                                       eτ λ l
                                  τ eτ λ l          eτ λ l                                   
                                  2                                                          
                                  τ τ λl               τ λl    τ λl
                                         e         τ  e       e
                                                                                              
                                  2!                                                         
                   eJ(λl ,dl ) = 
                                        ..        τ 2 τ λl      τ λ     . .
                                                                                              
                                                                                                (426)
                                         .        2!  e     τ e     l       .                
                                                                                              
                                         ..          ..       ..        ..      ..           
                                 
                                          .              .        .         .      .         
                                                                                              
                                     d
                                    τ l −1                              2
                                                                       τ τ λl
                                             eτ λl    · · ·    · · ·      e    τ e τ λl eτ λl
                                   (dl −1)!                            2!


Using the scalar version of Lemma 1, we conclude that eJ(λl ,dl ) = Θ τ dl −1 eτ λl , treating size
                                                                                   

dl of the Jordan blocks as constant. This implies the following bound on the matrix exponential
function.

Proposition 28. Let C be a square matrix with the Jordan form decomposition C = SJS −1 . Then,
                                                               
                                 τC                  dl −1 τ λl
                               e    = Θ κS max τ          e       ,                      (427)
                                                   l


where κS ≥ ∥S∥ S −1 is an upper bound on the Jordan condition number, and the maximization
is over all Jordan blocks J(λl , dl ) with eigenvalue λl and size dl .
    Depending on the specific value of λl and dl , the factor Θ τ dl −1 eτ λl behaves differently as
                                                                              

follows:

   1. ℜ(λl ) < 0: In this case, Θ τ dl −1 eτ λl = Θ eτ (ℜ(λl )+o(1)) decays exponentially with τ .
                                                                     

   2. ℜ(λl ) = 0 and dl = 1: In this case, λl is a nondefective eigenvalue, and Θ τ dl −1 eτ λl =
                                                                                                   

      Θ(1) is bounded as a function of τ .

   3. ℜ(λl ) = 0 and dl ≥ 2: In this case, Θ τ dl −1 eτ λl = Θ τ dl −1 grows polynomially.
                                                                       

   4. ℜ(λl ) > 0: In this case, Θ τ dl −1 eτ λl = Θ eτ (ℜ(λl )+o(1)) grows exponentially with τ .
                                                                     

    Thus, the scaling of eτ C largely depends on the spectral abscissa defined as

                                          max ℜ (λl (C)) .                                     (428)
                                            l


                                                 93
Specifically, maxl ℜ(λl ) < 0 implies that eτ C asymptotically decays as a function τ ; maxl ℜ(λl ) =
0 corresponds to the case where the growth of eτ C is at most polynomial further determined
by size of the Jordan blocks with imaginary spectra; and maxl ℜ(λl ) > 0 means eτ C blows
up exponentially. This estimate is particularly useful for analyzing existing quantum differential
equation algorithms such as [50], because the complexity of that algorithm is expressed in terms of
spectral norm of the matrix exponential function.

A.2    Matrix polynomial bound with Bernstein’s theorem
Unlike [50], our Chebyshev-based eigenvalue algorithms have complexity depending on the spectral
norm of various matrix polynomials. In deriving a similar bound as above, the challenge here is to
handle the high-order derivatives in Eq. (97) for a general polynomial function. We overcome this
using the following Bernstein’s theorem.
Lemma 29 (Bernstein’s theorem [47, Eqs. (6) and (12)]). Given a degree-j polynomial pj , it holds
                                                   j
                                   p′j (x) ≤ p               ∥pj ∥max,[a,b]                            (429)
                                              (x − a)(b − x)
for any a < x < b.
   This bound should not be confused with the related Markov brothers’ inequality often used in
the study of query complexity [18], which instead reads

                                                         2j 2
                                      p′j max,[a,b] ≤         ∥pj ∥max,[a,b] .                         (430)
                                                        b−a
Here, the Markov inequality has a prefactor scaling quadratically with the polynomial degree,
whereas the Bernstein inequality introduces a prefactor linear in the polynomial degree. We thus
have
                                                   j
                          p′j max,[a+δ,b−δ] ≤ p             ∥pj ∥max,[a,b] ,               (431)
                                               δ(b − a − δ)
as long as we use a nonzero margin δ > 0. By recursively applying the above analysis, we obtain
the following bound. Alternatively, one may also use the sharper estimate from [47, Equation (37)].
Corollary 30 (Recursive Bernstein’s theorem). For degree-j polynomials pj and δ > 0, it holds
that                                                                   !
                                                 j d−1
                                                   
                       (d−1)
                     pj                    =O   √        ∥pj ∥max,[a,b] ,               (432)
                             max,[a+δ,b−δ]        δ
with b − a = Ω(1) and a fixed positive integer d.
Proof. For d = 2 and a margin δ > 0, we have from the Bernstein’s theorem that
                                           j                               j
   p′j max,[a+δ,b−δ] ≤     max       p               ∥pj ∥max,[a,b] = p             ∥pj ∥max,[a,b] .   (433)
                         x∈[a+δ,b−δ]  (x − a)(b − x)                   δ(b − a − δ)
We shrink the interval by a margin δ again for d = 3:
                                                j−1
                     p′′j max,[a+2δ,b−2δ] ≤ p                p′j max,[a+δ,b−δ]
                                             δ(b − a − 3δ)
                                                                                                       (434)
                                                      (j − 1)j
                                          ≤p              p                 ∥pj ∥max,[a,b] .
                                             δ(b − a − 3δ) δ(b − a − δ)

                                                        94
Performing this recursively,
                                                                                          !d−1
                  (d−1)                                                    j
                pj                                     ≤  p                            ∥pj ∥max,[a,b]
                           max,[a+(d−1)δ,b−(d−1)δ]         δ (b − a − (2d − 3)δ)
                                                                                    !                               (435)
                                                              j d−1
                                                                 
                                                       =O    √        ∥pj ∥max,[a,b] ,
                                                                δ

assuming b − a = Ω(1) and d is a fixed constant.
                                                            δ
    The claimed bound then follows from the rescaling δ 7→ d−1 , which only introduces a constant
prefactor and does not change the asymptotic estimate.

Corollary 31. Let C be a matrix with eigenvalues belonging to the real interval [a+δ, b−δ] with δ >
0. Suppose that C = SJS −1 has a Jordan form decomposition with upper bound κS ≥ ∥S∥ S −1
on the Jordan condition number and size dmax of the largest Jordan block. For degree-j polynomials
pj , it holds that                                                     !
                                              j dmax −1
                                                
                         ∥pj (C)∥ = O κS √               ∥pj ∥max,[a,b] ,                     (436)
                                               δ
assuming b − a = Ω(1) and dmax = O(1).

    We now apply this result to analyzetheperformance of Chebyshev-based eigenvalue algorithms.
Let us first bound maxj=0,1,...,n−1 Uj αAA , which appears in the asymptotic complexity expres-
sion of the algorithm for generating Chebyshev history states. By using the rescaling trick Eq. (113)
for block encoding, we may assume without loss of generality that the normalization factor satisfies
αA ≥ 2 ∥A∥. For a fixed value of j, we thus have
       
         A                                                                                      
  Uj           = O κS j dmax −1 ∥Uj ∥max,[− 3 , 3 ] = O κS j dmax −1 ∥Tj ∥max,[−1,1] = O κS j dmax −1 ,
        αA                                  4 4

                                                                                                   (437)
                      2          2     2
using the fact that Tj (x) − (x − 1)Uj−1 (x) = 1. This implies the scaling
                                                                      
                                                    αU = O κS ndmax −1                                              (438)

claimed in the remark succeeding Theorem 1.         
                                       Pn−1 e e     A
    Next, we consider maxl=0,1,...,n−1  k=l βk Tk−l αA |ψ⟩ , which is used to describe complexity
of the eigenvalue estimation algorithm. We again assume αA ≥ 2 ∥A∥ without loss of generality,
obtaining for a fixed l
        n−1                                        n−1
        X                      A                     X
               βek T
                   e k−l                |ψ⟩ ≤ ∥S∥          βek T
                                                               e k−l (J)   S −1 |ψ⟩
                               αA
         k=l                                         k=l
                                                                                                                  (439)
                                                                                n−1
                                                                                X
                                            = O ∥S∥ S −1 |ψ⟩ ndmax −1                βek T
                                                                                          e k−l                .
                                                                                k=l               max,[−1,1]




                                                                95
Here, the shifted Chebyshev partial sum can be further bounded as
                         n−1
                         X                       n−1
                                                 X
                               βek T
                                   e k−l (x) =           βek cos ((k − l) arccos (x))
                         k=l                     k=l
                                                 n−1             i(k−l) arccos(x) + e−i(k−l) arccos(x)
                                                 X           e
                                            =            βek
                                                                                  2
                                                 k=l
                                                   n−1                                n−1
                                              1    X                           1      X
                                            ≤              βek eik arccos(x) +              βek e−ik arccos(x)            (440)
                                              2                                2
                                                     k=l                              k=l
                                                     n−1                              l−1
                                                 1   X                         1      X
                                            ≤              βek eik arccos(x) +              βek eik arccos(x)
                                                 2                             2
                                                     k=0                              k=0
                                                       n−1                                  l−1
                                                     1 X                              1     X
                                                 +               βek e−ik arccos(x) +             βek e−ik arccos(x) .
                                                     2                                2
                                                          k=0                               k=0

Note that all the four terms in the last step are one-sided Fourier partial sums, but we would
recover the original polynomial p if we had the two-sided Fourier series. Thus, by Eq. (85), they
all have the scaling ∼ ∥p∥max,[−1,1] log(n) in the worst case. Hence,
                                                                                      
                                  α eT,ψ = O ∥S∥ S −1 |ψ⟩ ndmax −1 log(n) ∥p∥max,[−1,1] .                                 (441)

This establishes the asymptotic scaling asserted in the remark succeeding Theorem 4.

A.3       Average-case analysis with Carleson-Hunt theorem
In the previous subsection, we have analyzed asymptotic scaling of the Chebyshev-based eigenvalue
algorithms using a recursive version of the Bernstein’s theorem. For the quantum differential
equation algorithm, we have a polynomial that approximates the exponential function e−iαA tx , so
the above analysis yields
  n−1                        
  X                      A
         βek T
             e k−l                |ψ⟩ ≲ ∥S∥ S −1 |ψ⟩ log(n) e−iαA t(·)                              = ∥S∥ S −1 |ψ⟩ log(n) (442)
                         αA                                                           max,[−1,1]
   k=l

for a diagonalizable input A = SΛS −1 . On the other hand,
                                      q
                           −itA
                         e      |ψ⟩ = ⟨ψ|S −† eitΛ S † Se−itΛ S −1 |ψ⟩
                                      q
                                    ≥ λmin (S † S) ⟨ψ|S −† S −1 |ψ⟩                                                       (443)
                                      s
                                              1         −1           S −1 |ψ⟩
                                    =                 S    |ψ⟩  =             .
                                        ∥(S † S)−1 ∥                 ∥S −1 ∥

This implies that
                                                         αT,ψ
                                                                = O (κS log(n))                                           (444)
                                                           e

                                                         αexp,ψ
in the worst case as is claimed in the remark succeeding Theorem 7.



                                                                       96
    However, we show that one can shave off the log(n) factor when running the algorithm
                                                                                     P∞ on−ijω  an
average input. To this end, recall that the one-sided Fourier expansion H(g)(ω) = j=0 ξj e
                                                                           e
relates to the two-sided expansion g(ω) = ∞           −ijω via the Hilbert transform H(g)(ω) as
                                          P
                                            j=−∞ ξj e
                                                                                   Z π
                                              i           1                                       1
                                   H(g)(ω) = − H(g)(ω) +
                                   e                                                     du g(u) + g(ω).                                 (445)
                                              2          4π                           −π          2

Therefore, by the Riesz inequality (Lemma 4), the one-sided expansion as a function of ω has the
L2 -norm
                   1                    1               1                             
    H(g)
    e             ≤ ∥H(g)∥2,[−π,π] + √ ∥g∥1,[−π,π] + ∥g∥2,[−π,π]] = O ∥g∥max,[−π,π] . (446)
         2,[−π,π]  2                  2 2π              2

Using the Carleson-Hunt theorem (Lemma 5), we have
                                                                    
                   S∗ H(g)
                      e           = O H(g)
                                        e            = O ∥g∥max,[−π,π]                                                                   (447)
                                          2,[−π,π]                              2,[−π,π]

                                                                  −ijω .
                                                                                                  Pn−1
for the Fourier maximal function S∗ e
                                   H(g)(ω) = supn=0,1,...j=0 ξj e
   Given a polynomial p and its Chebyshev expansion p(x) = n−1
                                                            P
                                                               j=0 βj Tj (x), we can bound the
                                                                     e e
shifted Chebyshev partial sum as
                            v
                                                      †
                            u                              
   n−1                              n−1                           n−1           
                 A                                      Λ                           Λ
   X                        u          X                            X
                                  −†                             †                      S −1 |ψ⟩
                            u
       βk Tk−l
       e  e           |ψ⟩ = t⟨ψ|S         βj Tj−l
                                           e  e               S S       βk Tk−l
                                                                         e  e
                 αA                                    αA                          αA
   k=l                                 j=l                          k=l
                                v                                                                (448)
                                u                               †
                                           n−1                    n−1              
                                                    e j−l Λ                e k−l Λ S −1 |ψ⟩,
                                u          X                        X
                          ≤ ∥S∥ t⟨ψ|S −† 
                                u
                                                βej T                   βek T
                                                            αA                     αA
                                                                     j=l                                      k=l


where the diagonal entries satisfy

                          n−1                   2       n−1                           2           l−1                       2
                          X                             X                                         X
                                βek T
                                    e k−l (x)       ≤         βek eik arccos(x)           +             βek eik arccos(x)
                          k=l                           k=0                                       k=0
                                                                                              2                                 2
                                                                                                                                         (449)
                                                            n−1
                                                            X                                           l−1
                                                                                                        X
                                                        +         βek e−ik arccos(x)              +           βek e−ik arccos(x) .
                                                            k=0                                         k=0

The four terms above are all Fourier partial sums, and we only bound one of them without loss
of generality. Now denote the eigenvalues of arccos(A/αA ) as ω0 , . . . , ωd−1 , and suppose that they
satisfy a probability distribution with density q(ω0 , . . . , ωd−1 ). Then on average,
                                                                                  2
 Z π                Z π                                       n−1
                                                              X                           Z π
        dω0 · · ·         dωd−1 q(ω0 , . . . , ωd−1 )               βej e−ijωl        ≤                             H(p(cos(ωl )))2
                                                                                                      dωl ql (ωl )S∗ e
   −π                −π                                       j=0                             −π

                                                                                                                                     2   (450)
                                                                                      ≤ ∥ql ∥max,[−π,π] S∗ H(p(cos))
                                                                                                           e
                                                                                                                        2,[−π,π]
                                                                                                             2
                                                                                      = O(∥ql ∥max,[−π,π] ∥p∥max,[−1,1] ),


                                                                           97
where
                Z π                   Z π               Z π                  Z π
   ql (ωl ) =            dω0 · · ·           dωl−1             dωl+1 · · ·         dωd−1 q(ω0 , . . . , ωl−1 , ωl , ωl+1 , . . . , ωd−1 )   (451)
                    −π                  −π                −π                  −π

is the lth marginal density function. This means that on average,
                                               v
  Z π           Z π                            u        n−1                  n−1                  
                                                                ij arccos αΛ           −ik arccos αΛ
                                               u        X                      X
      dω0 · · ·     dωd−1 q(ω0 , . . . , ωd−1 ) ⟨ψ|S
                                               t     −†     βj e
                                                            e              A       βk e
                                                                                   e               A S −1 |ψ⟩
  −π                −π                                                         j=0                       k=0
  v
  u        Z π           Z π                             n−1                   n−1                   
                                                                  ij arccos αΛ            −ik arccos αΛ
  u                                                      X                       X
 ≤ ⟨ψ|S
  t     −†     dω0 · · ·     dωd−1 q(ω0 , . . . , ωd−1 )     βj e
                                                             e               A       βk e
                                                                                     e                A S −1 |ψ⟩
                        −π                  −π                                      j=0                      k=0
    q                                       
                                         −1
 =O   max ∥ql ∥max,[−π,π] ∥p∥max,[−1,1] S |ψ⟩ ,
                l
                                                                                               (452)
where we have used Jensen’s inequality and positive semidefinite property of matrices. Assuming
maxl ∥ql ∥max,[−π,π] = O(1) is independent of the target polynomial p(x), this gives the scaling
                                                                                     
                                                  αT,ψ
                                                   e   = O ∥S∥ S −1 |ψ⟩ ∥p∥max,[−1,1]                                                       (453)

in analyzing the average-case runtime of eigenvalue transformation and
                                                                    αT,ψ
                                                                           = O (κS )                                                        (454)
                                                                      e

                                                                    αexp,ψ

for the differential equation solver, justifying the claims in the remarks following Theorem 4 and
Theorem 7.
    We now briefly explain how our analysis can be modified to handle additional logarithmic
factors, which is the case for the complexity of our algorithms. To this end, suppose we have some
nonnegative function g(ω0 , . . . , ωd−1 ) of the eigenvalues of arccos(A/αA ). Then, by the Cauchy-
Schwarz inequality,
               Z π           Z π
                   dω0 · · ·     dωd−1 q(ω0 , . . . , ωd−1 )g(ω0 , . . . , ωd−1 ) logr (g(ω0 , . . . , ωd−1 ))
                −π            −π
              sZ
                             π Z                 π
            ≤                    dω0 · · ·            dωd−1 q(ωd−1 , . . . , ωd−1 )g 2 (ω0 , . . . , ωd−1 )                                 (455)
                          −π                     −π
                        sZ
                                 π               Z π
                    ·                dω0 · · ·          dωd−1 q(ω0 , . . . , ωd−1 ) log2r (g(ω0 , . . . , ωd−1 )).
                             −π                   −π

We already know how to bound the first term. To handle the second term, we need to prove the
concavity of ln2r (y) for large values of y. Since

         d ln2r (y)   2r ln2r−1 (y)
                    =               ,
             dy             y
                                                                                                                                            (456)
        d2 ln2r (y)   2r(2r − 1) ln2r−2 (y) − 2r ln2r−1 (y)   2r ln2r−2 (y)
                    =                                       =               (2r − 1 − ln(y)) ,
           dy 2                       y2                           y2



                                                                              98
the function ln2r (y) is indeed concave for y sufficiently large. Therefore, Jensen’s inequality yields
                     Z π            Z π
                          dω0 · · ·      dωd−1 q(ω0 , . . . , ωd−1 ) log2r (g(ω0 , . . . , ωd−1 ))
                       −π            −π
                            Z π              Z π                                                   (457)
                         2r
                 ≤ log              dω0 · · ·     dωd−1 q(ω0 , . . . , ωd−1 )g(ω0 , . . . , ωd−1 ) .
                             −π           −π

The remaining analysis now proceeds as before.


B     Analysis of Faber-based algorithms
In this appendix, we analyze the Faber-based eigenvalue algorithms in more detail. Specifically, we
review previous bounds for matrix exponentials in Appendix B.1 based on the numerical abscissa.
We show in Appendix B.2 how this idea can be generalized to bound a matrix function with the help
of numerical range and Crouzeix-Palencia theorem. We prove an analogous bound in Appendix B.3
based on the notion of pseudospectrum. Finally, we bound the average complexity of our algorithms
in Appendix B.4 using the Carleson-Hunt theorem.

B.1    Matrix exponential bound based on numerical abscissa
We begin by reviewing a previous bound on norm of the matrix exponential function used in the
analysis of quantum differential equation algorithms [50] [53, Appendix D]. Specifically, our goal is
to bound eτ C for τ > 0 and square matrix C. The bound we will present does not depend on the
Jordan condition number, which avoids the potential issue of a ill-conditioned Jordan basis arising
in the setting of Appendix A.
    To this end, recall that any square matrix C can be uniquely written as [44, Theorem 4.1.2]

                                          C = ℜ(C) + iℑ(C)                                          (458)

for Hermitian matrices ℜ(C) and ℑ(C). Indeed, the existence of such a Toeplitz decomposition
follows by setting
                                      C + C†                C − C†
                             ℜ(C) =          ,     ℑ(C) =            ,                      (459)
                                         2                     2i
whereas an equality ℜ1 (C) + iℑ1 (C) = ℜ2 (C) + iℑ2 (C) would imply that ℜ1 (C) − ℜ2 (C) =
iℑ2 (C)−iℑ1 (C) is both Hermitian and anti-Hermitian, forcing ℜ1 (C) = ℜ2 (C) and ℑ1 (C) = ℑ2 (C).
We then define the numerical abscissa as
                                                               C + C†
                                                                      
                         max λl (ℜ(C)) = λmax (ℜ(C)) = λmax              .                  (460)
                          l                                        2

As the following proposition shows, the numerical abscissa can be used to bound the growth of
matrix exponentials [90, Theorem 17.1]. We present a short proof based on the Lie-Trotter product
formula which may be more familiar to readers of this work, due to its role in the study of quantum
simulation and beyond [22].

Proposition 32. For τ > 0 and square matrix C,

                                          eτ C ≤ eτ λmax (ℜ(C)) .                                   (461)



                                                   99
Proof. We start with the Lie-Trotter splitting:

                                       τ2                                     τ2
           eτ C − eτ ℜ(C) eiτ ℑ(C) ≤      ∥[ℜ(C), ℑ(C)]∥ eτ (∥ℜ(C)∥+∥ℑ(C)∥) ≤    ∥C∥2 e2τ ∥C∥ .          (462)
                                       2                                      2
This implies through the triangle inequality that

                                                                                     τ2
      eτ C ≤ eτ ℜ(C) eiτ ℑ(C) + eτ C − eτ ℜ(C) eiτ ℑ(C) ≤ eτ λmax (ℜ(C)) +              ∥C∥2 e2τ ∥C∥ ,   (463)
                                                                                     2
where we have used the fact that eiτ ℑ(C) is unitary and that eτ ℜ(C) = eτ λmax (ℜ(C)) .
   This bound works well when τ → 0. To analyze a long-time evolution, we divide it into r steps
and apply the above estimate within each step, obtaining
                                                                             r
                                                             τ2
                                         
                                τ    r       τ                         τ
                      τC          C            λ     (ℜ(C))        2 2   ∥C∥
                     e     ≤ er        ≤ er      max
                                                            + 2 ∥C∥ e r         .          (464)
                                                             2r

Let us choose                                      (                     )
                                                          eτ 2 ∥C∥2
                                         r ≥ max 2τ ∥C∥ ,                                                (465)
                                                              2ϵ
so that
                                          τ               τ2           ϵ
                                        e2 r ∥C∥ ≤ e,        2
                                                               ∥C∥2 e ≤ .                                (466)
                                                          2r           r
This implies
                                                                                             r
                     τC
                             τ
                                 λ     (ℜ(C))   ϵ r       τ λ    (ℜ(C))                ϵ
                    e     ≤ er     max
                                              +       =e      max
                                                                            1 + τ λ (ℜ(C))
                                                r                                re r max
                                                                                                         (467)
                                                                                            √ 
                                                                  
                                                         ϵ
                          ≤ eτ λmax (ℜ(C)) exp      τ                ≤   eτ λmax (ℜ(C))
                                                                                        exp  eϵ .
                                                  e r λmax (ℜ(C))

Here, the second inequality follows from the estimate (1+y)1/y ≤ e for y > 0 and the last inequality
follows from the observation that
                                       τ               |λmax (ℜ(C))|  1
                                         λmax (ℜ(C)) ≤               ≤ .                                 (468)
                                       r                  2 ∥C∥       2

The claimed bound is now established by letting ϵ → 0.

   We thus have that eτ C is bounded for all τ > 0 when the numerical abscissa satisfies
λmax (ℜ(C)) ≤ 0, and it decays exponentially with τ when the strict inequality λmax (ℜ(C)) < 0
holds. The bound does not depend on the Jordan condition number, and is thus applicable even
when the Jordan basis is ill conditioned. Note however that any matrix C satisfying λmax (ℜ(C)) ≤ 0
must automatically satisfy maxl ℜ (λl (C)) ≤ 0, so the numerical abscissa leads to a stronger as-
sumption on the input matrix in this respect.

B.2       Matrix function bound with Crouzeix-Palencia theorem
Unlike [50], our Faber-based eigenvalue algorithms have complexity scaling with the spectral norm
of various matrix functions. To derive a similar bound independent of the Jordan condition number,
we will need the notion of numerical range which extends the numerical abscissa introduced above.
See [43, 54, 82, 95] for more detailed discussions about this concept.

                                                        100
   Given a square matrix C, we define its numerical range (also known as the field of values) to
be the set
                              W(C) = {⟨ψ|C|ψ⟩ | ∥|ψ⟩∥ = 1} .                               (469)
It is clear that when C is a normal matrix, W(C) is the convex hull generated by all its eigenvalues.
In general, W(C) is still a convex and compact set containing all eigenvalues of C following the
Toeplitz-Hausdorff theorem, although it is no longer related to the spectra of C in a straightforward
way.
     As an illustration of this concept, we have that H is a Hermitian matrix if and only if W(H) ⊆ R
is a closed and bounded real interval. This follows directly from the characterizations of Hermitian
matrices in Section 2.3. Also, N is a normal matrix if and only if all its eigenvalues lie on the
boundary ∂W(N ) of its numerical range [39, Condition 66]. In general, when an eigenvalue of a
matrix lies on the boundary of its numerical range λl (C) ∈ W(C), then λl (C) is nondefective and
the eigenspace Ker (C − λl (C)I) is perpendicular to the remaining Jordan subspaces [43, Theorem
1.6.6]. As yet another example, we point out that the n-by-n lower shift matrix has numerical range
                  π                                       π
W(Ln ) = cos( n+1   )D given by the disk of radius cos( n+1  ) centered at the origin [91]. This fact will
be used to analyze the block encoding of the matrix Faber generating function in Section 8.2.
     The notion of numerical range provides a useful tool for bounding the spectral norm of matrix
functions. This is confirmed by the following Crouzeix-Palencia theorem.

Lemma 33 (Crouzeix-Palencia theorem [25, 74]). Given a square matrix C, for any function g
analytic in the interior of W(C) and continuous up to the boundary ∂W(C),
                                             √ 
                                ∥g(C)∥ ≤ 1 + 2 ∥g∥max,W(C) .                         (470)

   To illustrate the power of this result, let us prove a numerical-abscissa-type bound similar to
that of the previous subsection with only a one-line calculation:

              eτ C ≲ eτ (·)              = max eτ ℜ(W(C)) = max eτ W(ℜ(C)) = eτ λmax (ℜ(C)) .       (471)
                              max,W(C)

Here, we have used the property that the calculation of numerical range “commutes” with taking
the real part, which is formally stated as:

Proposition 34. For any square matrix C,

                                         ℜ(W(C)) = W(ℜ(C)).                                         (472)

Here ℜ on the left-hand side takes the real part of a complex number, whereas ℜ on the right-hand
side returns the Hermitian part of a square matrix.

Proof. The claimed equality follows from a direct verification

                                                   C + C†
                                                                         
    ℜ(W(C)) = {ℜ(⟨ψ|C|ψ⟩) | ∥|ψ⟩∥ = 1} = ⟨ψ|               |ψ⟩ | ∥|ψ⟩∥ = 1 = W(ℜ(C)).               (473)
                                                      2



   Therefore, by applying the Crouzeix-Palencia theorem, we can reproduce
                                                                       √ the numerical abscissa
bound from the previous subsection up to a constant prefactor of 1 + 2. The advantage of this
approach, however, is that it can be easily generalized to other analytic functions and regions of
the complex plane, through which our Faber-based eigenvalue algorithms can be analyzed.

                                                   101
                                                    
                                                 A
                                      F′j       αA
   Let us first bound                       j            , which appears in the asymptotic complexity expression of the

algorithm for generating Faber history
                                    states.
                                            To this end, we assume that the numerical range is
                                     A
enclosed by the Faber region as W αA ⊆ E. Using the Crouzeix-Palencia theorem, we have
                  
    F′j       A
              αA            F′j                                F′j
                                                                                             ≲ ∥Fj ∥max,∂W
                                                                                                                            ≤ ∥F ∥
                       ≲                                  =                                                                     j max,E = O(1),
                                                                                                                 
                                                                                                                      A
           j                j        max,W
                                                
                                                     A         j     max,∂W
                                                                                   
                                                                                        A                            αA
                                                    αA                                 αA

                                                                                            (474)
where the second inequality follows from the Bernstein’s theorem for twice continuously differen-
tiable curves stated below, and the last equality holds as long as boundary of the Faber region
has a finite total rotation
                       V(∂E). Under all these assumptions on the Faber region (enclosing the
numerical range W αAA with a twice continuously differentiable and finite rotation boundary), we
have
                                          αF′ = O(1),                                       (475)
which justifies the claim in the remark succeeding Theorem 9.

Lemma 35 (Bernstein’s theorem for twice continuously differentiable Jordan curves [47, Eqs. (26)
and (27)]). Given a degree-j polynomial pj and a Jordan curve C twice continuously differentiable
in a neighborhood of z ∈ C, it holds

                                                    p′j (z) ≤ (1 + o(1)) j2πωC (z) ∥pj ∥max,C ,                                                     (476)

where ωC (z) is the equilibrium density. Thus, if the entire curve C is twice continuously differen-
tiable,                                                                           
                  p′j max,C ≤ (1 + o(1)) j2π max ωC (z) ∥pj ∥max,C = O j ∥pj ∥max,C .          (477)
                                                                         z∈C
                                                               Pn−1                             
                                                                                            A
   Next, we consider maxl=0,1,...,n−1                |ψ⟩ , which is used to describe complexity
                                                                 k=l βk Fk−l                αA
                                                                      
of the Faber eigenvalue transformation algorithm. Assuming that W αAA ⊆ E, we apply the
Crouzeix-Palencia theorem to get
   n−1                                            n−1                                   n−1
   X                       A                        X                    A                  X
          βk Fk−l                   |ψ⟩ ≤                  βk Fk−l                 ≲                 βk Fk−l
                           αA                                            αA                                            
                                                                                                                            A
                                                                                                                                
   k=l                                               k=l                                     k=l               max,W       αA

                                                    n−1
                                                    X                                  n−1
                                                                                       X                                    n−1
                                                                                                                            X
                                        ≤                  βk Fk−l             =                 βk Fk−l             =              βk Fk−l               .
                                                     k=l             max,E              k=l                max,∂E           k=l               max,Ψ(∂D)
                                                                                           (478)
Recall that for regions with finite total rotation, we have the integral representation of Faber
polynomials                           ( R 2π
                                        1
                                              eikφ dφ v(φ, ω),     k ≥ 1,
                       Fk (Ψ(eiω )) = π1 R0 2π                                             (479)
                                        2π 0 dφ v(φ, ω) = 1,       k = 0,




                                                                               102
with the angular function v(φ, ω) = Arg Ψ(eiφ ) − Ψ(eiω ) . This means that
                                                         


          n                             n             Z 2π
          X                             X         1
                             iω
                 βk Fk+j−n (Ψ(e )) =           βk            ei(k+j−n)φ dφ v(φ, ω) − βn−j
                                                  π    0
         k=n−j                         k=n−j
                                        Z 2π     n
                                    1            X
                                  ≤                        βk eikφ |dφ v(φ, ω)| + |βn−j |
                                    π    0                                                       (480)
                                                k=n−j
                                        Z 2π
                                    1
                                  ≤      S[n−j,n] (φ) |dφ v(φ, ω)| + ∥p∥max,∂E
                                    π 0
                                                            
                                    V(∂E) 4
                                  ≤           log(n)  + O(1)    ∥p∥max,∂E + ∥p∥max,∂E ,
                                      π    π2

where the coefficients βk are the Fourier coefficients
                                            Z 2π
                                         1              p(Ψ(eiv ))
                                   βk =           dv eiv i(k+1)v .                               (481)
                                        2π 0             e
Hence,                                                      
                                    αF,ψ = O log(n) ∥p∥max,∂E ,                                  (482)

which establishes the claimed asymptotic complexity in the remark following Theorem 10.
    Finally, for solving linear differential equations, we have the following requirements on the Faber
region E that encloses numerical range of the input matrix.

  1. To ensure that αF′ = O(1) in Eq. (398), we require that the boundary ∂E is twice continuously
     differentiable.
                                               
  2. To ensure that αF,ψ = O log(n) ∥p∥max,∂E in Eq. (403), we need ∂E to have a finite total
     rotation.

  3. To ensure the validity of Lemma 27, we assume that E is convex and symmetric with respect
     to the real axis, lying on the left half of the complex plane.

One possible Faber region satisfying all the above requirements is shown in Figure 2d, which is a
smooth deformation of the Elliott semidisk of Figure 2c. This is sufficient to prove the asymptotic
query complexity of the differential equation solver. Note however that this is not the only option
for choosing E. One may instead numerically construct conformal maps that are easier to compute
leading to better constant prefactors in the gate complexity. We leave a complete study of such
optimizations as a subject for future work.

B.3      Matrix function bound based on pseudospectrum
Using the notion of numerical range and Crouzeix-Palencia theorem, we have shown that complexity
of the Faber-based method can be independent of the condition number of the basis transformation.
This yields an efficient QEVT algorithm even when the input matrix has an ill-conditioned Jordan
basis. We now provide an alternative analysis of the Faber-based algorithms based on the concept
of pseudospectrum, which also applies to matrices with ill-conditioned Jordan basis. We begin by
reviewing the definition of pseudospectrum and its properties most relevant to our paper, referring
the reader to [46, 90] for further discussions of this topic.

                                                      103
   For a given square matrix C and δ > 0, we define the δ-pseudospectrum to be the set of complex
numbers satisfying any one of the following equivalent conditions:

                Sδ (C) = {z ∈ C, ∥C|ψ⟩ − z|ψ⟩∥ < δ for some ∥|ψ⟩∥ = 1}
                         n                                               o
                       = z ∈ C, z is an eigenvalue of C
                                                      e for some Ce−C <δ
                                               
                                      1       1
                       = z ∈ C,            >
                                   z−C        δ
                       = {z ∈ C, σmin (C − z) < δ} .

Thus, pseudospectrum relaxes the definition of eigenvalues C|ψ⟩ = λ|ψ⟩ or σmin (C − λ) = 0
to approximately hold as ∥C|ψ⟩ − z|ψ⟩∥ < δ or σmin (C − z) < δ, whereas the usual spectrum is
recovered from the infinite intersection ∩δ>0 Sδ (C). This is an open and bounded set in the complex
plane that contains all δ-balls around eigenvalues of C:

                                            Sδ (C) ⊇ {λj (C)} + D(0, δ),

with equality if and only if C is a normal matrix. On the other hand, it is upper bounded by the
numerical range up to a perturbation of δ:

                                             Sδ (C) ⊆ W(C) + D(0, δ).
                                                                           1
   By definition, we have that z ∈ Sδ (C) if and only if                  z−C   > 1δ , and z ∈
                                                                                             / Sδ (C) if and only
if z−C1
          ≤ 1δ . We then use a continuity argument to conclude that z−C  1
                                                                               = 1δ on the boundary
z ∈ ∂Sδ (C). More generally, letting C be a contour enclosing the pseudospectrum Sδ (C) that are
all contained in the region of analyticity of f , we have from the Cauchy’s integral formula
                                            1
                                               Z
                                 f (C) =           dz f (z)(zI − C)−1
                                          2πi C
that
                                             Lδ (C)
                                                    ∥f ∥max,C
                                             ∥f (C)∥ ≤
                                              2πδ
             R
for Lδ (C) = C |dz| arc length of the contour C. This pseudospectrum-type bound for matrix
functions can be compared to that of Lemma 33 based on the notion of numerical range.
    We now analyze the performance of 
                                        Faber-based
                                         
                                                     eigenvalue transformation algorithms using
                                                        A
                                                 F′j   αA
pseudospectrum. We first bound                         j      , which shows up in the asymptotic complexity of

creating the Faber history state. Similar to the assumption
                                                         on numerical range, we assume that
                                                          A
the pseudospectrum is encosed by the Faber region as Sδ αA ⊆ E. We have
                                  
                    F′j       A
                              αA           F′j
                                       ≲                     ≲ ∥Fj ∥max,∂E = ∥Fj ∥max,E = O(1),
                          j                j       max,∂E


where in the second asymptotic estimate we have used Bernstein’s theorem assuming the boundary
E is sufficiently smooth, and in the last asymptotic estimate we have assumed that boundary of
the Faber region has a finite total rotation. This means that

                                                            αF′ = O(1),

                                                               104
which justifies the claim in the remark succeeding Theorem
                                                        9.
                                        Pn−1            A
   Next, we consider maxl=0,1,...,n−1      k=l βk Fk−l αA |ψ⟩ , which appears in the asymptotic
                                                                                  
complexity of the Faber eigenvalue transformation algorithm. Assuming that Sδ αAA ⊆ E, we
obtain
  n−1                       n−1                   n−1                n−1
  X              A            X             A         X                  X
      βk Fk−l         |ψ⟩ ≤       βk Fk−l          ≲      βk Fk−l     =      βk Fk−l         .
                αA                          αA
  k=l                                  k=l                        k=l              max,∂E        k=l        max,Ψ(∂D)

Proceeding in a similar way as in the numerical range case, we have
                                                            
                                  αF,ψ = O log(n) ∥p∥max,∂E ,

which establishes the claimed complexity in the remark following Theorem 10.

B.4     Average-case analysis with Carleson-Hunt theorem
In the previous subsection, we have analyzed asymptotic scaling of the Faber-based eigenvalue
algorithms based on either the numerical range or the pseudospectrum. However, there is a ∼ log(n)
factor in the bound of αF,ψ . Similar to the Chebyshev case, this logarithmic factor can be removed
for an average diagonalizable input matrix with the help of Carleson-Hunt theorem (by trading in
a scaling with the Jordan condition number), although the reasoning is somewhat different which
we present below.
    For any z in the interior of the Faber region E, we apply the Cauchy integral theorem to the
Faber generating function and get
                             n                       n
                                                                   1               ξ k+j−n Ψ′ (ξ)
                             X                       X                  Z
                                  βk Fk+j−n (z) =           βk                dξ
                                                                  2πi    ∂D           Ψ(ξ) − z
                         k=n−j                      k=n−j
                                                                                                                 (483)
                                                                        n
                                                    1                                 Ψ′ (ξ)
                                                        Z               X
                                                 ≤            dξ              βk ξ k          .
                                                   2π   ∂D                           Ψ(ξ) − z
                                                                    k=n−j

The result can be further upper bounded by a linear combination of partial sums of the form
                       ′
                    k Ψ (ξ)
 1
   R      Pn
2π ∂D dξ    k=0 βk ξ Ψ(ξ)−z . By definition of the contour integral,

                                 n                                          n
                                             Ψ′ (ξ)                                          Ψ′ (eiu )
                                                            Z 2π
               1                                        1
                   Z             X                                          X
                                             k
                         dξ            βk ξ          =              du            βk eiku               ,        (484)
              2π   ∂D                       Ψ(ξ) − z   2π     0                             Ψ(eiu ) − z
                                 k=0                                        k=0

where the coefficients βk are the Fourier coefficients
                                              Z 2π
                                            1            p(Ψ(eiv ))
                                    βk =           dv eiv i(k+1)v .                           (485)
                                           2π 0           e

Therefore, nk=0 βk eiku is exactly the one-sided Fourier partial sum for the function p(Ψ(eiu )) or,
           P
equivalently, the two-sided Fourier partial sum for the Hilbert transform of p(Ψ(eiu )). Therefore,
we have
                    n
                                Ψ′ (eiu )                                      Ψ′ (eiu )
         Z 2π                                    Z 2π
       1           X                           1
                       βk eiku                                         iu
                                                                            
               du                           ≤         du   S n H
                                                               e p(Ψ(e    ))              .   (486)
      2π 0                     Ψ(eiu ) − z    2π 0                            Ψ(eiu ) − z
                       k=0


                                                        105
   Here, the second factor can be further bounded as

                                            Ψ′ (eiu )    ∥Ψ′ ∥max,∂D
                                                       ≤             ,                                          (487)
                                           Ψ(eiu ) − z   Dist(z, ∂E)

whereas the first factor is handled by the Carleson-Hunt theorem as
                                              s
                Z 2π                            Z 2π
                                                                           2
                             e p(Ψ(eiu )) ≲
                                         
                     du Sn H                         du Sn He (p(Ψ(eiu )))
                 0                                0
                                                                                                            (488)
                                            ≲ p Ψ ei(·)              = ∥p∥max,∂E .
                                                                            max,[0,2π]

Altogether,
                                    n
                                    X                         ∥Ψ′ ∥max,∂D
                                         βk Fk+j−n (z) ≲                    ∥p∥max,∂E .                         (489)
                                                              Dist(z, ∂E)
                                 k=n−j

   Now,
    R    suppose that z is randomly distributed in E with probability density function q(z) such
that E dz q(z) = 1. Then,
                                                    2
                             n
                                                                                                 q(z)
           Z                                                                        Z
                                                               2
                             X
                  dz q(z)           βk Fk+j−n (z)       ≲   Ψ′ max,∂D ∥p∥2max,∂E         dz                 .   (490)
              E             k=n−j                                                    E        Dist2 (z, ∂E)

We assume that E dz Distq(z)
                R
                          2
                            (z,∂E)
                                   is finite, which happens if eigenvalues of the input matrix have less
chance to appear near boundary ∂E of the Faber region. In any case, this is a constant depending
only on properties of the Faber region. Proceeding as in the Chebyshev case, we obtain
                                                                     
                                 αF,ψ = O ∥S∥ S −1 |ψ⟩ ∥p∥max,∂E                                  (491)

for diagonalizable input matrices. This justifies the claimed scaling in the remark succeeding
Theorem 10.
    We end this section with a brief comment on the analysis of quantum eigenvalue algorithms. We
have bounded query complexity of the Chebyshev-based algorithms in Appendix A using the Jordan
condition number as well as size of the largest Jordan block, whereas we have handled the Faber-
based algorithms in Appendix B mostly using the notion of numerical range and pseudospectrum.
See Table 1 for a summary of results. This is however not the only way in which our algorithms
can be analyzed. For instance, our above analysis in Appendix B.4 works for diagonalizable input
matrices and is essentially a generalization of the Jordan condition number bound. The reverse
direction however does not lead to interesting new results. This is because, in order to apply the
Crouzeix-Palencia theorem, we would need to enclose numerical range of the input matrix inside
of a real interval (the pseudospectrum is an open set and can never be enclosed by a real interval).
But per the characterizations of Hermitian matrices in Section 2.3, this only happens if the input
matrix is Hermitian, which is already handled by the existing QSVT algorithm. In any case, it
would be fruitful to prove tighter bounds on the matrix functions used by our algorithms, as well
as to construct alternative methods for quantum eigenvalue processing that scale with different
matrix functions.




                                                            106
References
 [1] Abhijeet Alase and Salini Karuvade, Resolvent-based quantum phase estimation: Towards esti-
     mation of parametrized eigenvalues, 2024, arXiv:2410.04837, DOI: 10.48550/arXiv.2410.04837.
     (Cited on page 16).

 [2] Ronald L Allen and Duncan Mills, Signal analysis: time, frequency, scale, and structure, John
     Wiley & Sons, 2004, DOI: 10.1002/047166037X. (Cited on page 22).

 [3] Dong An, Andrew M. Childs, and Lin Lin, Quantum algorithm for linear non-unitary dynamics
     with near-optimal dependence on all parameters, Communications in Mathematical Physics
     407 (2025), no. 1, 19, arXiv:2312.03916, DOI: 10.1007/s00220-025-05509-w. (Cited on pages
     14 and 91).

 [4] Yuto Ashida, Zongping Gong, and Masahito Ueda, Non-Hermitian physics, Advances in
     Physics 69 (2020), no. 3, 249–435, arXiv:2006.01837, DOI: 10.1080/00018732.2021.1876991.
     (Cited on pages 5, 8, 13, and 25).

 [5] Yosi Atia and Dorit Aharonov, Fast-forwarding of Hamiltonians and exponentially pre-
     cise measurements, Nature Communications 8 (2017), no. 1, 1572, arXiv:1610.09619, DOI:
     10.1038/s41467-017-01637-7. (Cited on page 10).

 [6] Sheldon Axler, Linear algebra done right, Springer Nature, 2023, DOI: 10.1007/978-3-031-
     41026-0. (Cited on page 25).

 [7] Z. Bai, James Demmel, and A. McKenney, On computing condition numbers for the nonsym-
     metric eigenproblem, ACM Transactions on Mathematical Software 19 (1993), no. 2, 202–223,
     DOI: 10.1145/152613.152617. (Cited on pages 29 and 92).

 [8] Bernhard Beckermann and Lothar Reichel, Error estimates and evaluation of matrix functions
     via the Faber transform, SIAM Journal on Numerical Analysis 47 (2009), no. 5, 3849–3883,
     DOI: 10.1137/080741744. (Cited on pages 87 and 88).

 [9] Carl M. Bender, Dorje C. Brody, Hugh F. Jones, and Bernhard K. Meister, Faster than Hermi-
     tian quantum mechanics, Physical Review Letters 98 (2007), 040403, arXiv:quant-ph/0609032,
     DOI: 10.1103/PhysRevLett.98.040403. (Cited on pages 5, 8, and 92).

[10] Dominic W. Berry and Pedro C. S. Costa, Quantum algorithm for time-dependent differential
     equations using Dyson series, Quantum 8 (2024), 1369, arXiv:2212.03544, DOI: 10.22331/q-
     2024-06-13-1369. (Cited on page 11).

[11] Dominic W. Berry, Andrew M. Childs, Richard Cleve, Robin Kothari, and Rolando D. Somma,
     Exponential improvement in precision for simulating sparse Hamiltonians, Proceedings of the
     46th Annual ACM Symposium on Theory of Computing, pp. 283–292, 2014, arXiv:1312.1414,
     DOI: 10.1145/2591796.2591854. (Cited on page 32).

[12] Dominic W. Berry, Andrew M. Childs, Aaron Ostrander, and Guoming Wang, Quantum al-
     gorithm for linear differential equations with exponentially improved dependence on precision,
     Communications in Mathematical Physics 356 (2017), 1057–1081, arXiv:1701.03684, DOI:
     10.1007/s00220-017-3002-y. (Cited on pages 5, 7, 8, and 36).




                                               107
[13] Dominic W. Berry, Andrew M. Childs, Yuan Su, Xin Wang, and Nathan Wiebe,
     Time-dependent Hamiltonian simulation with L1 -norm scaling, Quantum 4 (2020), 254,
     arXiv:1906.07115, DOI: 10.22331/q-2020-04-20-254. (Cited on page 64).

[14] Earl Campbell, Random compiler for fast Hamiltonian simulation, Physical Review Letters
     123 (2019), 070503, arXiv:1811.08017, DOI: 10.1103/PhysRevLett.123.070503. (Cited on
     pages 12 and 91).

[15] Shantanav Chakraborty, András Gilyén, and Stacey Jeffery, The power of block-encoded matrix
     powers: Improved regression techniques via faster Hamiltonian simulation, 46th International
     Colloquium on Automata, Languages, and Programming (ICALP 2019), vol. 132, pp. 33:1–
     33:14, 2019, arXiv:1804.01973, DOI: 10.4230/LIPIcs.ICALP.2019.33. (Cited on page 5).

[16] Chi-Fang Chen and Fernando G. S. L. Brandão, Average-case speedup for product formu-
     las, Communications in Mathematical Physics 405 (2024), no. 2, 32, arXiv:2111.05324, DOI:
     10.1007/s00220-023-04912-5. (Cited on pages 12 and 91).

[17] S. Chevillard, The functions erf and erfc computed with arbitrary precision and explicit er-
     ror bounds, Information and Computation 216 (2012), 72–95, DOI: 10.1016/j.ic.2011.09.001.
     (Cited on page 77).

[18] Andrew M Childs, Lecture notes on quantum algorithms, https://www.cs.umd.edu/∼amchilds/
     qa/, Last accessed on 2024-01-09. (Cited on pages 5 and 94).

[19] Andrew M. Childs, On the relationship between continuous- and discrete-time quantum walk,
     Communications in Mathematical Physics 294 (2010), no. 2, 581–603, arXiv:0810.0312, DOI:
     10.1007/s00220-009-0930-1. (Cited on page 6).

[20] Andrew M. Childs, Dmitri Maslov, Yunseong Nam, Neil J. Ross, and Yuan Su, Toward the first
     quantum simulation with quantum speedup, Proceedings of the National Academy of Sciences
     115 (2018), no. 38, 9456–9461, arXiv:1711.10980, DOI: 10.1073/pnas.1801723115. (Cited on
     page 33).

[21] Andrew M. Childs, Aaron Ostrander, and Yuan Su, Faster quantum simulation by randomiza-
     tion, Quantum 3 (2019), 182, arXiv:1805.08385, DOI: 10.22331/q-2019-09-02-182. (Cited on
     pages 12 and 91).

[22] Andrew M. Childs, Yuan Su, Minh C. Tran, Nathan Wiebe, and Shuchen Zhu, Theory of Trot-
     ter error with commutator scaling, Physical Review X 11 (2021), 011020, arXiv:1912.08854,
     DOI: 10.1103/PhysRevX.11.011020. (Cited on page 99).

[23] John P. Coleman and Russell A. Smith, The Faber polynomials for circular sectors, Mathe-
     matics of Computation 49 (1987), 231, DOI: 10.2307/2008260. (Cited on page 8).

[24] Pedro C.S. Costa, Dong An, Yuval R. Sanders, Yuan Su, Ryan Babbush, and Dominic W.
     Berry, Optimal scaling quantum linear-systems solver via discrete adiabatic theorem, PRX
     Quantum 3 (2022), 040303, arXiv:2111.08152, DOI: 10.1103/PRXQuantum.3.040303. (Cited
     on pages 8, 12, and 34).
                                                                  √
[25] M. Crouzeix and C. Palencia, The numerical range is a (1 + 2)-spectral set, SIAM Jour-
     nal on Matrix Analysis and Applications 38 (2017), no. 2, 649–655, arXiv:1702.00668, DOI:
     10.1137/17M1116672. (Cited on page 101).

                                               108
[26] J. H. Curtiss, Faber polynomials and the Faber series, The American Mathematical Monthly
     78 (1971), no. 6, 577–596, DOI: 10.1080/00029890.1971.11992813. (Cited on page 79).

[27] Alexander M. Dalzell, A shortcut to an optimal quantum linear system solver, 2024,
     arXiv:2406.12086, DOI: 10.48550/arXiv.2406.12086. (Cited on pages 8, 12, and 34).

[28] Juan Arias de Reyna, Pointwise convergence of Fourier series, Springer, 2002, DOI:
     10.1007/b83346. (Cited on page 25).

[29] Ronald de Wolf, Quantum computing: Lecture notes, 2019, arXiv:1907.09415, DOI:
     10.48550/arXiv.1907.09415. (Cited on page 5).

[30] Yulong Dong, Lin Lin, and Yu Tong, Ground-state preparation and energy estimation on early
     fault-tolerant quantum computers via quantum eigenvalue transformation of unitary matrices,
     PRX Quantum 3 (2022), 040305, arXiv:2204.05955, DOI: 10.1103/PRXQuantum.3.040305.
     (Cited on page 92).

[31] S. W. Ellacott, Computation of Faber series with application to numerical polynomial approxi-
     mation in the complex plane, Mathematics of Computation 40 (1983), no. 162, 575–587, DOI:
     10.2307/2007534. (Cited on page 80).

[32] Graham Hallett Elliott, The construction of Chebyshev approximations in the complex plane,
     Ph.D. thesis, Imperial College London, 1978. (Cited on page 80).

[33] L. Elsner and Kh.D. Ikramov, Normal matrices: an update, Linear Algebra and its Applications
     285 (1998), no. 1, 291–303, DOI: 10.1016/S0024-3795(98)10161-1. (Cited on pages 29 and 34).

[34] Di Fang, Lin Lin, and Yu Tong, Time-marching based quantum solvers for time-dependent
     linear differential equations, Quantum 7 (2023), 955, arXiv:2208.06941, DOI: 10.22331/q-2023-
     03-20-955. (Cited on pages 11, 14, and 91).

[35] Josep Ferrer, David Mingueza, and M. Eulalia Montoro, Determinant of a matrix that com-
     mutes with a Jordan matrix, Linear Algebra and its Applications 439 (2013), no. 12, 3945–
     3954, DOI: 10.1016/j.laa.2013.10.023. (Cited on page 27).

[36] Yimin Ge, Jordi Tura, and J. Ignacio Cirac, Faster ground state preparation and high-precision
     ground energy estimation with fewer qubits, Journal of Mathematical Physics 60 (2019), no. 2,
     022202, arXiv:1712.03193, DOI: 10.1063/1.5027484. (Cited on page 14).

[37] András Gilyén, Yuan Su, Guang Hao Low, and Nathan Wiebe, Quantum singular value trans-
     formation and beyond: Exponential improvements for quantum matrix arithmetics, Proceed-
     ings of the 51st Annual ACM SIGACT Symposium on Theory of Computing, pp. 193–204,
     2019, arXiv:1806.01838, DOI: 10.1145/3313276.3316366. (Cited on pages 4, 5, 12, 32, 33, 34,
     and 35).

[38] Vittorio Giovannetti, Seth Lloyd, and Lorenzo Maccone, Quantum metrology, Physical Review
     Letters 96 (2006), 010401, arXiv:quant-ph/0509179, DOI: 10.1103/PhysRevLett.96.010401.
     (Cited on pages 10 and 54).

[39] Robert Grone, Charles R. Johnson, Eduardo M. Sa, and Henry Wolkowicz, Normal matrices,
     Linear Algebra and its Applications 87 (1987), 213–225, DOI: 10.1016/0024-3795(87)90168-6.
     (Cited on page 101).


                                               109
[40] Paul R Halmos, Normal dilations and extensions of operators, Summa Brasiliensis Math 2
     (1950), 125–134. (Cited on page 32).

[41] Aram W. Harrow, Avinatan Hassidim, and Seth Lloyd, Quantum algorithm for linear sys-
     tems of equations, Physical Review Letters 103 (2009), 150502, arXiv:0811.3171, DOI:
     10.1103/PhysRevLett.103.150502. (Cited on page 4).

[42] Peter Henrici, Applied and computational complex analysis. Volume 1: Power series, integra-
     tion, conformal mapping, location of zeros, Wiley, 1974. (Cited on pages 36 and 81).

[43] Roger A. Horn and Charles R. Johnson, Topics in matrix analysis, Cambridge University
     Press, 1994, DOI: 10.1017/CBO9780511840371. (Cited on pages 36, 81, 84, 90, 100, and 101).

[44] Roger A. Horn and Charles R. Johnson, Matrix analysis, Cambridge University Press, 2012,
     DOI: 10.1017/CBO9781139020411. (Cited on pages 19, 25, 26, 27, 29, 30, 31, 32, 75, and 99).

[45] Jeffrey Humpherys, Tyler J Jarvis, and Emily J Evans, Foundations of applied mathematics,
     volume 1: Mathematical analysis, Society for Industrial and Applied Mathematics, Philadel-
     phia, PA, 2017, DOI: 10.1137/1.9781611974904. (Cited on page 52).

[46] Arne Jensen, Lecture notes on spectra and pseudospectra of matrices and operators, 2009,
     https://people.math.aau.dk/∼matarne/11-kaleidoscope2/notes2.pdf, Last accessed on 2024-
     03-15. (Cited on page 103).

[47] Sergei Kalmykov, Béla Nagy, and Vilmos Totik, Bernstein- and Markov-type inequalities, 2021,
     arXiv:2104.02348, DOI: 10.48550/arXiv.2104.02348. (Cited on pages 94 and 102).

[48] Iordanis Kerenidis and Anupam Prakash, Quantum recommendation systems, 8th Innova-
     tions in Theoretical Computer Science Conference (ITCS 2017), vol. 67, pp. 49:1–49:21, 2017,
     arXiv:1603.08675, DOI: 10.4230/LIPIcs.ITCS.2017.49. (Cited on page 5).

[49] Frederick W. King, Hilbert transforms, Encyclopedia of Mathematics and its Applications,
     vol. 1, Cambridge University Press, 2009, DOI: 10.1017/CBO9780511721458. (Cited on page
     24).

[50] Hari Krovi, Improved quantum algorithms for linear and nonlinear differential equations, Quan-
     tum 7 (2023), 913, arXiv:2202.01054, DOI: 10.22331/q-2023-02-02-913. (Cited on pages 7, 11,
     13, 18, 29, 30, 43, 85, 87, 91, 92, 93, 94, 99, and 100).

[51] Serge Lang, Complex analysis, vol. 103, Springer Science & Business Media, 2013, DOI:
     10.1007/978-1-4757-3083-8. (Cited on page 84).

[52] Joonho Lee, Dominic W. Berry, Craig Gidney, William J. Huggins, Jarrod R. McClean,
     Nathan Wiebe, and Ryan Babbush, Even more efficient quantum computations of chemistry
     through tensor hypercontraction, PRX Quantum 2 (2021), 030305, arXiv:2011.03494, DOI:
     10.1103/PRXQuantum.2.030305. (Cited on page 5).

[53] Randall J LeVeque, Finite difference methods for ordinary and partial differential equations:
     steady-state and time-dependent problems, Society for Industrial and Applied Mathematics,
     2007, DOI: 10.1137/1.9780898717839. (Cited on pages 93 and 99).

[54] Chi-Kwong Li, Lecture notes on numerical range, 2005, https://cklixx.people.wm.edu/nrnote.
     pdf, Last accessed on 2024-01-10. (Cited on page 100).

                                               110
[55] Lin Lin, Lecture notes on quantum algorithms for scientific computation,                2022,
     arXiv:2201.08309, DOI: 10.48550/arXiv.2201.08309. (Cited on page 5).
[56] Lin Lin and Yu Tong, Near-optimal ground state preparation, Quantum 4 (2020), 372,
     arXiv:2002.12508, DOI: 10.22331/q-2020-12-14-372. (Cited on pages 14, 69, 73, 74, and 77).
[57] Lin Lin and Yu Tong, Optimal polynomial based quantum eigenstate filtering with application to
     solving quantum linear systems, Quantum 4 (2020), 361, arXiv:1910.14596, DOI: 10.22331/q-
     2020-11-11-361. (Cited on page 5).
[58] Lin Lin and Yu Tong, Heisenberg-limited ground-state energy estimation for early fault-
     tolerant quantum computers, PRX Quantum 3 (2022), 010318, arXiv:2102.11340, DOI:
     10.1103/PRXQuantum.3.010318. (Cited on page 92).
[59] Seth Lloyd, Universal quantum simulators, Science 273 (1996), 1073–1078, DOI: 10.1126/sci-
     ence.273.5278.1073. (Cited on page 4).
[60] Guang Hao Low and Isaac L. Chuang, Hamiltonian simulation by uniform spectral amplifica-
     tion, 2017, arXiv:1707.05391, DOI: 10.48550/arXiv.1707.05391. (Cited on pages 22, 35, and
     75).
[61] Guang Hao Low and Isaac L. Chuang, Optimal Hamiltonian simulation by quantum signal pro-
     cessing, Physical Review Letters 118 (2017), 010501, arXiv:1606.02685, DOI: 10.1103/Phys-
     RevLett.118.010501. (Cited on pages 5, 13, 22, 69, 70, and 73).
[62] Guang Hao Low and Isaac L. Chuang, Hamiltonian simulation by qubitization, Quantum 3
     (2019), 163, arXiv:1610.06546, DOI: 10.22331/q-2019-07-12-163. (Cited on pages 6, 32, 69,
     and 70).
[63] Guang Hao Low and Yuan Su, Quantum eigenvalue processing, 2024 IEEE 65th Annual Sym-
     posium on Foundations of Computer Science (FOCS), pp. 1051–1062, 2024, arXiv:2401.06240,
     DOI: 10.1109/FOCS61266.2024.00070. (Cited on page 1).
[64] Guang Hao Low and Yuan Su, Quantum eigenvalue processing, SIAM Journal on Computing
     55 (2026), no. 1, 135–215, arXiv:2401.06240, DOI: 10.1137/24M1689363. (Cited on page 1).
[65] Guang Hao Low and Yuan Su, Quantum linear system algorithm with optimal queries to initial
     state preparation, Quantum 10 (2026), 2041, arXiv:2410.18178, DOI: 10.22331/q-2026-03-23-
     2041. (Cited on pages 8, 12, 34, 44, 54, 56, 58, 73, 77, 85, 86, 88, and 89).
[66] A. I. Markushevich, Theory of functions of a complex variable, vol. 296, American Mathemat-
     ical Society, 2005. (Cited on page 78).
[67] John M. Martyn, Zane M. Rossi, Andrew K. Tan, and Isaac L. Chuang, Grand unifi-
     cation of quantum algorithms, PRX Quantum 2 (2021), 040203, arXiv:2105.02859, DOI:
     10.1103/PRXQuantum.2.040203. (Cited on page 5).
[68] Sam McArdle and David P. Tew, Improving the accuracy of quantum computational chemistry
     using the transcorrelated method, 2020, arXiv:2006.11181, DOI: 10.48550/arXiv.2006.11181.
     (Cited on pages 5, 8, 13, and 25).
[69] Ashley Montanaro and Changpeng Shao, Quantum and classical query complexities of func-
     tions of matrices, Proceedings of the 56th Annual ACM Symposium on Theory of Computing,
     pp. 573–584, 2024, arXiv:2311.06999, DOI: 10.1145/3618260.3649665. (Cited on page 5).

                                               111
[70] I. Moret and P. Novati, The computation of functions of matrices by truncated Faber series, Nu-
     merical Functional Analysis and Optimization 22 (2001), no. 5-6, 697–719, DOI: 10.1081/NFA-
     100105314. (Cited on page 87).

[71] Mario Motta, Tanvi P. Gujarati, Julia E. Rice, Ashutosh Kumar, Conner Masteran, Joseph A.
     Latone, Eunseok Lee, Edward F. Valeev, and Tyler Y. Takeshita, Quantum simulation of
     electronic structure with a transcorrelated Hamiltonian: improved accuracy with a smaller
     footprint on the quantum computer, Physical Chemistry Chemical Physics 22 (2020), 24270–
     24281, arXiv:2006.02488, DOI: 10.1039/D0CP04106H. (Cited on page 8).

[72] Paolo Novati, A polynomial method based on Fejér points for the computation of functions
     of unsymmetric matrices, Applied Numerical Mathematics 44 (2003), no. 1, 201–224, DOI:
     10.1016/S0168-9274(02)00139-3. (Cited on pages 87 and 88).

[73] David Poulin and Pawel Wocjan, Preparing ground states of quantum many-body systems on
     a quantum computer, Physical Review Letters 102 (2009), 130503, arXiv:0809.2705, DOI:
     10.1103/PhysRevLett.102.130503. (Cited on page 14).

[74] Thomas Ransford and Felix√ L. Schwenninger, Remarks on the Crouzeix–Palencia proof that the
     numerical range is a (1 + 2)-spectral set, SIAM Journal on Matrix Analysis and Applications
     39 (2018), no. 1, 342–345, arXiv:1708.08633, DOI: 10.1137/17M1143757. (Cited on page 101).

[75] Steven Roman, Advanced linear algebra, vol. 135, Springer Science & Business Media, 2013,
     DOI: 10.1007/978-0-387-72831-5. (Cited on pages 25 and 30).

[76] Timothy T. Royston, An investigation into Crouzeix’s conjecture, Master’s thesis, California
     Polytechnic State University, 2022. (Cited on page 84).

[77] Yuval R. Sanders, Dominic W. Berry, Pedro C.S. Costa, Louis W. Tessler, Nathan Wiebe,
     Craig Gidney, Hartmut Neven, and Ryan Babbush, Compilation of fault-tolerant quantum
     heuristics for combinatorial optimization, PRX Quantum 1 (2020), 020312, arXiv:2007.07391,
     DOI: 10.1103/PRXQuantum.1.020312. (Cited on page 62).

[78] Yuval R. Sanders, Guang Hao Low, Artur Scherer, and Dominic W. Berry, Black-box
     quantum state preparation without arithmetic, Physical Review Letters 122 (2019), 020502,
     arXiv:1807.03206, DOI: 10.1103/PhysRevLett.122.020502. (Cited on page 42).

[79] Menahem Schiffer, Faber polynomials in the theory of univalent functions, Bulletin of the
     American Mathematical Society 54 (1948), no. 12, 503–517, DOI: 10.1090/S0002-9904-1948-
     09027-9. (Cited on page 79).

[80] Changpeng Shao, Computing eigenvalues of diagonalizable matrices in a quantum computer,
     2019, arXiv:1912.08015, DOI: 10.48550/arXiv.1912.08015. (Cited on page 9).

[81] Changpeng Shao and Jin-Peng Liu, Solving generalized eigenvalue problems by or-
     dinary differential equations on a quantum computer, 2020, arXiv:2010.15027, DOI:
     10.48550/arXiv.2010.15027. (Cited on page 9).

[82] Joel H. Shapiro, Notes on the numerical range, 2017, https://joelshapiro.org/Pubvit/
     Downloads/NumRangeNotes/numrange notes.pdf, Last accessed on 2024-01-10. (Cited on
     page 100).



                                                112
[83] V.V. Shende, S.S. Bullock, and I.L. Markov, Synthesis of quantum-logic circuits, IEEE Trans-
     actions on Computer-Aided Design of Integrated Circuits and Systems 25 (2006), no. 6, 1000–
     1010, arXiv:quant-ph/0406176, DOI: 10.1109/TCAD.2005.855930. (Cited on pages 33, 44, and
     58).
[84] Peter W. Shor, Polynomial-time algorithms for prime factorization and discrete logarithms
     on a quantum computer, SIAM Journal on Computing 26 (1997), 1484–1509, arXiv:quant-
     ph/9508027, DOI: 10.1137/S0097539795293172. (Cited on pages 4 and 5).
[85] P. K. Suetin and EV Pankratiev, Series of Faber polynomials, vol. 1, CRC Press, 1998. (Cited
     on pages 8, 15, 78, 79, and 80).
[86] Souichi Takahira, Asuka Ohashi, Tomohiro Sogabe, and Tsuyoshi S. Usuda, Quantum algo-
     rithm for matrix functions by Cauchy’s integral formula, Quantum Information and Compu-
     tation 20 (2020), 14–36, arXiv:2106.08075, DOI: 10.26421/QIC20.1-2-2. (Cited on pages 14
     and 91).
[87] Souichi Takahira, Asuka Ohashi, Tomohiro Sogabe, and Tsuyoshi S Usuda, Quantum algo-
     rithms based on the block-encoding framework for matrix functions by contour integrals, Quan-
     tum Information and Computation 22 (2022), no. 11&12, 965–979, arXiv:2106.08076, DOI:
     10.26421/QIC22.11-12-4. (Cited on pages 14 and 91).
[88] Terence Tao, Almost everywhere convergence of Fourier series, 2020, https://terrytao.
     wordpress.com/2020/05/14/247b-notes-4-almost-everywhere-convergence-of-fourier-series/,
     Last accessed on 2023-12-05. (Cited on page 25).
[89] Lloyd N. Trefethen, Approximation theory and approximation practice, Society for Industrial
     and Applied Mathematics, Philadelphia, 2019, DOI: 10.1137/1.9781611975949. (Cited on page
     21).
[90] Lloyd N. Trefethen and Mark Embree, Spectra and pseudospectra: The behavior of nonnormal
     matrices and operators, Princeton university press, 2005, DOI: 10.1515/9780691213101. (Cited
     on pages 17, 29, 92, 99, and 103).
[91] Adiyasuren Vandanjav and Batzorig Undrakh, On the numerical range of some weighted
     shift matrices and operators, Linear Algebra and its Applications 449 (2014), 76–88, DOI:
     10.1016/j.laa.2014.02.018. (Cited on pages 84 and 101).
[92] Martin Vetterli, Jelena Kovačević, and Vivek K Goyal, Foundations of signal processing, Cam-
     bridge University Press, 2014, DOI: 10.1017/CBO9781139839099. (Cited on page 22).
[93] Vera von Burg, Guang Hao Low, Thomas Häner, Damian S. Steiger, Markus Reiher, Mar-
     tin Roetteler, and Matthias Troyer, Quantum computing enhanced computational catalysis,
     Physical Review Research 3 (2021), 033055, arXiv:2007.14460, DOI: 10.1103/PhysRevRe-
     search.3.033055. (Cited on page 5).
[94] Kianna Wan, Mario Berta, and Earl T. Campbell, Randomized quantum algorithm for statis-
     tical phase estimation, Physical Review Letters 129 (2022), 030503, arXiv:2110.12071, DOI:
     10.1103/PhysRevLett.129.030503. (Cited on pages 22 and 75).
[95] Pei Yuan Wu and Hwa-Long Gau, Numerical Ranges of Operators and Matrices, 413–439,
     Springer Nature Switzerland, Cham, 2023, pp. 413–439, DOI: 10.1007/16618 2023 52. (Cited
     on page 100).

                                               113
[96] Theodore J. Yoder, Guang Hao Low, and Isaac L. Chuang, Fixed-point quantum search with
     an optimal number of queries, Physical Review Letters 113 (2014), 210501, arXiv:1409.3305,
     DOI: 10.1103/PhysRevLett.113.210501. (Cited on page 5).

[97] Xiao-Ming Zhang, Yukun Zhang, Wenhao He, and Xiao Yuan, Exponential quantum advan-
     tages for practical non-Hermitian eigenproblems, Physical Review Letters 135 (2025), 140601,
     arXiv:2401.12091, DOI: 10.1103/3n8f-k8pl. (Cited on page 5).

[98] Qi Zhao, You Zhou, Alexander F. Shaw, Tongyang Li, and Andrew M. Childs, Hamiltonian
     simulation with random inputs, Physical Review Letters 129 (2022), 270502, arXiv:2111.04773,
     DOI: 10.1103/PhysRevLett.129.270502. (Cited on pages 12 and 91).

[99] Marcin Zwierz, Carlos A. Pérez-Delgado, and Pieter Kok, General optimality of the Heisenberg
     limit for quantum metrology, Physical Review Letters 105 (2010), 180402, arXiv:1004.3944,
     DOI: 10.1103/PhysRevLett.105.180402. (Cited on pages 10 and 54).




                                               114

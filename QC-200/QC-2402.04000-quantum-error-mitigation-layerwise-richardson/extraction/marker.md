# Marker Extraction (Fallback via pdftotext -layout)

*Note: Marker (VikParuchuri/marker) was not available in this environment
(requires torch + heavy vision-transformer weights; not installed per the
"free endpoints only / no heavy install" constraint of this replication wave).
This extraction was produced via `pdftotext -layout` from the arXiv PDF as a
faithful text fallback. The full plain-text extraction of the paper follows.*

**Source:** `paper.pdf` — arXiv:2402.04000v3 (Russo & Mari, 21 Jan 2025) —
"Quantum error mitigation by layerwise Richardson extrapolation"

---

                                                             Quantum error mitigation by layerwise Richardson extrapolation

                                                                                       Vincent Russo1, ∗ and Andrea Mari1, 2
                                                                                                    1
                                                                                                      Unitary Fund
                                                       2
                                                           Physics Division, School of Science and Technology, Università di Camerino, 62032 Camerino, Italy
                                                              A widely used method for mitigating errors in noisy quantum computers is Richardson extrap-
                                                           olation, a technique in which the overall effect of noise on the estimation of quantum expectation
                                                           values is captured by a single parameter that, after being scaled to larger values, is eventually ex-
                                                           trapolated to the zero-noise limit. We generalize this approach by introducing layerwise Richardson
                                                           extrapolation (LRE), an error mitigation protocol in which the noise of different individual layers
                                                           (or larger chunks of the circuit) is amplified and the associated expectation values are linearly com-
                                                           bined to estimate the zero-noise limit. The coefficients of the linear combination are analytically
                                                           obtained from the theory of multivariate Lagrange interpolation. LRE leverages the flexible con-
                                                           figurational space of layerwise unitary folding, allowing for a more nuanced mitigation of errors by




arXiv:2402.04000v3 [quant-ph] 21 Jan 2025
                                                           treating the noise level of each layer of the quantum circuit as an independent variable. We provide
                                                           numerical simulations demonstrating scenarios where LRE achieves superior performance compared
                                                           to traditional (single-variable) Richardson extrapolation.


                                                               I.    INTRODUCTION                               to a single-variable polynomial interpolation of the noise-
                                                                                                                scaled expectation values.
                                               In recent years, the field of quantum technologies has              In this work, we generalize Richardson extrapolation
                                            witnessed extraordinary progress, especially in the evolu-          to a multivariate framework in which we consider mul-
                                            tion of noisy intermediate-scale quantum (NISQ) devices.            tiple independent noise parameters associated with the
                                            Despite their capacity to excel over classical devices in           different layers (or with different chunks) of the full cir-
                                            certain tasks [1–7], NISQ devices are notably hindered              cuit. We call this new approach layerwise Richardson ex-
                                            by substantial noise, adversely affecting their output.             trapolation (LRE), while we use the acronym RE for the
                                               As we await the advent of fault-tolerant devices [8], a          conventional approach based on single-variable Richard-
                                            significant field of exploration for addressing the preva-          son extrapolation. To generalize RE to the multivariate
                                            lent noise issues is quantum error mitigation (QEM) [9–             LRE technique, we need to address two sub-problems: (i)
                                            23]. QEM serves as an intermediate approach to fault                A way of scaling up the noise of specific layers, without
                                            tolerance that can be realized at present to overcome the           perturbing the rest of the circuit. (ii) A way of post-
                                            hurdle of noisy devices. There are a variety of QEM                 processing the information obtained from the (layerwise)
                                            techniques that are the subject of active research, for             noise-scaled circuits to infer the zero-noise limit.
                                            example, zero-noise extrapolation (ZNE) [10, 11, 13],                  A noise-scaling strategy that can be used to solve the
                                            probabilistic-error cancellation (PEC) [11, 12, 24, 25],            first sub-problem is layerwise folding [36, 37]: an ap-
                                            dynamical decoupling [26–29], and Clifford data regres-             proach that considers a quantum circuit as being com-
                                            sion [30, 31].                                                      prised of several layers and where a variable amount of
                                                                                                                folding [15, 35] can occur at any given layer of the circuit.
                                               In this work, we focus on ZNE, a technique that
                                                                                                                Layerwise folding has been used in [36, 37] as a circuit
                                            has been used in many quantum computing experiments
                                                                                                                debugging technique, for example, to assess what layers
                                            [13, 16, 18, 32–34] and that has shown strong perfor-
                                                                                                                in a quantum circuit are particularly susceptible to noise.
                                            mance despite the simplicity of its practical implemen-
                                                                                                                Instead, in this work, we are not interested in using lay-
                                            tation. For a given quantum circuit, the primary idea
                                                                                                                erwise folding as an error characterization method, but
                                            of ZNE contains two steps; intentionally scaling up the
                                                                                                                as an error mitigation tool.
                                            noise of the circuit and then extrapolating to the noiseless
                                            limit.                                                                 The second sub-problem that we need to solve is how
                                                                                                                to generalize Richardson extrapolation in a framework
                                               For the first step, there are several techniques one can
                                                                                                                in which the expectation value of an observable can be
                                            consider to intentionally increase the noise, one of which
                                                                                                                considered as a multivariate function of the noise levels
                                            is unitary folding [15, 35]; a process that increases the
                                                                                                                associated with different layers. We address this sub-
                                            length of the quantum circuit, and by proxy, the noise.
                                                                                                                problem by applying the mathematical theory of multi-
                                            The second step is achieved by fitting a curve to the
                                                                                                                variate Lagrange interpolation [38, 39], which allows us
                                            expectation values measured at different noise levels to
                                                                                                                to express the zero-noise limit as a linear combination
                                            extrapolate to the noiseless expectation value. One such
                                                                                                                of the noise-scaled expectation values, each one weighted
                                            method, Richardson extrapolation (RE) [11], corresponds
                                                                                                                with a suitable real coefficient which only depends on the
                                                                                                                noise scaling factors.
                                                                                                                   It is interesting to compare the characteristic features
                                                                                                                of LRE for two similar techniques: PEC and RE. Like
                                            ∗ vincent@unitary.fund
                                                                                                                PEC, LRE involves a linear combination of many cir-
                                                                                                                         2

cuits in which only some specific layers are changed, while                        A.       Noise scaling
the rest of the circuit is kept unmodified. Unlike PEC
but similar to RE, LRE does not necessitate full knowl-          In RE, one of the mechanisms that is often used to
edge of the noise model. This is because the generation       scale the noise is unitary folding [15, 35]. A more targeted
of modified circuits in LRE is deterministic and solely       way in which the noise can be scaled is to apply layerwise
depends on the choice of the noise scale factors. It is       folding, as proposed in, for instance, [36, 37]. Instead of
also worth noting that for the case of linear extrapola-      increasing the depth of the entire circuit considered as
tion, LRE reduces to the noise-scaling variant of the NOX     a single global entity, layerwise folding acts on specific
(noiseless output extrapolation) method described in the      layers of the circuit (see Figure 1).
Appendix of [40]. A further interesting connection is to         An n-qubit quantum circuit C may be represented as
the NEPEC (noise-extended probabilistic error cancella-       a series of ℓ layers. Each layer Lk for 1 ≤ k ≤ ℓ contains
tion) technique introduced in [41], in which noise scaling    one or more quantum gates acting concurrently on an
has been proposed as a way to build quasi-probability         n-qubit system
representations of individual gates (or layers) to be used
for probabilistic error cancellation. Our technique is also                      C = Lℓ Lℓ−1 · · · L2 L1 .             (1)
related to [42], in which ZNE has been proposed for mit-
igating a multi-parameter noise model.                        In what follows, we denote each term Lk as a layer. How-
                                                              ever, the full theory of LRE is equally applicable assum-
   In [42], however, the parameters are associated with       ing that each Lk represents a multi-layer chunk of the
different physical errors acting uniformly along the cir-     full circuit (see Section II C for more details).
cuit (e.g. the values of T1 and T2 for a qubit), noise          Consider a collection of N different scale factor vectors
scaling is obtained by running the same circuit on differ-
ent qubits, and the final extrapolation is obtained by a                         Λ = {λ1 , λ2 , . . . , λN },          (2)
numerical best fit. In this work instead, we tune the noise
level of different layers by using localized folding opera-   where each λi is a vector of ℓ scale factors that specifies
tions and without introducing additional qubits. More-        how the noise is scaled across different layers
over, instead of using a numerical best fit, we provide an                                        
                                                                                (i)  (i)       (i)     (i)
analytic expression for the zero-noise limit based on the              λi = λ1 , λ2 , . . . , λℓ , λk ≥ 1.           (3)
theory of Richardson extrapolation.
                                                              For a collection of scale factor vectors defined by Λ, we
   This article is organized as follows. In Section II, we    denote
formally define the LRE technique and describe the noise
scaling (Section II A) and extrapolation strategies (Sec-                     C Λ = {C λ1 , C λ2 , . . . , C λN }      (4)
tion II B). We also consider how one can apply LRE to
a circuit in chunks (Section II C) as well as the sam-        as the corresponding set of circuits. Each circuit in C Λ
pling overhead of LRE (Section II D). In Section III, we      is layerwise noise-scaled according to the corresponding
showcase some examples and numerical experiments us-          scale factor vector.
ing LRE, illustrating its practical advantages and limita-       While layerwise folding is our chosen method for scal-
tions. We conclude in Section IV with future directions       ing the noise, it is important to note that this approach is
and potential applications for the LRE technique.             not the only option. In principle, various methods can be
                                                              employed to selectively scale the noise of specific circuit
                                                              layers. For example, a promising alternative is given by
                                                              the pulse-stretching method [11, 13], assuming the possi-
                                                              bility of applying different stretchings to different layers.
                                                                                                           (i)
                                                                 For layerwise folding, each scale factor λk corresponds
         II.    LAYERWISE RICHARDSON                          to the k-th layer Lk of the circuit C and is defined as
               EXTRAPOLATION (LRE)
                                                                                      (i)             (i)
                                                                                    λk = 1 + 2mk .                     (5)
                                                                       (i)
   In this section we present the layerwise Richardson ex-    Here, mk is a non-negative integer representing the
trapolation (LRE) technique, for the mitigation of errors     number of times the k-th layer Lk is to be folded. The
acting on quantum circuits. Much like RE, it consists         folding operation [15, 35] for each layer Lk is expressed
of two major steps; noise scaling and extrapolation. For      as
noise scaling, in Section II A, we evaluate an expectation                                    m(i)
                                                                                   (i)
value at different vectors of scale factors via a layerwise
                                                                                       
                                                                                 λ              k
                                                                                Lk k = Lk L†k       Lk ,               (6)
folding approach. For extrapolation and post-processing
of these expectation values, covered in Section II B, we                (i)
                                                                       λ
make use of the mathematical theory of multivariate La-       where Lk k is the new k-th layer after the folding op-
grange interpolation.                                         eration. If Lk represents a chunk of the circuit that
                                                                                                                                        3

is itself composed of t elementary sub-layers Lk =                                            B.    Extrapolation
Gk,t · · · Gk,2 Gk,1 , unitary folding can be applied in dif-
ferent ways. One option, known as global folding [15],                     Once we have scaled the noise via the layerwise folding
corresponds to Equation (6). A common alternative op-                    approach discussed in Section II A and obtained a vec-
tion, known as local folding [15], is instead:                           tor of expectation values evaluated at different vectors
     (i)
                                                                         of scale factors as in Equation (9), we proceed to post-
    λ                    (i)                             (i)
  Lk k = (Gk,t G†k,t )mk Gk,t · · · (Gk,1 G†k,1 )mk Gk,1 .         (7)   process this raw data by a multivariate generalization of
                                                                         Richardson extrapolation.
                                                   (i)                     For a vector of scale factors λ = (λ1 , . . . , λℓ ), we define
Both methods scale the depth of Lk by λk ≥ 1 and are
                                                                         the basis of all monomial terms of ℓ variables of maximum
exactly equivalent when t = 1. For large t, one can apply
                                                                         degree d as M(λ, d). For instance, for λ = (λ1 , λ2 ) and
unitary folding partially or randomly [15, 35], such that
                    (i)                                                  d = 2, we have
the scale factor λk is not constrained to take the odd
integer values as implied by Equation (5). However, for                              M(λ, 2) = {1, λ1 , λ2 , λ21 , λ1 λ2 , λ22 }.     (10)
simplicity, in this work, we always assume odd integer
                                                                         In general, the number of monomial terms is given by
scale factors since they are always implementable for any                                                     
t. In this sense, each sub-layer Gk,j in the local folding                                               d+ℓ
scheme can be treated as an elementary unit, analogous                                  M ≡ |M(λ, d)| =          ,          (11)
                                                                                                           d
to how the entire layer Lk is treated in the global folding
scheme.                                                                  and we assume that the monomials are ordered with an
   For a given vector λi of scale factors, the resulting                 increasing total degree. For example, a typical choice is
circuit C λi is represented as                                           the graded lexicographic order [43]. This implies that the
                                                                         first element of the list of monomials is 1, i.e., the term
                        λ
                         (i)   (i)
                               λ        λ
                                         (i)   (i)
                                               λ                         of zero degree that survives when taking the zero-noise
              C λi = Lℓ ℓ Lℓ−1
                            ℓ−1
                                · · · L2 2 L1 1 .                  (8)   limit λ → 0, where 0 is the all-zero vector.
                                                                            For our purposes, typical values of the maximum de-
In this framework, the vector of scale factors λi explicitly             gree are d = 1 or d = 2, corresponding to a linear scaling
defines which layers of the circuit are to be folded and                 M = ℓ + 1 and a quadratic scaling M = (ℓ + 1)(ℓ + 2)/2
the number of times each specified layer is folded. A                    of the number of terms, respectively. More generally, for
depiction of the folding operation for an arbitrary circuit              a fixed extrapolation order d, the number of monomials
is shown in Figure 1.                                                    M scales polynomially with respect to ℓ since we have
                                                                                                     d
                                                                                                 1 Y
                                                                                         M=             (ℓ + i) = O(ℓd ).             (12)
                                                                                                 d! i=1

                                                                            We aim to interpolate a multivariate polynomial func-
                                                                         tion that captures the relationship between the vectors of
                                                                         scale factors and the expectation values as defined from
                                                                         Equation (9). Specifically, we model the dependence of
                                                                         the expectation value as a function of the noise scale fac-
Figure 1. An arbitrary quantum circuit consisting of three               tors as a generic polynomial of degree d
layers; L1 , L2 , and L3 . The circuit on the right is con-
structed according to a vector of noise scale factors λi =                                               M
                                                                                                         X
   (i)  (i) (i)
(λ1 , λ2 , λ3 ) that determines how much the depth of each                                ⟨O(λ)⟩ =             cj Mj (λ, d),          (13)
layer is scaled up by unitary folding (or by any other noise                                             j=1
scaling method which can act layerwise). Without noise, the
two circuits are equivalent. With noise, the circuit on the              where {cj } are real coefficients. We are particularly in-
right is subject to more errors. Moreover, noise is amplified            terested in extrapolating Equation (13) to the zero-noise
on some specific layers and less amplified (or unchanged) on             limit, that is
other layers.                                                                                             M
                                                                                                          X
                                                                                   OLRE ≡ ⟨O(0)⟩ =              cj Mj (0, d) = c1 .   (14)
  For each circuit in C Λ from Equation (4), one may                                                      j=1
compute the corresponding expectation value of a fixed
observable of interest O. Specifically, we denote all the                   Given the collection Λ of scale factor vectors, as defined
expectation values associated with C Λ as                                in Equation (2), we define the sample matrix
                                                                                                                       
                                                               T
                                                                                                 a1,1 a1,2 · · · a1,M
           z = (⟨O(λ1 )⟩, ⟨O(λ2 )⟩, . . . , ⟨O(λN )⟩)              (9)                          a2,1 a2,2 · · · a2,M 
                                                                                    A(Λ, d) =  .        .. . .      ..  ,       (15)
                                                                                                                       
where ⟨O(λi )⟩ is the expectation value of the observable                                       . .      .     .     . 
O, estimated from the execution of the circuit C λi .                                            aN,1 aN,2 · · · aN,M
                                                                                                                                       4


   Circuit                                                   Vectors of scale factors              LRE coefficients




                              Layerwise folding

                                                                                                  Zero-noise limit


            Folded circuits




                                          Quantum circuit layers


Figure 2. An overview of the LRE experimental workflow. As input, we consider an n-qubit quantum circuit consisting              of ℓ
layers or, equivalently, l circuit chunks. Given the parameter l and the extrapolation order d, we generate M = d+l
                                                                                                                          
                                                                                                                        d
                                                                                                                            linearly-
independent vectors of scale factors (see Equation (21) for a convenient generation pattern). In practice, for each vector of scale
factors, one can set most elements to 1 (no noise scaling) and assign larger values to just a few elements. From this, we perform
layerwise folding on the input circuit generating M different circuits, one for each vector of scale factors. Each generated circuit
is almost identical to the input one, except for a few layers that are folded to amplify their noise sensitivity. For each resulting
circuit (Equation (4)), we experimentally estimate the respective expectation value (Equation (9)). The linear combination
coefficients {ηj } can be computed straightforwardly from the multivariate Lagrange interpolation formula (Equation (20)) and,
remarkably, they only depend on the scale factor vectors. By taking a linear combination of the noise-scaled expectation values,
we obtain the error-mitigated result.


where each entry in the matrix is defined as                                  determinant is non-zero. This implies that the number
                                                                              N of different scale factor vectors is not arbitrary but it
                                   ai,j = Mj (λi , d).                (16)    must be equal to the number of monomials, i.e.,
As a notational convention, we often write Equation (15)
as just A, whenever it is clear what the values of Λ and                                 N =M       and    det (A(Λ, d)) ̸= 0.      (18)
d are. Each row of A corresponds to a specific scale
factor vector, while each column corresponds to a specific
monomial. The interpolation problem can be cast as a                          In practice, for a given number of layers ℓ and a given
linear system,                                                                degree d of the interpolating polynomial, the number of
                                                                              different noise scaling configurations and the number of
                                        Ac = z,                       (17)    different expectation values that one needs to measure is
where z is the known vector of noise-scaled expectation                       given by Equation (11). Note that assuming det(A) ̸= 0
values as defined in Equation (9) and c = (c1 , . . . , cM )T                 is not a strong limitation since, in the case of a zero (or
is the unknown vector of coefficients defined in Equa-                        close to zero) determinant, one can always change some
tion (13). In principle, solving for c, one can determine                     of the scale factor vectors in such a way to avoid an ill-
all the coefficients of the interpolating polynomial, which                   conditioned system of equations.
can be used to evaluate new domain points, including                             By a direct application of the theory of multivariate
the zero-noise limit (⟨O(0)⟩ = c1 ). However, if we are                       Lagrange interpolation (as shown in Appendix V B), we
only interested in the zero-noise limit, it is not necessary                  can obtain the zero-noise limit via the following linear
to evaluate the full vector of coefficients c. We will use                    combination of the noisy expectation values
the theory of Lagrange interpolation to obtain a simple
formula that directly provides the zero-noise limit.                                                      M
   To have a unique solution for the system of equations,
                                                                                                          X
                                                                                               OLRE =           ηi ⟨O(λi )⟩,        (19)
we assume that the sample matrix is square and that its                                                   i=1
                                                                                                                                               5

where the coefficients are given by                                 Note that only Step 6 of the above protocol involves
                                                                  the actual usage of a quantum computer, all the other
                              det (Mi )                           steps are just classical pre- or post-processing.
                       ηi =             ,                 (20)
                              det (A)

where Mi is the matrix obtained from A after replacing                         D.    Sampling overhead of LRE
the i-th row by the vector e1 = (1, 0, . . . , 0) consisting of
a 1 followed by zeros.
                                                                     The error-mitigated expectation value obtained from
                                                                  layerwise Richardson extrapolation is subject to statis-
     C.    Applying LRE to chunks of the circuit
                                                                  tical uncertainty. Each noisy expectation value in the
                                                                  right-hand side of Equation (19) must be measured with
                                                                  a finite number of shots and, therefore, each term will be
   As we anticipated in Section II A, if instead of decom-        subject to a statistical error (shot noise). After taking
posing the circuit into a sequence of elementary layers (of       the linear combination, the left-hand side of the equa-
depth one) we split the circuit into chunks of arbitrary          tion will be subject to statistical uncertainty due to the
depth, the whole theory of LRE is equally applicable. In-         propagation of the statistical error of each term on the
deed, in the theoretical derivation developed in the pre-         right-hand side.
vious sections, we never had to invoke any assumption                For a fixed target of statistical error, the total number
on the actual depth of each term Lk in Equation (1).              of shots stot required to evaluate Equation (19) is larger
   In practice, this means that the total number of chunks        than the number of shots su required to directly estimate
l in Equation (1) is an arbitrary hyperparameter of LRE           the unmitigated expectation value ⟨O(λ)⟩|λ=1 . The sam-
that we are free to choose at our convenience. This flex-         pling overhead required to apply LRE is captured by the
ibility allows us to interpolate from l = 1 corresponding         ratio stot /su . Assuming all the noisy expectation values
to traditional (single-chunk) RE, up to l = lmax , where          of Equation (19) have equal variance and that they are
lmax is the maximum number of elementary layers of the            measured with the same number of shots stot /M , it is
circuit.                                                          easy to show [9] that:
   Operationally, given a circuit C of depth lmax and a
target observable O, the implementation of LRE corre-                                                M
                                                                                                                      ! 21
sponds to the following protocol (see also Figure 2):                    stot                        X                                stot
                                                                   c̃ :=      = M γ̃ 2 ,   γ̃ :=            |ηi | 2
                                                                                                                             , si =        . (22)
                                                                          su                                                          M
   1. Choose the hyperparameters: the extrapolation or-                                              i=1
      der d, the number of splittings l ≤ lmax , and the
                                                                    However, the sampling overhead can be reduced by us-
      minimum noise scaling gap ∆. By default, use
                                                                  ing more shots on the terms that are more “important”
      ∆ = 2 (minimum gap allowed by unitary folding).
                                                                  in the linear combination of Equation (19). For a fixed
      See Section II D for more details on hyperparame-
                                                                  total budget of shots stot , it is more convenient to in-
      ters.
                                                                  vest si ∝ |ηj | shots when estimating each noise-scaled
   2. Compute the number M of degrees of freedom using            expectation value ⟨O(λi )⟩. In this case, we have [9, 11]:
      Equation (11).
                                                                                                   M
                                                                            stot                   X                          stot |ηi |
   3. Choose M different vectors of scale factors                    c :=        = γ2,     γ :=          |ηi |,       si =               .   (23)
                                                                             su                                                  γ
      λ1 , λ2 , . . . , λM . A simple choice is the following                                      i=1


             λi = 1 + mi ∆,      i = 1, 2, . . . , M,     (21)       The fact that the one norm γ of the linear combina-
                                                                  tion of coefficients in (19) is related to the error mit-
      where 1 = (1, 1, . . . ) and {mi } are all the vectors      igation overhead is well-known in the error mitigation
      of l non-negative integers with ∥mi ∥1 ≤ d.                 literature [9, 11, 44], and it is a consequence of Hoeffd-
                                                                  ing’s inequality applied within the context of probabilis-
   4. Evaluate the corresponding M real coefficients              tic Monte-Carlo algorithms. Here we have just confirmed
      η1 , η2 , . . . , ηM using Equation (20).                   that the same result also holds for deterministic LRE, as-
                                                                  suming that each expectation value in (19) is measured
   5. Split C into l chunks and apply layerwise folding
                                                                  with the appropriate number of shots. As a direct conse-
      as defined in Equations (5-8), generating M noise-
                                                                  quence of the Cauchy-Schwartz inequality (see e.g. [9]),
      scaled circuits C λ1 , C λ2 , . . . , C λM .
                                                                  we have c̃ > c, meaning that Equation (23) is the ap-
   6. Evaluate the corresponding M expectation val-               propriate figure of merit for the optimal sampling cost.
      ues ⟨O(λ1 )⟩, ⟨O(λ2 )⟩, . . . , ⟨O(λM )⟩ on the quan-       On the other hand, in real experiments, it can be more
      tum computer.                                               practical to estimate noisy expectation values with the
                                                                  same number of shots stot /M for each noise-scaled cir-
   7. Compute the error-mitigated result using OLRE =             cuit. In this case, c̃ is a more appropriate estimate of the
      PM
        i=1 ηi ⟨O(λi )⟩.                                          sampling cost.
                                                                                                                                                                                    6



                                          d = 2, ∆ = 3                                                                                                              d = 2, l = 10
                                          d = 1, ∆ = 3                                                                                                              d = 1, l = 10




   Error mitigation overhead c                                                          Error mitigation overhead c
                                 102
                                                                                                                      102




                                 101                                                                                  101




                                           2          4             6            8                                            2    4   6     8      10    12   14     16      18
                                                Number of layers (or chunks) l                                                             Noise scaling gap ∆

Figure 3. Sampling overhead of layerwise Richardson extrap-                          Figure 4. Sampling overhead of layerwise Richardson extrap-
olation for quadratic (d = 2) and linear (d = 1) interpolation                       olation for quadratic (d = 2) and linear (d = 1) interpolation
as a function of the number of layers (or circuit chunks). The                       as a function of the minimum gap between scale factors ∆.
overhead is estimated according to Equation (23) assuming                            For both curves, we assume the same number of layers (or
the specific choice of scale factors given in Equation (21), with                    circuit chunks) l = 10. The vectors of scale factors are chosen
∆ = 2 (the minimum gap achievable via layerwise folding).                            according to Equation (21).
The noise of each circuit chunk is scaled by local folding as
defined in Equation (7).

                                                                                                                            III.   NUMERICAL EXPERIMENTS
   In Figure 3 we plot c as a function of the number of
layers (or circuit chunks) l and for different values of the                            In the previous section, we presented the theory of lay-
extrapolation order d. In this figure, we keep fixed the                             erwise Richardson extrapolation. In this section, we test
minimum gap between scale factors ∆ = 2, correspond-                                 the technique with several numerical experiments to un-
ing to the minimum gap of noise scaling achievable with                              derstand its practical advantages and its limitations. In
folding operations.                                                                  particular, we focus on a systematic comparison between
                                                                                     LRE and traditional single-variable Richardson extrapo-
                                                                                     lation (RE).
                                 1.    Methods for reducing the sampling overhead      A convenient choice of circuits for benchmarking er-
                                                                                     ror mitigation strategies are those which, without noise,
   In Figure 4, we fix l = 10 and show the dependence                                restore all the qubits to the initial state |00 . . .⟩. In this
of the sampling overhead as a function of the minimum                                case, by taking as a target observable the projector on the
gap between scale factors ∆ = 2, 4, 6, . . . corresponding                           zero state, i.e. O = |00 . . .⟩⟨00 . . . |, the ideal expectation
to a gap in the number of folding operations equal to                                value is always equal to 1 for a noiseless quantum com-
1, 2, 3, . . . , respectively (see Equation (5)). We observe                         puter. For a noisy backend instead, we can quantify the
that using a large gap between scale factors reduces the                             performance of different mitigation strategies by check-
sampling cost. On the other hand, high values of noise                               ing how close their associated predictions are to the ideal
scaling can increase the bias of the polynomial extrapola-                           value of 1. For all of the quantum circuits simulated in
tion, since the noisy expectation value is sampled further                           this section, we assume a local amplitude damping noise
away from the zero-noise limit. Therefore, by altering ∆                             model as described in Appendix V A.
one can change the variance-bias tradeoff of the error-                                 In our analysis (which is depicted in Figures 6, 7, 8, 9,
mitigated result.                                                                    10, and 12), we always fix the same total budget of shots
   Another simple way of reducing the overhead is by                                 stot that must be used by each error mitigation strategy
splitting the full circuit into a smaller number of chunks                           (trivial unmitigated, LRE, RE, etc.). This means that
l, where each chunk contains multiple elementary layers.                             if an error mitigation technique requires running M cir-
From Figure 3, it is clear that using a small value of l is                          cuits, the total budget of shots is optimally split among
a direct way of reducing the sampling cost.                                          the M circuits such that the PMtotal sum of circuit execu-
   In practice, even for very deep circuits, we can always                           tions is kept constant, i.e. i=1 si = stot . For both LRE
keep the overhead of LRE under control by setting an                                 and RE, we use the optimal splitting si defined in Equa-
upper bound to the number of splittings l or by increas-                             tion (23) (recalling that RE is a special case of LRE with
ing ∆, at the cost of increasing the estimation bias (see                            l = 1). If not explicitly specified, we fix a total budget of
Sections III A 4 and III A 5 for numerical examples).                                stot = 106 shots.
                                                                                                                                                           7

   A.     Benchmarking LRE with GHZ-like circuits

                                                                                            1.0
  The first type of benchmark circuit that we use to test
LRE is based on the concatenation of a GHZ circuit fol-                                     0.9
lowed by its inverse, as shown in Figure 5.                                                 0.8




                                                                        Expectation value
                                                                                            0.7
         |0⟩1     H                  ···               H
                                                                                            0.6
         |0⟩2                        ···
                                                                                            0.5
          |0⟩3                       ···                                                                Ideal value
           ···                       ···                                                    0.4         LRE
                                                                                                        Unmitigated
        |0⟩n−1                       ···                                                    0.3         RE
         |0⟩n                        ···                                                          4        6          8     10        12     14   16
                                                                                                                      Number of layers `
Figure 5. A GHZ-like benchmarking circuit composed of an
n-qubit GHZ circuit followed by its inverse. By construction,        Figure 6.            Expectation value of the observable O =
the expectation value of O = |00 . . .⟩⟨00 . . . | evaluated on an   |00 . . .⟩⟨00 . . . | estimated with different error mitigation
ideal noiseless device is equal to 1.                                strategies for a GHZ-like circuit as defined in Figure 5. Each
                                                                     data point is averaged over 10 trials. For each trial, a to-
  The intermediate states during the execution of a                  tal budget of stot = 106 shots is used. Error bars for each
                                                                     data point represent the standard deviation over the 10 in-
GHZ-like circuit are highly entangled and, therefore,
                                                                     dependent trials. For all the data points considered in this
highly sensitive to environmental noise and decoherence.             example, layerwise Richardson extrapolation (LRE) is more
For this reason, they provide a good playground for test-            accurate than traditional single-variable Richardson extrapo-
ing the efficacy of LRE on structured, entangling circuits.          lation (RE) and direct unmitigated estimation.

                                                                        Depth                         Unmitigated          RE        LRE     Improvement
                  1.    Vary over number of layers                        2                             0.2078           0.0306     0.0174      75.41%
                                                                          3                             0.3483           0.1107     0.0390     183.75%
   In Figure 6 and Table I, we compare the performance                    4                             0.4599           0.2110     0.0662     218.79%
of LRE relative to RE and the unmitigated case as the                     5                             0.5495           0.3121     0.0906     244.34%
number of layers l increases (the number of qubits in-                    6                             0.6206           0.4058     0.1640     147.40%
                                                                          7                             0.6789           0.4856     0.2130     127.98%
creases as well since l = 2n).
                                                                          8                             0.7261           0.5546     0.2607     112.76%
   Increasing the size of a GHZ circuit elevates its com-
plexity and susceptibility to errors. As expected, the               Table I. Table of mean absolute estimation errors for each
estimation error increases with l for all the results but,           data point reported in Figure 6. The last column provides a
for each l, the expectation value estimated with LRE is              percentage of improvement for the performance of layerwise
closer to the ideal value. Error bars are evaluated by re-           Richardson extrapolation (LRE) over single-variable Richard-
peating the same experiment for 10 trials and computing              son extrapolation (RE). We observe that the performance im-
the standard deviation of the results. We observe that               provement is significant even if the noise model (amplitude
LRE results are subject to higher statistical uncertainty.           damping) is fixed and uniform along the circuit. This fact
This is expected from the overhead analysis presented in             can be explained by noticing that, due to the specific struc-
                                                                     ture of the circuit, noise has different impacts on the final
Section II D and from Figure 3: the error mitigation cost
                                                                     expectation value depending on which specific layer it acts
c of LRE increases with the number of layers (or circuit             on. On the contrary, RE is completely insensitive to such
chunks) and, for a fixed budget of shots stot = 106 , this           fine-grained resolution of the noise impact.
implies a proportional increase of the statistical variance.
Note however that, even taking into account error bars,
the overall estimation error of LRE is smaller than RE               the bias of both LRE and RE decreases with the extrap-
due to a strong reduction of the estimation bias.                    olation order d. However, statistical noise increases (ex-
                                                                     ponentially) with d. In practice, for real-world use cases,
                                                                     we expect LRE and RE to be useful for 1 ≤ d ≤ 3, since
                 2.    Vary over extrapolation order                 large values of d are subject to the instabilities typical of
                                                                     high-order polynomial interpolation.
   In Figure 7, we explore how the performance of LRE                   For applications where high fidelity is paramount, and
and RE varies with the extrapolation order d, i.e., the              resource constraints are less stringent, high extrapola-
degree of the interpolating polynomial. Specifically, for            tion orders (e.g. quadratic or cubic) may be preferable.
both LRE and RE, we compare the results obtained via                 Conversely, for more resource-constrained environments
linear, quadratic, and cubic extrapolation. As expected,             or where moderate improvements in fidelity are sufficient,
                                                                                                                                                          8

                                                                                From our previous analysis of the sampling overhead
                                                                             of LRE, we know that increasing the gap between noise
                                   Ideal value                               scale factors reduces the sampling cost (see Figure 4).
                       1.1         Unmitigated
                                   LRE                                       Equivalently, for a fixed number of shots stot , we ex-
                       1.0
                                   RE                                        pect a reduction of statistical noise for larger values of



   Expectation value
                                                                             ∆. This is indeed what we observe for LRE in Figure 9,
                       0.9                                                   where error bars get smaller for increasing ∆. A similar
                                                                             reduction is also present for single-variable RE but, error
                       0.8                                                   bars are too small to be visible in the plot. In Figure 9 we
                                                                             also see the drawback of using a large gap between noise
                       0.7
                                                                             scale factors: the bias of the associated extrapolation in-
                       0.6


                              1                           2              3
                                                 Extrapolation order d
                                                                                                    1.2                                     Ideal value
                                                                                                                                            LRE
Figure 7.             Expectation value estimated with layerwise                                                                            Unmitigated
Richardson extrapolation (LRE) and single-variable Richard-                                                                                 RE
                                                                                                    1.0




                                                                                Expectation value
son extrapolation (RE) for different values of the extrapo-
lation degree d (linear, quadratic, cubic). As a benchmark
circuit we used a 4-qubit GHZ-like circuit having the struc-                                        0.8
ture shown in Figure 5 and as observable we used O =
|00 . . .⟩⟨00 . . . |. The error bars are obtained by calculating
the standard deviation over 10 trials. For each trial, a fixed                                      0.6
budget of stot = 106 shots is used.

                                                                                                    0.4

low extrapolation orders (e.g. linear) might be more suit-                                                104       105             106             107
able.                                                                                                                Shots budget stot

                                                                             Figure 8.            Expectation value of the observable O =
                                                                             |00 . . .⟩⟨00 . . . | estimated with different error mitigation
                                    3.   Vary over number of shots           strategies for a 6-qubit GHZ-like circuit as defined in Fig-
                                                                             ure 5. Each data point is averaged over 10 trials. For each
   In the previous simulations, for each expectation value                   trial, we use a budget of shots as reported in the horizontal
estimation, we used a fixed budget of stot = 106 shots                       axis. The error bars in each data point illustrate the standard
                                                                             deviation over the 10 trials.
(total number of circuit executions). We now analyze
what happens if we vary stot . The results are depicted
in Figure 8.
   Increasing the number of shots induces a reduction of
                                                                                                    1.0                                     Ideal value
the statistical variance for any estimation strategy (un-                                                                                   Unmitigated
mitigated, LRE, RE). However, we observe that LRE is                                                0.9                                     LRE
much more sensitive to statistical noise and, as a conse-                                           0.8
                                                                                                                                            RE




                                                                                Expectation value
quence, to the number of shots. For a small number of
shots, the statistical variance of LRE is too large to pro-                                         0.7
duce a reliable estimation. In this regime, one could try                                           0.6
to reduce the overhead of LRE by reducing the number
of chunks l or by increasing the gap ∆ between scale fac-                                           0.5
tors. As the number of shots increases, the performance                                             0.4
of LRE stabilizes, yielding more consistent and reliable
results.                                                                                            0.3

                                                                                                          2     4            6          8           10
                                                                                                                    Noise scaling gap ∆

                             4.   Vary over the gap between scale factors
                                                                             Figure 9.            Expectation value of the observable O =
                                                                             |00 . . .⟩⟨00 . . . | estimated with increasing gap ∆ between scale
   This section delves into the impact of increasing the                     factors, for an 8-qubit GHZ-like circuit. We assume a fixed
minimum gap ∆ between noise scale factors, as a way                          and limited number of shots stot = 105 for any estimation
of reducing statistical noise at the cost of increasing the                  strategy. The error bars are obtained by calculating the stan-
estimation bias. The results are presented in Figure 9.                      dard deviation over the 10 trials.
                                                                                                                                           9

creases due to stronger noise amplification. For practical                        tical noise for large l, as expected. The overall interpre-
scenarios, we expect that the net effect of increasing ∆                          tation of Figure 10 is that, if we can afford the sampling
is typically not a convenient strategy when using tradi-                          overhead, it is always convenient to increase l. However,
tional RE, but it can help when using LRE due to its                              we also expect that for deeper circuits (e.g. lmax > 100)
larger sampling cost.                                                             the complexity and the sampling cost of applying LRE
                                                                                  at the level of single layers may become too large such
                                                                                  that applying LRE on a smaller number of multi-layer
                             5.   Vary over the number of circuit chunks          chunks is a more pragmatic solution.

   Finally, we explore the influence of varying the number
of circuit chunks l on the estimation accuracy of LRE.                             B.   Benchmarking LRE with randomized circuits
As discussed in Section II C, we are not forced to apply
LRE to depth-1 layers, but we can apply it to multi-                                 In this subsection, we use a different benchmark circuit
layer chunks of the input circuit. This implies that we                           to test the error mitigation performance of LRE. Instead
are free to split the circuit into an arbitrary number l =                        of the GHZ-like circuit used in the previous examples, we
1, 2, . . . , lmax of chunks, where the upper limit lmax is the                   use randomized circuits having the following structure:
total number of depth-1 layers.
                                                                                                             −1
                                                                                                        C = Crand Crand ,               (24)

                                                                                  where Crand is a random circuit obtained via a random-
                       1.0                                          Ideal value   ized application of single-qubit gates (H, X, Y, Z, S, T )
                                                                    Unmitigated
                       0.9                                          RE
                                                                                  and CNOT gates. An instance of Crand is shown in Fig-
                                                                    LRE           ure 11. To increase the amount of entanglement dur-
                       0.8




   Expectation value
                                                                                  ing the circuit execution, we assign a high probabilistic
                       0.7                                                        weighting to CNOT gates (pCNOT = 0.9), thus ensuring
                                                                                  a high density of CNOT gates in the benchmark circuits.
                       0.6

                       0.5                                                                       |0⟩1   H
                       0.4                                                                       |0⟩2
                       0.3                                                                       |0⟩3        Y
                              1     3     5      7     9     11    13    15 16
                                                                                                 |0⟩4
                                              Number of chunks l

Figure 10.            Expectation value of the observable O =                     Figure 11. An example of a randomly generated 4-qubit cir-
|00 . . .⟩⟨00 . . . | evaluated via layerwise Richardson extrapola-               cuit Crand , with high CNOT density. Note that the actual
tion (LRE) as a function of the number of chunks into which                                                             −1
                                                                                  circuit used to benchmark LRE is C = Crand Crand .
the input circuit is split (as proposed in Section II C). As a
benchmark circuit, we use an 8-qubit GHZ-like circuit. The
blue line represents the unmitigated expectation value, the                          Unlike GHZ-like circuits in which the depth is implied
orange line depicts the result of applying single-variable RE,                    by the number of qubits, for the randomized circuits con-
and the green triangles show the results after applying LRE.                      sidered in this subsection, we are free to independently
As expected, LRE reduces to RE for l = 1. Error bars report                       vary the number of qubits and the number of layers. This
the standard deviation over 10 trials. For each trial, a fixed                    freedom allows us to explore the performance of LRE
budget of stot = 106 shots is used.                                               when varying the number of qubits (at constant depth).
                                                                                     Figure 12 presents a comparative analysis of the er-
   In Figure 10, we apply LRE to an 8-qubit GHZ-like                              ror mitigation performance when varying the number of
circuit assuming a splitting of the circuit into a different                      qubits. The plot aggregates results obtained across 10
number of chunks. In practice, for each l, we split the                           randomly generated circuits. The results are qualita-
circuit into l chunks of approximately equal depth (up to                         tively similar to the GHZ-like case reported in Figure 6,
a rounding error of at most a single layer). Afterward, we                        in the sense that LRE outperforms both single-variable
apply LRE in the same way as in the previous examples                             RE and the trivial unmitigated estimation. However, we
but, instead of associating a noise scale factor to each                          also notice an important difference: error bars do not
depth-1 layer, we associate a scale factor to each chunk.                         grow when increasing the number of qubits. This is a
For each circuit chunk, we use local folding as defined in                        characteristic feature of Richardson extrapolation (both
Equation (7) (also employed for RE).                                              LRE and RE), for which the sampling overhead only de-
   By construction, LRE reduces to RE for l = 1. For                              pends on the choice of noise scale factors. This implies
larger values of l, we observe a significant reduction of                         that the overhead of LRE depends only on the depth l
the bias for LRE. We also observe an increase in statis-                          (or number of circuit chunks) but not on the number of
                                                                                                                                  10

qubits. Even if the statistical variance is constant con-                    The new technique proposed in this work opens up
cerning the number of qubits, the bias of all estimation                  avenues for further research. In our examples, we consid-
strategies (LRE, RE, unmitigated) gets larger for wider                   ered numerical experiments based on a simple amplitude-
circuits.                                                                 damping noise model. It would be interesting to nu-
                                                                          merically investigate other noise models or, even bet-
                                                                          ter, test LRE on real hardware. An aspect worth
                                       IV.      DISCUSSION                exploring is the design of suitable calibration experi-
                                                                          ments [25, 36, 37, 40, 45] to estimate the noise levels
   We introduced layerwise Richardson extrapolation                       of different layers or to determine the optimal hyperpa-
(LRE), an error mitigation technique inspired by                          rameters of the LRE protocol, given a specific backend.
conventional (single-variable) Richardson extrapolation                   For example, one could run calibration experiments to
(RE) [11–13] but generalized to a framework in which                      optimize the noise scaling gap ∆, the number of circuit
the errors acting on different layers of a circuit can be                 splittings l, and the extrapolation order d.
amplified independently. We then presented several nu-                       An interesting analysis would be an experimental com-
merical experiments in which we compared LRE against                      parison between LRE and PEC [11, 12]. In theory, PEC
conventional RE and direct unmitigated estimation.                        can provide a more tailored error mitigation, since it is
   Our findings suggest that LRE can be a convenient                      a noise-aware technique while LRE is noise-agnostic. In
technique for practical applications since it presents sev-               practice, however, it is not obvious what technique is
eral advantages (low bias, flexible sampling cost, noise-                 more competitive in a real-world scenario [32]. PEC re-
model agnostic). The main limitations of LRE are its                      quires many noise characterization experiments [25, 40]
statistical uncertainty (higher than RE) and the require-                 that are known to be complex, costly, and subject to im-
ment of running a significant number of different circuits                perfections which have a strong impact on the quality of
(similar to PEC [11, 12]). We also explored different ways                the final result. LRE is instead simpler and perhaps more
of reducing the sampling cost, such as increasing the gap                 robust to imperfections since, by construction, the exe-
between scale factors or reducing the number of circuit                   cuted circuits are generated according to a noise-agnostic
splittings, that can be useful for controlling the balance                and deterministic protocol.
between error mitigation bias and sampling cost in large-                    Inspired by the PEC protocol, a future direction worth
scale experiments. From a theoretical perspective, LRE                    exploring is the probabilistic implementation of LRE.
also provides a general multivariate formalism in which                   Rather than executing all the M circuits necessary for
previous techniques are recovered as special limits. For                  computing the sum in Equation (19), a Monte Carlo
example, LRE reduces to conventional RE for l = 1 and                     method employing importance sampling could be uti-
to the noise-scaling version of the NOX protocol [40] for                 lized. This approach would selectively and probabilis-
d = 1.                                                                    tically evaluate only a subset of the terms in the full sum
                                                                          and could potentially extend the applicability of LRE to
                                                                          more layers l and to higher orders d.

                       1.0

                                                                                          CODE AVAILABILITY
                       0.8




   Expectation value
                                                                            Software that implements the LRE method along with
                       0.6                                                the code that is used to generate the data and plots in
                                                                          this work is available in [46].
                       0.4
                                 Ideal value
                                 Unmitigated
                       0.2       RE                                                      ACKNOWLEDGMENTS
                                 LRE

                             2           3           4            5   6
                                               Number of qubits
                                                                            VR acknowledges Nate T. Stemen and Nathan
                                                                          Shammah for insightful discussions as well as William J.
Figure 12.           Expectation value of the observable O =              Zeng for suggesting the idea of applying layerwise fold-
|00 . . .⟩⟨00 . . . | estimated with different error mitigation           ing as a tool for error mitigation. This work was sup-
strategies for a randomized circuit as defined in Equation (24)           ported by the U.S. Department of Energy, Office of Sci-
having total depth lmax = 4. Each data point is averaged over             ence, Office of Advanced Scientific Computing Research,
10 different random instances of the benchmark circuit. Error             Accelerated Research in Quantum Computing under
bars for each data point represent the standard deviation over            Award Numbers DE-SC0020266 and DE-SC0020316 as
the 10 random instances. For each circuit, a total budget of              well as by IBM under Sponsored Research Agreement
stot = 106 shots is used.                                                 No. W1975810.
                                                                                                                             11




 [1] F. Arute, K. Arya, R. Babbush, D. Bacon, J. C.              [16] R. LaRose, A. Mari, S. Kaiser, P. J. Karalekas, A. A.
     Bardin, R. Barends, R. Biswas, S. Boixo, F. G. Brandao,          Alves, P. Czarnik, M. El Mandouh, M. H. Gordon,
     D. A. Buell, et al., “Quantum supremacy using a pro-             Y. Hindy, A. Robertson, et al., “Mitiq: A software pack-
     grammable superconducting processor,” Nature, vol. 574,          age for error mitigation on noisy quantum computers,”
     no. 7779, pp. 505–510, 2019.                                     Quantum, vol. 6, p. 774, 2022.
 [2] H.-S. Zhong, H. Wang, Y.-H. Deng, M.-C. Chen, L.-           [17] S. Endo, Z. Cai, S. C. Benjamin, and X. Yuan, “Hybrid
     C. Peng, Y.-H. Luo, J. Qin, D. Wu, X. Ding, Y. Hu,               quantum-classical algorithms and quantum error mitiga-
     et al., “Quantum computational advantage using pho-              tion,” Journal of the Physical Society of Japan, vol. 90,
     tons,” Science, vol. 370, no. 6523, pp. 1460–1463, 2020.         no. 3, p. 032001, 2021.
 [3] C. Neill, P. Roushan, K. Kechedzhi, S. Boixo, S. V.         [18] Y. Kim, C. J. Wood, T. J. Yoder, S. T. Merkel, J. M.
     Isakov, V. Smelyanskiy, A. Megrant, B. Chiaro,                   Gambetta, K. Temme, and A. Kandala, “Scalable error
     A. Dunsworth, K. Arya, et al., “A blueprint for                  mitigation for noisy quantum circuits produces competi-
     demonstrating quantum supremacy with superconduct-               tive expectation values,” Nature Physics, pp. 1–8, 2023.
     ing qubits,” Science, vol. 360, no. 6385, pp. 195–199,      [19] B. Koczor, “Exponential error suppression for near-term
     2018.                                                            quantum devices,” Physical Review X, vol. 11, no. 3,
 [4] L. S. Madsen, F. Laudenbach, M. F. Askarani, F. Ror-             p. 031057, 2021.
     tais, T. Vincent, J. F. Bulmer, F. M. Miatto, L. Neuhaus,   [20] A. He, B. Nachman, W. A. de Jong, and C. W. Bauer,
     L. G. Helt, M. J. Collins, et al., “Quantum computa-             “Zero-noise extrapolation for quantum-gate error mit-
     tional advantage with a programmable photonic proces-            igation with identity insertions,” Physical Review A,
     sor,” Nature, vol. 606, no. 7912, pp. 75–81, 2022.               vol. 102, no. 1, p. 012426, 2020.
 [5] Y. Wu, W.-S. Bao, S. Cao, F. Chen, M.-C. Chen,              [21] W. J. Huggins, S. McArdle, T. E. O’Brien, J. Lee, N. C.
     X. Chen, T.-H. Chung, H. Deng, Y. Du, D. Fan, et al.,            Rubin, S. Boixo, K. B. Whaley, R. Babbush, and J. R.
     “Strong quantum computational advantage using a su-              McClean, “Virtual distillation for quantum error mitiga-
     perconducting quantum processor,” Physical review let-           tion,” Physical Review X, vol. 11, no. 4, p. 041036, 2021.
     ters, vol. 127, no. 18, p. 180501, 2021.                    [22] V. R. Pascuzzi, A. He, C. W. Bauer, W. A. De Jong, and
 [6] S. Ebadi, T. T. Wang, H. Levine, A. Keesling, G. Se-             B. Nachman, “Computationally efficient zero-noise ex-
     meghini, A. Omran, D. Bluvstein, R. Samajdar, H. Pich-           trapolation for quantum-gate-error mitigation,” Physical
     ler, W. W. Ho, et al., “Quantum phases of matter on              Review A, vol. 105, no. 4, p. 042406, 2022.
     a 256-atom programmable quantum simulator,” Nature,         [23] C. Song, J. Cui, H. Wang, J. Hao, H. Feng, and Y. Li,
     vol. 595, no. 7866, pp. 227–232, 2021.                           “Quantum computation with universal error mitigation
 [7] A. J. Daley, I. Bloch, C. Kokail, S. Flannigan, N. Pear-         on a superconducting quantum processor,” Science ad-
     son, M. Troyer, and P. Zoller, “Practical quantum advan-         vances, vol. 5, no. 9, p. eaaw5686, 2019.
     tage in quantum simulation,” Nature, vol. 607, no. 7920,    [24] S. Zhang, Y. Lu, K. Zhang, W. Chen, Y. Li, J.-N. Zhang,
     pp. 667–676, 2022.                                               and K. Kim, “Error-mitigated quantum gates exceeding
 [8] J. Preskill, “Quantum computing in the NISQ era and              physical fidelities in a trapped-ion system,” Nature com-
     beyond,” Quantum, vol. 2, p. 79, 2018.                           munications, vol. 11, no. 1, p. 587, 2020.
 [9] Z. Cai, R. Babbush, S. C. Benjamin, S. Endo, W. J. Hug-     [25] E. Van Den Berg, Z. K. Minev, A. Kandala, and
     gins, Y. Li, J. R. McClean, and T. E. O’Brien, “Quan-            K. Temme, “Probabilistic error cancellation with sparse
     tum error mitigation,” arXiv preprint arXiv:2210.00921,          Pauli–Lindblad models on noisy quantum processors,”
     2022.                                                            Nature Physics, pp. 1–6, 2023.
[10] Y. Li and S. C. Benjamin, “Efficient variational quan-      [26] L. F. Santos and L. Viola, “Dynamical control of qubit
     tum simulator incorporating active error minimization,”          coherence: Random versus deterministic schemes,” Phys-
     Physical Review X, vol. 7, no. 2, p. 021050, 2017.               ical Review A, vol. 72, no. 6, p. 062303, 2005.
[11] K. Temme, S. Bravyi, and J. M. Gambetta, “Error miti-       [27] L. Viola and E. Knill, “Random decoupling schemes
     gation for short-depth quantum circuits,” Physical review        for quantum dynamical control and error suppression,”
     letters, vol. 119, no. 18, p. 180509, 2017.                      Physical review letters, vol. 94, no. 6, p. 060502, 2005.
[12] S. Endo, S. C. Benjamin, and Y. Li, “Practical quantum      [28] B. Pokharel, N. Anand, B. Fortman, and D. A. Lidar,
     error mitigation for near-future applications,” Physical         “Demonstration of fidelity improvement using dynam-
     Review X, vol. 8, no. 3, p. 031027, 2018.                        ical decoupling with superconducting qubits,” Physical
[13] A. Kandala, K. Temme, A. D. Córcoles, A. Mezzacapo,             review letters, vol. 121, no. 22, p. 220502, 2018.
     J. M. Chow, and J. M. Gambetta, “Error mitigation ex-       [29] P. Sekatski, M. Skotiniotis, and W. Dür, “Dynamical
     tends the computational reach of a noisy quantum pro-            decoupling leads to improved scaling in noisy quantum
     cessor,” Nature, vol. 567, no. 7749, pp. 491–495, 2019.          metrology,” New Journal of Physics, vol. 18, no. 7,
[14] A. Strikis, D. Qin, Y. Chen, S. C. Benjamin, and Y. Li,          p. 073034, 2016.
     “Learning-based quantum error mitigation,” PRX Quan-        [30] P. Czarnik, A. Arrasmith, P. J. Coles, and L. Cincio,
     tum, vol. 2, no. 4, p. 040330, 2021.                             “Error mitigation with Clifford quantum-circuit data,”
[15] T. Giurgica-Tiron, Y. Hindy, R. LaRose, A. Mari, and             Quantum, vol. 5, p. 592, 2021.
     W. J. Zeng, “Digital zero noise extrapolation for quan-     [31] A. Lowe, M. H. Gordon, P. Czarnik, A. Arrasmith, P. J.
     tum error mitigation,” in 2020 IEEE International Con-           Coles, and L. Cincio, “Unified approach to data-driven
     ference on Quantum Computing and Engineering (QCE),              quantum error mitigation,” Physical Review Research,
     pp. 306–316, IEEE, 2020.                                         vol. 3, no. 3, p. 033098, 2021.
                                                                                                                               12

[32] V. Russo, A. Mari, N. Shammah, R. LaRose, and W. J.                diqi, and J. J. Wallman, “Efficiently improving the per-
     Zeng, “Testing platform-independent quantum error mit-             formance of noisy quantum computers,” arXiv preprint
     igation on noisy quantum computers,” IEEE Transac-                 arXiv:2201.10672, 2022.
     tions on Quantum Engineering, 2023.                           [41] A. Mari, N. Shammah, and W. J. Zeng, “Extending
[33] C. Cirstoiu, S. Dilkes, D. Mills, S. Sivarajah, and R. Dun-        quantum probabilistic error cancellation by noise scal-
     can, “Volumetric benchmarking of error mitigation with             ing,” Physical Review A, vol. 104, no. 5, p. 052607, 2021.
     Qermit,” Quantum, vol. 7, p. 1059, 2023.                      [42] M. Otten and S. K. Gray, “Recovering noise-free quan-
[34] R. LaRose, A. Mari, V. Russo, D. Strano, and W. J.                 tum observables,” Physical Review A, vol. 99, no. 1,
     Zeng, “Error mitigation increases the effective quan-              p. 012338, 2019.
     tum volume of quantum computers,” arXiv preprint              [43] D. Cox, J. Little, and D. OShea, Ideals, varieties, and
     arXiv:2203.05489, 2022.                                            algorithms: An introduction to computational algebraic
[35] A. He, B. Nachman, W. A. de Jong, and C. W. Bauer,                 geometry and commutative algebra. Springer Science &
     “Resource efficient zero noise extrapolation with identity         Business Media, 2013.
     insertions,” arXiv preprint arXiv:2003.04941, 2020.           [44] R. Takagi, S. Endo, S. Minagawa, and M. Gu, “Funda-
[36] F. A. Calderon-Vargas, T. Proctor, K. Rudinger, and                mental limits of quantum error mitigation,” npj Quantum
     M. Sarovar, “Quantum circuit debugging and sensitivity             Information, vol. 8, no. 1, p. 114, 2022.
     analysis via local inversions,” Quantum, vol. 7, p. 921,      [45] L. Hour, S. Heng, M. Go, and Y. Han, “Improving
     2023.                                                              zero-noise extrapolation for quantum-gate error mitiga-
[37] T. Patel, D. Silver, and D. Tiwari, “Charter: Identify-            tion using a noise-aware folding method,” arXiv preprint
     ing the most-critical gate operations in quantum circuits          arXiv:2401.12495, 2024.
     via amplified gate reversibility,” in SC22: International     [46] UnitaryFund,       “UnitaryFund      Research.”    https:
     Conference for High Performance Computing, Network-                //github.com/unitaryfund/research/, Feb. 2024.
     ing, Storage and Analysis, pp. 1–16, IEEE, 2022.              [47] Qiskit contributors, “Qiskit: An open-source framework
[38] K. Saniee, “A simple expression for multivariate La-               for quantum computing,” 2023.
     grange interpolation,” SIAM undergraduate research on-        [48] M. Gasca and T. Sauer, “Polynomial interpolation in sev-
     line, vol. 1, no. 1, pp. 1–9, 2008.                                eral variables,” Advances in Computational Mathematics,
[39] P. J. Olver, “On multivariate interpolation,” Studies in           vol. 12, pp. 377–410, 2000.
     Applied Mathematics, vol. 116, no. 2, pp. 201–240, 2006.
[40] S. Ferracin, A. Hashim, J.-L. Ville, R. Naik, A. Carignan-
     Dugas, H. Qassim, A. Morvan, D. I. Santiago, I. Sid-
                                                                                                                         13

                                                    V.     APPENDIX

                                           A.   Noise model for experiments

  For the experiments in Section III, we consider a noise model characterized by amplitude damping errors. Let the
probability of amplitude damping error for a single qubit and two-qubit gate be denoted as p1 and p2 respectively,
with p1 = 0.04 and p2 = 0.08. The single-qubit amplitude damping channel is represented as

                                                 E1 (ρ) = E0 ρE0† + E1 ρE1†                                            (25)

where,
                                                                            √ 
                                               1 √ 0                          0 p1
                                       E0 =                      and E1 =          .                                   (26)
                                               0 1 − p1                       0 0

This channel is added to all single-qubit gates. For the two-qubit CNOT gate, we apply the tensor product of two
single-qubit channels,

                                                           Ei ⊗ Ej ρ Ei† ⊗ Ej† ,
                                                X X
                                      E2 (ρ) =                                                              (27)
                                                 i∈{0,1} j∈{0,1}

where we replace p1 in Equation (26) with p2 = 0.08 . We use the Qiskit Aer simulator [47] to simulate circuits with
the above noise model.


                                  B.   Multivariate Lagrange interpolation in LRE

   Single-variable Lagrange interpolation constructs a single-variable polynomial to fit a set of N points in R2 [48].
In the case of multivariate Lagrange interpolation, this approach is extended to handle the multivariate polynomial
interpolation of points in higher-dimensional spaces. Here, for a set of N points of a polynomial with l variables,
the interpolation is conducted in Rl+1 [38, 39]. In this appendix we adapt the mathematical formalism of Lagrange
interpolation of [38] to the specific notation of the LRE framework introduced in Section II B.
   We aim to find the interpolating l-variable polynomial passing through a set of N points representing the noise-
scaled expectation values of an observable. Each of these points corresponds to a circuit execution under a specific
noise scaling, captured by a vector λ containing l real scale factors, corresponding to the amount of noise scaling
applied to the l-th layer of the circuit. Given the N measured points, we define the set of scale factor vectors as
Λ = {λ1 , λ2 , . . . , λN } and the array of the associated expectation values as
                                                                                    T
                                         z = (⟨O(λ1 )⟩, ⟨O(λ2 )⟩, . . . , ⟨O(λN )⟩) .                                  (28)

The most general l-variable polynomial of degree d can be written as
                                                           M
                                                           X
                                                 P (λ) =         cj Mj (λ, d),                                         (29)
                                                           j=1

where {cj } are real coefficients and {Mj (λ, d) : j = 1, 2, . . . , M } is the set of all l-variable monomials of degree at
most d. The number of monomials is given by M = d+l
                                                         
                                                       d   and is therefore fixed by l and d. The interpolation problem
corresponds to determining the M unknown coefficients {cj } such that the polynomial passes through the measured
points, i.e.:

                                            P (λi ) = ⟨O(λi )⟩ = zi ,    ∀λi ∈ Λ.                                      (30)

Define the following sample matrix which contains the values of all monomials evaluated at each scale factor vector
in Λ:
                                                                                  
                                         M1 (λ1 , d) M2 (λ1 , d) · · · MM (λ1 , d)
                                        M1 (λ2 , d) M2 (λ2 , d) · · · MM (λ2 , d) 
                             A(Λ, d) =       ..          ..               ..      .                          (31)
                                                                                  
                                                                   . .
                                              .           .           .    .      
                                         M1 (λN , d) M2 (λN , d) · · · MM (λN , d)
                                                                                                                          14

If we cast the coefficients of the polynomial in a vector c = (c1 , c2 , . . . , cM )T , the interpolation problem can be
expressed as the following linear system:

                                                                    Ac = z.                                             (32)

To have a unique solution, we assume N = M and det(A) ̸= 0. In practice, given l and d, this is a constraint on the
number and the values of the scale factor vectors in the set Λ that is straightforward to check and satisfy.
  One way of determining the interpolating polynomial would be to solve for c and to replace the solution into
Equation (29). There is however an alternative way, which does not require the explicit computation of c and is given
by the following Lagrange interpolation formula [38]:

                                                              M
                                                              X                det (Mi (λ))
                                                    P (λ) =         ⟨O(λi )⟩                ,                           (33)
                                                              i=1
                                                                                 det (A)

where Mi (λ) is the matrix obtained by substituting the i-th row of the sample matrix A with the same row of
monomials but evaluated on the generic polynomial variable λ (instead of λi ∈ Λ), for example:
                                                                                  
                                         M1 (λ1 , d) M2 (λ1 , d) · · · MM (λ1 , d)
                                        M1 (λ, d) M2 (λ, d) · · · MM (λ, d) 
                             M2 (λ) =       ..           ..               ..      .                   (34)
                                                                                  
                                                                 ..
                                             .            .         .      .      
                                        M1 (λN , d) M2 (λN , d) · · · MM (λN , d)

By construction, the right-hand side of Equation (33) is a polynomial in the variable λ of degree at most d. Moreover,
it is easy to check that it also interpolates all points since, if we evaluate the expression at a specific λj ∈ Λ, we have
                           M
                           X                det (Mi (λj ))            det (Mj (λj ))            det (A)
               P (λj ) =         ⟨O(λi )⟩                  = ⟨O(λj )⟩                = ⟨O(λj )⟩         = ⟨O(λj )⟩,     (35)
                           i=1
                                               det (A)                   det (A)                det (A)

where we used that, for i ̸= j, det (Mi (λj )) = 0 since the i-th row and the j-th row are equal.
  Evaluating Equation (33) at the zero-noise limit (denoted as λ = 0), we get:
                                                                     M
                                                                     X                det (Mi (0))
                                               OLRE = P (0) =              ⟨O(λi )⟩                .                    (36)
                                                                     i=1
                                                                                        det (A)

The matrix Mi (0) can be obtained from the sample matrix A after replacing the i-th row by the array e1 =
(1, 0, . . . , 0)T , since all monomials are zero at λ = 0, with the exception of the constant one M1 (0, d) = M1 (λ, d) = 1.
Here, we implicitly assumed that monomials are ordered with increasing degree. Otherwise, the element 1 in the
vector e1 should be shifted to the position associated with the zero-order monomial. Equation (36) corresponds to
Equations (19) and (20) of the main text.

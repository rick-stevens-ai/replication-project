<!-- FALLBACK EXTRACTION: Marker was not installed on this host. Content below is pdftotext -layout output preserved verbatim for downstream text pipelines. Header added by replicator. -->

# Spectral Analysis of Product Formulas for Quantum Simulation
# arXiv:2102.12655v1  Changhao Yi and Elizabeth Crosson (UNM, 2021)

> Source: paper.pdf → pdftotext -layout

                                                            Spectral Analysis of Product Formulas for Quantum Simulation

                                                                                        Changhao Yi1, ∗ and Elizabeth Crosson1, †
                                                                     1
                                                                         Center for Quantum Information and Control, University of New Mexico
                                                                                             (Dated: February 26, 2021)
                                                            We consider Hamiltonian simulation using the first order Lie-Trotter product formula under the
                                                         assumption that the initial state has a high overlap with an energy eigenstate, or a collection of
                                                         eigenstates in a narrow energy band. This assumption is motivated by quantum phase estimation
                                                         (QPE) and digital adiabatic simulation (DAS). Treating the effective Hamiltonian that generates the
                                                         Trotterized time evolution using rigorous perturbative methods, we show that the Trotter step size
                                                         needed to estimate an energy eigenvalue within precision  using QPE can be improved in scaling
                                                         from  to 1/2 for a large class of systems (including any Hamiltonian which can be decomposed as
                                                         a sum of local terms or commuting layers that each have real-valued matrix elements). For DAS we
                                                         improve the asymptotic scaling of the Trotter error with the total number of gates M from O(M −1 )




arXiv:2102.12655v1 [quant-ph] 25 Feb 2021
                                                         to O(M −2 ), and for any fixed circuit depth we calculate an approximately optimal step size that
                                                         balances the error contributions from Trotterization and the adiabatic approximation. These results
                                                         partially generalize to diabatic processes, which remain in a narrow energy band separated from the
                                                         rest of the spectrum by a gap, thereby contributing to the explanation of the observed similarities
                                                         between the quantum approximate optimization algorithm and diabatic quantum annealing at small
                                                         system sizes. Our analysis depends on the perturbation of eigenvectors as well as eigenvalues, and
                                                         on quantifying the error using state fidelity (instead of the matrix norm of the difference of unitaries
                                                         which is sensitive to an overall global phase).


                                                                INTRODUCTION                                   trary initial state |ψi, we identify situations in which an-
                                                                                                               alyzing f and θ for specific initial states produces tighter
                                               The Lie-Trotter product formula [1, 2] was originally           error bounds than the general case.
                                            used by Lloyd [3] to establish the first method for effi-             Our results are based on a spectral analysis of the effec-
                                            ciently approximating the dynamics U (t) = e−itH gen-              tive Hamiltonian H   e that generates the Trotterized time
                                            erated by a local Hamiltonian H with a universal quan-             evolution,
                                            tum computer. After many refinements [4–6] this ap-
                                                                                                                         e ≡ i log(T (δt))/δt,
                                                                                                                         H                         T (δt) = e−iHδt         (3)
                                                                                                                                                                    e
                                            proach (often called “Trotterization”) continues to be an
                                            appealing method for Hamiltonian simulation from both
                                            experimental and mathematical perspectives.                        Regarding δt as a small parameter, perturbative methods
                                               The method is based on dividing U (t) into L short-             can be used to compare the spectrum {Ek , |ψk i} of the
                                            time evolutions U (t) = U L (δt), t = Lδt, and replacing           original Hamiltonian H to the spectrum {E    ek , |ψek i} of the
                                            each U (δt) with an approximation T (δt). The parameter            effective Hamiltonian H̃. These methods lead us to con-
                                            L is the number of Trotter steps and δt > 0 is the Trotter         sider applications in which the initial state |ψi is (or is
                                            step size. Given a decomposition  of the Hamiltonian into          close to) an eigenstate of H, enabling an improved upper
                                                                 PΓ
                                            a sum of layers H = n=1 Hn [7], the first order product            bound on the Trotter step size in Quantum Phase Esti-
                                            formula approximation is                                           mation (QPE) and Digital Adiabatic Simulation (DAS).
                                                                                                                  QPE is one of the most important quantum simulation
                                                                           Γ
                                                                           Y                                   algorithms [8], which relates Hamiltonian time-evolution
                                                               T (δt) ≡          e−iHn δt ,            (1)
                                                                                                               U (t) = e−itH to the measurement of energy eigenval-
                                                                           n=1
                                                                                                               ues [9–11]. In the ideal version of the algorithm, measur-
                                            where δt and L are chosen to depend on the tolerable               ing the output of the phase estimation circuit collapses
                                            level of error, as we subsequently discuss.                        the system into an energy eigenstate of H. If we replace
                                               Most prior works quantify the Trotter error in terms            the time evolution with the product formula approxima-
                                            of the operator norm kU (δt) − T (δt)k, but in this work           tion T (δt)L , then (in the ideal case) we will instead mea-
                                            we directly compare states evolved under the exact and             sure an energy eigenvalue of e   H. Therefore the Trotter
                                            approximate time evolution to produce a tighter error              error is directly related to the difference in spectrum be-
                                            estimate for the specific class of initial states we consider.     tween H and e   H. Under conditions which are satisfied in
                                            We quantify the Trotter error in terms of the phase error          many cases of interest, we show that the first order per-
                                            θ and the fidelity error f ,                                       turbative correction vanishes and use this to rigorously
                                                              p                      p
                                                T (δt)L |ψi = 1 − f eiθ U (t)|ψi + f U (t)|ψ ⊥ i. (2)          show that the Trotter error in phase can be reduced from
                                                                                                               O(Lδt2 ) to O(Lδt3 ). In terms of the target precision  of
                                            where |ψi is the initial state. While the operator norm            the QPE, this means the Trotter step size can be enlarged
                                            can always be used to upper bound f and θ for an arbi-             from δt = O() to δt = O(1/2 ).
                                                                                                                          2

   DAS can be used to implement adiabatic quantum                        Improved f : Spectral Analysis
computation [12–14] and adiabatic state preparation [15,
16] on a digital quantum computer. The scaling of Trot-         The Trotterized evolution operator T (δt)L can be
ter error in DAS has previously been analyzed in terms       viewed as an exact evolution under an effective Hamil-
of the operator norm [17, 18]. We find this measure of       tonian H e ≡ i log(T (δt))/δt. Owing to the tiny size of
error is dominated by the accumulation of a global phase,    δt, the spectrum of H e is {E
                                                                                         ek , |ψek i} is close to that of H.
whereas in adiabatic algorithms it is generally only the     Based on this observation, suppose the initial state is one
fidelity error f that matters. We regard the Trotterized     of the eigenstate |ψk i of H, f and θ can be quantified by
time evolution as a discretized adiabatic evolution under    the difference between spectrum:
an effective Hamiltonian, and obtain tighter bounds on
the fidelity error by applying an adiabatic theorem to the                      f = O(1 − |hψk |ψek i|2 )                (8)
effective Hamiltonian.                                                            θ = O(|E
                                                                                         ek − Ek |t)                     (9)
   This paper is organized as follows: we first illustrate
the setting of the problems and our main results, together   To ensure there exists a one-to-one correspondence be-
with the techniques and lemmas used in the proof. The        tween |ψk i and |ψ̃k i, we assume the spectrum is non-
primary mathematical tools are a rigorous perturbation       degenerate. Therefore there is some spectral gap λk =
method [19] and the Magnus expansion [20]. Then we ap-       min(Ek − Ek−1 , Ek+1 − Ek ) around this eigenstate. We
ply the main results to analyze Trotter error in QPE and     use λ as a general lower bound for the spectral gap around
DAS, in both cases we achieve improvements in circuit        an initial eigenstate.
complexity.                                                     The upper bound for the difference between energy
                                                             eigenvalues is based on an upper bound for kHk.  e Using
                                                             the Baker-Campbell-Hausdorff formula,
                   MAIN RESULTS                                                      iδt X
                                                                      H(δt)
                                                                       e     =H+           [Hl , Hm ] + O(δt2 ).    (10)
                                                                                      2
                 Set up and Notations                                                    l>m

                                                             The first few terms of the standard (Rayleigh-
  Usually, the Trotter error is quantified by the norm       Schrodinger) perturbation theory can be used to esti-
distance between operators:                                  mate f and θ, but to avoid convergence issues and derive
                 ˆ        ˆ ≡ T (δt)L − U (t)                rigorous results we use other methods [19, 21] that are
            ∆ ≡ k∆k,      ∆                           (4)    widely used in proofs of adiabatic theorems. By Weyl’s
The notation k · k refers to the operator norm : kM k =      inequality, the perturbation in the eigenvalues satisfies
maxkxk2 =1 kM |xik2 , where k · k2 is the Euclidean norm                        |E
                                                                                 ek − Ek | ≤ kH
                                                                                              e − Hk                    (11)
                   √
of vector kvk2 = vv † . To quantify ∆, it’s enough to
                                                             The perturbation of the eigenvectors is derived from the
quantify the norm distance error of a single Trotter step
                                                             following lemma.
δ ≡ kT (δt) − U (δt)k as ∆ ≤ Lδ. For a given error tol-
erance , the restriction of ∆ ≤  determines the gate       Lemma 1 (Rigorous perturbation method [21]).
complexity of the algorithm.                                 H(s) is a parameterized Hamiltonian with spectrum
  In this paper, we separate the digital error into phase    :{Ej (s), Pj (s)}, define
error θ and fidelity error f defined by                                                       m
                                                                                              X
                                                                                   P (s) =          Pj (s)
              f ≡ 1 − |hψ|U † (t)T (δt)L |ψi|2        (5)
                                                                                              j=1
              θ ≡ Arg hψ|U † (t)T (δt)L |ψi
                                             
                                                      (6)
                                                             as the projector into a subspace A spanned by m eigen-
where |ψi                                                    states. Its derivative has norm upper bound:
         √ is an initial state. For any L, δt that satisfy
∆ ≤ 1/ 2, the Euclidean distance error E ≡ k∆|ψik  ˆ                                     √
                                                         2                    kP 0 (s)k ≤ mkH 0 (s)k/λ         (12)
satisfies (see Appendix A)
                                                             where λ is the lower bound of energy gap between the
                    θ2                                       eigenstates in and outside region A.
                 f+    ≤ E 2 ≤ 2f + θ2                (7)
                    4
                                                              For a single eigenvector, lemma 1 implies
Without further assumptions about H and |ψi, the two          q
parameters are bounded by f = O(∆2 ), |θ| = O(∆) as            1 − |hψek |ψk i|2 = kPek − Pk k
E ≤ ∆. However, in some special cases, we find that
                                                                                 = kP (δt) − P (0)k ≤ δt max kP 0 (s)k
both f and θ2 have a different parameteric scaling with                                                      s∈[0,δt]
∆. This means that ∆ does not always reflect the true                                         e0
                                                                                 ≤ max kH (s)kδt/λ
Trotter error that we are interested in, which leads us to                         s∈[0,δt]
a different approach.                                                                                                   (13)
                                                                                                                              3

The term kHe 0 (s)k quantifies the size of the perturbation.     Then the leakage rate can be bounded by the norm dis-
The necessary bound on kH   e 0 k has already been obtained      tance between P and corresponding effective projector Pe
using the Magnus expansion in previous work, see Ap-                        e if kP − Pek < 1:
                                                                 induced by H
pendix B for more details.                                                                                         
Lemma 2 (Magnus Expansion[22]). Given H         e defined in            1 − Tr(T (δt)L ρT † (δt)L P ) = O kP − Pek2
                           −1
Eq : (3), when δt = O(N ), for all s ∈ [0, δt]:                                                          
                                                                                                           mh2 δt2
                                                                                                                   
                                                                                                      =O
     ke
      H(s) − Hk = O(hδt), kH  e 0 (s)k = O(h)            (14)                                                λ2
                α 4                                              where λ is the lower bound of energy gap between the
             h = + (β + 128αkHk)δt                       (15)
                 2 X3                                            eigenstates in and outside region A.
                α≡     ||[Hn , Hm ]||
                        n>m
                      X
               β≡             ||[Hl , [Hn , Hm ]]||                        Improved θ : Special Perturbation
                    l≥n>m
                                                                    The bound θ = O(∆) can be tight, even when the
                            PN
  For example, if H = j=1 hj is a local Hamiltonian              initial state is an eigenstate. However, we show that it
on N qubits that satisfies [hj , hk ] = 0, ∀|j − k| > 1, then    can be improved by a factor of δt under assumptions that
h = O(N ) + O(N 2 δt) = O(N ). In general, the param-            are satisfied for many Hamiltonians of interest, and this
eter dependence of h is complicated but will always be           improves the scaling of the Trotter step size needed for
poly(N ) for any k-local Hamiltonian. To simplify the no-        QPE. This can be illustrated by the simple case H =
tation we retain the form of h in the following paragraph.       HA + HB in which the Hamiltonian is decomposed into
  The following result follows from Lemma 1 with                 two commuting layers,
Lemma 2, see Appendix C.
                                                                             T (δt) = e−iHA δt e−iHB δt = e−iHδt ,
                                                                                                                 e
Corollary 1 (Eigenstate as initial state). For any H and
any eigenstate |ψk i of H separated from the rest of the                      e = H − i δt [HA , HB ] + O(δt2 ).
                                                                              H
spectrum by a spectral gap λ, the time evolution under                                   2
the 1st-order product formula satisfies :
                     p                      p                    The leading perturbation term is V ≡ −iδt[HA , HB ]/2.
      T (δt)L |ψk i = 1 − f eiθ U (t)|ψk i + f |ψk⊥ i            In standard perturbation theory, the 1st order correction
                                                                 in energy is E (1) = hψk |V |ψk i. However,
where the fidelity error and phase error satisfy
                  |θ| = O(Lhδt2 )                        (16)            hψk |[HA , HB ]|ψk i = hψk |[H, HB ]|ψk i = 0.
                   2 2                 
                      h δt        2 2 4
          f = min O         , O(L  h δt )                (17)    In previous section we prove an upper bound of Trotter
                        λ2                                       error in energy of order O(hδt). While under this special
with h defined in Lemma 2.                                       situation, because E (1) = 0, the shift in energy at most
                                                                 has order O(δt2 ). This improvement can be applied to
   As a comparison, ∆ = O(Lhδt2 ) in general. Corollary                                          PΓ
                                                                 a general decomposition H = n=1 Hn . Whenever the
1 implies that the fidelity error f eventually stops grow-
                                                                 leading order correction,
ing with with the total number of Trotter steps L, which
is an extreme example of f  ∆2 . After a short initial                                      iδt X
period, the Trotter error only accumulates in the global                               V =         [Hl , Hm ],
                                                                                              2
phase. This fact can be related to the leakage rate prop-                                       l>m
erty [23] of the Trotterized
                          P evolution operator. Suppose
the initial state is |ψi = k ck |ψk i, where |ψk i all belong    is off-diagonal in the eigenbasis of H, we can reduce the
to a special region A, like low-energy states. The leakage       Trotter error in energy from O(δt) to O(δt2 ). In the
rate is the percentage for |ψi to go outside that region         setting of Corollary 1, the following result is proven by
after T (δt)L : 1 − Tr(PA T (δt)L |ψihψ|T † (δt)L ). Using the   rigorous perturbative methods in Appendix E.
argument about H    e we prove:
                                                                 Lemma 3. H is a normalized local Hamiltonian on N
Theorem 1 (Leakage rate). T (δt)L is Trotterized evo-            sites with spectrum {Ek , |ψk i}, H
                                                                                                   e is its corresponding ef-
lution operator, if the initial state ρ belongs to subregion     fective Hamiltonian induced from 1st order product for-
A spanned by m eigenstates:                                      mula. The new spectrum is {E    ek , |ψek i}. The first pertur-
                      m
                      X                                          bation of H is off-diagonal in the eigenbasis of H:
                                                                            e
                P =         Pj ,   Tr(ρP ) = 1
                      j=1                                                    ∀|ψk i,         e − H|ψk i = O(δt2 )
                                                                                        hψk |H                             (18)
                                                                                                                                   4

Further if δt = O(λ/N ), where λ is the lower bound              distance can’t reflect Trotter error in Euclidean distance
of spectral gap between |ψk i and neighboring eigenstates,       either.
then the shift in energy satisfies:                                 Finally, we provide an example H = H1 + H2 + H3 in
                                                             which V is not off-diagonal to show the result in Lemma
                              2 2          1                     3 is not fully general. Let H be a diagonal matrix Λ in
          |Ek − Ek | = O N δt max 1, 2
           e                                         (19)
                                          λ                      the eigenbasis of itself. In this basis choose:
                                                                    H1 = X ⊗ I,        H2 = Y ⊗ I,           H3 = Λ − H1 − H2
   In addition to Hamiltonians that can be decomposed
into two commuting layers (of which a prominent class            Thus:
of examples are Hamiltonians H = HX + HZ that have                            V /δt = i[(X + Y ) ⊗ I, Λ]/2 + Z ⊗ I
local terms which involve only Pauli X or Pauli Z oper-
ators), we list other different conditions where Eq : (18)       The first term is off-diagonal, the second term is not.
is satisfied.                                                    Thus V is not off-diagonal.
   • Real Hamiltonians. Assume all of the local terms
     of H have real matrix elements in some basis. The                        Improved f : Adiabatic Theorem
     components of an eigenstate |ψk i of any real sym-
     metric matrices can all be taken to be real. Con-             DAS is a special type of time-dependent evolution sim-
     sider an arbitrary commutator in V , hψk |Hl Hm |ψk i       ulation task [26, 27] that leverages the quantum adia-
     is conjugate to hψk |Hm Hl |ψk i, and both are real         batic theorem [21, 28]. Physically, when the Hamilto-
     numbers. So they are equal and appear with                  nian evolves with time slowly enough, an initial state in
     opposite signs in the commutator. Therefore,                some eigenspace will stay close to that eigenspace of the
     ∀k, l, m, hψk |[Hl , Hm ]|ψk i = 0.                         time-dependent Hamiltonian at all times. The evolution
   • Any Hamiltonian whose layers (or local terms) can           operator under Ĥ(t) has expression:
     be totally ordered to satisfy [Hl , Hm ] = 0, ∀|l −                  d
     m| > 1. This condition is satisfied by 1D Hamilto-               i      |ψ(t)i = Ĥ(t)|ψ(t)i,      |ψ(T )i = Â(T )|ψ(0)i
                                                                          dt
     nians with nearest-neighbor interactions, as well as                                                Z T        !
     general lattice Hamiltonians regarded as 1D chains                          Â(T ) = expT       −i      Ĥ(t)dt
     of super-sites (since our results do not depend on                                                  0
     the local dimension). This condition leads to a
                                                                 We restrict out attention to the linear adiabatic path
     recursive relation: [Hl , Hl+2 ] = [Hl , H − Hl−1 −
                                                                 Ĥ(t) = (1 − t/T )Hi + t/T Hf . In terms of the dimension-
     Hl+1 ] = 0. If [Hl−1 , Hl ] is off-diagonal, [Hl , Hl+1 ]
                                                                 less parameter s = t/T ,
     is also off-diagonal as any operator in the form of
     [O, H] is off-diagonal in the eigenbasis of H. The                        H(s) ≡ Ĥ(T s) = (1 − s)Hi + sHf
     case of l = 1 is special as we don’t have H0 . Thus                                      Z 1        
     [H1 , H2 ] = [H1 , H] is off-diagonal. As a result,                    A(T ) ≡ expT −iT       H(s)ds = Â(T )
     ∀l, [Hl , Hl+1 ] is off-diagonal. These assumptions                                             0

     can be satisfied for any Hamiltonian with geomet-           T → ∞ corresponds to the case where evolution is per-
     rically local terms in 1D.                                  formed adiabatically:
   • Frustration-free Hamiltonians [24].           This type                           lim A(T )|ψi i = |ψf i
                                                                                      T →∞
                                          P
     of Hamiltonian satisfies H =             j j H|ψ0 i =
                                                Π ,
     E|ψ0 i, Πj |ψ0 i = Ej |ψ0 i where |ψ0 i is ground state.    |ψi i is one eigenstate of initial Hamiltonian Hi and |ψf i is
     With this property, when the initial state is the           the corresponding one of Hf . T quantifies how slowly the
     ground state, there will be no Trotter error no             evolution is, it also reflects how close the evolved state
     matter how big δt is. In Lemma 3, the upper                 is to |ψf i. We apply the following rigorous adiabatic
     bound on the Trotter error is inversely propor-             theorem.
     tional to the spectral gap λ. However, it’s possible
     for frustration-free Hamiltonian to be gapless [25].        Lemma 4 (Adiabatic theorem [21]). The error of adia-
     This example shows that our methods can still over-         batic evolution is quantified by:
     estimate the Trotter error for gapless Hamiltonians.                         adb ≡ kPf − A(T )Pi A† (T )k                  (20)
The second part of Eq : (7) indicates that f and θ can be        where Pf = |ψf ihψf |, Pi = |ψi ihψi |. A(T ) is the adia-
used to bound the Euclidean distance error as well. We           batic evolution operator. Then:
have just proved that f and θ2 can both be much smaller
than ∆, which means under these conditions the norm                                       adb ≤ G(T, H)                         (21)
                                                                                                                                    5

with
                            kH 0 (0)k kH 0 (1)k
                                                        
                   1
       G(T, H) ≡                     +
                   T         λ(0)2     λ(1)2
                       Z 1                                   (22)
                 1           kH 00 (s)k     kH 0 (s)k2
               +                        + 7            ds
                 T      0     λ2 (s)         λ3 (s)

λ(s) is the lower bound of energy gap between |ψ(s)i and
other eigenstates during evolution. |ψ(s)i is the eigen-
state in H(s) associated with |ψi i.

Notice the adiabatic theorem refers to fidelity error,
                    q
             adb = 1 − |hψf |A(T )|ψi i|2 .

To simulate this process with Trotterization, we first ap-
proximate A by a product of short time evolutions,
                        M
                                                         ¯
                        Y
               Ad ≡           Ua ,       Ua ≡ e−iHa δt       (23)
                        a=1
                      T                         a
                 ¯
                 δt ≡   ,            Ha ≡ H                  (24)
                      M                              M
Here M is the discretization number. Note that going
from A to Ad already incurs some discretization error.
Each short time evolution operator is further Trotterized,
                       M
                       Y                             a
              At ≡           Uat ,       Uat ≡ U t           (25)
                       a=1
                                                         M
                                     ¯               ¯
               U t (s) ≡ e−iδt(1−s)Hi e−iδtsHf               (26)
                                                                    Figure
                                                                       P 1. Error P       scaling of DAS. The example is Hi =
Therefore the parameter M determines both the dis-                  − i Xi , Hf = − i (Zi + Zi Zi+1 ) on N = 8 sites without
cretization error and the additional Trotter error. The             periodic boundary conditions. The initial state is the ground
expression of U t (s) actually depends on how the Trot-             state of Hi . The discretization number is fixed at M = 2000.
terization is performed, while our argument applies to              The figures illustrate how 0tot , 0adb and tro scale with pa-
general product formulas, thus we use the above defini-             rameter T ranging from [M/50, M ] evenly. Each point is a
tion as an instance.                                                complete run of DAS and there are 50 of them in one line.
   The total error of DAS, which is the fidelity distance           The vertical axis is shown on a log10 scale. The first figure
                                                                    is only about 0tot , the second figure is a combination of 0adb
between At |ψi i and |ψf i, is divided into three parts. The        and tro . As to 0adb , the overall scaling of O(T −1 ) indicates
first part comes from adiabatic evolution itself, it can            the correctness of prediction by adiabatic theorem. Note that
be quantified by Lemma 4. The other two stem from                   the Trotter error remains small when T, M are comparable to
discretization and Trotterization steps. To simplify the            each other. 0tot is close to the summation of 0adb and tro .
question, we only study the case where the error caused             The overall scaling is similar to that of 0adb , while after a
by discretization is negligible comparing to the error from         turning point the error grows rapidly, and the curve matches
adiabatic theorem, which is to say:                                 with that of tro . The turning point is the place where the
                                                                    minimal error is reached. Approximately it’s 0.75M .
                   0adb ≡ kPf − Ad Pi A†d k                 (27)
                 dis ≡ |0adb − adb |  adb               (28)   the fidelity error, and by building on the techniques in
                                                                    Corollary 1 we will demonstrate that tro has a tighter
We focus on the Trotter error in DAS,                               upper bound that differs from kAd − At k. We associate
                                                                    a time-evolving effective Hamiltonian H(s)  with U t (s),
       tro ≡ kAd Pi A†d − At Pi A†t k ≤ kAd − At k
                                                                                                           e
                                                             (29)
                                                                                       H(s)
                                                                                       e                     ¯
                                                                                            ≡ i log(U t (s))/δt                  (30)
which has previously been bounded in terms of operator
norm : kAd − At k = O(T 2 /M ) [17]. However, as indi-              Notice that at the beginning point s = 0 and end point
cated by the adiabatic theorem, all we need to control is           s = 1, H(s)
                                                                           e    is the same as Hi and Hf . So the adiabatic
                                                                                                                            6

evolution under H(s)
                 e     can also transform |ψi i to |ψf i.                           APPLICATIONS
Naturally the total error should also be quantified with
adiabatic theorem.                                                            Quantum Phase Estimation

                  0tot ≡ kPf − At Pi A†t k             (31)
                                                                   The QPE algorithm constructs a quantum circuit to
Again, we require that the error caused by discretization       detect the phase θ of a unitary operator: U |ψi = eiθ |ψi.
is negligible:                                                  For an exact QPE algorithm, the measurement outcome
                                                                is the integer a closest to 2l θ, where l is the size of the
              tot ≡ kPf − A(T
                           e )Pi A e† (T )k
                                                                first register. Since it’s unlikely for 2l θ to be an integer,
                                                                there is an inherent error ξ = O(2−l ) in this algorithm.
                              Z 1          
            A(T ) ≡ expT −iT
            e                      H(s)ds
                                    e
                                                                The probability of measuring the value closest to the true
                                      0
                                                                θ is at least 4/π 2 [11].
                 edis ≡ |0tot − tot |  tot
                                                                   The influence of the Trotter error comes from two as-
Here tot is the adiabatic error of evolution under H(s),
                                                      e         pects. Again we regard the Trotterized evolution op-
                                        0
which is also the continuous limit of tot . Using the adi-     erator as an exact evolution operator under the effective
abatic theorem we have:                                         Hamiltonian H.  e This effective Hamiltonian has an eigen-
                                                                state |ψi, which is very close to initial eigenstate |ψi :
                                                                        e
                                                                        √        e + √p|ψe⊥ i. As a result, the final phase
                       tot ≤ G(T, H)
                                   e                    (32)    |ψi = 1 − p|ψi
   Combining with Lemma 2, Lemma 4 and the trian-               detected should be θe and the success rate should be de-
gle inequality tro ≤ 0adb + 0tot , we prove the following    creased by a factor of (1 − p). However, since usually p is
proposition in Appendix F.                                      much smaller comparing to 1, this change in success rate
                                                                is almost negligible.
Proposition 1. Consider a digital adiabatic evolution              More importantly, the Trotter error in phase δθ = |θe−
with initial Hamiltonian Hi , final Hamiltonian Hf , total      θ| should satisfy δθ < ξ, otherwise the phase error caused
evolution time T , and discretization number M . If the         by Trotterization will be detected. This relation gives us
discretization error is negligible comparing to the contin-     a constraint on the Trotter error:
uous limit then
                                                                                        |E
                                                                                         e − E|t ≤ ξ                     (36)
                 dis  adb ,    edis  tot          (33)
                                                                In QPE, θ should be set to be close to 1 to avoid wast-
then the Trotter error has upper bound:                         ing the accuracy provided by the first register, thus
                                                                t = O(1/|E|). However, we can only guess about E be-
              tro = O(G(T, H) + G(T, H))
                                      e                 (34)    fore the algorithm. Here we use t0 to denote an appro-
                                                                priate choice of time scale in U . Thus
with G introduced in Lemma 4. Define:
                                                                                               
                                                                                                t0
              C0 ≡ kHi k,     C1 ≡ k[Hi , Hf ]k                                        L=O                         (37)
                                                                                                δt
                      D ≡ kHi − Hf k
                                                                where L is the Trotterization number.
when D/λ  1, where λ is the lower bound of spectral             The following result follows from Lemma 3.
gap during adiabatic evolution under H(s) and H(s),
                                              e     and         Corollary 2. Suppose there’s a quantum circuit per-
(C0 + 3D/2)T < M/4, we obtain:                                  forming QPE, the size of the first register is l thus the
                       2
                        D
                                   2 
                                     C1 T                       inherent error is ξ = O(2−l ). The unitary operator is
            tro = O          + O                   (35)        U = e−iHt0 where Hsatisfies one of the conditions from
                       T λ3         M 2 λ3
                                                                Lemma 3 in the previous section. To guarantee that the
                                                                Trotter error in phase is smaller than the inherent error
   From Proposition 1 we already derive a result different      ξ, we have:
from kAd − At k. Numerical results (see Fig. 1) seem                                       r                !
to indicate that tro is close to 0tot − 0adb , which means                           1      ξ
                                                                               δt = O             min{1, λ}          (38)
this result can be further improved. Also this result only                              N t0
works for T /M = O(N −1 ).                                                           s                      
                                                                                             3
                                                                                                          
   Though taken for granted in most works, the criterion                                   t 0           1
                                                                             L = O N          max 1,               (39)
for Eq : (33) to hold is critical to the error analysis. This                               ξ            λ
question has its independent interest. The discretized                                  s                        
adiabatic evolution has been the subject of some anal-                                           3 t3
                                                                                                               
                                                                                              N     0         1
ysis [19], but we believe the result can be intrinsically           Circuit Depth = O                max 1,        (40)
                                                                                                ξ3            λ
improved and thus leave it for future work.
                                                                                                                           7

λ is the lower bound of spectral gap between initial state         However, the Tc derived still deviates a lot from the
|ψi and its neighboring eigenstates.                            turning point in Fig. 1, because our estimation of 0tot
                                                                is much larger than the actual value. A tighter bound
 As a comparison, in general case with |E      e − E| =
                                                                for 0tot would lead to a more accurate estimate of Tc .
                                       2 2 2
O(N δt), the final circuit depth is O(N t0 /ξ ).                Additional factors may contribute to the location of the
                                                                turning point; for example, if the spectral gap of H(s)
                                                                                                                     e
       Optimizing Digital Adiabatic Simulation
                                                                closes as δt gets larger, the application of the adiabatic
                                                                theorem will eventually fail.
    Although a better upper bound of tro has been derived
in Proposition 1, it is really 0tot rather than tro that is
the most relevant quantity, for it doesn’t matter whether                    CONCLUSION & OUTLOOK
the error originates from numerical procedure or the fi-
nite size of T . Motivated by this, here we elaborate on           Our main contribution is the observation that refined
a different question: given a DAS task with Hi , Hf and         estimation of Trotter error can be established from effec-
|ψi i specified, and a quantum computer with fixed circuit      tive Hamiltonian e  H. When the initial state is an eigen-
depth M , find the optimal T to minimize the estimated          state, we first relate the fidelity error and phase error to
total error 0tot .                                             the spectrum analysis of e   H, and find that during evo-
    There exists a trade-off between Trotter error and adi-     lution, most error accumulates in the phase. Further, if
abatic error: on one hand, T can’t be too small as the adi-     the leading perturbation term of H   e vanishes in the eigen-
abatic error is inversely proportional to T ; on the other      basis of H, the Trotter error in energy is reduced from
hand, the error caused by Trotterization increases with         O(δt) to O(δt2 ), which results in improvement of QPE.
T (for a fixed depth M ). The trade-off is balanced when        We remark that the improvement in Trotter step size
the two errors are of the same magnitude. We use Tc             with phase estimation error  from  to 1/2 can be com-
to denote the balanced point, which is exactly the turn-        pared to the step size of 1/2 that is obtained from the use
ing point in Fig. 1, if our estimation of tot is accurate      of a second-order product formula approximation. Sim-
enough. The value of Tc depends on the estimation of            ilar results apply to other QPE methods such as robust
0tot . In Proposition 1 we have derived an upper bound         phase estimation [32] (see Appendix G), as long as the
for 0tot and denote it with the function G(T, H). e    The     Trotterized unitary operator is used. Finally, we show
critical value of Tc and the optimal error are defined by       that the spectral analysis method is particularly suitable
                                                                to analyzing Trotter error in DAS, and we demonstrate
     opt ≡ inf G(T, H),
                     e      Tc ≡ arg min G(T, H).
                                              e         (41)    how consideration of the various types of error leads to
               T
                                                                an optimal time parameter Tc for DAS when the circuit
The next Corollary indicates that Tc is proportional to M       depth of the quantum circuit is fixed.
and their optimal ratio determines the gate complexity             There are many targets to pursuit in future work. Here
of DAS. The result follows from Proposition 1.                  we have only studied Trotter error for the 1st order prod-
Corollary 3 (Optimal choice of T ). In the setting of           uct formula, and it will be interesting to see whether
Proposition 1, we intend to perform a digital adiabatic         similar properties exist for higher-order product formu-
evolution on a quantum device with circuit depth M . If         las. One may also seek examples of f  ∆2 in time-
(8C0 +12D)D ≤ 3C1 , then the upper bound of 0tot reaches       dependent Hamiltonian situation, in which the initial
its minimal value at:                                           state is the eigenstate of the initial Hamiltonian, general-
                                                                izing our results for DAS. Third, numerically the Trotter
                               2M D
                        Tc =                            (42)    error in DAS is more close to 0tot − 0adb rather than the
                                3C1                             summation of them, we believe with detail analysis this
Accordingly,                                                    improvement can be achieved. The forth point is the cri-
                                                              terion for the time step scale T /M in DAS that keeps
                                   DC1                          the error caused by discretization negligible. Finally, we
                    opt = O                            (43)
                                   M λ3                         would like to try the effective Hamiltonian idea in other
                                                                quantum simulation algorithms [6, 33–35].
Alternatively, to achieve an error  we can keep the ratio
Tc /M fixed and take the depth of quantum circuit M to
be:
                                                                             ACKNOWLEDGEMENT
                                   N DC1
              Circuit Depth = O                       (44)
                                     λ3 
                                                                  We thank Rolando Somma and Burak Şahinoğlu for
N is the width of quantum circuit and λ is the lower            helpful discussions. This material is based upon work
bound of spectral gap.                                          supported by the U.S. Department of Energy, Office
                                                                                                                                 8

of Science, National Quantum Information Science Re-                     arXiv:2004.04164, 2020.
search Centers, Quantum Systems Accelerator (QSA).                  [17] Rami Barends, Alireza Shabani, Lucas Lamata, Julian
                                                                         Kelly, Antonio Mezzacapo, Urtzi Las Heras, Ryan Bab-
                                                                         bush, Austin G Fowler, Brooks Campbell, Yu Chen, et al.
                                                                         Digitized adiabatic quantum computing with a supercon-
                                                                         ducting circuit. Nature, 534(7606):222–226, 2016.
  ∗
     yichanghao123@unm.edu                                          [18] Yin Sun, Jun-Yi Zhang, Mark S Byrd, and Lian-Ao
  †
     crosson@unm.edu                                                     Wu. Adiabatic quantum simulation using trotterization.
 [1] Hale F Trotter. On the product of semi-groups of opera-             arXiv preprint arXiv:1805.11568, 2018.
     tors. Proceedings of the American Mathematical Society,        [19] Andris Ambainis and Oded Regev. An elementary proof
     10(4):545–551, 1959.                                                of the quantum adiabatic theorem. arXiv preprint quant-
 [2] Masuo Suzuki. Generalized trotter’s formula and sys-                ph/0411152, 2004.
     tematic approximants of exponential operators and inner        [20] Sergio Blanes, Fernando Casas, JA Oteo, and José Ros.
     derivations with applications to many-body problems.                The magnus expansion and some of its applications.
     Communications in Mathematical Physics, 51(2):183–                  Physics reports, 470(5-6):151–238, 2009.
     190, 1976.                                                     [21] Sabine Jansen, Mary-Beth Ruskai, and Ruedi Seiler.
 [3] Seth Lloyd. Universal quantum simulators. Science,                  Bounds for the adiabatic approximation with applica-
     pages 1073–1078, 1996.                                              tions to quantum computation. Journal of Mathematical
 [4] Andrew M Childs, Yuan Su, Minh C Tran, Nathan                       Physics, 48(10):102111, 2007.
     Wiebe, and Shuchen Zhu. A theory of trotter error. arXiv       [22] Minh C Tran, Yuan Su, Daniel Carney, and Jacob M
     preprint arXiv:1912.08854, 2019.                                    Taylor. Faster digital quantum simulation by symmetry
 [5] Andrew M Childs and Yuan Su. Nearly optimal lattice                 protection. arXiv preprint arXiv:2006.16248, 2020.
     simulation by product formulas. Physical review letters,       [23] Burak Şahinoğlu and Rolando D Somma. Hamiltonian
     123(5):050503, 2019.                                                simulation in the low energy subspace. arXiv preprint
 [6] Earl Campbell. Random compiler for fast hamiltonian                 arXiv:2006.02660, 2020.
     simulation. Physical review letters, 123(7):070503, 2019.      [24] Sergey Bravyi and Barbara Terhal. Complexity of sto-
 [7] As usual in trotterization, the guideline for the decompo-          quastic frustration-free hamiltonians. Siam journal on
     sition is that one has a way to implement eitHj efficiently         computing, 39(4):1462–1485, 2010.
     for each Hj . A sufficient condition for this is for each Hj   [25] Sergey Bravyi, Libor Caha, Ramis Movassagh, Daniel
     to be a sum of pairwise commuting local terms.                      Nagaj, and Peter W Shor. Criticality without frustra-
 [8] A Yu Kitaev. Quantum measurements and the abelian                   tion for quantum spin-1 chains. Physical review letters,
     stabilizer problem. arXiv preprint quant-ph/9511026,                109(20):207202, 2012.
     1995.                                                          [26] David Poulin, Angie Qarry, Rolando Somma, and Frank
 [9] Markus Reiher, Nathan Wiebe, Krysta M Svore, Dave                   Verstraete.    Quantum simulation of time-dependent
     Wecker, and Matthias Troyer. Elucidating reaction mech-             hamiltonians and the convenient illusion of hilbert space.
     anisms on quantum computers. Proceedings of the Na-                 Physical review letters, 106(17):170501, 2011.
     tional Academy of Sciences, 114(29):7555–7560, 2017.           [27] Dominic W Berry, Andrew M Childs, Yuan Su, Xin
[10] Ian D Kivlichan, Craig Gidney, Dominic W Berry,                     Wang, and Nathan Wiebe. Time-dependent hamiltonian
     Nathan Wiebe, Jarrod McClean, Wei Sun, Zhang Jiang,                 simulation with l1 -norm scaling. Quantum, 4:254, 2020.
     Nicholas Rubin, Austin Fowler, Alán Aspuru-Guzik,             [28] Donny Cheung, Peter Høyer, and Nathan Wiebe. Im-
     et al. Improved fault-tolerant quantum simulation of                proved error bounds for the adiabatic approximation.
     condensed-phase correlated electrons via trotterization.            Journal of Physics A: Mathematical and Theoretical,
     Quantum, 4:296, 2020.                                               44(41):415302, 2011.
[11] Michael A Nielsen and Isaac Chuang. Quantum compu-             [29] Lucas T Brady, Christopher L Baldwin, Aniruddha Ba-
     tation and quantum information, 2002.                               pat, Yaroslav Kharkov, and Alexey V Gorshkov. Opti-
[12] Edward Farhi, Jeffrey Goldstone, Sam Gutmann, Joshua                mal protocols in quantum annealing and qaoa problems.
     Lapan, Andrew Lundgren, and Daniel Preda.                  A        arXiv preprint arXiv:2003.08952, 2020.
     quantum adiabatic evolution algorithm applied to ran-          [30] Guido Pagano, Aniruddha Bapat, Patrick Becker,
     dom instances of an np-complete problem. Science,                   Katherine S Collins, Arinjoy De, Paul W Hess, Harvey B
     292(5516):472–475, 2001.                                            Kaplan, Antonis Kyprianidis, Wen Lin Tan, Christopher
[13] Dorit Aharonov, Wim Van Dam, Julia Kempe, Zeph Lan-                 Baldwin, et al. Quantum approximate optimization of
     dau, Seth Lloyd, and Oded Regev. Adiabatic quantum                  the long-range ising model with a trapped-ion quantum
     computation is equivalent to standard quantum compu-                simulator. Proceedings of the National Academy of Sci-
     tation. SIAM review, 50(4):755–787, 2008.                           ences, 2020.
[14] Tameem Albash and Daniel A Lidar. Adiabatic quantum            [31] Leo Zhou, Sheng-Tao Wang, Soonwon Choi, Hannes
     computation. Reviews of Modern Physics, 90(1):015002,               Pichler, and Mikhail D Lukin. Quantum approximate
     2018.                                                               optimization algorithm: performance, mechanism, and
[15] Dorit Aharonov and Amnon Ta-Shma. Adiabatic quan-                   implementation on near-term devices. arXiv preprint
     tum state generation and statistical zero knowledge. In             arXiv:1812.01041, 2018.
     Proceedings of the thirty-fifth annual ACM symposium on        [32] AE Russo, KM Rudinger, BCA Morrison, and
     Theory of computing, pages 20–29, 2003.                             AD Baczewski. Evaluating energy differences on a quan-
[16] Kianna Wan and Isaac Kim.              Fast digital meth-           tum computer with robust phase estimation. arXiv
     ods for adiabatic state preparation. arXiv preprint                 preprint arXiv:2007.08697, 2020.
                                                                                                                                9

[33] Guang Hao Low and Isaac L Chuang. Hamiltonian sim-                       review letters, 118(1):010501, 2017.
     ulation by qubitization. Quantum, 3:163, 2019.                      [35] Dominic W Berry, Andrew M Childs, Richard Cleve,
[34] Guang Hao Low and Isaac L Chuang. Optimal hamilto-                       Robin Kothari, and Rolando D Somma. Simulating
     nian simulation by quantum signal processing. Physical                   hamiltonian dynamics with a truncated taylor series.
                                                                              Physical review letters, 114(9):090502, 2015.




                                            Appendix A : Proof of Eq : (7)

  First we will quantify the region for f and θ in Eq : (2). We know that f ∈ [0, 1] by definition. As to θ, consider
the inner product:

                                          hψ|U † (t)T (δt)L |ψi = 1 + hψ|U † (t) ˆ
                                                                                ∆|ψi
                                √
Since ∆ ≡ kT (δt)L − U (t)k ≤ 1/ 2:
                                                                              √
                                                                ˆ
                                          | sin θ| ≤ |hψ|U † (t)∆|ψi| ≤ ∆ ≤ 1/ 2.

Thus |θ| ∈ [−π/4, π/4]. In this region, θ satisfies:

                                                          θ2               θ2
                                                  1−         ≤ cos θ ≤ 1 −
                                                          2                4
Similarly,
                                                               p        f
                                                  1−f ≤         1−f ≤1−
                                                                        2
The Euclidean distance between two evolved states E = kT (δt)L |ψi − U (t)|ψik2 can be exactly represented with f
and θ.
                                                       p
                                            E 2 = 2 − 2 1 − f cos θ                                          (45)

From above estimation, we can quantify the upper/lower bound of E in terms of f and θ:
                                         p                        f       θ2      θ2
                                    2−2    1 − f cos θ ≥ 2 − 2(1 − )(1 − ) ≥ f +
                                                                  2       4        4
                                         p                               θ2
                                    2 − 2 1 − f cos θ ≤ 2 − 2(1 − f )(1 − ) ≤ 2f + θ2
                                                                         2
Combine them together:

                                                           θ2
                                                   f+         ≤ E 2 ≤ 2f + θ2
                                                           4


                                            Appendix B : Proof of Lemma 2

  Here we exhibit how to compare the spectrum and eigenstates of effective Hamiltonian {E      ek , |ψek i} with that of
original Hamiltonian {Ek , |ψk i} rigorously. The method has already been established in [22]. Magnus expansion sets
up connection between two types of exponential operators:
                                         Z t                                X
                                  expT −i      E(τ )dτ = exp(−iX), −iX =          Ωj
                                              0                                                    j
                                                  Z t               Z tn−1
                         1 X (−1)d (−i)j
                    Ωj = 2       d
                                         ·              dt1 · · ·            dtn [E(t1 ), · · · , [E(tn−1 ), E(tn )], · · · ]
                        j      Cj−1                0                 0
                             σ∈Sj
                                                                                                                          10

where Sj is permutation group and d is a constant related to a permutation. This infinite series {Ωj } is called Magnus
expansion. It has been proved that:
                                                                    αδt
                                             kH
                                              e − Hk ≤                  + δt2 (β + 32αkHk)
                                                                     2
With parameters defined in Lemma 2. There are lots of constrains for δt in the derivation, we summarize these
constraints by setting δt = O(N −1 ). As to kHe 0 k, previous results show:
                                                            Z δt
                                   e = H − i α̂δt + 1                      1 X
                                  H                              dxβ̂(x) +        Ωn (δt)
                                             2         δt 0                δt n=2
                                               X
                                          α̂ =       [Hl , Hm ], kβ̂(x)k ≤ x2 β
                                                     l>m
                                                               XZ            Z
                                                kΩn k ≤                ···       dt1 · · · dtn Cn
                                                                σ
                                         Cn ≤ 2n (kHk + αδt + βδt2 )n−1 (αδt + βδt2 )

When we upper bound the derivatives, we separate the above expression into three parts and consider the worst case:
(we write δt as t temporarily for abbreviation)
                                  Z t        0
                                                                1 t
                                                                  Z
                                   1                 1                           4
                               k       β̂(x)dx k ≤ kβ̂(t)k + 2       kβ̂(x)kdx ≤ βt
                                   t 0               t         t 0               3

Next we will prove k n=2 Ω0n (t)k ≤ ωt2 to directly use the above scenario.
                     P

                                  X                 X            tn−1
                              k         Ω0 (t)k ≤         n!            Cn
                                  n=2               n=2
                                                               (n − 1)!
                                                    X
                                                ≤         ntn−1 2n (kHk + αt + βt2 )n−1 (αt + βt2 )
                                                    n=2
                                                                     X
                                                = 2t(α + βt)               n(2kHkt + 2αt2 + 2βt3 )n−1
                                                                     n=2
                                                = 2t(α + βt)g(2kHkt + 2αt2 + 2βt3 )

where g(y) = (y 2 /(1 − y))0 < 4y + 4y 2 < 8y when y < 1/2. Thus:

                                                                ω = 128αkHk

Replace t with δt. Finally:

                                               e 0 (δt)k ≤          α 4
                                              kH                      + (β + 128αkHk)δt
                                                                    2  3

                                            Appendix C : Proof of Cororllary 1

  This result is a special case of Theorem 1. Here we prove it in aP         more direct way. Calculate the inner product
between U (t)|ψk i and T (δt)L |ψk i using spectral decomposition H      e =
                                                                              j Ej Pj :
                                                                                e e
                            p
                              1 − f eiθ = hψk |U † (t)T (δt)L |ψk i
                                           X
                                         =    ei(Ek −Ej )t |hψk |ψej i|2
                                                       e

                                                j
                                                                                 X
                                                i(Ek −E
                                                                                        ei(Ek −Ej )t |hψk |ψej i|2
                                                      ek )t
                                           =e                  |hψk |ψek i|2 +
                                                                                                 e

                                                                                 j6=k
                                                                                                                    
                                                                                    X
                                           = ei(Ek −Ek )t |hψk |ψek i|2 +                 ei(Ek −Ej )t |hψk |ψej i|2 
                                                    e                                         e   e

                                                                                    j6=k
                                                                                                                    11

Define ε and η as:
                                                                  X
                                  ε = 1 − |hψk |ψek i|2 ,    η=          ei(Ek −Ej )t |hψk |ψej i|2
                                                                            e   e

                                                                  j6=k

Then:

                               1 − f = |1 − ε + η|2 ,       θ = (Ek − E
                                                                      ek )t + Arg(1 − ε + η)

The complex number η is upper bounded by |η| ≤ ε and the equality is satisfied when all the phases (E
                                                                                                    ej − E
                                                                                                         ek )t differ
by 2πj, hence:

                                     f = O(1 − |hψk |ψek i|2 ),     θ = O(|E
                                                                           ek − Ek |t)

Combine with Lemma 2:
                                                     2 2
                                                     h δt
                                          f =O             ,       |θ| = O(Lhδt2 )
                                                      λ2
Of course, f = θ = 0 when L = 0. However, in this upper bound f is irrelevant to L. To fix this, notice we have
another upper bound for f from Eq : (7):

                                               f ≤ E 2 ≤ ∆2 = O(L2 h2 δt4 )



                                 Appendix D : Proof of Eq : (13) and Theorem 1

  Consider the norm distance between two projectors δp = kPx − Py k, Px = |xihx|, Py = |yihy|, one observation is
that this matrix is normal, hence its norm is the largest value of absolute eigenvalues of the following matrix:
                                                                    1 − a2 −ab
                                                                               
                                                      ⊥
                                      |yi = a|xi + b|x i, ∆P =
                                                                     −ab −b2

Although ∆P is only the representation of projector difference in a subspace spanned by {|xi, |yi}, other dimensions
won’t effect the spectrum of it. The parameters a, b can be set as non-negative real numbers for there are two degrees
of freedom on the phases of |yi and |x⊥ i. Also a2 is the fidelity between two states.
   Solve this matrix, the largest absolute value of ∆P is:
                                                          p
                                                 δp = b = 1 − |hx|yi|2

  We also also extend this result to multi-state projectors. Suppose we have two projectors PA and PB that each
corresponds to an m-dimensional subspace. A,B are the invariant spaces of the two projectors. To make the problem
meaningful, they should be close to each other in the sense that kPA − PB k < 1. In another word, A and B share
m − 1 dimensions. Then we can re-choose two sets of basis in A and B such that only one element is different. Then
the problem is reduced to the previous one. Based on this observation:

                                        min tr(PB |φa ihφa |) = 1 − kPA − PB k2
                                      |φa i∈HA

Similar result can be extended to mixed state, since the extreme status corresponds to pure state:

                                            min tr(PB ρa ) = 1 − kPA − PB k2                                      (46)
                                           ρa ∈HA

In Theorem 1, we have an original projector P that is composed of m eigenstate projectors, and an “effective” projector
Pe which is very close to P . Their norm distance has been well-quantified. Write:

                                                        δp ≡ kPe − P k

Our initial state ρ is a mixed state inside the space of P , which means tr(ρP ) = 1. In Eq : (46) we have proved that:

                                                     tr(ρPe) ≥ 1 − δp2
                                                                                                                 12

Now we want to quantify the leakage rate:

                                             1 − tr(U  e † P ) = 1 − tr(ρU
                                                    e ρU                 e †P U
                                                                              e)

where U
      e is the Trotterized evolution operator. Easy to see that [U
                                                                 e , Pe] = 0. Therefore:

                                                  e †P U
                                            kPe − U    e k = kPe − P k = δp
                                        e †P U
                                        U    e = P + (Pe − P ) + (Ue †P U
                                                                        e − Pe)
                                                     e †P U
                                                    kU    e − P k ≤ 2δp

Use the same argument in Eq : (46) we derive:

                                                  tr(ρUe †P U
                                                            e ) ≥ 1 − 4δp2
                                                 1 − tr(ρUe †P U
                                                               e ) = O(δp2 )

The leakage rate has order O(δp2 ).


                                          Appendix E : Proof of Lemma 3

  Define H(s) as:

                                                                     i X
                                        H(s) ≡ H + sV,         V ≡       [Hl , Hm ]
                                                                     2
                                                                      l>m

with eigenstates and eigenvalues:

                                                 H(s)|ψ(s)i = E(s)|ψ(s)i

The actual effective Hamiltonian satisfies H   e = H(δt) + V2 . Use the method in Lemma 2 we can prove kV2 k =
O(δt2 (β + 32αkHk)). We focus on the error in energy caused by H(s) first. Lemma 3 states that hψ(0)|V |ψ(0)i = 0.
To exploit this condition, define fidelity distance f (s) from the following equation:
                                                 p                   p
                                       |ψ(s)i = 1 − f (s)|ψ(0)i + f (s)|ψ(0)⊥ i

We don’t need eiθ(s) as there’s a degree of freedom on the phase of |ψ(s)i. Use the method in Corollary 1 we have:

                                      1 − |hψ(0)|ψ(s)i|2 = f (s) = kP (s) − P (0)k2
                                                                                         kV k
                               kP (s) − P (0)k ≤ s max kP 0 (x)k, max kP 0 (x)k ≤
                                                     x∈[0,s]          x∈[0,s]             λ
                    2 2
Hence, f (s) ≤ kVλk2 s . Since E(s) = hψ(s)|H(s)|ψ(s)i and hψ(0)|V |ψ(0)i = 0:

                    E(s) − E(0) =hψ(s)|H(s)|ψ(s)i − hψ(0)|H|ψ(0)i
                               =f (s)(hψ(0)⊥ |H|ψ(0)⊥ i − hψ(0)|H|ψ(0)i) + f (s)shψ(0)⊥ |V |ψ(0)⊥ i
                                     p
                                + s (1 − f (s))f (s)(hψ(0)|V |ψ(0)⊥ i + c.c)

Here we use the following argument for upper bound:
                                                          1
                                                   |φi = √ (|φi + |ψ ⊥ i)
                                                           2
                                             1
                                hφ|V |φi =     (hψ|V |ψi + hψ ⊥ |V |ψ ⊥ i + hψ|V |ψ ⊥ i + c.c)
                                             2
                                                  hψ|V |ψ ⊥ i + c.c ≤ 2kV k
                                                                                                                         13

Finally:

                                                     kV k2 · kHks2   2kV k2 s2   kV k3 s3
                                |E(s) − E(0)| ≤              2
                                                                   +           +
                                                           λ            λ          λ2
When kV ks < λ and kHk > 2λ, only the first term remains. Thus:

                                                                           kV k2 · kHkδt2
                                                                                            
                                        |E(δt) − E(0)| = O                                                              (47)
                                                                                 λ2

Quantify the error caused by V2 with Weyl’s inequality:

                              |E
                               e − E(0)| ≤ |E
                                            e − E(δt)| + |E(δt) − E(0)|
                                                                      kV k2 · kHkδt2
                                                                                    
                                               2
                                         = O(δt (β + 32αkHk)) + O
                                                                            λ2
                                                               
                                                              1
                                         = O N 2 δt2 max 1, 2
                                                              λ


                              Appendix F : Proof of Proposition 1 and Corollary 3

  The content in this Appendix is nothing more than combining Lemma 2 with Lemma 4. To quantify G(T, H),
                                                                                                     e our
target is the derivative of H(s) defined as:
                            e

                                  H(s)
                                  e    ≡ i log (exp(−it(1 − s)Hi ) exp(−itsHf )) /t

We use t to denote δt for simplicity in this Appendix. H
                                                       e satisfies:

                                 e−itH(s) = e−itHi · eistHi e−istHf = e−itHi e−itG(s)
                                     e                             


We separate the calculation of H
                               e into two parts. In the first part we take derivative with respect to t, and represent
H with Hi and G(s); next we calculate G(s) by taking derivatives with respect to s instead. The procedure is similar
 e
to that of Appendix B. The following special functions are used in the estimation:
                                                               ∞
                                                               X                1
                                                  F0 (x) =             xj =
                                                               j=0
                                                                               1−x
                                                      ∞
                                                      X1 j−1
                                         F1 (x) =        x    = − ln(1 − x)/x
                                                  j=1
                                                       j
                                                 ∞           Z x
                                                X    1 j
                                       F2 (x) =       2
                                                        x  =     − ln(1 − x0 )dx0
                                                j=2
                                                    j         0


They have the following upper bounds when 0 ≤ x ≤ 1/2:

                                                                                        x2
                                    F0 ≤ 1 + 2x,          F1 ≤ 1 + x,           F2 ≤       (1 + x)
                                                                                        2

We express H
           e in terms of G first. Under the setting of Magnus expansion:

                                       ∞
                                       X
                           −itH(s)
                              e    =         Ωj (s, t),    E(s, t) = −ie−itHi (Hi + G(s, t))eitHi
                                       j=1
                                                    Z t               Z tj−1
                                   1 X (−1)d
                       Ωj (s, t) = 2     d
                                                          dt1 · · ·            dtj [E(t1 ), · · · [E(tj−1 ), E(tj )]]
                                  j    Cj−1          0                 0
                                     σ∈Sj
                                                                                                                                          14

d is a constant relevant to permutation σ. As to H    e 0 (s), the integrand in Ω0 (s) becomes summation over j different
                                                                                  j
commutators; while for H e 00 (s), the integrand of Ω00 (s) contains j(j − 1) pairs of E 0 or j E 00 . Thus:
                                                     j

                                                  e 0 (s)k ≤ kG0 k · F1 (2(kHi + Gk)t)
                                                 kH
                               e 00 (s)k ≤ kG00 k · F1 (2(kHi + Gk)t) + 2kG0 k2 t · F0 (2kH + Gkt)
                              kH
The next step is to represent G(s, t) with Hi and Hf , and we consider s as variable instead.
                           d −itG(s,t)   e t)e−itG(s,t) , E(s,  e t) = eistHi (itHi − itHf )e−istHi
                             e         = E(s,
                          ds
                                                   Z s     Z s0                                   ∞
                                                                         00                 00    X
                     G(s, t) = its(Hi − Hf ) + t 2
                                                       ds0
                                                                ds00 eits Hi [Hi , Hf ]e−its Hi +   Ω
                                                                                                    e j (s, t)
                                                          0          0                                           j=2
                                                       d Z s               Z sj−1
                         e j (s, t) = 1
                                          X (−1)
                         Ω              2     d
                                                               ds1 · · ·            dsj [E(s1 ), · · · , [E(sj−1 ), E(sj )]]
                                      j     Cj−1          0                 0
                                          σ∈Sj

To abbreviate the result, define:
                        C0 ≡ kHi k,       C1 ≡ k[Hi , Hf ]k,         C2 ≡ k[Hi , [Hi , Hf ]]k,          D ≡ kHi − Hf k
                     e 1 (s, t) separately to derive a better result. The norm of G(s, t), G0 (s, t) and G00 (s, t) can be
Notice that we treat Ω
bounded by:
                                                                                1
                                                      kG(s, t)k ≤ sD +             F2 (2stD)
                                                                                2t
                                                      d
                                                  k      G(s, t)k ≤ D + stC1 F1 (2stD)
                                                      ds
                                   d2
                               k       G(s, t)k ≤ C1 t + 2C12 s2 t3 F0 (2stD) + C2 st2 (F1 (2stD) − 1)
                                   ds2
Combine everything together:
                                      kHe 0 (s)k ≤ [D + C1 t(1 + 2Dt)][1 + (2C0 + 3D)t]

            e 00 (s)k ≤ C1 t + 4C12 t3 + 2DC2 t3 [1 + (2C0 + 3D)t] + 2t (D + C1 t(1 + 2Dt))2
                                                                                                                             1
           kH
                                                                                                                       1 − (2C0 + 3D)t
Here it’s required that tD < 1/4 and (kHi k + max kG(s)k)t < 1/4.
  Put the above results in G(T, H):
                                 e
                                                                   !
                                         k e 0 (0)k kH    e 0 (1)k     1 1 kH    e 00 (s)k     e 0 (s)k2
                                                                                              kH
                                                                        Z
                                   1       H
                        G(T, H) =
                             e                       +               +                     +7             ds
                                   T       e 2
                                           λ(0)           e 2
                                                          λ(1)         T 0 λ     e2 (s)        e3 (s)
                                                                                               λ
                                     2            e 0 (s)k + 1 max kH    e 00 (s)k + 7 max kH      e 0 (s)k2
                                ≤      2
                                         max kH                   2
                                   Tλ                          Tλ                       T λ3
λ ≡ inf s {e
           λ(s)}. In this upper bound, He 00 (s) won’t appear in the leading term. Given N as the size of the system,
roughly, the magnitudes of quantities are t = O(N −1 ), D = O(N ), Ck = O(N k+1 ). As a result, kH
                                                                                                 e 0 k = O(N ), kH
                                                                                                                 e 00 k =
O(N ), and the leading term of the upper bound is:
                                                                                        
                                             1                      2                  2
                               tot ≤ O         (D +  C1 t(1 + 2Dt))  [1 + (2C0 + 3D)t]
                                          T λ3
                                                             2 !
                                             1         3C1 T
                                    =O            D+
                                          T λ3          2M

The maximal of the above upper bound is reached at:
                                                                   Tc   2D
                                                                      =                                                                  (48)
                                                                   M    3C1
We further requires that (8C0 + 12D)D ≤ 3C1 to let Tc satisfies (kHi k + max kG(s)k)T < M/4.
                                                                                                                           15

                               Appendix G : Trotter Error in Robust Phase Estimation

  The idea of Robust Phase Estimation is, begin with two quantum states:
                                                               1
                                                        |αi = √ (|0i + |1i)
                                                                2
                                                              1
                                                       |βi = √ (|0i + i|1i)
                                                               2
The target is the phase difference (E0 − E1 )t. It can be derived from the outcome of two measurements:
                                                              1
                                         Pα = |hα|U (t)|αi|2 =  (1 + cos((E1 − E0 )t))
                                                              2
                                                              1
                                         Pβ = |hα|U (t)|βi|2 = (1 + sin((E1 − E0 )t))
                                                              2
Thus:
                                                                             2Pβ − 1
                                                   tan((E1 − E0 )t) =
                                                                             2Pα − 1
Now let’s consider the Trotterized version:
                                                          p                  p
                                                  |0i =       1 − f0 |e
                                                                      0i +           0⊥ i
                                                                                 f0 |e
                                                          p                  p
                                                  |1i =       1 − f1 |e
                                                                      1i +           e⊥ i
                                                                                 f1 |1
                                               0i = e−iE0 t |e
                                            e |e
                                            U                0i ,         1i = e−iE1 t |e
                                                                       e |e
                                                                       U                1i
                                                       e                          e


From here we have:
                               1 −iEe0 t                 p                            p
              hα|U
                 e (t)|αi =      [e       + e−iE1 t + 2 f1 Re(he   0|e1⊥ i)e−iE0 t + 2 f0 Re(he 0⊥ |e
                                                                                                    1i)e−iE1 t ] + O(f )
                                                e                              e                          e
                               2
                                   e (t)|βi = 1 [e−iEe0 t + ie−iEe1 t + f0 e−iEe1 t (ihe
                                                                        p
                              hα|U                                                     0⊥ |e
                                                                                           1i + ihe 0⊥ i)
                                                                                                  1|e
                                              2
                                               p
                                             + f1 e−iE0 t (ihe   1⊥ i + h1
                                                               0|e        e⊥ |e
                                                                              0i)] + O(f )
                                                          e


And calculate the new probability:
                                                 1          e1 − E
                                                                             p
                                                                 e0 )t)] + O( f )
                                            Peα = [1 + cos((E
                                                 2
                                                 1          e1 − E
                                                                             p
                                                                 e0 )t)] + O( f )
                                            Peβ = [1 + sin((E
                                                 2
The final value for phase difference is:
                                                       "          #
                                                         2Peβ − 1
                                          δ θ = arctan
                                            e
                                                         aPeα − 1
                                                                               p
                                             = arctan(tan((Ee1 − Ee0 )t) + O( f ))
                                                                      √
                                                                  O( f )
                                             = (E1 − E0 )t +
                                                e     e                           + ···
                                                             1 + |Ee1 − Ee0 |2 t2
                                                                                   p
                                                     e1 − E1 − E
                                             = δθ + (E          e0 + E0 )t + O( f )
                                            √
The second equation is only true when O( f )  [1 + cos((E     e1 − Ee0 )t)]/2.
  We have proved that the trotter
                                √   error in fidelity doesn’t grow  linearly  with L. Thus, if t is a constant instead of a
small quantity, the effect of O( f ) can be neglected. The final error in energy difference has order:

                                                    |δ θe − δθ|/t = O(|E
                                                                       e − E|)

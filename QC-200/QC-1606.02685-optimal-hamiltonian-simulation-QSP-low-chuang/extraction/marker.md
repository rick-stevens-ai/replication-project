<!-- FALLBACK PARSE: neither Marker (`marker_single`) nor a pre-parsed copy of arXiv:1606.02685
     was available on this host at replication time. As a documented substitute, this file is a
     lightly cleaned-up `pdftotext -layout` dump of paper.pdf. It preserves the paper's textual
     content so that downstream corpus tools have a Markdown handle, but tables/equations may
     be reflowed. Rerun `marker_single paper.pdf` once Marker is installed to replace this. -->

# Optimal Hamiltonian Simulation by Quantum Signal Processing

Guang Hao Low, Isaac L. Chuang — MIT, 2016 (arXiv:1606.02685v2, Dec 2016).

                                                           Optimal Hamiltonian Simulation by Quantum Signal Processing

                                                                                         Guang Hao Low, Isaac L. Chuang
                                                            Department of Physics, Center for Ultracold Atoms, and Research Laboratory of Electronics
                                                                  Massachusetts Institute of Technology, Cambridge, Massachusetts 02139, USA
                                                                                           (Dated: December 22, 2016)
                                                            The physics of quantum mechanics is the inspiration for, and underlies, quantum computation. As
                                                         such, one expects physical intuition to be highly influential in the understanding and design of many
                                                         quantum algorithms, particularly simulation of physical systems. Surprisingly, this has been chal-
                                                         lenging, with current Hamiltonian simulation algorithms remaining abstract and often the result of
                                                         sophisticated but unintuitive constructions. We contend that physical intuition can lead to optimal
                                                         simulation methods by showing that a focus on simple single-qubit rotations elegantly furnishes an
                                                         optimal algorithm for Hamiltonian simulation, a universal problem that encapsulates all the power
                                                         of quantum computation. Specifically, we show that the query complexity of implementing time




arXiv:1606.02685v2 [quant-ph] 20 Dec 2016
                                                         evolution by a d-sparse Hamiltonian Ĥ for time-interval t with error  is O(tdkĤkmax + logloglog(1/)
                                                                                                                                                             (1/)
                                                                                                                                                                   ),
                                                         which matches lower bounds in all parameters. This connection is made through general three-
                                                         step “quantum signal processing” methodology, comprised of (1) transducing eigenvalues of Ĥ into
                                                         a single ancilla qubit, (2) transforming these eigenvalues through an optimal-length sequence of
                                                         single-qubit rotations, and (3) projecting this ancilla with near unity success probability.

                                                         PACS numbers: 03.67.Ac, 89.70.Eg


                                                      “If you want to make a simulation of nature,               plicable to generic quantum algorithms without this in-
                                                      you’d better make it quantum mechanical, and by
                                                                                                                 termediary. Indeed, the fact that intuition of the sim-
                                                      golly it’s a wonderful problem, because it doesn’t
                                                      look so easy.”                                             plest quantum control – discrete single-qubit rotations
                                                                                                                               θ
                                                                                                                 R̂φ (θ) = e−i 2 (σ̂x cos φ+σ̂y sin φ) – can extend to algorithms
                                                                                  Richard P. Feynman [1]         such as Grover search supports this notion.
                                               Introduction – Quantum computers are based on the                    This relationship is made concrete by interpreting dis-
                                            physics of quantum mechanics, a fundamental tenant of                crete sequences of physical operations as programs that
                                            Nature as we know it. Thus it seems natural to expect                compute functions. In the simplest setting, chaining N
                                                                                                                                                           N
                                            that the design and interpretation of quantum algorithms             identical rotations generates h1|R̂π/2       (θ)|0i = sin (N θ/2).
                                            be heavily driven by physical intuition. The adiabatic               With θ as the input, this computes the function f (θ) =
                                            algorithm [2, 3] inspired by adiabaticity, and quantum               sin (N θ/2), which may be estimated through measure-
                                            walks [4, 5] inspired by locality, are prominent examples.           ment. As Pauli matrices σ̂x,y,z form a complete basis for
                                            However, many quantum algorithms, most surprisingly                  2-by-2 matrices, generic sequences of the form
                                            those for the simulation of physical systems [6], are not
                                                                                                                     V̂ (θ) = R̂φN (θ)R̂φN −1 (θ) · · · R̂φ1 (θ),   ~ ∈ RN ,
                                                                                                                                                                    φ          (1)
                                            as similarly insightful, and successive improvements in
                                            their complexity and analysis trend towards increasing                          = A(θ)1̂ + iB(θ)σ̂z + iC(θ)σ̂x + iD(θ)σ̂y ,
                                            abstraction and mathematical sophistication.
                                               Analogous to physical theories, good quantum algo-                which we fully characterized in [8], then compute more
                                            rithms for physics simulations should, beyond being cor-             general functions of θ in the real A, B, C, D, through a
                                            rect, also ideally be simple. In seeking simplicity, not             program specified by some choice of phases φ.   ~ In fact,
                                            only is their implementation on physical machines eased,             the isomorphism of single-qubit rotations to those on a
                                            but so too could their performance and understanding be              sphere (up to a double covering), furnishes an intuitive
                                            enhanced. As the essence of coherent quantum computa-                classical interpretation for this simple model of quantum
                                            tion is the design of unitary operations with desired prop-          computation. Moreover, the quantum control in Eq. 1,
                                            erties, this motivates consideration of its closest analogue         being piecewise, is naturally compatible with the inher-
                                            in experiments: physical quantum control [7], which has a            ently discrete nature of fault-tolerant architectures.
                                            similar goal of designing quantum response functions [8].               Though physically appealing, the computational merit
                                               This hints at a deep connection between the design of             of directly exploiting the structure of single-qubit rota-
                                            optimal quantum algorithms and the synthesis of opti-                tions, or any physical system, ultimately rests on two cri-
                                            mal quantum control policies. While robust time-optimal              teria: (1) usefulness in solving important problems, and
                                            control [9, 10] is certainly an established tool in quan-            (2) optimality in space and time resources. It is also par-
                                            tum computing, its role is often secondary to the ends:              ticularly challenging to see how this approach could apply
                                            the synthesis of computing primitives, such as Clifford              generally to the complex multi-qubit dynamics arising in
                                            gates or even the quantum Fourier transform. It would                the simulation of quantum systems.
                                            be more desirable if physical dynamics were directly ap-                The simulation problem maps one set of physical dy-
                                                                                                                                                    2

namics of interest – described by Hamiltonian Ĥ – to                  a
                                                                                                                   
another physical system that can be precisely controlled.
                                                                                  
                                                                                  V θ                Rϕ1 θ          Rϕ2 θ       ⋯ R θ  ϕN

Thus one expects the role of physics to be preeminent and              b                                                                    
obvious. Following seminal work by Lloyd [11] for Hamil-                                            eⅈϕσz 2       Had          Had   e ⅈϕσz 2
                                                                                  Uϕ                                     
tonians with local interactions, and Aharonov and Ta-                                                                    W
Shma [12] for more general sparse Hamiltonians, many                   c                                
                                                                                                       Rϕ θλ
celebrated results have been obtained over the years [13–                         Uϕ
                                                                           uλ〉               uλ〉
19] for approximating the time evolution operator e−iĤt
                                                                       d
for time-interval t with error . Encouragingly, intuitive                                                                                
quantum walks are already part of state-of-art. More,                      ψ〉
                                                                                   V
                                                                                              ψ〉
                                                                                                            U ϕ1         U ϕ2    ⋯           U ϕN

however, could be hoped from their other components.
   The complexity of such quantum algorithms is usually                FIG. 1. Quantum circuits mapping (a) a sequence of single-
judged by the number of queries made to a unitary quan-                qubit rotations V̂ (θ) to (d) quantum signal processing V̂ .
tum oracle Ô that provides a description of Ĥ. Many                  Each single-qubit rotation R̂φ (θ) is replaced by (b) Ûφ , built
interesting physical system are described by the espe-                 from Hadamard gates and controlled-W with eigenstates
cially well-studied model of d-sparse Ĥ with at most d                Ŵ |uλ i = eiθλ |uλ i. Thus (c) Ûφ on input |uλ i reduces to a
non-zero elements in every row, and the best known al-                 single-qubit rotation R̂φ (θλ ). By linearity, V̂ on an arbitrary
gorithms [18] are based on the Childs quantum walk [14],               input |ψi may be understood as rotations V̂ (θλ ) controlled
which builds upon the Szegedy walk [20], that simulates                by a superposition of |uλ i. By some choice of single-qubit
                                                                       input state and measurement basis, coefficients of the |uλ i
time evolution by arcsin (Ĥ) which must be linearized.
                                                                       are then rescaled by the components of the function V̂ (θλ )
The difficulty lies in finding a quantum circuit that does                                ~
                                                                       programmed by φ.
this with the fewest queries to Ô and the fewest number
of additional primitive quantum gates.
   Lower bounds on the query cost are well-known. The
“no-fast-forwarding” theorem [13, 18] demands at least                 using the fewest queries to controlled-Ŵ for any real func-
Ω(τ ) queries independent of , where τ = tdkĤkmax and                tion h(θ). We call our solution to this “quantum sig-
kĤkmax is the largest element of Ĥ in absolute value,                nal processing” (Fig. 1), and its application to d-sparse
and impressive recent work [17, 18] proved an exact error              Hamiltonian simulation leads to tremendous simplifica-
                                                                       tion and the claimed improvements. Our success here
scaling of Θ logloglog(1/)
                             
                        (1/) for τ = O(1). Though this sug-           elevates optimal discrete quantum control in general as
gests a naive additive lower bound Ω τ + logloglog(1/)
                                                              
                                                         (1/) [18],   a tool that can be rigorous and essential in the design of
the best algorithms to date approach these factors multi-              optimal quantum algorithms, thus providing a medium
plicatively with either linear scaling in time O( √τ ) [14] or        through which physical intuition may flow.
sub-logarithmic scaling in error O τ logloglog(τ(τ /) 
                                                      /) [17, 21].
                                                                          Two key properties distinguish quantum signal pro-
Long unanswered is the existence of an algorithm that                  cessing from routines that can effect similar transforma-
is additively optimal, with implications for the relation              tions, such as quantum phase estimation [23] or linear-
between continuous and discrete-time models of physics,                combination-of-unitaries [16, 18, 19] which require a large
and of interest in problems [22] where τ,  scale together.            number of ancilla. First, is its intuitive use of just a sin-
   We achieve precisely this with a simple algorithm that              gle ancilla qubit. Second, the query complexity of the
matches the additive lower bound. In fact, it also real-               methodology is exactly the degree N of optimal trigono-
izes the optimal trade-off between time and error, thus no             metric polynomial approximations to eih(θ) with error
further improvement in query complexity for this formu-                 [24–27], without the decaying success probability of
lation of Hamiltonian simulation is possible. Compared                 prior art. Analogous to digital filter design techniques
to prior art [14, 17], this represents up to a square-root             in discrete-time signal processing [28] this also elegantly
improvement. Moreover, the space overhead in ancilla                   bridges the design of a number of quantum algorithms to
qubits, beyond those required for the quantum walk, is                 the vast field of function approximation [26].
reduced from scaling with some function of τ / to just 1.                In the following, we describe the reduction of quantum
   Most remarkably, this is achieved by finding a class of             signal processing to optimal quantum control, and show
computational problems addressed by the optimal con-                   how to efficiently choose the phases φ   ~ Eq. 1 such that
trol of the single-qubit in Eq. 1 in a very natural way.               any unitary transformation Eq. 2 is approximated with
Given a unitary Ŵ with eigenstates Ŵ |uλ i = eiθλ |uλ i,             error  and success probability 1 − O(). The essential
we consider the general problem of constructing a quan-                features of the quantum walk are then reviewed to show
tum circuit V̂ideal with transformed eigenphases                       how quantum signal processing for the special case of
                               X                                       h(θ) = −τ sin (θ) solves the sparse Hamiltonian simula-
             Ŵ 7→ V̂ideal =       eih(θλ ) |uλ ihuλ |,          (2)   tion problem. That this achieves lower bounds follows by
                                λ                                      analyzing the scaling between N, τ,  of quantum signal
                                                                                                                                 3

                                                                                                             †
processing for this h(θ).                                        uncomputed by alternating between Ûφ and Ûφ+π since
   Quantum signal processing – All quantum algo-                             †
                                                                 R̂φ (θ) = R̂φ+π (θ) and N is even.
rithms require a rigorous analysis of their resource costs          (c) Signal projection of the ancilla onto some basis,
in space and time. Thus any form of quantum control              to select desired components of V̂ (θλ ) in Eq. 1. As the de-
repurposed to such ends must have a similarly rigorous           sired phase transformation can be implemented through
characterization. Previously [8], we studied the optimal         A(θ), C(θ), Consider the input state |+i|uλ i, and posts-
control of arbitrary sequences of single-qubit rotations in      elect on measuring h+|. Other choices are of course pos-
Eq. 1, provided an intuitive characterization of the func-       sible. This applies onto state |uλ i the coefficient
tions A, B, C, D achievable by some choice of φ,~ and pro-
vided efficient algorithms for synthesizing all these func-      h+|V̂ |+i|uλ i = (A(θλ ) + iC(θλ )) |uλ i,                     (6)
tions and the required φ~ from some partial specification.
                                                                             p = min |h+|V̂ (θ)|+i| = min |A(θ) + iC(θ)|2 ,
                                                                                                         2
The results relevant here are:                                                    θ∈R                         θ∈R

Theorem 1 (Achievable (A,C)). ∀ even N > 0, a choice             with worst-case success probabilitiy p. Thus (a)-(c) pro-
of real functions A(θ), C(θ) can be implemented by some          vide a reduction from finding quantum algorithms for ap-
~ ∈ RN if and only if all these are true:
φ                                                                proximating V̂ideal to finding Fourier approximations of
(1) ∀θ ∈ R, A2 (θ) + C 2 (θ) ≤ 1. (2) A(0) = 1.                  A(θ) + iC(θ) to eih(θ) .
             PN/2                                                   By applying Thm. 1 to these three steps of quantum
(3) A(θ) = k=0 ak cos (kθ), {ak } ∈ RN/2+1 .
             PN/2                                                signal processing, we now prove following theorem which
(4) C(θ) = k=1 ck sin (kθ), {ck } ∈ RN/2 .                       furnishes the complexity of implementing V̂ideal given this
Moreover, φ ~ can be efficiently computed from A(θ), C(θ).
                                                                 Fourier approximation:
   Note that in [8], A, C are expressed as trigonometric         Theorem 2 (Quantum Signal Processing). ∀ real odd
polynomials, but can be rewritten a Fourier series (3),          periodic functions h : (−π, π] → (−π, π] and even
(4) using Chebyshev polynomials of the first and second          N > 0, let (A(θ), C(θ)) be real Fourier series in
kind Tk (cos (θ)) = cos (kθ) and Uk (cos θ) = sin ((k+1)θ)
                                                   sin θ   .     (cos (kθ), sin (kθ)), k = 0, ..., N/2, that approximate
   We now map these results, in three steps, to quan-
tum signal processing                                                         max |A(θ) + iC(θ) − eih(θ) | ≤ .                 (7)
                   P which transforms an arbitrary in-                         θ∈R
put unitary Ŵ = λ eiθλ |uλ ihuλ | into one with modified
eigenphases V̂ideal = λ eih(θλ ) |uλ ihuλ |:
                      P
                                                                 Given A(θ), C(θ), one can efficiently compute the φ~ such
   (a) Signal transduction of Ŵ into a signal unitary           that h+|V̂ |+i in Eq. 5 applies Ûφ a number N times to
classically controlled by φ ∈ R:                                 approximate V̂ideal in Eq. 2 with success probability p ≥
                     P                                           1 − 16 and trace distance
               Ûφ = λ R̂φ (θλ ) ⊗ |uλ ihuλ |.            (3)
                                                                          Tr = max k(h+|V̂ |+i − V̂ideal )|ψik ≤ 8.           (8)
                                                                                 |ψi
This is implemented in Fig. 1b with one controlled-Ŵ ,
which is always possible on a quantum computer in the               Note that the restricted symmetry of h(θ) is for con-
worst-case by replacing all of its gates with controlled         sistency with the parity and periodicity of A(θ), C(θ).
version, and O(1) single-qubit rotations:                           Given A(θ), C(θ) that satisfy Eq. 7, conditions (1), (2)
                                                                 of Thm. 1 will not generally be satisfied. (1) is violated
           Ûφ = (e−iφσ̂z /2 ⊗ 1̂)Û0 (eiφσ̂z /2 ⊗ 1̂),    (4)   as maxθ (|A(θ)|, |C(θ)|) ≤ 1 + . Thus we rescale
           Û0 = |+ih+| ⊗ 1̂ + |−ih−| ⊗ Ŵ
                                                                    A1 (θ) = A(θ)/(1 + ),        C1 (θ) = C(θ)/(1 + ),        (9)
               = λ eiθλ /2 R̂0 (θλ ) ⊗ |uλ ihuλ |,
                 P
                                                                                              ih(θ)
                                                                    |(A1 (θ) + iC1 (θ)) − e           | ≤ /(1 + ) +  ≤ 2,
                |0i+|1i
where |±i =       √
                    2
                        .   As Ûφ acting on |uλ i selects the   at the cost of a slightly larger error 2. Note that
                                                                                   2
rotation R̂φ (θλ ) = huλ |Ûφ |uλ i as seen in Fig. 1c, these    A21 + C12 ≥ 1−                                          1−
                                                                                1+ . (2) is violated as A1 (0) = cos δ ≥ 1+
are precisely the single-qubit ancilla rotations in Eq. 1
                                                                 for some δ ∈ R. Fixing this is more involved. As V̂ (θ)
with rotation angle θλ controlled by the λ index, but
                                                                 is unitary, A21 + B 2 + C12 + D2 = 1. We can apply
with an additional global phase eiθλ /2 .
                                                                 the prescription in [8] using polynomial sum-of-squares
  (b) Signal transformation by computing unitary
                                                                 to compute the unspecified B, D from A1 , C1 such that
functions V̂ (θλ ) over a superposition of θλ on the single-     B, D are of the form (3) and (4) respectively. Thus
qubit ancilla through the simple circuit of Fig. 1d:
                                                                 A21 (0) + B 2 (0) = 1, and |B(0)| = | sin δ|. Define
       V̂ = ÛφN ÛφN −1 · · · Ûφ1 ,   ~ ∈ RN , N even.
                                        φ                  (5)                   A2 (θ) = A1 (θ) cos δ + B(θ) sin δ,  (10)
                                                                                                           √
As this invokes Ŵ a number N times, its query cost                                         2            2 
                                                                       |A2 (θ) − A1 (θ)| ≤       + |B(θ)|       ≤ 6.
is O(N ). Note that the unwanted phase eiθλ /2 can be                                      1+            1+
                                                                                                                             4

This introduces an additional error by using the triangle       controlled Ŵ 1,...,N such that the success probability de-
                                              2     4
inequality and B 2 ≤ 1 − A21 − C12 ≤ 1 − 1−
                                          1+    = (1+) 2.
                                                                cays with N . Our quantum signal processing method-
By construction, A2 (0) = 1. The functions A2 (θ), C1 (θ)       ology, does not experience such a decay and its direct
thus satisfy Thm. 1. By adding the errors in Eqs. 9, 10,        application furnishes an optimal Hamiltonian simulation
the distance of h+|V̂ |+i from V̂ideal in Eq. 2 and the         algorithm
worst-case success probability in Eq. 6 are                       Hamiltonian Simulation – Applying quantum sig-
                                                                nal processing in Thm. 2 to Hamiltonian simulation re-
      Tr ≤ max |A2 (θ) + iC1 (θ) − eih(θ) | ≤ 8,      (11)    quires a good Fourier approximation to
             θ∈R

        p ≥ (1 − 8)2 ≥ 1 − 16.                                            A(θ) + iC(θ) ≈ eih(θ) = e−iτ sin (θ) ,         (15)
   The optimality of this remarkably simple procedure           which is provided by the Jacobi-Anger expansion [30]
for eigenphase transformation follows from its role in ob-
                                                                                               P∞
taining the best possible quantum algorithm for d-sparse          cos (τ sin (θ)) = J0 (τ ) + 2 k even>0 Jk (τ ) cos (kθ),
Hamiltonian simulation. We now highlight essential fea-                               P∞
                                                                   sin (τ sin (θ)) = 2 k odd>0 Jk (τ ) sin (kθ),         (16)
tures of a quantum walk Ŵ constructed from the oracles
Ô describing sparse Ĥ.                                        where Jk (τ ) are Bessel functions of the first kind. Note
   Childs’ quantum walk [14] – Ŵ can be constructed            that these Fourier series are already in the form re-
from oracles that specify a d-sparse Hamiltonian Ĥ with        quired by conditions (3), (4) of Thm. 1. As |Jk (τ )| ≤
n-qubit eigenstates Ĥ|λi = λ|λi. Access to two ora-             1   τ |k|
                                                                |k|! 2     [30] decays rapidly with k, good approxima-
cles ÔH , ÔF is commonly assumed: ÔH accepts the in-
put (j, k) ∈ [2n ] × [2n ] on 2n-qubit registers and returns    tions are obtained truncating Eq. 16 at k > N/2. This
Hj,k = hj|Ĥ|ki in another m-qubit register. ÔF accepts        approximates e−iτ sin (θ) with error shown in [18] for
the input (j, l) ∈ [2n ] × [d] on the same 2n-qubit registers   τ ≤ N/2 = q − 1 to be
and computes in place the column index f (j, l) ∈ [2n ] of                     ∞
the lth nonzero element in the j th row of Ĥ.
                                                                               X                    4τ q     eτ q 
                                                                          ≤         2|Jk (τ )| ≤    q
                                                                                                         =O            .   (17)
                                                            †
   It is well-known [29] that with 1 query to ÔF , ÔH , ÔH                                       2 q!       2q
                                                                               k=q
each and O(n + m poly(log m)) primitive gates, one
can implement an isometry T̂ that maps every state              Inserting into Thm. 2, the query complexity of Hamil-
|λi|0i⊗n+m+2 onto two eigenstates |λ±i of Ŵ :                  tonian simulation follows by solving Eq. 17 for N , using
                                          √                     the implementation of Ûφ in Eq. 4 with O(1) queries, and
                 T̂ |λi = (|λ+i + |λ−i) / 2.             (12)   that V̂ in Eq. 5 contains N applications of Ûφ .
                                                                  The optimality of this result for all input param-
Moreover, T̂ is constructed such that the walk Ŵ =             eters follows from known lower bounds. Specifically,
iŜ(2T̂ T̂ † − 1̂) has eigenvalues Ŵ |λ±i = eiθλ± |λ±i,        Eq. 17 is matched with a corresponding lower bound
     θλ± = ± arcsin (λ/kĤkmax d) + (1 ∓ 1)π/2,         (13)    N = Ω(q) [18, 31] for any q satisfying

                                                                                     1     τ  q     τ q 
that depends on the Ĥ eigenvalues λ. As Ŵ corresponds                        <      sin        =O           .           (18)
                                                                                     2      q           q
to reflection about T̂ T̂ † followed by swapping (2n + 2)-
qubit registers with Ŝ, its query and gate complexities          Note that Eqs. 17, 18 are solved by the Lambert W -
are identical to T̂ up to constant factors.                     function [32] which captures the detailed trade-off be-
  Hamiltonian simulation is achieved by creatively ap-          tween τ and . Its asymptotic behavior may be under-
plying Ŵ some number of times to implement |λ±i 7→             stood by substituting q = 2e (τ +γ), where τ, γ ≥ 0. When
e−iλt |λ±i, independent of the ± index. Uncomputing
                                                                τ = O(γ), one finds γ = O logloglog(1/)
                                                                                                          
with T̂ † then maps |λ±i back onto |λi|0i⊗n+m+2 with                                                 (1/) . Thus we express
                                                                the complexity of Hamiltonian simulation as
the desired phase evolution. However, some difficulties
arise. First, the applied phase θλ± is nonlinear in λ. Sec-     Theorem 3 (Optimal sparse Hamiltonian simulation).
ond, each eigenstate |λ±i evolves under Ŵ with phases in       A d-sparse Hamiltonian Ĥ on n qubits with matrix el-
opposite directions. Thus uncomputing with T̂ † does not        ements specified to m bits of precision can be simulated
map Ŵ T̂ |λi|0i⊗n+m+2 back onto the basis |λi|0i⊗n+m+2 .       for time-interval t, error , and success probability at least
In [18], these are overcome by approximating the unitary                                      log (1/) 
                                                                1−2 with O tdkĤkmax + log log (1/) queries and a factor
transformation in Eq. 2 with target function
                                                                O((n + mpolylog(m))) additional quantum gates.
          h(θ) = −τ sin (θ) ⇒ h(θλ± ) = −λt,            (14)
                                                                  This is valid for τ = O( logloglog(1/)
                                                                                                      (1/) ) and stronger than
resulting in the desired phase, but implemented us-             prior art [17, 18] which assumes τ = O(1). Unlike
ing a technique combining a linear combination of N -           most Hamiltonian simulation algorithms, the query cost
                                                                                                                             5

is additive in the simulation length τ and the target er-       [11] S. Lloyd, “Universal quantum simulators,” Science 273,
ror . As such, the τ term matches the lower bound                   1073 (1996).
Ω(τ ) [13, 18] with no multiplicative dependence on error.      [12] D. Aharonov and A. Ta-Shma, “Adiabatic quantum state
                                                                     generation and statistical zero knowledge,” in Proceed-
   Conclusion – We have shown that optimal quantum
                                                                     ings of the Thirty-fifth Annual ACM Symposium on The-
algorithms for Hamiltonian simulation can be remark-                 ory of Computing, STOC ’03 (ACM, New York, NY,
ably simple and physically-motivated. Here, physical in-             USA, 2003) pp. 20–29.
tuition flows into the process by directly using the dy-        [13] D. W. Berry, G. Ahokas, R. Cleve, and B. C. Sanders,
namics of discrete single-qubit rotations as a computa-              “Efficient quantum algorithms for simulating sparse
tional module, which proves to be exceptionally useful               hamiltonians,” Commun. Math. Phys. 270, 359–371
when translated into quantum signal processing. Indeed,              (2007).
                                                                [14] A. M. Childs, “On the relationship between continuous-
we have focused on choosing target functions (A, C) for
                                                                     and discrete-time quantum walk,” Commun. Math. Phys.
even N in Thm. 1, but many other choices described                   294, 581–603 (2010).
in [8] are possible. For example, fixed-point ampli-            [15] A. M. Childs and R. Kothari, “Theory of quantum com-
tude amplification [33] and Heisenberg-limited quantum               putation, communication, and cryptography,” (Springer
imaging [34] are special cases for the choice (A(θ) ∝                Berlin Heidelberg, 2011) pp. 94–103.
TN (β cos(θ/2)), B(θ) = 0), β > 1.                              [16] A. M. Childs and N. Wiebe, “Hamiltonian simulation us-
   Directly exploiting the structured dynamics in other              ing linear combinations of unitary operations,” Quantum
                                                                     Info. Comput. 12, 901–924 (2012).
physical systems could lead to powerful tools for a sim-
                                                                [17] D. W. Berry, A. M. Childs, R. Cleve, R. Kothari, and
ilarly intuitive approach to rigorous and optimal quan-              R. D. Somma, “Exponential improvement in precision
tum algorithms. The question of what other important                 for simulating sparse hamiltonians,” in Proceedings of the
quantum algorithms can be designed or improved in this               46th Annual ACM Symposium on Theory of Computing,
manner is an exciting natural extension to this work.                STOC ’14 (ACM, New York, NY, USA, 2014) pp. 283–
   Acknowledgements – G.H. Low and I.L. Chuang                       292.
thank Cedric Yen-Yu Lin, Robin Kothari, and Matthew             [18] D. W. Berry, A. M. Childs, and R. Kothari, “Hamil-
                                                                     tonian simulation with nearly optimal dependence on
Hastings for insightful discussions, and acknowledge
                                                                     all parameters,” in Foundations of Computer Science
funding by the ARO Quantum Algorithms Program, the                   (FOCS), 2015 IEEE 56th Annual Symposium on (2015)
NSF CUA, and NSF RQCC Project No.1111337.                            pp. 792–809.
                                                                [19] D. W. Berry, A. M. Childs, R. Cleve, R. Kothari, and
                                                                     R. D. Somma, “Simulating hamiltonian dynamics with
                                                                     a truncated taylor series,” Phys. Rev. Lett. 114, 090502
                                                                     (2015).                                        √
 [1] R. P. Feynman, “Simulating physics with computers,”        [20] M. Szegedy, “Spectra of quantized walks and a δ rule,”
     International Journal of Theoretical Physics 21, 467–488        arXiv preprint quant-ph/0401053 (2004).
     (1982).                                                    [21] R. Cleve, D. Gottesman, M. Mosca, R. D. Somma, and
 [2] E. Farhi, J. Goldstone, S. Gutmann, and M. Sipser,              D. Yonge-Mallo, “Efficient discrete-time simulations of
     “Quantum computation by adiabatic evolution,” arXiv             continuous-time quantum query algorithms,” in Proceed-
     preprint quant-ph/0001106 (2000).                               ings of the Forty-first Annual ACM Symposium on The-
 [3] A. Mizel, D. A. Lidar, and M. Mitchell, “Simple proof of        ory of Computing, STOC ’09 (ACM, New York, NY,
     equivalence between adiabatic quantum computation and           USA, 2009) pp. 409–416.
     the circuit model,” Phys. Rev. Lett. 99, 070502 (2007).    [22] G. J. Sussman and J. Wisdom, “Numerical evidence that
 [4] A. M. Childs, “Universal computation by quantum                 the motion of pluto is chaotic,” Science 241, 433–437
     walk,” Phys. Rev. Lett. 102, 180501 (2009).                     (1988).
 [5] A. M. Childs, D. Gosset, and Z. Webb, “Universal com-      [23] M. A. Nielsen and I. L. Chuang, Quantum Computation
     putation by multiparticle quantum walk,” Science 339,           and Quantum Information, 1st ed. (Cambridge Univer-
     791–794 (2013).                                                 sity Press, 2004).
 [6] I. M. Georgescu, S. Ashhab, and F. Nori, “Quantum          [24] J. McClellan, T. Parks, and L. Rabiner, “A computer
     simulation,” Rev. Mod. Phys. 86, 153–185 (2014).                program for designing optimum FIR linear phase digital
 [7] K. Khodjasteh, D. A. Lidar, and L. Viola, “Arbitrarily          filters,” IEEE Trans. Audio Electroacoust. 21, 506–526
     accurate dynamical control in open quantum systems,”            (1973).
     Phys. Rev. Lett. 104, 090501 (2010).                       [25] R. Pachón and L. N. Trefethen, “Barycentric-remez al-
 [8] G. H. Low, T. J. Yoder, and I. L. Chuang, “The method-          gorithms for best polynomial approximation in the cheb-
     ology of composite quantum gates,” arXiv preprint               fun system,” BIT Numerical Mathematics 49, 721–741
     arXiv:1603.03996 (2016).                                        (2009).
 [9] T. Caneva, M. Murphy, T. Calarco, R. Fazio, S. Mon-        [26] M. J. D. Powell, Approximation theory and methods
     tangero, V. Giovannetti, and G. E. Santoro, “Optimal            (Cambridge University Press, 1981).
     control at the quantum speed limit,” Phys. Rev. Lett.      [27] L. N. Trefethen, Approximation theory and approxima-
     103, 240501 (2009).                                             tion practice (Siam, Philadelphia, 2013).
[10] K. Khodjasteh and L. Viola, “Dynamically error-            [28] A. Oppenheim and R. Schafer, Discrete-time Signal Pro-
     corrected gates for universal quantum computation,”             cessing (3rd Ed.), Prentice-Hall signal processing series
     Phys. Rev. Lett. 102, 080501 (2009).
                                                                                                                            6

     (Prentice Hall, 2010).                                    [32] R. M. Corless, G. H. Gonnet, D. E. G. Hare, D. J. Jeffrey,
[29] D. W. Berry and A. M. Childs, “Black-box hamiltonian           and D. E. Knuth, “On the lambert w function,” Advances
     simulation and unitary implementation,” Quantum Info.          in Computational Mathematics 5, 329–359 (1996).
     Comput. 12, 29–62 (2012).                                 [33] T. J. Yoder, G. H. Low, and I. L. Chuang, “Fixed-point
[30] M. Abramowitz, I. A. Stegun, et al., “Handbook of math-        quantum search with an optimal number of queries,”
     ematical functions,” Applied mathematics series 55, 62         Phys. Rev. Lett. 113, 210501 (2014).
     (1966).                                                   [34] G. H. Low, T. J. Yoder, and I. L. Chuang, “Quan-
[31] R. Kothari, (private communication).                           tum imaging by coherent enhancement,” Phys. Rev. Lett.
                                                                    114, 100801 (2015).

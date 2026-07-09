<!-- BACKFILL 2026-07-05: pdftotext -layout fallback (Marker not installed locally).
     Source: paper.pdf (fetched from https://arxiv.org/pdf/quant-ph/9601018)
     SHA256: d6edeff2d388fc0229cda2d28379fb45336b1eda2df748c2802d21b257f1b556
     arXiv:quant-ph/9601018
     Backfill from central Marker corpus when available. -->

                                               Approximate Quantum Fourier Transform and
                                                             Decoherence

                                            Adriano Barencoa , Artur Ekerta , Kalle-Antti Suominenb and Päivi Törmäc

                                        a
                                          Clarendon Laboratory, Department of Physics, University of Oxford, Parks Road, OX1




arXiv:quant-ph/9601018v1 21 Jan 1996
                                                                            3PU Oxford, U.K.
                                       b
                                         Theoretical Physics Division, Department of Physics, University of Helsinki, PL 9, 00014
                                                                       Helsingin yliopisto, Finland
                                       c
                                         Research Institute for Theoretical Physics, University of Helsinki, PL 9, 00014 Helsingin
                                                                            yliopisto, Finland




                                                                         November 26, 2024


                                                                               Abstract
                                                We discuss the advantages of using the approximate quantum Fourier trans-
                                             form (AQFT) in algorithms which involve periodicity estimations. We analyse
                                             quantum networks performing AQFT in the presence of decoherence and show
                                             that extensive approximations can be made before the accuracy of AQFT (as
                                             compared with regular quantum Fourier transform) is compromised. We show
                                             that for some computations an approximation may imply a better performance.



                                             PACS: 89.70.+c, 03.65.-w, 42.50.Lc        Submitted to Phys. Rev. A. (Jan. 96)


                                       1    Introduction
                                       In the course of history many ingenious mechanical, acoustic and optical devices have
                                       been invented for performing Fourier transforms [1] (including nature’s own such as
                                       the human ear). Most of them are now of merely historical interest since the arrival of
                                       the computer–based algorithm known as the fast Fourier transform (FFT) [2, 3] which
                                       efficiently computes the discrete Fourier transform. The FFT algorithm can also be
                                       phrased in terms of quantum dynamics, i.e., in terms of unitary operations performed
                                       by a quantum computer on quantum registers. Indeed, all known quantum algorithms
                                       employ the quantum version of Fourier transforms, either explicitly or indirectly. It
                                       is used for the periodicity estimation in the Shor algorithm [4] and its approximate
                                       version (the Hadamard transform) is commonly used to prepare quantum registers
                                       in coherent superpositions of different values.
                                              In this paper we analyse the performance of the quantum Fourier transform
                                       (QFT) in the presence of decoherence. In particular we show that as far as the peri-

                                                                                   1
odicity estimation is concerned the approximate quantum Fourier transform (AQFT)
can yield better results than the full Fourier transform.
      In the following we use some terms which were originally adopted from the
classical theory of information and computer science and became standard in the lore
of quantum computation. More detailed descriptions can be found e.g. in Refs. [5, 6,
7] and in some recent reviews [8].

    • A qubit is a two–state quantum system; it has a chosen ‘computational basis’
      {|0i, |1i} corresponding to the classical bit values 0 and 1. Boolean operations
      which map sequences of 0’s and 1’s into another sequences of 0’s and 1’s are
      defined with respect to this computational basis. A collection of L qubits is
      called a register of size L.

    • Information is stored in the registers in binary form. For example, number 6 is
      represented by a register in state |1i ⊗ |1i ⊗ |0i. In more compact notation: |ai
      stands for the direct product |aL−1 i ⊗ |aL−2 i . . . |a1 i ⊗ |a0 i which represents a
      quantum register prepared with the value a = 20 a0 + 21 a1 + . . . 2L−1 aL−1 .

    • A quantum logic gate is an elementary quantum computing device which per-
      forms a fixed unitary operation on selected qubits in a fixed period of time.

    • A quantum network is a quantum computing device consisting of quantum
      logic gates whose computational steps are synchronised in time. The outputs
      of some of the gates are connected by wires to the inputs of others. The size
      of the network is its number of gates.

    • A quantum computer will be viewed here as a quantum network (or a family of
      quantum networks). Quantum computation is defined as a unitary evolution of
      the network which takes its initial state “input” into some final state “output”.

      Our presentation starts with a brief mathematical introduction to the approxi-
mate discrete Fourier transform which is followed by the description of its quantum
implementation in terms of quantum networks. Then we analyse how the perfor-
mance of the QFT in the periodicity estimation is affected by the approximations in
the algorithms and by decoherence. We also comment on possible simplifications in
practical implementations of quantum networks effecting the QFT and AQFT. The
quantum algorithm for the fast Fourier transform which we use in this paper was
originally proposed by Coppersmith and by Deutsch (independently) [9].


2    Discrete Fourier Transforms
The discrete Fourier transform is a unitary transformation of a s–dimensional vector
{f (0), f (1), f (2), . . . , f (s − 1)} defined by:

                               ˜       1 s−1
                                              e2πiac/s f (a),
                                          X
                               f (c) = √                                                (1)
                                        s a=0




                                             2
where f (a) and f˜(c) are in general complex numbers. It can also be represented as
a unitary matrix
                                                                       
                         1        1          1      ...       1
                        1        ω          ω2     ... ω    (s−1)
                                                                   
                                                                    
                         1        ω2         ω4     . . . ω 2(s−1) 
                                                                   
                     1 
                     √ 
                        1        ω3         ω6     . . . ω 3(s−1) 
                                                                    
                                                                      ,             (2)
                      s
                        .
                                                                    
                        .         ..         ..    ..         ..   
                        .          .          .        .       .   
                                                                    
                                                                  2
                             1 ω (s−1) ω 2(s−1)     . . . ω (s−1)

where ω = exp(2πi/s) is the sth root of unity. In the following we assume that s is
a power of 2, i.e., s = 2L for some L; this is a natural choice when binary coding
is used. The approximate discrete Fourier transform can be conveniently described
when we write the product ac in the exponent on the r.h.s. of Eq. (1) in the binary
notation. Writing
                               L−1                        L−1
                                         i
                                                                ci 2i
                               X                          X
                          a=         ai 2    ;     c=                               (3)
                               i=0                        i=0
we obtain

            ac = a0 c0 + (a0 c1 + a1 c0 )2 + (a0 c2 + a1 c1 + a2 c0 )22 + . . .
                 + (a0 cL−1 + . . . + aL−1 c0 )2L−1 + O(2L ).                       (4)

Because ω x = 1 for x ≥ s, the terms O(2L ) do not contribute to the transform, and
the term exp(2πiac/2L ) in Eq. (1) can be expressed as

       exp(2πiac/2L ) = exp(2πi(a0 c0 )/2L ) exp(2πi(a0 c1 + a1 c0 )/2L−1 ) . . .
                             × exp(2πi(a0 cL−1 + . . . + aL−1 c0 )/2).              (5)

Beginning from the right of this expression, the arguments in the exponentials become
smaller and smaller. In the approximate Fourier transform parameterised by an
integer m, the L − m smallest terms are neglected. In all the remaining terms the
arguments are then multiples of 2π/2m . The 2m th root of unity becomes the basic
element of the approximate Fourier transform as opposed to 2L th root of unity which
used in the ordinary Fourier transform. (The ordinary Fourier transform is obtained
for m = L; when m = 1 we obtain the Hadamard transform, for which all terms but
the last one are dropped.)
      The quantum version of the discrete Fourier transform is a unitary transfor-
mation which can be written in a chosen computational basis {|0i, |1i, . . . , |s − 1i}
as
                                        1 s−1
                                            X
                      QFTs : |ai 7−→ √          exp(2πiac/s) |ci.                   (6)
                                          s c=0
More generally, QFTs effects the discrete Fourier transform of the input amplitudes.
If
                                                    f˜(c)|ci,
                                X                X
                        QFTs :      f (a)|ai 7−→                                 (7)
                                     a                c

then the coefficients f˜(c) are the discrete Fourier transforms of f (a)’s. This defini-
tion can be trivially extended to cover the approximate quantum Fourier transform

                                             3
(AQFT). We will analyse the approximations involved in the AQFT in terms of
computational networks.


3    Quantum Networks for AQFT
Quantum networks for AQFT can be constructed following the description of the
fast Fourier transform algorithm (as described by Knuth [10]). This efficient classical
algorithm needs to be re–expressed in terms of unitary operations [9]. The con-
struction requires only two basic unitary operations. The first operation is a one–bit
transformation Ai (one–bit gate) that acts on a qubit qi of the register and effects

               |0i −→ √12 (|0i + |1i)
                                                            qi    Ai               (8)
               |1i −→ √12 (|0i − |1i).

The diagram on the right provides a schematic representation of the gate acting on
a qubit q. The second operation is a two–bit gate Bjk that effects

          |00i −→ |00i                      qj       ✈           qj    θjk
          |01i −→ |01i
                                                           ≡                       (9)
          |10i −→ |10i                      qk                   qk
                                                   θjk                  ✈
          |11i −→ exp(iθjk )|11i

where θjk depends on the qubits j and k on which the gate acts and equals θjk =
π/2k−j . The transformation Bjk is an elementary two qubit operation which affects
only states with a 1 in both position j and k regardless the state of the remaining
qubits.
      The QFT on a register of size 1 reduces to a single operation A performed on
a single qubit (cf. equation (6) for s = 2). The extension of the QFT network to a
register of any size L follows a simple pattern of gates A and B which can be seen
in Fig. 1. It shows the QFT network operating on four qubits which can be written
as the sequence of the following 10 elementary operations (read from left to right)

                      (A3 )(B23 A2 )(B13 B12 A1 )(B03 B02 B01 A0 ).               (10)

The bit values at the output should be read in the reversed order (see Fig. 1).
      The number of gates needed to complete the QFT grows only as a quadratic
function of the size of the register: for a transformation on a L qubit register, we
require L operations A and L(L − 1)/2 operations B, in total L(L + 1)/2 elementary
operations. Thus the quantum QFT can be performed efficiently.
      The AQFT of degree m is represented by a similar network in which the two–
bit gates that act on qubits which are far apart (in the register) are neglected, i.e.,
those operations Bjk for which the phase shift θjk ≡ π/2k−j < π/2m for some m
such that 1 ≤ m ≤ L are dropped (cf. Eq.(5)). In that case, we need L operations
A, and (2L − m)(m − 1)/2 operations B, which is an improvement on the QFT case
since m < L. In Fig. 2 we show the m = 2 AQFT network counterpart to the QFT
network shown in Fig. 1. The matrix elements of the QFT and the AQFT differ by
a multiplicative factors of the form exp(iǫ) with |ǫ| ≤ 2πL/2m . The execution time
of the AQFT grows as ∼ Lm.

                                           4
4    Estimating Periodicity
The quantum Fourier transform, like the ordinary Fourier transform, is a powerful
tool for uncovering periodicities. Any periodicity in probability amplitudes describing
a quantum state of a register in a computational basis can be estimated (with some
probability of success) by performing the QFT followed by a measurement of the
register in the computational basis. The result is obtained by reading the qubits of
the register in the reversed order.
      For example, an interesting periodic state which plays an important role in
Shor’s quantum factoring algorithm can be written as
                                            L
                                      1 2X−1
                               |Ψi = √       f (a)|ai,                             (11)
                                       N a=0

where N is an appropriate normalisation factor and

                                  f (a) = δl, a mod r .                            (12)

It is the state of a quantum register of size L in which the probability amplitudes
f (a) occur with periodicity r and offset l. If this offset is unknown, a measurement
performed in the computational basis cannot reveal r or any of its integer multiples
directly. This is illustrated in Fig. 3(a). However, if we perform the QFT on the
register first and subsequently measure its state we obtain number c̄ which, with
probability greater than 4/π 2 , is a multiple of 2L /r regardless the offset l (cf. Ap-
pendix). The probability is not equal to unity, because the finite size of the register
leads to a “broadening” of the Fourier–transformed data, as illustrated in Fig. 3(b).
(This is because 2L /r is not necessarily an integer, and the quantum register can
have only integer values; this is discussed in detail in the Appendix).
      For the AQFT the corresponding probability, in the limit of large L, satisfies
                                      8      πm
                                                         
                              ProbA ≥ 2 sin2    .                                  (13)
                                     π       4L
This result is derived in the Appendix. The effect of the approximation is illustrated
in Fig. 4 where we plot the modulus of the amplitude of the transformed state |Ψi
(with l = 9 and r = 10) for the AQFT of different orders m. Fig. 5 shows how the
phase of the transformed state becomes corrupted when m becomes smaller.
      If the quantum Fourier transform forms a part of a randomised algorithm then
the computation can be repeated several times in order to amplify the probability of
the correct result. In such cases the performance of the AQFT is only polynomially
less efficient than that of the QFT. For example, consider Shor’s quantum factoring
algorithm and substitute the AQFT for the QFT. In order to obtain a correct factor
with a prescribed probability of success, we have to repeat the computation several
times. Let k and k′ be the number of runs respectively with the QFT and the AQFT
so that we obtain the same probability of getting at least one correct result, i.e.,
                                                              ′
                             1 − (1 − p)k = 1 − (1 − p′ )k .                       (14)



                                           5
                                            
Here p = 4/π 2 and p′ = π82 sin2 π4 m
                                    L are the corresponding probabilities of success
                            ′
in a single run. The ratio k /k scales as
                                                       
                          k′              log 1 − π42                     
                                                                              L
                                                                                  3
                               =                                < C                               (15)
                          k        log 1 − π82 sin2        4m                 m
                                                           π L

for some C (the upper bound is found graphically). This shows that in the quantum
factoring algorithm the AQFT is not less efficient than the ordinary QFT, i.e., the
ratio k′ /k scales only polynomially with L/m. Moreover, we will show that in the
presence of decoherence the AQFT can perform better than the QFT even in a single
computational run!


5    Decoherence
Quantum computation requires a controlled, quantum–mechanically coherent evo-
lution at the level of individual quantum systems such as atoms or photons. This
imposes severe requirements on quantum computer hardware. If we are to harness
the unique power of quantum computers, such systems will have to be manufactured
with unprecedented tolerances and shielded from noise to an unprecedented degree.
Even a minute interaction with the environment will lead to a non–unitary evolution
of the computer and its state will, in general, evolve into a mixed state described
by a reduced density operator ρ, which is obtained from the density operator ρtotal
of the total computer+environment system by taking a trace over all the quantum
states of the environment:
                                     ρ = Trenvironment (ρtotal ).                                     (16)
Consider, for example, a quantum register of size L which is prepared initially in some
pure state and then left on its own. As time goes by, the qubits become entangled
with the environment. Both the diagonal and the off–diagonal elements of the density
matrix ρ (expressed in a computational basis) are usually affected by this process
(cf. [11, 12]). The rate of change of the diagonal and the off–diagonal elements
depends on the type of coupling to the environment, however, there are realistic
cases where the dissapearance of the off–diagonal elements, known as decoherence,
takes place on much faster time scale. In this case a simple mathematical model of
decoherence has been proposed [13]. It assumes that the environment effectively acts
as a measuring apparatus, i.e., a single qubit in state c0 |0i + c1 |1i evolves together
with the environment as
                         (c0 |0i + c1 |1i)|ai −→ c0 |0i|a0 i + c1 |1i|a1 i,                           (17)
where states |ai, |a0 i, |a1 i are the states of the environment and |a0 i, |a1 i are usually
not orthogonal (ha0 |a1 i 6= 0). The elements of the density matrix evolve as
         ρij (0) = ci (0)c∗j (0) −→ ρij (t) = ci (t)c∗j (t)hai (t)|aj (t)i,            i, j = 0, 1.   (18)
States |a0 i and |a1 i become more and more orthogonal to each other whilst the
coefficients {ci } remain unchanged. Consequently the off–diagonal elements of ρ
disappear due to the ha0 (t)|a1 (t)i factor and the diagonal elements are not affected.

                                                   6
      There is an alternative way of thinking about this process. The environment
is regarded as a bosonic heat bath, which introduces phase fluctuations to the qubit
states, i.e., it induces random phase fluctuations in the coefficients c0 and c1 such
that
                         c0 | 0i + c1 | 1i → c0 e−iφ | 0i + c1 eiφ | 1i .        (19)
The direction and the magnitude of each phase fluctuation φ is chosen randomly
following the Gaussian distribution
                                               "     2 #
                                     1         1      φ
                         P (φ)dφ = √     exp −               dφ,                    (20)
                                     2πδ       2      δ

where the distribution width δ defines the strength of the coupling to the quantum
states of the environment. The elements of the density matrix ρ are then recon-
structed as ρij = hci c∗j i, where the average hi is taken over different realisations of
the phase fluctuations within a given period of time (cf. [12]). The diagonal elements
do not depend on φ, whereas the off–diagonal term hc0 c1 ei2φ i averages to zero for a
sufficiently long period of time.
      The latter approach to decoherence is very convenient for numerical simulations
and was chosen for the purpose of this paper. It is similar to the Monte Carlo wave
function method used in quantum optics [14].


6    AQFT and Decoherence
We have analysed decoherence in the AQFT networks assuming that the environment
introduces a random phase fluctuation in a qubit probability amplitudes each time the
qubit is affected by gate B. In our model we have not attached any decoherence effects
to gate A. In most of the suggested physical realisations the single qubit operations
are quite fast, whereas the conditional logic needed in two–qubit operations is often
much harder to produce, which makes these operations slower than the single qubit
ones, and often much more susceptible to decoherence. For instance, in the ion trap
model proposed by Cirac and Zoller [15] single qubit operations require only one laser
pulse interacting with one atom, whereas in a two–qubit operation two subsequent
laser pulses are needed, and the atoms involved must form an entangled state with a
trap phonon mode between the pulses. In any case, introducing decoherence to gate
A operations and ‘wires’ in the network would not affect our results much, only the
time scale for decoherence would change.
      We have quantified the performance of the AQFT by introducing the quality
factor Q. It is simply the probability of obtaining an integer which is closest to
any integer multiple of 2L /r, when the state of the register is measured after the
transformation. In the decoherence free environment analysed in Sec. 4 we obtain
Q = 1 for integer values of 2L /r and for a randomly selected r the
                                                                    quality factor Q
                    2                                   8    2 4m
is of the order 4/π for the QFT and of the order of π2 sin π L for the AQFT of
degree m.
      In Fig. 6 we show how the quality factor Q behaves as a function of m and δ
(which characterises the strength of the coupling to the environment). For δ > 0


                                           7
the maximum of Q is obtained for m < L. Thus in the presence of decoherence one
should use the AQFT rather than the QFT.
     This ‘less is more’ result can be easily understood. The AQFT means less
gates in the network and because each B gate introduces phase fluctuations the
approximate network generates less decoherence as compared to the regular QFT
network. By decreasing m we effectively decrease the impact of decoherence. On the
other hand decreasing m implies approximations which reduces the quality factor.
This trade-off between the two phenomena results in the maximum value Q for
m ∈ [1, L].
     It is worth pointing out that for δ = 0 (no decoherence) Q remains almost
constant for those values of m that satisfy the lower bound condition (derived in the
Appendix)
                                  m > log2 L + 2.                                (21)
and when δ > 0 the optimum m is found near this lower bound. In Fig. 7 we also
show how Q decreases rapidly with L in the QFT network (although there is not
enough data in the figure to determine if it really decreases exponentially).
     Our simulations were performed for ensembles which consisted typically of a
one to two thousands individual realisations.


7    Conclusions and comments
We have analysed the approximate quantum Fourier transform in the presence of de-
coherence and found that the approximation does not to imply a worse performance.
On the contrary, using the periodicity estimation as an example of a computational
task, we have shown that for some algorithms the approximation may actually imply
a better performance.
      Needless to say, there is room for further simplifications of the quantum Fourier
transform which may lead to at least partial suppressing of unwelcome effects of
decoherence. For example, if the QFT is followed by a bit by bit measurement of the
register then the conditional dynamics in the network can be converted to a sequence
of conditional bit by bit measurements (cf. [16]). Here, we wanted to show that there
are cases where quantum networks that are composed of imprecise components can
guarantee a ‘pretty good performance’. This topic has also a more general context;
it has been shown that reliable classical networks can be assembled from unreliable
components [17]. It is an open question whether a similar result holds for quantum
networks.

Acknowledgements
A. B. thanks E. S. Trounz for discussions. A. E. is supported by the Royal Society.
A. B. acknowledges the Berrow fund at Lincoln College (Oxford), and K.-A. S. and
P. T. acknowledge the Academy of Finland for financial support, and thank A. E.
and the rest of the group for kind hospitality during visits to Oxford.




                                          8
Consider the quantum state
                                                  L
                                         1 2X−1
                                  |Ψi = √       f (a)|ai,                           (22)
                                          N a=0

where
                                     f (a) = δl, a mod r .                          (23)
Here f (a) is a periodic function with period r ≪ 2L and offset l, which is an arbitrary
positive integer smaller than r; see Fig. 3(a). The normalization factor is equal to
the number of non–zero values f (a): N = [2L /r]. Because r ≪ 2L we use from
now on [2L /r] ≃ 2L /r. The state (22) plays an important role in the Shor quantum
factorisation algorithm (the algorithm enables us to factorise an integer N by finding
r such that xr = (1 mod N ) for some x coprime with N — r is estimated from a
quantum computation that generates a state of the form (22).)
      Applying QFT to this state we obtain

                                                      f˜(c)|ci,
                                              X
                                     |Ψ̃i =                                         (24)

where
                              √ 2L /r−1
                                 r X
                       f˜(c) = L        exp(2πi(jr + l)c/2L ).                      (25)
                               2   j=0

The probability of seeing an integer c is then
                                                                              2
                                          2L /r−1
                                r
            Prob(c) = |f˜(c)| = 2L
                              2                                       L   L
                                            X
                                                      exp(2πij(rc mod 2 )/2 ) .     (26)
                               2            j=0

As it can be seen from Fig. 3(b) the peaks of the power spectrum of f (a) are centered
at integers c which are the closest approximation to multiplies of 2L /r.
      Let us now evaluate Prob(c̄) for c̄ being the closest integer to λ2L /r, i.e., c̄ =
[λ2L /r]. By definition c̄ must satisfy

                                        1          2L  1
                                    −     < c̄ − λ    < .                           (27)
                                        2           r  2
We define θc̄ = 2π(rc̄ mod 2L ) so that Prob(c̄) now involves a geometric series
with ratio exp(iθc̄ ). By viewing these terms as vectors on an Argand diagram it
is clear that the total distance from the origin decreases as θc̄ increases. Hence
Prob(c̄) ≥ Prob( c̄ with largest allowed θc̄ ). Let us denote by θmax the largest allowed
θc̄ . By Eq. (27), θmax ≤ πr/2L and summing the geometric series with θmax = πr/2L
(see Fig. 8) we obtain
                                          r       1        4 1
                          Prob(c̄) ≥                    ≃      ,                   (28)
                                          2L               π2 r
                                                 
                                         2 sin 2   π r
                                                     L  22




                                              9
where we have used the fact that r/2L is small. Since there are r such values c̄, the
total probability of seeing one of them is

                                                Prob ≥ 4/π 2 .                                             (29)

By performing this measurement several times on different states |Ψi (each one with
possibly different l), one gets with high probability values c̄0 , c̄1 , . . . that are the
closest integers to n0 2L /r, n1 2L /r, . . . and which allow to calculate r [cf. inset in
Fig. 3(b)].
      We estimate now the probability of measuring one of the desired values c̄ when
the AQFT of order m has been performed instead of the QFT. The difference between
the QFT and the AQFT of order m is in the arguments of the exponentials in Eq.
(26). The phase difference for each term in the sum is
                                                                                     
                                                L−1
                                      2π 
                                                      aj ck 2j+k  ,
                                                X
                             ∆(a, c) = L ac −                                                              (30)
                                      2       (j,k)∈E

where
               E = {(j, k) | 0 ≤ j, k ≤ L − 1, L − m ≤ j + k ≤ L − 1} .                                    (31)
     The probability to measure |c̄i, where c̄ is the closest integer to one of the r
values n2L /r now becomes
                                                                                                       2
                                 2L /r−1
                       r
                                           exp(2πij(rc mod 2L )/2L − i∆(jr, c)) .
                                     X
           ProbA (c) = 2L                                                                                  (32)
                      2              j=0

This is the same summation as is involved in the QFT, except that in the case of the
AQFT, each vector of the Argand diagram of Fig. 8(a) may be rotated by an angle
∆(jr, c), as shown in Fig. 9. In the worst case, when a = c = 2L − 1, i.e., ai = ci = 1
∀i, ∆(a, c) is equal to
                                               2π
                               ∆max =             (L − m − 1 + 2m−L ).                                     (33)
                                               2m
However, for any other values of a and c, 0 ≤ ∆(a, c) < ∆max .
      We are interested in the lower bound for the probability so we assume that the
vectors in the Argand diagram fill one half of the circle (θmax = πr/2L ) as illustrated
in Fig. 8(b). The approximation allows to rotate each vector by the maximum angle
∆max . The minimum of the probability is obtained when half of the vectors are
rotated by ∆max , see Fig. 9(b). In this case vectors in two areas of size ∆max cancel
each other, and all we have to do is to calculate geometrical sums of the vectors in  
                                                                          L
the two areas of size π/2 − ∆max . In an area of that size there are 2r 12 − ∆max   π
vectors, since the total number of vectors is 2L /r. Note that because 2L ≫ r, we can
assume that [2L /r] ± 1 ≃ 2L /r. The square of the geometric sum then becomes
                                                         2
               2L         ∆max
                    ( 12 −X    )−1
                                                                                              
                                                                            1   π
                                                                 sin2
                                                                                         
                                                                                2 − ∆max
                r          π
                                          πr
                                                    
                                                                            2
                                     exp i L j               =                                   .       (34)
                       j=0
                                          2                             sin2        π r
                                                                                    2 2L



                                                         10
      The two sum vectors in the two areas of size π/2 − ∆max are of equal length
and orthogonal to each other, so the square of their sum vector, contributing to the
total probability, is twice the value given by (34). Finally we obtain
                                                          
                                     1    π
                          sin2
                                                   
                     r2                   2 − ∆max               8      1          π
                                                                                            
                                     2
         ProbA ≥ 2 2L                                        ≃ 2 sin2              − ∆max        .   (35)
                  2              sin2         π r               π       2          2
                                              2 2L

For ∆max = 0 this expression reduces to the result derived for the QFT:
                                                 8        π              4
                                                                
                             ProbA ≥               2
                                                     sin2            =      ,                          (36)
                                                 π        4              π2

and for ∆max = π/2 we have ProbA ≥ 0. To avoid a zero probability, ∆max must
always be bounded by
                                         2π                      π
                          ∆max =          m
                                            (L − m − 1 + 2m−L ) < ,                                    (37)
                                         2                       2
which for large L implies
                                           m > log2 L + 2.                                             (38)
Eq. (21) gives a lower bound to the order of the AQFT performed on a register
of length L, if one wants to have a non–zero probability of success in measuring a
value c̄. Simple geometric considerations also show that ∆max < π/2 is a limit for a
non–negligible probability: for ∆max > π/2 the vectors in the Argand diagram can
be rotated so that there is no longer any constructive interference, see Fig. 10.
      For large L we can write
                                                         2π
                                         ∆max ≃             (L − m).                                   (39)
                                                         2m
If we use the lower bound for m (21), we obtain

                                                π    m
                                                                    
                                         ∆max ≤   1−   ,                                               (40)
                                                2    L

which allows to write the probability (35) in a simple form

                                                     8        πm
                                                                        
                                 ProbA ≥               2
                                                         sin2    .                                     (41)
                                                     π        4L

References
 [1] J. B. J. Fourier, Théorie Analytique de la Chaleur (F. Didot, Paris, 1822);
     reprinted (Gabay, Sceaux, 1988); translated The Analytical Theory of Heat
     (Dover, New York, 1955).

 [2] J. W. Cooley and J. W. Tukey, Math. Computation 19, 297 (1965).

 [3] E. O. Brigham, The Fast Fourier Transform (Prentice Hall, Englewood Cliffs,
     N.J., 1974).


                                                         11
 [4] P. W. Shor, in Proceedings of the 35th Annual Symposium on the Foundations
     of Computer Science, edited by S. Goldwasser (IEEE Computer Society Press,
     Los Alamitos, CA, 1994), p. 124.

 [5] A. Barenco, D. Deutsch, A. Ekert, and R. Jozsa, Phys. Rev. Lett. 74, 4083
     (1995); D. Deutsch, A. Barenco, and A. Ekert, Proc. R. Soc. London, Ser. A
     449, 669 (1995); A. Barenco, ibid. 449, 679 (1995).

 [6] T. Sleator and H. Weinfurter, Phys. Rev. Lett. 74, 4087 (1995).

 [7] V. Vedral, A. Barenco, and A. Ekert, submitted to Phys. Rev. A.

 [8] A. Barenco, Physics and Quantum Computers, to appear in Contemporary
     Physics (1996). C. Bennett, Phys. Today 48(10), 24 (1995); D. P. DiVincenzo,
     Science 270, 255 (1995); S. Lloyd, Sci. Am. 273(4), 44 (1995).

 [9] D. Coppersmith, IBM Research Report No. RC19642 (1994); D. Deutsch, un-
     published.

[10] D. E. Knuth, The Art of Computer Programming, Volume 2: Seminumerical
     Algorithms, 2nd ed. (Addison–Wesley, Reading, MA, 1981).

[11] W. Unruh, Phys. Rev. A 51, 992 (1995).

[12] G. M. Palma, K.–A. Suominen, and A. Ekert, to appear in Proc. R. Soc. London
     Ser. A (1996).

[13] W. H. Zurek, Phys. Today 44(10), 36 (1991).

[14] J. Dalibard, Y. Castin, and K. Mølmer, Phys. Rev. Lett. 68, 580 (1992); Y.
     Castin, K. Mølmer, and J. Dalibard, J. Opt. Soc. Am. B 10, 524 (1993).

[15] J. I. Cirac and P. Zoller, Phys. Rev. Lett. 74, 4091 (1995).

[16] R. B. Griffiths and C. S. Niu, Semiclassical Fourier Transform for Quantum
     Computation, Carnegie Mellon University preprint (1995), quant–ph/9511007
     (unpublished).

[17] U. Feige, P. Raghavan, D. Peleg, and U. Upfal, SIAM J. Comput. 23, 1001
     (1994).




                                         12
       a0                                                 ✈      ✈      ✈     A      c3

       a1                           ✈       ✈     A                   θ10            c2

       a2             ✈     A             θ21                  θ20                   c1

       a3     A      θ32           θ31                  θ30                          c0




Figure 1: QFT network operating on a four–bit register. The phases θjk that appear
in the operations Bjk are related to the “distance” of the qubits (j − k) and are given
by θjk = π/2j−k . The network should be read form the left to the right: first the
gate A is effected on the qubit a3 , then B(φ32 ) on a2 and a3 , and so on.


       a0                                                               ✈     A      c3

       a1                                   ✈     A                   θ10            c2

       a2             ✈     A             θ21                                        c1

       a3     A      θ32                                                             c0




      Figure 2: AQFT network operating on a four–bit register when m = 2.

Figure 3: (a) Function f (a) in Eq. (12). The parameters are l = 8, r = 10 and the
number of bits in the calculation is L = 9 so that numbers up to 2L − 1 = 511 can be
encoded. (b) |f˜(c)|, obtained from f (a) by a QFT. The inset shows c̄3 = 155 which
is the closest integer to 3 · 512/10 = 153.6. (See the Appendix for more details).

Figure 4: Different orders of approximation in the AQFT performed on a state |Ψi
for which f (a) = δ 9, a mod 10 .


  Figure 5: As Fig. 4, but showing the phase of the amplitudes, i.e., arg(f˜(c)).

Figure 6: The quality factor Q as a function of m for selected values of δ. The register
sizes are (a) L = 9 and (b) L = 16. Statistical errors are too small to be represented
on the graph.


                                          13
Figure 7: The quality factor Q as a function of the register size L for QFT, with
varying levels of decoherence, from δ = 0.1 (top line) to δ = 0.5 (bottom line).
Statistical errors are too small to be represented on the graph.




Figure 8: (a) Argand diagram corresponding to the sum of the phases that appear
in the expression of f (c̄) for c̄ close to one of the values n2L /r. Prob(c̄) is the norm
of the vector resulting from the sum of each vector in the diagram. (b) Prob(c̄) is
bounded by the worst case situation in which we have taken θmax instead of θc̄ , in
this case the phases lie on an interval [0, π] on the Argand diagram and a closed form
expression can be found.




Figure 9: (a) Argand diagram for the AQFT. Vectors are rotated by an angle
∆(jr, c). (b) To obtain a closed form for a bound for ProbA (c̄) we consider the worst
case in which half of the phases pick up a factor ∆max .




Figure 10: In the case that the order m of the AQFT is such that ∆max > π/2,
the individual phases can get scrambled in such a way that there is no constructive
interference effect. The probability ProbA (c̄) can become vanishingly small and the
AQFT of order m is inefficient.




                                           14
                                                                       L
                                                                   ni 2r     ci
 (a)                                (b)
                                                           0.4

|f(a)|                             ~
                                  |f(c)|                   0.2

         l   r r   r                           L L
                                           2 2             0
                                            r r                  150       155
 0.1                                0.2



 0                                  0
         0   20    40 a 480 500            0         200    c      400
                         m=9 (QFT)                                               m=5

         0.3                                                   0.3


         0.2                                                   0.2
|f(c)|
~                                                     |f(c)|
                                                      ~
         0.1                                                   0.1

          0                                                     0
               0   100    200       300   400   500                  0   100   200       300   400   500
                                c                                                    c

                           m=3                                           m=1 (Hadamard)

         0.3                                                   0.3


         0.2                                                   0.2
|f(c)|
~                                                     |f(c)|
                                                      ~
         0.1                                                   0.1

          0                                                     0
               0   100    200       300   400   500                  0   100   200       300   400   500
                                c                                                    c
              [rad]         m=9 (QFT)                                  [rad]           m=5
               4                                                         4
               3                                                         3
               2                                                         2

Arg( f(c) )                                              Arg( f(c) )
~              1                                         ~               1
               0                                                         0
              -1                                                        -1
              -2                                                        -2
              -3                                                        -3
              -4                                                        -4
                 0    100    200       300   400   500                     0   100   200       300   400   500
                                   c                                                       c

              [rad]           m=3                                      [rad]   m=1 (Hadamard)
                4                                                        4
                3                                                        3
                2                                                        2

Arg( f(c) )                                              Arg( f(c) )
~               1                                        ~               1
                0                                                        0
               -1                                                       -1
               -2                                                       -2
               -3                                                       -3
               -4                                                       -4
                  0   100    200       300   400   500                     0   100   200       300   400   500
                                   c                                                       c
a)                         L=12           b)                             L=16

     0.8                                       0.8

     0.6                                       0.6
Q                                         Q
     0.4                                       0.4

     0.2                                       0.2

       0                                        0
           0   2   4   6   8 10   12 14              0   2   4   6   8    10 12 14 16
                            m                                             m
    1
                               =0.01



                               =0.02
Q 0.5

                               =0.03


    0
        6   8   10   12   14     16    18   20
                          L
(a)       (b)



      c         max
(a)   (b)
            max

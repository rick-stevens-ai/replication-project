# Marker Extraction (Fallback via pdftotext -layout)

*Note: Marker (VikParuchuri/marker) was not available in this environment
(requires torch + heavy vision-transformer weights; not installed per the
"no paid endpoints / no heavy install" constraint of this replication wave,
and Python 3.14 wheels are not yet published for the marker stack). This
extraction was produced via `pdftotext -layout` from the arXiv PDF as a
faithful, reading-order text fallback that preserves column structure.*

**Source:** `paper.pdf` — arXiv:quant-ph/9603004v2 (Lo & Chau, PRL 78, 3410, 1997)
**Extraction tool:** `pdftotext -layout` (poppler)
**Command:** `pdftotext -layout work/paper.pdf work/paper_layout.txt`

---

                                                                  Is Quantum Bit Commitment Really Possible?

                                                                                  Hoi-Kwong Lo∗ and H. F. Chau†
                                                      School of Natural Sciences, Institute for Advanced Study, Olden Lane, Princeton, NJ 08540
                                                                                          (November 26, 2024)
                                                    We show that all proposed quantum bit commitment schemes are insecure because the sender,
                                                   Alice, can almost always cheat successfully by using an Einstein-Podolsky-Rosen type of attack and
                                                   delaying her measurement until she opens her commitment.

                                                   PACS Numbers: 89.70.+c, 03.65.Bz, 89.80.+h

                                         Work on quantum cryptography was started by S. J.               that all proposed QBC schemes are insecure: A dishon-
                                      Wiesner in a paper written in about 1970, but remained             est party can exploit the non-local Einstein-Podolsky-
                                      unpublished until 1983 [1]. Recently, there have been              Rosen (EPR) [18] type correlations in quantum mechan-




arXiv:quant-ph/9603004v2 2 Apr 1997
                                      lots of renewed activities in the subject. The most well-          ics to cheat successfully. To do so, she generally needs
                                      known application of quantum cryptography is the so-               to maintain the coherence of her share of a quantum sys-
                                      called quantum key distribution (QKD) [2–4], which is              tem by using a quantum computer. We remark that all
                                      useful for making communications between two users to-             proposed QBC schemes contain an invalid implicit as-
                                      tally unintelligible to an eavesdropper. QKD takes ad-             sumption that some measurements are performed by the
                                      vantage of the uncertainty principle of quantum mechan-            two participants. This is why this EPR-type of attack
                                      ics: Measuring a quantum system in general disturbs it.            was missed in earlier analysis.
                                      Therefore, eavesdropping on a quantum communication                   Let us first introduce bit commitment. A bit com-
                                      channel will generally leave unavoidable disturbance in            mitment scheme generally involves two parties, a sender,
                                      the transmitted signal which can be detected by the legit-         Alice and a receiver, Bob. Suppose that Alice has a bit
                                      imate users. Besides QKD, other quantum cryptographic              (b = 0 or 1) in mind, to which she would like to be
                                      protocols [5] have also been proposed. In particular, it is        committed towards Bob. That is, she wishes to provide
                                      generally believed [4] that quantum mechanics can pro-             Bob with a piece of evidence that she has already chosen
                                      tect private information while it is being used for public         the bit and that she cannot change it. Meanwhile, Bob
                                      decision. Suppose Alice has a secret x and Bob a secret            should not be able to tell from that evidence what b is.
                                      y. In a “two-party secure computation” (TPSC), Alice               At a later time, however, it must be possible for Alice
                                      and Bob compute a prescribed function f (x, y) in such a           to open the commitment. In other words, Alice must be
                                      way that nothing about each party’s input is disclosed to          able to show Bob which bit she has committed to and
                                      the other, except for what follows logically from one’s pri-       convince him that this is indeed the genuine bit that she
                                      vate input and the function’s output. An example of the            had in mind when she committed.
                                      TPSC is the millionaires’ problem: Two persons would                  A concrete example of an implementation of bit com-
                                      like to know who is richer, but neither wishes the other           mitment is for Alice to write down her bit in a piece of
                                      to know the exact amount of money he/she has.                      paper, which is then put in a locked box and handed
                                         In classical cryptography, TPSC can be achieved ei-             over to Bob. While Alice cannot change the value of the
                                      ther through trusted intermediaries or by invoking some            bit that she has written down, without the key to the
                                      unproven computational assumptions such as the hard-               box Bob cannot learn it himself. At a later time, Alice
                                      ness of factoring large integers. The great expectation            gives the key to Bob, who opens the box and recovers the
                                      is that quantum cryptography can get rid of those re-              value of the committed bit. This illustrative example of
                                      quirements and achieve the same goal using the laws of             implementation is, however, inconvenient and insecure.
                                      physics alone. At the heart of such optimism has been              A locked box may be very heavy and Bob may still try
                                      the widespread belief that unconditionally secure quan-            to open it by brute force (e.g. with a hammer).
                                      tum bit commitment (QBC) schemes exist [6]. Here we                   What do we mean by cheating? As an example, a
                                      put such optimism into very serious doubt by showing               cheating Alice may choose a particular value of b during
                                                                                                         the commitment phase and tell Bob another value during
                                                                                                         the opening phase. A bit commitment scheme is secure
                                                                                                         against a cheating Alice only if such a fake commitment
                                       ∗
                                         Present Address: BRIMS, Hewlett-Packard Labs, Fil-              can be discovered by Bob. For concreteness, it is instruc-
                                      ton Road, Stoke Gifford, Bristol BS12 6QZ, UK. e-mail:             tive to consider a simple QBC protocol due to Bennett
                                      hkl@hplb.hpl.hp.com                                                and Brassard [2]. Its procedure goes as follows: Alice and
                                       †
                                         Present Address: Department of Physics, University              Bob first agree on a security parameter, a positive integer
                                      of Hong Kong, Pokfulam Road, Hong Kong.        e-mail:             s. The sender, Alice, chooses the value of the committed
                                      hfchau@hkusua.hku.hk
                                                                                                         bit, b. If b = 0, she prepares and sends Bob a sequence


                                                                                                     1
of s photons each of which is randomly chosen to be ei-           defeat an EPR-type of attack. Our goal here is to demon-
ther horizontally or vertically polarized. Of course, the         strate that, contrary to popular belief, precisely the same
value of b is kept secret during the commitment phase.            type of EPR attack defeats all proposed QBC schemes.
Moreover, the actual polarization of each photon chosen              All proposed schemes involve only one-way communi-
by Alice is not announced to Bob. Similarly, if b = 1, she        cations from Alice to Bob. On the conceptual level, they
prepares and sends Bob a sequence of s photons each of            all involve Alice sending two quantum systems to Bob,
which is randomly chosen to be either 45-degree or 135-           one during the commit phase and the other during the
degree polarized but once again the actual polarization           opening phase. [There is no loss of generality in our anal-
of each photon is kept secret by Alice. Bob chooses ran-          ysis in considering quantum communications alone since
domly between the rectilinear (horizontal and vertical)           classical communications is just a special case of quantum
and diagonal (45-degree or 135-degree) bases to measure           communications.] More precisely, the general procedure
the polarization of each photon. This completes the com-          of any proposed QBC scheme can be rephrased in the
mitment phase. A simple calculation shows that, the two           following manner:
density matrices describing the s photons corresponding              (1) Alice chooses the value of a bit b to which she would
to b = 0 and b = 1 respectively are exactly the same (and         like to be committed towards Bob. If b = 0, she prepares
are proportional to the identity matrix). Consequently,           a state
Bob cannot learn anything about the value of b.                                        X
                                                                                 |0i =     αi |ei iA ⊗ |φi iB ,            (1)
   At a later time, Alice may open her commitment by
                                                                                         i
announcing the value of b and the actual polarization of
each of the s photons. Since Bob has chosen his ba-               where hei |ej iA = δij but the normalized states |φi iB ’s
sis (rectilinear or diagonal) of measurement randomly             are not necessarily orthogonal to each other. Similarly,
for each photon in the commitment phase, on average,              if b = 1, she prepares a state
only half of the s photons, have been measured by him                                  X
                                                                                 |1i =    βj |e′j iA ⊗ |φ′j iB ,        (2)
in the correct basis. For those photons, Bob can verify
                                                                                         j
that Alice’s announced polarizations match his measure-
ment results. Baring EPR attacks, a cheating Alice may,           where he′i |e′j iA = δij but |φ′j iB ’s are not necessarily or-
for example, send rectilinear photons in the commitment           thogonal to each other.
phase (hence commits to b = 0) but tell Bob that they are            Both Alice and Bob are supposed to know the states
diagonal photons in the opening phase (hence announces            |0i and |1i. This implies, in particular, that both of them
b = 1). This is cheating. Alice then has to make ran-             know the states |φi iB and |φ′j iB .
dom guess for the polarizations of the photons that Bob              (2) An honest Alice is now supposed to make a mea-
has measured along the diagonal basis. Since Bob, on              surement on the first register and determine the value of
average, measures s/2 photons along the diagonal basis,           i if b = 0 (j if b = 1).
Alice, with such a cheating strategy, has only a probabil-           (3) Alice sends the second register to Bob as a piece of
ity of (1/2)s/2 for success. See [7] for details.                 evidence for her commitment.
   A key weakness of Bennett and Brassard’s scheme is                (4) At a later time, Alice opens the commitment by
that Alice can always cheat successfully by using EPR-            declaring the value of b and of i or j.
pairs. Alice can prepare s EPR-pairs of photons and                  (5) Bob performs measurements on the second register
send a member of each pair to Bob during the commit-              to verify that Alice has indeed committed to the genuine
ment phase. She skips her measurements and decides on             bit. More precisely, the data received from Alice (the val-
the value of b only at the beginning of the opening phase.        ues of b and also i or j) should be correlated with Bob’s
If she chooses the value of b to be 0, she measures the           experimental results on the second register. If such ex-
polarization of the photons in her share along the recti-         pected correlations do appear, Bob accepts that Alice has
linear basis. It is a standard property (the EPR paradox)         executed the protocol honestly. Otherwise, Bob suspects
of an EPR pair that Alice’s measurement result on a pho-          that Alice is cheating.
ton will always be perpendicular to Bob’s result on the              We emphasize that all proposed QBC schemes follow
other photon of the pair. Alice can, therefore, proudly           the five-step procedure described above. For instance,
announce those polarizations. Similarly, for b = 1, she           Bennett and Brassard’s scheme described earlier falls into
simply measures along the diagonal basis and proceeds             this class if we give Bob the liberty to store up his photons
in a similar manner. There is no way for Bob to detect            and measure them only after the opening (step 4) of the
this attack.                                                      commitment by Alice. But, if Alice can cheat against
   Bennett and Brassard noted this weakness in the same           even such a powerful Bob, clearly she can cheat against
paper in which they proposed their scheme [2]. Nonethe-           Bob who has no such storage capability.
less, new QBC schemes have been proposed and it has                  Our proof of insecurity of QBC goes as follows: First of
been generally accepted in the literature [4,7,8] that they       all, in order that Bob cannot tell what b is, the second reg-
                                                                  ister (the quantum system that Bob receives during the

                                                              2
commit phase) must contain very little information about               reason why earlier researchers came to the erroneous con-
which bit Alice has committed to. As a start, let us con-              clusion that the BCJL scheme is provably unbreakable.
sider the ideal case in which the second register contains                In the above discussion, we have assumed the ideal sit-
absolutely no information about the value of b. [Bennett               uation in which Bob has absolutely no information about
and Brassard’s scheme [2] and Ardehali’s scheme [9] are                the value of b during the commitment phase and hence
ideal whereas Brassard and Crépeau’s scheme [7] and the               the density matrices describing the second register for
most well-known BCJL scheme [8] are non-ideal. We will                 the two cases b = 0 and b = 1 are the same. (See Eq.
come to the non-ideal case near the end of this Letter.]               (3).) However, Brassard and Crépeau’s scheme [7] and
In the ideal case, to ensure that Bob has no information               the BCJL scheme [8] are non-ideal in the sense that they
about the committed bit b, the density matrices describ-               violate Eq. (3) slightly and give Bob some probability of
ing the second register associated with the bits 0 and 1               distinguishing between ρB           B
                                                                                                  0 and ρ1 . Intuition seems to
are the same. i.e.,                                                    indicate that this is not going to change our conclusion:
                                                                       On the one hand, if Bob has a large probability of dis-
           TrA |0ih0| ≡ ρB    B
                         0 = ρ1 ≡ TrA |1ih1|.               (3)        tinguishing between the two states, the scheme will be
                                                                       unsafe against a cheating Bob. On the other hand, if
  It then follows from the Schmidt decomposition [19]                  Bob has only a very small probability of distinguishing
that                                                                   between the two states, clearly the two density matrices
                  X√                                                   ρB        B
            |0i =      λk |êk iA ⊗ |φ̂k iB ,     (4)                    0 and ρ1 must be close to each other in some sense and
                                                                       essentially the same physics should apply.
                      k
                                                                          Following Mayers [20], we now consider the non-ideal
and                                                                    case when ρB        B
                                                                                     0 6= ρ1 . The closeness between two states
                      X√                                               of B specified by the two density matrices ρB            B
                                                                                                                       0 and ρ1 ,
              |1i =        λk |ê′k iA ⊗ |φ̂k iB ,          (5)        is commonly described by the concept fidelity [21] which
                      k                                                can be defined in terms of purifications. Imagine a system
                                                                       A attached to Bob’s system B. There are many pure
where {|êk iA }, {|ê′k iA } and {|φ̂k iB } are orthonormal           states |ψ0 i and |ψ1 i on the composite system such that
bases of the corresponding Hilbert spaces and λk ’s are the
eigenvalues of the reduced density operator, TrA |0ih0| =                TrA (|ψ0 ihψ0 |) = ρB
                                                                                             0      and     TrA (|ψ1 ihψ1 |) = ρB
                                                                                                                                1 .
TrA |1ih1|. Notice that the λk ’s and |φ̂k iB ’s are the same                                                                    (6)
for the two states and the only difference lies in Al-
ice’s system |êk iA ’s vs |ê′k iA ’s. Now consider the unitary       The pure states |ψ0 i and |ψ1 i are called the purifications
transformation UA which maps |êk iA to |ê′k iA . It clearly          of the density matrices ρB          B
                                                                                                 0 and ρ1 . The fidelity can be
maps |0i to |1i. Note that the transformation UA acts on               defined as
Alice’s system alone and yet rotates |0i to |1i. That is,
                                                                                              B
Alice can apply UA without Bob’s help. Therefore, Alice                              F (ρB
                                                                                         0 , ρ1 ) = max|hψ0 |ψ1 i|               (7)
can cheat by changing b = 0 to b = 1 in the opening
                                                                       where the maximization is over all possible purifications.
phase.
                                                                       0 ≤ F ≤ 1. F = 1 if and only if ρB           B
                                                                                                            0 = ρ1 . We remark
   More concretely, consider the following cheating strat-
                                                                       that for any fixed purification of ρB
                                                                                                           1 , e.g. |1i in Eq. (2),
egy: In the first step, Alice always prepares |0i corre-
                                                                       there exists a maximally parallel purification of ρB0 which
sponding to b = 0. She then skips the second (mea-
                                                                       satisfies Eq. (7).
surement) step and sends the second register to Bob as
                                                                         For non-ideal QBC schemes, the fact that Bob has a
prescribed in the third step. She decides on the value                                                                           B
                                                                       small probability for distinguishing between ρB   0 and ρ1
of b to announce only in the beginning of the opening
                                                                       means that [20]
phase (step 4). Should she now choose b to be zero,
she executes the protocol honestly. On the other hand,                                    F (ρB    B
                                                                                              0 , ρ1 ) = 1 − δ                   (8)
if she now chooses b to be one, she applies the unitary
transformation UA to rotate |0i to |1i and executes the                for some small δ > 0. It then follows from Eqs. (7) and
protocol for b = 1 instead. Consequently, Alice can al-                (8) that, for the state |1i given in Eq. (2), there exists a
ways cheat successfully. Notice that Alice is able to cheat            purification |ψ0 i of ρB
                                                                                              0 such that
primarily because she can delay her measurement until
                                                                                    |hψ0 |1i| = F (ρB    B
                                                                                                    0 , ρ1 ) = 1 − δ.            (9)
step four. To do so, Alice generally needs a quantum
computer. While it is a challenging technological feat to                 The strategy of a cheating Alice for a non-ideal bit
build a quantum computer, it is not forbidden by the                   commitment scheme is the same as before. She prepares
laws of quantum physics. The possibility of a dishonest                the state |0i corresponding to b = 0 in the first step, skips
Alice skipping the second step (i.e., delaying her measure-            the second (measurement) step and sends the second reg-
ments) was not considered in Ref. [8]. This was the chief              ister to Bob as prescribed in the third step. She decides

                                                                   3
on the value of b only in the beginning of the opening                      [2,7–9], quantum oblivious mutual identification [10] and
phase (step 4). If she now chooses b = 0, she simply                        quantum oblivious transfer [11–16]. Kilian [17] has shown
follows the rule. If she chooses b = 1, she applies a uni-                  that, in classical cryptography, oblivious transfer forms
tary transformation to the quantum system on her share                      the basis of many other protocols including two-party se-
to obtain the state |ψ0 i which satisfies Eq. (9). Such a                   cure computations [17]. This chain of arguments seems
                                                                            to suggest that quantum bit commitment alone is suf-
unitary transformation exists because, as can be seen in
                                                                            ficient for implementing two-party secure computations,
the Schmidt decomposition [19], all purifications |φiAB                     thus solving a long standing problem in cryptography.
of a fixed density matrix ρB are related to one another                 [7] G. Brassard and C. Crépeau, in Advances in Cryptology:
by unitary transformations acting on A alone and A is in                    Proceedings of Crypto ’90, Lecture Notes in Computer
Alice’s hands. Notice that if Alice had been honest, she                    Science, Vol. 537, (Springer-Verlag, 1991) p. 49.
would have prepared |1i in the first step instead. (See                 [8] G. Brassard, C. Crépeau, R. Jozsa and D. Langlois, in
Eq. (2).) Nonetheless, since |ψ0 i and |1i are so similar to                Proceedings of the 34th annual IEEE Symposium on the
each other (See Eq. (9).), Bob clearly has a hard time in                   Foundation of Computer Science, (IEEE Computer So-
detecting the dishonesty of Alice. Therefore, Alice can                     ciety Press, Los Alamitos, CA, 1993) p. 362.
cheat successfully with a very large probability.                       [9] M. Ardehali, “A perfectly secure quantum bit com-
   We thank helpful discussions with M. Ardehali, C. H.                     mitment protocol,” Los Alamos preprint archive quant-
                                                                            ph/9505019.
Bennett, G. Brassard, C. Crépeau, D. P. DiVincenzo, L.
                                                                       [10] C. Crépeau and L. Salvail, in Advances in Cryptology—
Goldenberg, R. Jozsa, J. Kilian, D. Mayers, J. Preskill,                    Proceedings of Eurocrypt ’95, (Springer-Verlag, 1995) p.
P. Shor, T. Toffoli and F. Wilczek after the completion of                  133.
an earlier version of this Letter. This work is supported              [11] C. H. Bennett, G. Brassard, C. Crépeau, and M.-H.
in part by DOE grant DE-FG02-90ER40542.                                     Skubiszewska, in Advances in Cryptology: Proceedings of
   Notes added: The insecurity of the BCJL scheme [8]                       Crypto ’91, Lecture Notes in Computer Science, Vol. 576
has also been investigated independently by Mayers [20].                    (Springer-Verlag, 1992) p. 351.
More recently, Mayers [22] has generalized the above re-               [12] C. Crépeau, Journal of Mod. Optics 41, 2445 (1994).
sult to prove that all quantum bit commitment schemes,                 [13] D. Mayers and L. Salvail, preprint distributed at Work-
including ones that involve two-way (quantum) commu-                        shop on Quantum Computing and Communication, Na-
nications between Alice and Bob, are insecure. The same                     tional Institute of Standards and Technology, Gaithers-
                                                                            burg, Maryland, 1994 (unpublished).
result and the impossibility of ideal quantum coin toss-
                                                                       [14] D. Mayers, in Advances in Cryptology: Proceedings of
ing are discussed in our recent preprint [23]. The im-                      Crypto ’95, Lecture Notes in Computer Sciences, Vol.
possibility of some other quantum protocols has recently                    963 (Springer-Verlag, 1995) p. 124.
been demonstrated by Lo [24]. These surprising discover-               [15] M. Ardehali, “A simple quantum oblivious transfer pro-
ies constitute a major setback to quantum cryptography.                     tocol,” Los Alamos preprint archive quant-ph/9512026.
The exact boundary to the power of quantum cryptog-                    [16] A. C.-C. Yao, in Proceedings of the 26th Symposium on
raphy remains an important subject for future investiga-                    the Theory of Computing, (ACM, New York, NY, 1995).
tions.                                                                 [17] J. Kilian, in Proceedings of 1988 ACM Annual Sympo-
                                                                            sium on Theory of Computing, (ACM, Chicago, 1988) p.
                                                                            20.
                                                                       [18] A. Einstein, B. Podolsky, and N. Rosen, Phys. Rev. 47,
                                                                            777 (1935).
                                                                       [19] See, for example, the Appendix of L. P. Hughston, R.
                                                                            Jozsa and W. K. Wootters, Phys. Lett. A183, 14 (1993).
 [1] S. Wiesner, SIGACT News 15, 78 (1983); manuscript                 [20] D. Mayers, “The trouble with quantum bit commit-
     written around 1970.                                                   ment,” Los Alamos preprint archive quant-ph/9603015,
 [2] C. H. Bennett and G. Brassard, in Proceedings of IEEE                  submitted to Journal of Cryptology.
     International Conference on Computers, Systems, and               [21] R. Jozsa, Journal of Modern Optics 41, 2343 (1994).
     Signal Processing, (IEEE, New York, 1984) p. 175.                 [22] D. Mayers, “Unconditionally secure quantum bit com-
 [3] A. K. Ekert, Phys. Rev. Lett. 67, 661 (1991).                          mitment is impossible,” accepted for publication in PRL.
 [4] For reviews on the subject, see for example, G. P. Collins,       [23] H.-K. Lo and H. F. Chau, “Why quantum bit commit-
     Physics Today 45, No. 11, 23 (1992); C. H. Bennett, G.                 ment and ideal quantum coin tossing are impossible,”
     Brassard, and A. K. Ekert, Sci. Am. 267, 50 (1992).                    in Proceedings of the fourth workshop on Physics and
 [5] For a review, see G. Brassard and C. Crépeau, SIGACT                  Computation PhysComp’ 96 (New England Complex Sys-
     News 27, No. 3, 13 (1996).                                             tems Institute, Boston, 1996), p. 76, also available at Los
 [6] Various quantum bit commitment schemes [2,7–9] have                    Alamos preprint archive quant-ph/9605026.
     been proposed and at least one of them, the so-called             [24] H.-K. Lo, “Insecurity of Quantum Secure Computa-
     BCJL scheme, is even claimed to be provably unbreak-                   tions”, Los Alamos preprint archive quant-ph/9611031,
     able [8]. Quantum bit commitment is an important pro-                  submitted to Phys. Rev. A.
     tocol from which one can construct quantum coin tossing



                                                                   4

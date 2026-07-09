# Quantum Proofs of Deletion for Learning with Errors

*Alexander Poremba* — California Institute of Technology  <aporemba@caltech.edu>

**arXiv:** 2203.01610v4 (7 Jan 2023)

> **Extraction note (2026-07-05):** produced via `pdftotext -layout`
> post-processed into GFM. `marker-pdf` (v0.2.6) fails with an internal
> `TypeError: Invalid input type 'PdfDocument'` at
> `pdftext.extraction._load_pdf` on Darwin 25 + Python 3.12/3.14 + the
> `pypdfium2 == 4.30.0` combination available on this host. See
> `extraction/README.md`. This is an honest surrogate, prominently marked.

                                                    Quantum Proofs of Deletion for Learning with Errors
                                                                                       Alexander Poremba*

                                                                              California Institute of Technology




arXiv:2203.01610v4 [quant-ph] 7 Jan 2023
                                                                                         January 10, 2023



                                                                                               Abstract
                                                  Quantum information has the property that measurement is an inherently destructive process. This
                                              feature is most apparent in the principle of complementarity, which states that mutually incompatible
                                              observables cannot be measured at the same time. Recent work by Broadbent and Islam (TCC 2020)
                                              builds on this aspect of quantum mechanics to realize a cryptographic notion called certified deletion.
                                              While this remarkable notion enables a classical verifier to be convinced that a (private-key) quantum
                                              ciphertext has been deleted by an untrusted party, it offers no additional layer of functionality.
                                                  In this work, we augment the proof-of-deletion paradigm with fully homomorphic encryption (FHE).
                                              We construct the first fully homomorphic encryption scheme with certified deletion – an interactive
                                              protocol which enables an untrusted quantum server to compute on encrypted data and, if requested, to
                                              simultaneously prove data deletion to a client. Our scheme has the desirable property that verification of a
                                              deletion certificate is public; meaning anyone can verify that deletion has taken place. Our main technical
                                              ingredient is an interactive protocol by which a quantum prover can convince a classical verifier that a
                                              sample from the Learning with Errors (LWE) distribution in the form of a quantum state was deleted. As
                                              an application of our protocol, we construct a Dual-Regev public-key encryption scheme with certified
                                              deletion, which we then extend towards a (leveled) FHE scheme of the same type. We introduce the
                                              notion of Gaussian-collapsing hash functions – a special case of collapsing hash functions defined by
                                              Unruh (Eurocrypt 2016) – and we prove the security of our schemes under the assumption that the Ajtai
                                              hash function satisfies a certain strong Gaussian-collapsing property in the presence of leakage.
                                                  Our results enable a form of everlasting cryptography and give rise to new privacy-preserving quan-
                                              tum cloud applications, such as private machine learning on encrypted data with certified data deletion.




                                           * aporemba@caltech.edu



                                                                                                   1
Contents
1 Introduction                                                                                            3
  1.1 Main results . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4
  1.2 Overview . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4
  1.3 Applications . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 10
  1.4 Related work . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 11

2 Preliminaries                                                                                             12
  2.1 Quantum computation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .         12
  2.2 Classical and quantum entropies . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       15
  2.3 Fourier analysis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    16
  2.4 Generalized Pauli operators . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     17
  2.5 Lattices and the Gaussian mass . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .      18
  2.6 Cryptography . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .      22
  2.7 The Short Integer Solution problem . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .        22
  2.8 The Learning with Errors problem . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .        23

3 Primal and Dual Gaussian States                                                                           23
  3.1 Duality lemma . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       24
  3.2 Efficient state preparation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .   25
  3.3 Invariance under Pauli-Z dephasing . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .        25

4 Uncertainty Relation for Fourier Basis Projections                                                     28
  4.1 Fourier basis projections . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 28
  4.2 Uncertainty relation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 28

5 Gaussian-Collapsing Hash Functions                                                                    30
  5.1 Ajtai’s hash function . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 31
  5.2 Strong Gaussian-collapsing conjecture . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 34

6 Public-Key Encryption with Certified Deletion                                                           36
  6.1 Definition . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 36
  6.2 Certified deletion security . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 37

7 Dual-Regev Public-Key Encryption with Certified Deletion                                               37
  7.1 Construction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 37
  7.2 Proof of security . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 39

8 Fully Homomorphic Encryption with Certified Deletion                                                    43
  8.1 Definition . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 43
  8.2 Certified deletion security . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 44

9 Dual-Regev Fully Homomorphic Encryption with Certified Deletion                                           45
  9.1 Construction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    45
  9.2 Rewinding lemma . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       50
  9.3 Proof of security . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     54


                                                      2
1 Introduction
Data protection has become a major challenge in the age of cloud computing and artificial intelligence.
The European Union, Argentina, and California recently introduced new data privacy regulations which
grant individuals the right to request the deletion of their personal data by media companies and other data
collectors – a legal concept that is commonly referred to as the right to be forgotten [GGV20]. While
new data privacy regulations have been put into practice in several jurisdictions, formalizing data deletion
remains a fundamental challenge for cryptography. A key question, in particular, prevails:

How can we certify that user data stored on a remote cloud server has been deleted?

Without any further assumptions, the task is clearly impossible to realize in conventional cloud com-
puting. This is due to the fact that there is no way of preventing the data collector from generating and
distributing additional copies of the user data. Although it impossible to achieve in general, proofs-of-
secure-erasure [PT10, DKW11] can achieve a limited notion of data deletion under bounded memory
assumptions. Recently, Garg, Goldwasser and Vasudevan [GGV20] proposed rigorous definitions that
attempt to formalize the right to be forgotten from the perspective of classical cryptography. However, a
fundamental challenge in the work of Garg et al. [GGV20] lies in the fact that the data collector is always
assumed to be honest, which clearly limits the scope of the formalism.
    A recent exciting idea is to use quantum information in the context of data privacy [CRW19, BI20].
Contrary to classical data, it is fundamentally impossible to create copies of an unknown quantum state
thanks to the quantum no-cloning theorem [WZ82]. Broadbent and Islam [BI20] proposed a quantum
encryption scheme which enables a user to certify the deletion of a quantum ciphertext. Unlike classical
proofs-of-secure-erasure, this cryptographic notion of certified deletion is achievable unconditionally in
a fully malicious adversarial setting [BI20]. All prior protocols for certified deletion enable a client to
delegate data in the form of plaintexts and ciphertexts with no additional layer of functionality. A key
question raised by Broadbent and Islam [BI20] is the following:

Can we enable a remote cloud server to compute on encrypted data, while simultaneously allowing
the server to prove data deletion to a client?

This cryptographic notion can be seen as an extension of fully homomorphic encryption
schemes [RAD78, Gen09, BV11a] which allow for arbitrary computations over encrypted data. Prior
work on certified deletion makes use of very specific encryption schemes that seem incompatible with
such a functionality; for example, the private-key encryption scheme of Broadbent and Islam [BI20]
requires a classical one-time pad, whereas the authors in [HMNY21b] use a particular hybrid encryption
scheme in the context of public-key cryptography. While homomorphic encryption enables a wide range of
applications including private queries to a search engine and machine learning classification on encrypted
data [BPTG14], a fundamental limitation remains: once the protocol is complete, the cloud server is still
in possession of the client’s encrypted data. This may allow adversaries to break the encryption scheme
retrospectively, i.e. long after the execution of the protocol. This potential threat especially concerns data
which is required to remain confidential for many years, such as medical records or government secrets.
    Fully homomorphic encryption with certified deletion seeks to address this limitation as it allows a
quantum cloud server to compute on encrypted data while simultaneously enabling the server to prove data
deletion to a client, thus effectively achieving a form of everlasting security [MQU07, HMNY21a].


                                                      3
1.1 Main results
Our contributions are the following.

Quantum superpositions of LWE samples. We use Gaussian states to encode samples from the Learning
with Errors (LWE) distribution [Reg05] for the purpose of certified deletion while simultaneously preserving
their full cryptographic functionality. Because verification of a deletion certificate amounts to checking
whether it is a solution to the (inhomogenous) short integer solution problem [Ajt96], our encoding results
in encryption schemes with certified deletion which are publicly verifiable – in contrast to prior work based
on hybrid encryption and BB84 states [BI20, HMNY21a]. Our technique suggests a generic template for
certified deletion protocols which can be applied to many other cryptographic primitives based on LWE.

Gaussian-collapsing hash functions. To analyze the security of our quantum encryption schemes based
on Gaussian states, we introduce the notion of Gaussian-collapsing hash functions – a special class of
so-called collapsing hash functions defined by Unruh [Unr15]. Informally, a hash function h is Gaussian-
collapsing if it is computationally difficult to distinguish a superposition of Gaussian-weighted pre-images
under h from a single (measured) pre-image. We prove that the Ajtai collision-resistant hash function [Ajt96]
is Gaussian-collapsing assuming the quantum subexponential hardness of decisional LWE.

Dual-Regev public-key encryption with certified deletion. Using Gaussian superpositions, we construct
a public-key encryption scheme with certified deletion which is based on the Dual-Regev scheme introduced
by Gentry, Peikert and Vaikuntanathan [GPV07]. We prove the security of our scheme under the assumption
that Ajtai’s hash function satisfies a certain strong Gaussian-collapsing property in the presence of leakage.

(Leveled) fully homomorphic encryption with certified deletion. We construct the first (leveled) fully
homomorphic encryption (FHE) scheme with certified deletion based on our aforementioned Dual-Regev
encryption scheme with the identical security guarantees. Our FHE scheme is based on the (classical) dual
homomorphic encryption scheme used by Mahadev [Mah18], which is a variant of the FHE scheme by
Gentry, Sahai and Waters [GSW13]. Our protocol supports the evaluation of polynomial-sized Boolean
circuits on encrypted data and, if requested, also enables the server to prove data deletion to a client.

1.2 Overview
How can we certify that sensitive information has been deleted by an untrusted party? Quantum information
allows us to achieve a cryptographic notion called certified deletion [CRW19, FM18, BI20]. The main idea
behind this concept is the principle of complementarity. This feature allows us to encode information in two
mutually incompatible bases – a notion that has no counterpart in a classical world.
    Broadbent and Islam [BI20] construct a private-key quantum encryption scheme with certified deletion
using a BB84-type protocol that closely resembles the standard quantum key distribution (QKD) proto-
col [BB84, TL17]. The crucial idea behind the scheme is that the information which is necessary to decrypt
is encoded in the computational basis, whereas certifying deletion requires a measurement in the incompat-
ible Hadamard basis. The scheme in [BI20] achieves a rigorous notion of certified deletion security: once
the ciphertext is successfully deleted, the plaintext m remains hidden even if the private key is later revealed.
    Using a standard hybrid encryption scheme, Hiroka, Morimae, Nishimaki and Yamakawa [HMNY21b]
extended the scheme in [BI20] to both public-key and attribute-based encryption with certified dele-
tion via the notion of receiver non-committing (RNC) encryption [JL00, CFGN96]. The security proof

                                                       4
in [HMNY21b] relies heavily on the fact that the classical public-key encryption is non-committing, i.e. it
comes with the ability to equivocate ciphertexts to encryptions of arbitrary plaintexts. As a complemen-
tary result, the authors also gave a public-key encryption scheme with certified deletion which is publicly
verifiable assuming the existence of one-shot signatures and extractable witness encryption. This property
enables anyone to verify a deletion certificate using a publicly available verification key.
     All prior protocols for certified deletion enable a client to delegate data in the form of ciphertexts with no
additional layer of functionality. In this work, we answer a question raised by Broadbent and Islam [BI20]
affirmatively, namely whether it is possible to construct a homomorphic quantum encryption scheme with
certified deletion. This cryptographic notion is remarkably powerful as it would allow a quantum cloud
server to compute on encrypted data, while simultaneously enabling the server to prove data deletion to a
client. So far, however, none of the encryption schemes with certified deletion can enable such a function-
ality. Worse yet, the hybrid encryption paradigm appears insufficient in order to construct homomorphic
encryption with certified deletion (see Section 1.4), and thus an entirely new approach is necessary.
     Our techniques deviate from the hybrid encryption paradigm of previous works [BI20, HMNY21a] and
allow us to construct the first homomorphic quantum encryption scheme with certified deletion which has the
desirable feature of being publicly verifiable. The main technical ingredient of our scheme is an interactive
protocol by which a quantum prover can convince a classical verifier that a sample from the Learning with
Errors [Reg05] distribution in the form of a quantum state was deleted.

Quantum superpositions of LWE samples. The Learning with Errors (LWE) problem was introduced
by Regev [Reg05] and has given rise to numerous cryptographic applications, including public-key encryp-
tion [GPV07], homomorphic encryption [BV11b, GSW13] and attribute-based encryption [BGG+ 14].
    The problem is described as follows. Let n, m ∈ N and q ≥ 2 be a prime modulus, and α ∈ (0, 1)
be a noise ratio parameter. In its decisional formulation, the LWEm
                                                                  n,q,αq problem asks to distinguish between
            − Z nq ×m , s · A + e (mod q)) from the LWE distribution and a uniformly random sample
            $
a sample (A ←
     − Z nq ×m , u ←
                   − Zm             − Z nq is a uniformly random row vector and e ∼ DZm ,αq is a row vector
     $             $                $
(A ←                  q ). Here, s ←
which is sampled according to the discrete Gaussian distribution DZm ,αq . The latter distribution assigns
                                              2 2
probability proportional to ̺r (x) = e−π kxk /r to every lattice point x ∈ Z m , for r = αq > 0.
    How can we certify that a (possibly malicious) party has deleted a sample from the LWE distribution?
The main technical insight of our work is that one can encode LWE samples as quantum superpositions
for the purpose of certified deletion while simultaneously preserving their full cryptographic functionality.
Superpositions of LWE samples have been considered by Grilo, Kerenidis and Zijlstra [GKZ19] in the
context of quantum learning theory and by Alagic, Jeffery, Ozols and Poremba [AJOP20], as well as by
Chen, Liu and Zhandry [CLZ21], in the context of quantum cryptanalysis of LWE-based cryptosystems.
Let us now describe the main idea behind our constructions. Consider the Gaussian superposition,1

                                   |ψ̂ i XY =    ∑ ̺σ (x) |xi X ⊗ |A · x (mod q)iY .
                                                x∈Z m
                                                    q


                                               m            m      q q
Here, we let σ = 1/α and use Z m
                               q to represent Z ∩ (− 2 , 2 ] . By measuring system Y in the computational
                                                                                                                     √
   1 A standard tail bound shows that the discrete Gaussian D m is essentially only supported on {x ∈ Z m : kxk ≤ σ m }. We
                √                                            Z ,σ                                                 ∞
                                                         q q
choose σ ≪ q/ m and consider the domain Z m ∩ (− 2 , 2 ] m instead. For simplicity, we also ignore that | ψ̂i is not normalized.




                                                               5
basis with outcome y ∈ Z nq , the state |ψ̂ i collapses into the quantum superposition

                                       |ψ̂y i =         ∑           ̺ σ ( x) | xi .                                       (1)
                                                      x∈Z m
                                                          q :
                                                   Ax=y (mod q )

Note that the state |ψ̂y i is now a superposition of short Gaussian-weighted solutions x ∈ Z m q subject to the
constraint A · x = y (mod q). In other words, by measuring the above state in the computational basis,
we obtain a solution to the so-called (inhomogenous) short integer solution (ISIS) problem specified by
(A, y) (see Definition 13). The quantum state |ψ̂y i in Eq. (1) has the following duality property; namely, by
applying the (inverse) q-ary quantum Fourier transform we obtain the state
                                                             −hs,yi
                             |ψy i = ∑     ∑ ̺ ( e) ω q
                                                    q
                                                    σ
                                                                       |sA + e (mod q)i ,                                 (2)
                                    s∈Z nq e∈Z m
                                               q


where ωq = e2πi/q is the primitive q-th root of unity. We make this statement more precise in Lemma 16.
Throughout this work, we will refer to |ψy i and |ψ̂y i as the primal and dual Gaussian state, respectively.
Notice that the resulting state |ψy i is now a quantum superposition of samples from the LWE distribution.
This relationship was first observed in the work of Stehlé et al. [SSTX09] who gave quantum reduction
from SIS to LWE based on Regev’s reduction [Reg05], and was later implicitly used by Roberts [Rob19]
and Kitagawa et al. [KNY21] to construct quantum money and secure software leasing schemes.
    Our quantum encryption schemes with certified deletion exploit the fact that a measurement of |ψy i
in the Fourier basis yields a short solution to the ISIS problem specified by (A, y), whereas ciphertext
information which is necessary to decrypt is encoded using LWE samples in the computational basis.

Dual-Regev public-key encryption with certified deletion. The key ingredient of our homomorphic
encryption scheme with certified deletion is the Dual-Regev public-key encryption scheme introduced by
Gentry, Peikert and Vaikuntanathan [GPV07]. Using Gaussian states, we can encode Dual-Regev ciphertexts
for the purpose of certified deletion while simultaneously preserving their full cryptographic functionality.
Our scheme Dual-Regev scheme with certified deletion consists of the following efficient algorithms:
                                                                                              n ×( m +1)
    • To generate a pair of keys (sk, pk), sample a random matrix A ∈ Z q         together with a particular
      short trapdoor vector t ∈ Z m + 1 such that A · t = 0 (mod q), and let pk = A and sk = t.
    • To encrypt b ∈ {0, 1} using the public key pk = A, generate the following for a random y ∈ Z nq :
                                                                         −hs,yi                                  q
              vk ← (A, y),       |CTi ← ∑               ∑    ̺ q ( e) ω q
                                                                σ
                                                                                   |sA + e + b · (0, . . . , 0, ⌊ ⌋)i ,
                                                                                                                 2
                                           s∈Z nq e∈Z m
                                                      q
                                                        +1


      where vk is a public verification key and |CTi is the quantum ciphertext for σ = 1/α.
    • To decrypt a ciphertext |CTi using the secret key sk, measure in the computational basis to obtain an
                                                                                   q
      outcome c ∈ Z qm+1 , and output 0, if cT · sk ∈ Z q is closer to 0 than to ⌊ 2 ⌋, and output 1, otherwise.
   To delete the ciphertext |CTi, we simply perform measurement in the Fourier basis. In Corollary 1, we
show that the Fourier transform of the ciphertext |CTi results in the dual quantum state
                                                                    hx,b ·(0,...,0,⌊ 2q ⌋)i
                              |c
                               CTi =         ∑          ̺ σ ( x) ω q                          | xi .                      (3)
                                         x∈Z m +1 :
                                             q
                                       Ax=y (mod q )



                                                            6
                         ∑           ̺ σ ( x) | xi               ≈c           |x0 i, x0 ∼ DΛyq (A), √σ
                                                                                                           2
                        x∈Z m
                            q
                    Ax=y (mod q )                            (Thm. 4)




                       FTq       (Lem. 16)                                                   FTq


                                                             (Thm. 5)
                                           −hs,yi                                        −hu,x0 i
                  ∑ ∑           ̺ q ( e) ω q
                                  σ
                                                  |sA + ei           ≈c          ∑ ωq               |u i
                 s∈Z nq e∈Z m
                            q                                                   u ∈Z m
                                                                                     q




Figure 1: Technical overview of the main quantum states and their properties used throughout this work.
The computational indistinguishability property holds under the (subexponential) quantum hardness of the
                                                      y
(decisional) LWE assumption (Definition 15). Here, Λq (A) = {x ∈ Z m : A · x = y (mod q)} denotes a
particular coset of the q-ary lattice Λ⊥             m
                                       q (A) = {x ∈ Z : A · x = 0 (mod q)} defined in Section 2.5.


Notice that a Fourier basis measurement of |CTi necessarily erases all information about the plaintext
b ∈ {0, 1} and results in a short vector π ∈ Z qm+1 such that A · π = y (mod q). In other words, to
verify a deletion certificate we can simply check whether it is a solution to the ISIS problem specified by
the verification key vk = (A, y). Our scheme has the desirable property that verification of a certificate
π is public; meaning anyone in possession of (A, y) can verify that |CTi has been successfully deleted.
Moreover, due to the tight connection between worst-case lattice problems and the average-case ISIS prob-
lem [MR07,GPV07], it is computationally difficult to produce a valid deletion certificate from (A, y) alone.
    To formalize security, we use the notion of certified deletion security (i.e. IND-CPA-CD security) [BI20,
HMNY21a] which roughly states that, once deletion of the ciphertext is successful, the plaintext remains
hidden even if the secret key is later revealed (see Definition 23). We prove the security of our schemes
under the assumption that the Ajtai collision-resistant hash function hA (x) = A · x (mod q) satisfies a
certain strong collapsing property in the presence of leakage.

Gaussian-collapsing hash functions. Unruh [Unr15] introduced the notion of collapsing hash functions
in his seminal work on computationally binding quantum commitments. Informally, a hash function h is
called collapsing if it is computationally difficult to distinguish between a superposition of pre-images, i.e.
∑x: h(x)=y αx |xi, and a single measured pre-image |x0 i such that h(x0 ) = y. Motivated by the properties
of the dual Gaussian state in Eq. (1), we consider a special class of hash functions which are collapsing
with respect to Gaussian superpositions. We say that a hash function h is σ-Gaussian-collapsing (formally
defined in Definition 19), for some σ > 0, if the following states are computationally indistinguishable:

                                   ∑        ̺ σ ( x) | xi   ≈c       |x0 i , s.t. h(x0 ) = y.
                                x: h(x)=y

Here, x0 is the result of a computational basis measurement of the the Gaussian superposition (on the left).
Notice that any collapsing hash function h is necessarily also Gaussian-collapsing, since a superposition

                                                                 7
of Gaussian-weighted vectors constitutes a special class of inputs to h. Liu and Zhandry [LZ19] implicitly
showed that the Ajtai hash function hA (x) = A · x (mod q) is collapsing – and thus Gaussian-collapsing –
via the notion of lossy functions and (decisional) LWE. In Theorem 4, we give a simple and direct proof of
the Gaussian-collapsing property assuming (decisional) LWE, which might be of independent interest.
    The fact Ajtai’s hash function is Gaussian-collapsing has several implications for the security of our
schemes. Because our Dual-Regev ciphertext corresponds to the Fourier transform of the state in Eq. (3), the
Gaussian-collapsing property immediately implies the semantic (i.e., IND-CPA) security under decisional
LWE (see Theorem 5). We refer to Figure 1 for an overview of our Gaussian states and their properties.
    To prove the stronger notion of IND-CPA-CD security of our Dual-Regev scheme with certified deletion,
we have to show that, once deletion has taken place, the plaintext remains hidden even if the secret key (i.e., a
short trapdoor vector t in the kernel of A) is later revealed. In other words, it is sufficient to show that Ajtai’s
hash function satisfies a particular strong Gaussian-collapsing property in the presence of leakage; namely,
once an adversary A produces a valid short certificate π with the property that A · π = y (mod q), then A
cannot tell whether the input at the beginning of the experiment corresponded to a Gaussian superposition of
pre-images or a single (measured) pre-image, even if A later receives a short trapdoor vector t in the kernel
of A. Here, it is crucial that A receives the trapdoor vector t only after A provides a valid pre-image witness
π, otherwise A could trivially distinguish the two states by applying the Fourier transform and using the
trapdoor t to distinguish between a superposition of LWE samples and a uniform superposition.
    Unfortunately, we currently do not know how to prove the strong Gaussian-collapsing property of the
Ajtai hash function from standard assumptions (such as LWE or ISIS). The problem emerges when we
attempt to give a reduction between the IND-CPA-CD security of our Dual-Regev public-key encryption
scheme with certified deletion and the LWE (or ISIS) problem. In order to simulate the IND-CPA-CD game
successfully, we have to eventually forward a short trapdoor vector t ∈ Z m+1 (i.e. the secret key) to the
adversary once deletion has taken place. Notice, however, that the reduction has no way of obtaining a short
trapdoor vector t such that A · t = 0 (mod q) as it is trying to break the underlying LWE (or ISIS) problem
with respect to A in the first place (!) Recently, Hiroka, Morimae, Nishimaki and Yamakawa [HMNY21a]
managed to overcome similar technical difficulties using the notion of receiver non-committing (RNC)
encryption [JL00, CFGN96] in the context of hybrid encryption in order to produce a fake secret key. In
our case, we cannot rely on similar techniques involving RNC encryption as it seems difficult to reconcile
with homomorphic encryption, which is the main focus of this work. Instead, we choose to formalize the
strong Gaussian-collapsing property of the Ajtai hash function as a simple and falsifiable conjecture in
Conjecture 5.2. We prove the following result in Theorem 7 (assuming that Conjecture 5.2 holds):

Theorem (informal): The Dual-Regev PKE scheme with certified deletion (see Construction 1) is
IND-CPA-CD-secure under the strong Gaussian-collapsing assumption in Conjecture 5.2.

To see why Conjecture 5.2 is plausible, consider the following natural attack. Given as input either
a Gaussian superposition of pre-images or a single (measured) pre-image, we perform the quantum Fourier
transform, reversibly shift the outcome by a fresh LWE sample2 and store the result in an auxiliary register.
If the input corresponds to a superposition, we obtain a separate LWE sample which is re-randomized,
whereas if the input is a single (measured) pre-image, the outcome remains random. Hence, if the
aforementioned procedure succeeded without disturbing the initial quantum state, we could potentially
provide a valid certificate π and also distinguish the auxiliary system with access to the trapdoor. However,
   2 To smudge the Gaussian error of the initial superposition, we can choose an error from a discrete Gaussian distribution which

has a significantly larger standard deviation.



                                                                8
by shifting the state by another LWE sample, we have necessarily entangled the two systems in a way that
prevents us from finding a valid certificate via a Fourier basis measurement. We make this fact more precise
in Section 4, where we prove a general uncertainty relation for Fourier basis projections (Theorem 3) that
rules out a large class of attacks, including the shift-by-LWE-sample attack described above.
    Next, we extend our Dual-Regev scheme towards a (leveled) FHE scheme with certified deletion.

Dual-Regev fully homomorphic encryption with certified deletion. Our (leveled) FHE scheme with
certified deletion is based on the (classical) Dual-Regev leveled FHE scheme used by Mahadev [Mah18] –
a variant of the scheme due to Gentry, Sahai and Waters [GSW13]. Let n, m ∈ N, let q ≥ 2 be a prime
modulus, and let α ∈ (0, 1) be the noise ratio with σ = 1/α. Let N = (n + 1)⌈log q⌉ and let G ∈
  ( m +1)× N
Zq           denote the gadget matrix (defined in Section 9.1) designed to convert a binary representation of
a vector back to its Z q representation. The scheme consists of the following efficient algorithms:
                                                                                          ( m +1)× n
    • To generate a pair of keys (sk, pk), sample a random matrix A ∈ Z q         together with a particular
      short trapdoor vector t ∈ Z m + 1 such that t · A = 0 (mod q), and let pk = A and sk = t.
                                                                         ( m +1)× n
    • To encrypt a bit x ∈ {0, 1} using the public key A ∈ Z q        , generate the following pair consisting
      of a verification key and ciphertext for a random Y ∈ Z nq × N with columns y1 , . . . , y N ∈ Z nq :

                                                                                      −Tr[S T Y]
               vk ← (A, Y),        |CTi ←      ∑           ∑            ̺q/σ (E) ωq                |A · S + E + x · G i ,
                                            S∈Z nq × N E∈Z (qm +1)× N

                     ( m +1)× N
      where G ∈ Z q               denotes the gadget matrix and where σ = 1/α.

    • To decrypt a quantum ciphertext |CTi using the secret key sk, measure in the computational basis to
                               ( m +1)× N
      obtain an outcome C ∈ Z q           and compute c = skT · cN ∈ Z q , where cN ∈ Z qm+1 is the N-th
                                                                    q
      column of C, and then output 0, if c is closer to 0 than to ⌊ 2 ⌋, and output 1, otherwise.
We remark that deletion and verification take place as in our Dual-Regev scheme with certified deletion.
     Our FHE scheme supports the evaluation of polynomial-sized Boolean circuits consisting entirely of
NAND gates, which are universal for classical computation. Inspired by the classical homomorphic NAND
operation of the Dual-Regev scheme [GSW13, Mah18], we define an analogous quantum operation UNAND
in Definition 28 which allows us to apply a NAND gate directly onto Gaussian states. When applying ho-
momorphic operations, the new ciphertext maintains the form of an LWE sample with respect to the same
public key pk, albeit for a new LWE secret and a new (non-necessarily Gaussian) noise term of bounded
magnitude. Notice, however, that the resulting ciphertext is now a highly entangled state since the unitary
operation UNAND induces entanglement between the LWE secrets and Gaussian error terms of the superpo-
sition. This raises the following question: How can a server perform homomorphic computations and, if
requested, afterwards prove data deletion to a client? In some sense, applying a single homomorphic NAND
gates breaks the structure of the Gaussian states in a way that prevents us from obtaining a valid deletion
certificate via a Fourier basis measurement. Our solution to the problem involves a single additional round
of interaction between the quantum server and the client in order to certify deletion.
     After performing a Boolean circuit C via a sequence of UNAND gates starting from the ciphertext
|CTi = |CT1 i ⊗ · · · ⊗ |CTℓ i in system Cin corresponding to an encryption of x = ( x1 , . . . , xℓ ) ∈ {0, 1}ℓ ,
the server simply sends the quantum system Cout containing an encryption of C ( x) to the client. Then,
using the secret key sk (i.e., a trapdoor for the public matrix pk), it is possible for the client to extract

                                                            9
the outcome C ( x) from the system Cout with overwhelming probability without significantly damaging
the state. We show that it is possible to rewind the procedure in a way that results in a state which is
negligibly close to the original state in system Cout . At this step of the protocol, the client has learned the
outcome of the homomorphic application of the circuit C while the server is still in possession of a large
number of auxiliary systems (denoted by Caux ) which mark intermediate applications of the gate UNAND .
We remark that this is where the standard FHE protocol ends. In order to enable certified deletion, the
client must now return the system Cout to the server. Having access to all three systems Cin Caux Cout ,
the server is then able to undo the sequence of homomorphic NAND gates in order to return to the
original product state in system Cin (up to negligible trace distance). Since the ciphertext in the server’s
possession is now approximately a simple product of Gaussian states, the server can perform a Fourier basis
measurement of systems Cin, as required. Once the protcol is complete, it is therefore possible for the client
to know C ( x) and to be convinced that data deletion has taken place. We prove the following in Theorem 10.

Theorem (informal): Our Dual-Regev (leveled) FHE scheme with certified deletion (Construction 3)
is IND-CPA-CD-secure under the strong Gaussian-collapsing assumption in Conjecture 5.2.

Open problems. Our results leave open many interesting future research directions. For example, is
it possible to prove Conjecture 5.2 – and thus the IND-CPA-CD security of our constructions – from the
hardness of LWE or ISIS? Another interesting direction is the following. Since the verification of our proofs
of deletion only requires classical computational capabilities, this leaves open the striking possibility that all
communication that is required for fully homomorphic encryption with certified deletion can be dequantized
entirely, similar to work of Mahadev [Mah18] on delegating quantum computations, as well as recent work
on classically-instructed parallel remote state preparation by Gheorghiu, Metger and Poremba [GMP22].

1.3 Applications
Data retention and the right to be forgotten. The European Union, Argentina, and California recently
introduced new data privacy regulations – often referred to as the right to be forgotten [GGV20] – which
grant individuals the right to request the deletion of their personal data by media companies. However,
formalizing data deletion still remains a fundamental challenge for cryptography. Our fully homomorphic
encryption scheme with certified deletion achieves a rigorous notion of long-term data privacy: it enables a
remote quantum cloud server to compute on encrypted data and – once it is deleted and publicly verified –
the client’s data remain safeguarded against a future leak that reveals the secret key.

Private machine learning on encrypted data. Machine learning algorithms are used for wide-ranging
classification tasks, such as medical predictions, spam detection and face recognition. While homomorphic
encryption enables a form of privacy-preserving machine learning [BPTG14], a fundamental limitation
remains: once the protocol is complete, the cloud server is still in possession of the client’s encrypted data.
This threat especially concerns data which is required to remain confidential for many years. Our results
remedy this situation by enabling private machine learning on encrypted data with certified data deletion.

Everlasting cryptography. Assuming that the server has not broken the computational assumption before
data deletion has taken place, our results could potentially transform a long-term LWE assumption [Reg05]
into a temporary one, and thus effectively achieve a form of everlasting security [MQU07, HMNY21a].



                                                       10
1.4 Related work
The first work to formalize a notion resembling certified deletion is due to Unruh [Unr13] who proposed
a quantum timed-release encryption scheme that is revocable. The protocol allows a user to return the
ciphertext of a quantum timed-release encryption scheme, thereby losing all access to the data. Unruh’s
security proof exploits the monogamy of entanglement in order to guarantee that the quantum revocation
process necessarily erases all information about the plaintext. Subsequently, Coladangelo, Majenz and
Poremba [CMP20] adapted this property to revocable programs in the context of secure software leasing, a
weaker notion of quantum copy-protection which was proposed by Ananth and La Placa [AP20].
      Fu and Miller [FM18] gave the first quantum protocol that proves deletion of a single bit using classical
interaction alone. Subsequently, Coiteux-Roy and Wolf [CRW19] proposed a QKD-like conjugate coding
protocol that enables certified deletion of a classical plaintext, albeit without a complete security proof.
      Independently of [CRW19], Broadbent and Islam [BI20] construct a private-key quantum encryption
scheme with a rigorous definition of certified deletion using a BB84-type protocol that closely resembles
the standard quantum key distribution protocol [BB84, TL17]. There, the ciphertext (without the optional
quantum error correction part) consists of random BB84 states | xθ i = H θ1 | x1 i ⊗ · · · ⊗ H θn | xn i together
with a one-time pad encryption of the form f ( x|θi =0 ) ⊕ m ⊕ u, where u is a random string (i.e. a one-
time pad key), f is a two-universal hash function and x|θi =0 is the substring of x to which no Hadamard
gate is applied. The main idea behind the scheme is that the information which is necessary to decrypt is
encoded in the computational basis, whereas certifying deletion requires a Hadamard basis measurement.
Therefore, if the verification of a deletion certificate is successful, x|θi =0 must have high entropy, and thus
 f ( x|θi =0 ) is statistically close to uniform (i.e. f serves as an extractor). The private-key quantum encryption
scheme of Broadbent and Islam [BI20] achieves the notion of certified deletion security: once the ciphertext
is successfully deleted, the plaintext m remains hidden even if the private key (θ, f , u) is later revealed.
      Using a standard hybrid encryption scheme, Hiroka, Morimae, Nishimaki and Yamakawa [HMNY21b]
extended the scheme in [BI20] to both public-key and attribute-based encryption with certified deletion
via the notion of receiver non-committing (RNC) encryption [JL00, CFGN96]; for example, to obtain a
public-key encryption scheme with certified deletion, one simply outputs a quantum ciphertext of the [BI20]
scheme together with a classical (non-committing) public-key encryption of its private key. Given access
to the RNC secret key, it is therefore possible to decrypt the quantum ciphertext. Crucially, the hybrid
encryption scheme also inherits the certified deletion property of the [BI20] scheme; namely, once deletion
has taken place, the plaintext remains hidden even if the RNC secret key is later revealed. The security
proof in [HMNY21b] relies heavily on the fact that the classical public-key encryption is non-committing,
i.e. it comes with the ability to equivocate ciphertexts to encryptions of arbitrary plaintexts. To obtain a
homomorphic encryption scheme with certified deletion, one would have to instantiate the hybrid encryption
scheme with a classical (non-committing) homomorphic encryption scheme which is not known to exist.
While generic transformations for non-committing encryption have been studied [KNTY18], they tend to be
incompatible with basic homomorphic computations. Moreover, it is unclear whether the candidate hybrid
approach for homomorphic encryption is even secure: for all we know, a malicious adversary could use
homomorphic evaluation to decouple the quantum part from the classical part of the ciphertext in order to
obtain a classical encryption of the plaintext, thereby violating certified deletion security.
      Hiroka, Morimae, Nishimaki and Yamakawa [HMNY21a] studied certified everlasting zero-knowledge
proofs for QMA via the notion of everlasting security which was first formalized by Müller-Quade and
Unruh [MQU07]. A recent paper by Coladangelo, Liu, Liu and Zhandry [CLLZ21] introduces subspace
coset states in the context of unclonable crytography in a way that loosely resembles our use of primal and
dual Gaussian states.


                                                        11
    In a subsequent and independent work, Khurana and Bartusek [BK22] consider generic transformations
for encryption schemes with certified deletion. Similar to Broadbent and Islam [BI20], they use a hybrid
approach via BB84 states to construct (privately verifiable) public-key, attribute-based and homomorphic
encryption schemes with certified everlasting security: once deletion is successful, the security notion guar-
antees that the plaintext remains hidden even if the adversary is henceforth computationally unbounded.

Previous version of this paper. We remark that a prior version of this paper was posted to arXiv3 and
presented as unpublished work at QIP 2022. This paper contains substantial new improvements to the
previous constructions: compared to the prior version of the paper which presented security proofs in the
semi-honest adversarial model, this work features security proofs in a fully malicious setting under the
plausible strong Gaussian-collapsing property of the Ajtai hash function, and also offers revised Dual-Regev
encryption schemes with certified deletion that enable public verification of deletion certificates.

Acknowledgments. The author would like to thank Urmila Mahadev for pointing out an attack on an
earlier version of our protocols, and for the idea behind the proof of Theorem 4. The author would also like
to thank Thomas Vidick, Prabhanjan Ananth and Vinod Vaikuntanathan for many insightful discussions.
The author is also grateful for useful comments made by anonymous reviewers. The author is partially
supported by AFOSR YIP award number FA9550-16-1-0495 and the Institute for Quantum Information and
Matter (an NSF Physics Frontiers Center; NSF Grant PHY-1733907), and is also grateful for the hospitality
of the Simons Institute for the Theory of Computing, where part of this research was carried out.


2 Preliminaries
Notation. For x ∈ C n , we denote the ℓ2 norm by kxk. For x ∈ C n , we occasionally also use the max
norm kxk∞ = maxi | xi |. We denote the expectation value of a random variable X which takes values in X
                                                 $
by E [ X ] = ∑ x ∈X x Pr[ X = x]. The notation x ←
                                                 − X denotes sampling of x uniformly at random from X ,
whereas x ∼ D denotes sampling of an element x according to the distribution D. We call a non-negative
real-valued function µ : N → R + negligible if µ(n) = o(1/p(n)), for every polynomial p(n). Given an
                                                                                    q q m
integer m ∈ N and modulus q ≥ 2, we represent elements in Z m                 m
                                                               q as integers Z ∩ (− 2 , 2 ] .


2.1 Quantum computation
For a comprehensive overview of quantum computation, we refer to the introductory texts [NC11, Wil13].
We denote a finite-dimensional complex Hilbert space by H, and we use subscripts to distinguish between
different systems (or registers). For example, we let H A be the Hilbert space corresponding to a system A.
The tensor product of two Hilbert spaces H A and H B is another Hilbert space denoted by H AB = H A ⊗ H B .
The Euclideanp norm of a vector |ψi ∈ H over the finite-dimensional complex Hilbert space H is denoted
as kψk =       hψ|ψ i. Let L(H) denote the set of linear operators over H. A quantum system over the
2-dimensional Hilbert space H = C2 is called a qubit. For n ∈ N, we refer to quantum registers over
                             ⊗n
the Hilbert space H = C2          as n-qubit states. More generally, we associate qudits of dimension d ≥ 2
with a d-dimensional Hilbert space H = C d . We use the word quantum state to refer to both pure states
(unit vectors |ψi ∈ H) and density matrices ̺ ∈ D(H), where we use the notation D(H) to refer to the
space of positive semidefinite matrices of unit trace acting on H. For simplicity, we frequently consider
  3 https://arxiv.org/abs/2203.01610v1




                                                     12
subnormalized states, i.e. states in the space of positive semidefinite operators over H with trace norm not
exceeding 1, denoted by S≤ (H). The trace distance of two density matrices ̺, σ ∈ D(H) is given by
                                                    q                    
                                                1
                                  k̺ − σktr = Tr         (̺ − σ)† (̺ − σ) .
                                                2

We frequently use the compact notation ̺ ≈ε σ which means        pthat there exists some ε ∈ [0, 1] √
                                                                                                    such
                                                                                                       √ that
k̺ − σktr ≤ ε. The purified distance is defined as P(̺, σ) = 1 − F (̺, σ)2 , where F (̺, σ) = k ̺ σk1
denotes the fidelity. A classical-quantum (CQ) state ̺ ∈ D(H XB ) depends on a classical variable in system
X which is correlated with a quantum system B. If the classical system X is distributed according to a
probability distribution PX over the set X , then all possible joint states ̺XB can be expressed as

                                       ̺XB = ∑ PX ( x)| xih x| X ⊗ ̺xB .
                                                  x ∈X


Quantum channels and measurements. A quantum channel Φ : L(H A ) → L(H B ) is a linear map
between linear operators over the Hilbert spaces H A and H B . Oftentimes, we use the compact notation
Φ A→ B to denote a quantum channel between L(H A ) and L(H B ). We say that a channel Φ is completely
positive if, for a reference system R of arbitrary size, the induced map 1 R ⊗ Φ is positive, and we call it trace-
preserving if Tr[Φ( X )] = Tr[ X ], for all X ∈ L(H). A quantum channel that is both completely positive
and trace-preserving is called a quantum CPTP channel. Let X be a set. A generalized measurement on a
system A is a set of linear operators {MxA }x ∈X such that
                                                            †
                                            ∑ (MxA ) (MxA ) = 1 A .
                                           x ∈X

We can represent a measurement as a CPTP map M A→ X that maps states on system A to measurement
outcomes in a register denoted by X. For example, let ̺ ∈ D(H AB ) be a bipartite state. Then,
                                                                  h               i
                       M A→X : ̺ AB 7→ ∑ | xih x|X ⊗ tr A MxA ̺ AB MxA † ,
                                                         x ∈X

yields a normalized classical-quantum state. A positive-operator valued measure (POVM) on a quantum
system A is a set of Hermitian positive semidefinite operators {MxA }x ∈X such that

                                                   ∑ MxA = 1 A .
                                                   x ∈X
                                                                                        p
Oftentimes, we identify a POVM {MxA }x ∈X with an associated generalized measurement { MxA }x ∈X .
                                            y
The overlap c of two POVMs {MxA }x ∈X and {N A }y∈X acting on a quantum system A is defined by

                                                           q          q        2
                                                                           y
                                          c = max               MxA       NA       .
                                                  x,y
                                                                               ∞

We say that two measurements are mutually unbiased, if the overlap satisfies c = 1/d, where d = dim(H A )
is the dimension of the associated Hilbert space.




                                                                13
Quantum algorithms. By a polynomial-time quantum algorithm (or QPT algorithm) we mean a
                                                                  S
polynomial-time uniform family of quantum circuits given by C = n∈N Cn , where each circuit C ∈ C is
described by a sequence of unitary gates and measurements. Similarly, we also define (classical) probabilis-
tic polynomial-time (PPT) algorithms. A quantum algorithm may, in general, receive (mixed) quantum
states as inputs and produce (mixed) quantum states as outputs. Occasionally, we restrict QPT algorithms
implicitly. For example, if we write Pr[A(1λ ) = 1] for a QPT algorithm A, it is implicit that A is a QPT
algorithm that outputs a single classical bit.
    We extend the notion of QPT algorithms to CPTP channels via the following definition.

Definition 1 (Efficient CPTP maps). A family of CPTP maps {Φλ : L(H Aλ ) → L(H Bλ )}λ∈N is called
efficient, if there exists a polynomial-time uniformly generated family of circuits {Cλ }λ∈N acting on the
Hilbert space H Aλ ⊗ H Bλ ⊗ HCλ such that, for all λ ∈ N and for all ̺ ∈ H Aλ ,

                                 Φλ (̺λ ) = Tr Aλ Cλ [Cλ (̺λ ⊗ |0ih0| Bλ Cλ )].

Definition 2 (Indistinguishability of ensembles of random variables). Let λ ∈ N be a parameter. We say
that two ensembles of random variables X = {Xλ } and Y = {Yλ } are computationally indistinguishable,
denoted by X ≈c Y, if for all QPT distinguishers D which output a single bit, it holds that

                          Pr[D(1λ , Xλ ) = 1] − Pr[D(1λ , Yλ ) = 1] ≤ negl(λ) .

Definition 3 (Indistinguishability of ensembles of quantum states, [Wat06]). Let p : N → N be a polynomi-
ally bounded function, and let ̺λ and σλ be p(λ)-qubit quantum states. We say that {̺λ }λ∈N and {σλ }λ∈N
are quantum computationally indistinguishable ensembles of quantum states, denoted by ̺λ ≈c σλ , if, for
any QPT distinguisher D with single-bit output, any polynomially bounded q : N → N, any family of
q(λ)-qubit auxiliary states {νλ }λ∈N , and every λ ∈ N,

                     Pr[D(1λ , ̺λ ⊗ νλ ) = 1] − Pr[D(1λ , σλ ⊗ νλ ) = 1] ≤ negl(λ) .

Lemma 1 (”Almost As Good As New” Lemma, [Aar16]). Let ̺ ∈ D(H) be a density matrix over a Hilbert
space H. Let U be an arbitrary unitary and let (Π0 , Π1 = 1 − Π0 ) be projectors acting on H ⊗ Haux . We
interpret (U, Π0 , Π1 ) as a measurement performed by appending an ancillary system in the state |0ih0|aux ,
applying the unitary U and subsequently performing the two-outcome measurement {Π0 , Π1 } on the larger
system. Suppose that the outcome corresponding to Π0 occurs with probability 1 − ε, for some ε ∈ [0, 1].
In other words, it holds that Tr[Π0 (U̺ ⊗ |0ih0|aux U † )] = 1 − ε. Then,
                                                            √
                                             k̺e − ̺ktr ≤ ε,

where ̺e is the state after performing the measurement and applying U † , and after tracing out Haux :
                           h                                                             i
               ̺e = Traux U † Π0 U (̺ ⊗ |0ih0|aux )U † Π0 + Π1 U (̺ ⊗ |0ih0|aux )U † Π1 U .

   We also use the following lemma on the closeness to ideal states:

Lemma 2 ( [Unr13], Lemma 10). Let Π be an arbitrary projector and let |ψi be a normalized pure state
such that kΠ |ψi k2 = 1 − ε, for some ε ≥ 0. Then, there exists a (pure) ideal state,

                                                         Π |ψi
                                              |ψ̄ i =            ,
                                                        kΠ |ψi k

                                                        14
with the property that
                                                          √
                           k|ψihψ| − |ψ̄ ihψ̄|ktr ≤           ε       and            |ψ̄ i ∈ im(Π).

In other words, the state |ψ̄ i is within trace distance ε > 0 of the state |ψi and lies in the image of Π.

    We also use the following elementary lemma.

Lemma 3 ( [CMP20], Lemma 23). Let ̺, σ ∈ D(H) be two states with the property that k̺ − σktr ≤ ε,
for some ε ≥ 0. Let Π be an arbitrary matrix acting on H such that 0 ≤ Π ≤ 1. Then,

                                            |Tr[Π̺] − Tr[Πσ]| ≤ ε.

2.2 Classical and quantum entropies
Classical entropies. Let X be a random variable with an arbitrary distribution PX over an alphabet X .
The min-entropy of X, denoted by Hmin ( X ), is defined by the following quantity
                                                                       
                              Hmin ( X ) = − log max Pr [ X = x] .
                                                              x ∈X X ∼ PX

The conditional min-entropy of X conditioned on a correlated random variable Y is defined by
                                                 h                          i
                      Hmin ( X |Y ) = − log E max Pr [ X = x|Y = y] .
                                                      y ←Y    x ∈X X ∼ PX

Lemma 4 (Leftover Hash Lemma, [HILL88]). Let n, m ∈ N and q ≥ 2 a prime. Let P be a distribution
over Z m
       q and suppose that Hmin ( X ) ≥ n log q + 2 log (1/ε) + O (1) for ε > 0, where X denotes a random
variable with distribution P. Then, the following two distributions are within total variance distance ε:

                                                                                  − Z nq ×m , u ←
                                                                                                − Z nq .
                                                                                  $             $
                     (A, A · x (mod q))        ≈ε       (A, u) :                 A←

Quantum entropies.

Definition 4 (Quantum min-entropy). Let A and B be two quantum systems and let ̺ AB ∈ S≤ (H AB ) be
any bipartite state. The min-entropy of A conditioned on B of the state ̺ AB is defined as
                                                    n                                 o
                      Hmin ( A | B)̺ = max sup λ ∈ R : ̺ AB ≤ 2−λ 1 A ⊗ σB .
                                        σ∈S≤ (H B )

Definition 5 (Smooth quantum min-entropy). Let A and B be quantum systems and let ̺ AB ∈ S≤ (H AB ).
Let ε ≥ 0. We define the ε-smooth quantum min-entropy of A conditioned on B of ̺ AB as
                                  ε
                                 Hmin ( A | B)̺ =             sup              Hmin ( A | B)̺˜ .
                                                                ̺˜ AB
                                                        P ( ̺˜ AB ,̺ AB )≤ ε

    The conditional min-entropy of a CQ state ̺XB captures the difficulty of guessing the content of a
classical register X given quantum side information B. This motivates the following definition.



                                                             15
Definition 6 (Guessing probability). Let ̺XB ∈ D(H X ⊗ H B ) be a CQ state, where X is a classical register
over an alphabet X and B is a quantum system. Then, the guessing probability of X given B is defined as
                                                                  h           i
                        pguess ( X | B)̺ = sup ∑ Pr[ X = x]̺ · Tr MxB ̺B MxB † .
                                                  MxB x ∈X

    The following operational meaning of min-entropy is due to Koenig, Renner and Schaffner [KRS09].

Theorem 1 ( [KRS09], Theorem 1). Let ̺XB ∈ D(H X ⊗ H B ) be a CQ state, where X is a classical register
over an alphabet X and B is a quantum system. Then, it holds that
                                                                       
                                Hmin ( X | B)̺ = − log pguess ( X | B)̺ .

2.3 Fourier analysis
Let q ≥ 2 be an integer modulus and let m ∈ N. The q-ary (discrete) Fourier transform takes as input a
function f : Z m → C and produces a function fˆ : Z m
                                                    q → C (the Fourier transform of f ) defined by

                                                                                2πi
                                             fˆ(y) =                             q hy,xi
                                                           ∑ f ( x) · e                    .
                                                         x∈Z m

                                                 2πi
For brevity, we oftentimes write ωq = e q ∈ C to denote the primitive q-th root of unity. The m-qudit
q-ary quantum Fourier transform over the ring Z m
                                                q is defined by the operation,

                                                   p                     2πi
                                                                               hy,xi
                        FTq :    | xi     7→             q−m ∑ e q                     |y i ,   ∀x ∈ Z m
                                                                                                       q.
                                                              y∈Z nq


It is well known that the q-ary quantum Fourier transform can be efficiently performed on a quantum com-
puter for any modulus q ≥ 2 [HH00]. Note the quantum Fourier transform of a normalized quantum state

                             |Ψi =       ∑ f ( x) | xi            with           ∑ | f (x)|2 = 1,
                                        x∈Z m                                   x∈Z m

for a function f : Z m → C, results in the state (the Fourier transform of |Ψi) given by
                                         p                                2πi
                                                                                     
                                                                               hy,xi
                           FTq |Ψi = q       − m
                                                  ∑ ∑          f ( x ) · e  q          |y i
                                                         y∈Z nq    x∈Z m
                                             p
                                         =        q−m ∑ fˆ(y) |yi .
                                                         y∈Z nq

                                                                                                 q q
Notice that the Fourier transform of |Ψi is unitary if supp( f ) ⊆ Z m ∩ (− 2 , 2 ]m . We frequently make use
of the following standard identity for Fourier characters.
                                                                                                            2πi
Lemma 5 (Orthogonality of Fourier characters). Let q ≥ 2 be any integer modulus and let ωq = e q ∈ C
denote the primitive q-th root of unity. Then, for arbitrary x, y ∈ Z q :
                                                                  −v·y
                                                 ∑ ωqv·x ωq              = q δx,y .
                                                v ∈Z q



                                                                  16
2.4 Generalized Pauli operators
Definition 7 (Generalized Pauli operators). Let q ≥ 2 be an integer modulus and ωq = e2πi/q be the
primitive q-th root of unity. The generalized q-ary Pauli operators {Xbq }b∈Zq and {Zbq }b∈Zq are given by

                                        Xbq = ∑ | a + b (mod q)i h a| ,                   and
                                                a ∈Z q

                                        Zbq = ∑ ωqa·b | ai h a| .
                                                a ∈Z q

                                                             b1           bm          b1           bm
For b = (b1 , . . . , bm ) ∈ Z m                        b                        b
                               q , we use the notation Xq = Xq ⊗ · · · ⊗ Xq and Zq = Zq ⊗ · · · ⊗ Zq .

Lemma 6. Let q ≥ 2 be an integer modulus. Then, for all b ∈ Z q , it holds that

                                                         Zbq = FTq Xbq FT†q
                                                         Xbq = FT†q Zbq FTq .

Proof. It suffices to show the first identity only as the second identity follows by conjugation with FTq .
Using the orthogonality of Fourier characters over Z q (Lemma 5), we find that

           Zbq = ∑ ωqx ·b | xih x|
                   x ∈Z q
                                                                  !
                                       1                 − a·y′
               =     ∑        ωqx ·b       ∑    ωqx · a ωq            | x i y′
                     ′
                   x,y ∈Z q
                                       q a ∈Z q
                 1                          x ·y − x ′ ·y′
               =     ∑         ∑       ∑   ωq ωq           hy|a + b (mod q)i · h a| x′ i | xi y′
                 q x,y∈Zq x ′ ,y′ ∈Zq a∈Zq
                                           !                                                            
                 1                x ·y                                                       ′
                                                                                         − x ·y ′
                               ωq | xihy| ∑ | a + b (mod q)i h a|  ∑ ωq                          x′ y ′ 
                 q x,y∑
               =
                       ∈Z q                   a ∈Z q                        x ′ ,y′ ∈Z q

               = FTq Xbq FT†q .


Definition 8 (Pauli-Z dephasing channel). Let q ≥ 2 be an integer modulus and let m ∈ N. Let p be a
probability distribution over Z m
                                q . Then, the Pauli-Z dephasing channel with respect to p is defined as

                                   Zp ( ̺) =     ∑ pz Zzq ̺Z−q z ,               ∀̺ ∈ L((C q )⊗m ).
                                                z∈Z m
                                                    q


We use Z to denote the uniform Pauli-Z channel for which p is the uniform distribution over Z m
                                                                                              q.

   The following lemma shows that the uniform Pauli-Z channel on input ̺ returns a diagonal state which
consists of diagonal elements of ̺ encoded in the standard basis.
Lemma 7. Let q ≥ 2 be a modulus and m ∈ N. Then, the uniform Pauli-Z dephasing channel satsifies,

              Z(̺) = q−m ∑ Zzq ̺Z− z
                                 q =                        ∑ Tr[|xihx| ̺] |xihx| ,             ∀̺ ∈ L((C q )⊗m ).
                                  z∈Z m
                                      q                   x∈Z m
                                                              q



                                                                      17
Proof. Suppose that the state ̺ has the following form in the standard basis,
                                     ̺=      ∑ αx,y |xihy| ∈ L((Cq )⊗m ).
                                          x,y∈Z m
                                                q


Using the orthogonality of Fourier characters over Z q (Lemma 5), we obtain
                          Z(̺) = q−m ∑ Zzq ̺Z−
                                             q
                                               z

                                          z∈Z m
                                              q

                                 = q−m ∑            ∑ αx,y Zzq |xihy| Z−q z
                                          z∈Z m       m
                                              q x,y∈Z q
                                                                                       
                                                                         hx,zi    −hy,zi 
                                 =     ∑ αx,y q−m ∑ ωq                          ωq           |xihy|
                                     x,y∈Z m
                                           q                 z∈Z m
                                                                 q

                                 =    ∑ αx,x |xihx|
                                     x∈Z m
                                         q

                                 =    ∑ Tr[|xihx| ̺] |xihx| .
                                     x∈Z m
                                         q




2.5 Lattices and the Gaussian mass
A lattice Λ ⊂ R m is a discrete subgroup of R m . To avoid handling matters of precision, we will only
consider integer lattices Λ ⊆ Z m throughout this work. The dual of a lattice Λ ⊂ R m , denoted by Λ∗ , is
the lattice of all vectors y ∈ R m that satisfy hy, xi ∈ Z, for all vectors x ∈ Λ. In other words, we define
                              Λ∗ = {y ∈ R m : hy, xi ∈ Z, for all x ∈ Λ} .
Given a lattice Λ ⊂ R m and a vector t ∈ R m , we define the coset with respect to t as the lattice shift
Λ − t = {x ∈ R m : x + t ∈ Λ}. Note that many different shifts t can define the same coset.
   The Gaussian measure ̺σ with parameter σ > 0 is defined as the function
                                ̺σ (x) = exp(−π kxk2 /σ2 ),                      ∀x ∈ R m .
Let Λ ⊂ R m be a lattice and let t ∈ R m be a shift. We define the Gaussian mass of Λ − t as the quantity
                                          ̺ σ ( Λ − t) = ∑ ̺ σ ( y − t) .
                                                             y∈ Λ

   The discrete Gaussian distribution DΛ−t,σ is the distribution over the coset Λ − t that assigns probability
                         2  2
proportional to e−π kx−tk /σ for lattice points x ∈ Λ. In other words, we have
                                                        ̺ σ ( x − t)
                                     DΛ−t,σ (x) =                    ,       ∀x ∈ Λ.
                                                        ̺ σ ( Λ − t)
   We make use of the following tail bound for the Gaussian mass of a lattice [Ban93, Lemma 1.5 (ii)].
                                                                                                       1
Lemma 8. For any m-dimensional lattice Λ and shift t ∈ R m and for all σ > 0, c ≥ (2π )− 2 it holds that
                                          √                   m      2
                    ̺σ (Λ − t) \ B m (0, c mσ) ≤ (2πec2 ) 2 e−πc m ̺σ (Λ),
where Bm (0, s) = {x ∈ R m : kxk2 ≤ s} denotes the m-dimensional ball of radius s > 0.

                                                            18
q-ary lattices. In this work, we mainly consider q-ary lattices Λ that that satisfy qZ m ⊆ Λ ⊆ Z m , for
some integer modulus q ≥ 2. Specifically, we consider lattices generated by a matrix A ∈ Z nq ×m for some
n, m ∈ N. The first lattice consists of all vectors which are perpendicular to the rows of A, namely

                                Λ⊥             m
                                 q (A) = {x ∈ Z : A · x = 0 (mod q)}.

Note that Λ⊥                  m                                              m                         n
            q (A) contains qZ ; in particular, it contains the identity 0 ∈ Z . For any syndrome y ∈ Z q
                                                              y
in the column span of A, we also consider the lattice coset Λq (A) given by
                          y
                        Λq (A) = {x ∈ Z m : A · x = y (mod q)} = Λ⊥
                                                                  q (A) + u,

where u ∈ Z m is an arbitrary integer solution to the equation Au = y (mod q).
   The second lattice is the lattice generated by AT and is defined by

                      Λq (A) = {y ∈ Z m : y = AT · s (mod q), for some s ∈ Z n }.

The q-ary lattices Λq (A) and Λ⊥
                               q (A) are dual to each other (up to scaling). Specifically, we have


                          q · Λ⊥    ∗
                               q (A) = Λ q (A)            and       q · Λ q (A) ∗ = Λ ⊥
                                                                                      q (A).

Whenever A ∈ Z nq ×m is full-rank, i.e. the subset-sums of the columns of A generate Z nq , then
det(Λ⊥         n
     q (A)) = q . We use the following facts due to Gentry, Peikert and Vaikuntanathan [GPV07].

Lemma 9 ( [GPV07], Lemma 5.1). Let n ∈ N and let q ≥ 2 be a prime modulus with m ≥ 2n log q. Then,
for all but a q−n fraction of A ∈ Z nq ×m , the subset-sums of the columns of A generate Z nq . In other words,
                                − Z nq ×m is full-rank with overwhelming probability.
                                $
a uniformly random matrix A ←

Lemma 10 ( [GPV07], Corollary 5.4). Let np     ∈ N and q ≥ 2 be a prime with m ≥ 2n log q. Then, for all but
a 2q−n fraction of A ∈ Z nq ×m and σ = ω ( log m), the distribution of the syndrome A · e = u (mod q)
is within negligible total variation distance of the uniform distribution over Z nq , where e ∼ DZm ,σ .

    The following lemma is a consequence of [MR04, Lemma 4.4] and [GPV07, Lemma 5.3].

Lemma 11. Let n ∈ N and let q ≥ 2 be a prime modulus with m ≥ 2n log q. Let A ∈ Z nq ×m be a matrix
                                                   p
whose columns generate Z nq . Then, for any σ = ω ( log m) and for any syndrome y ∈ Z nq :
                                                  h           √     i
                                       Pr             kxk ≥       mσ ≤ negl(n).
                                   x∼ DΛy (A),σ
                                         q


Definition 9 (Periodic Gaussian). Let m ∈ N, let q ≥ 2 be a modulus and let σ > 0. The q-periodic
Gaussian ̺σ,q function is the periodic continuation of the Gaussian measure ̺σ , where

                                   ̺σ,q (x) = ̺σ (x + qZ m ),           ∀x ∈ R m .

    For any function f : Z m → C and lattice Λ ⊆ Z m , the well-known Poisson summation formula states
that f (Λ) = det(Λ∗ ) fˆ(Λ∗ ). We use the following variant of the formula which applies to q-ary lattices.




                                                          19
Lemma 12 (Poisson summation formula for q-ary lattices). Let q be a prime modulus and let A ∈ Z nq ×m
be any matrix whose columns generate Z nq . Let v, w ∈ Z m
                                                         q and σ > 0 be arbitrary. Then, it holds that

                                                 − 2πi
                                                    q hw,xi
                                                                   σm                        2πi
                          ∑       ̺ σ ( x) · e                 =    n
                                                                      · ∑ ̺q/σ,q (w + yA) · e q hy,vi .
                     x∈Λvq (A)
                                                                   q y∈Z n
                                                                                 q


Proof. Because A ∈ Z nq ×m is full-rank, it holds that det(Λ⊥         n        v
                                                            q (A)) = q . Let Λ q (A) be the lattice coset
given by Λ⊥                           m
          q (A) + u, for some u ∈ Z with A · u = v (mod q). By the Poisson summation formula,

                                         − 2πi
                                            q hw,xi                                     − 2πi
                                                                                           q hw,xi
                 ∑        ̺ σ ( x) · e                =        ∑         ̺ σ ( x) · e
              x∈Λvq (A)                                   x∈ Λ ⊥
                                                               q (A)+u

                                                              σm
                                                      =                              ∑       ̺1/σ (w + q · y) · e2πihy,ui
                                                          det(Λ⊥
                                                               q (A))        y∈ 1q Λ q (A)

                                                          σm                         2πi
                                                                                         hy,ui
                                                      =    n   ∑
                                                          q y∈ Λ (A)
                                                                     ̺q/σ (w + y) · e q
                                                                    q

                                                       σm                               2πi
                                                      = n ∑ ̺q/σ (w + yA + q · Z m ) · e q hA y,ui
                                                                                             ⊺

                                                        q y∈Z n
                                                                    q

                                                          σm                                         2πi
                                                      =        · ∑ ̺q/σ,q (w + yA) · e q hy,vi .
                                                          qn    y∈Z nq



                                                                                                     q q
    For x ∈ Z m , let [x]q denote the unique representative x̄ ∈ Z m ∩ (− 2 , 2 ]m such that x ≡ x̄ (mod q).
The following lemma due to Brakerski [Bra18] says that, whenever σ is much smaller than the modulus q,
the periodic Gaussian ̺σ,q is close to the non-periodic (but truncated) Gaussian.
Lemma 13 ( [Bra18], Lemma 2.6). Let q ≥ 2, x ∈ Z m such that k[x]q k < q/4 and σ > 0. Then,

                                                      ̺σ,q (x)             1      2
                                             1 ≤                 ≤ 1 + 2−( 2 (q/σ) −m) .
                                                      ̺σ ([x]q )

     A simple consequence of the tail bound in Lemma 8 is that√the discrete Gaussian DZm ,σ distribution is
essentially only supported on the finite set {x ∈ Z m : kxk ≤ σ m}, which suggests the use of truncation.
Given a modulus q ≥ 2 and σ > 0, we define the truncated discrete Gaussian distribution DZmq ,σ over the
                    q q                                     √
finite set Z m ∩ (− 2 , 2 ]m with support {x ∈ Z m
                                                 q : kxk ≤ σ m } as the density

                                                                             ̺ σ ( x)
                                               DZmq ,σ (x) =
                                                                             ∑  √
                                                                                         ̺σ (y)
                                                                   y∈Z m
                                                                       q ,kyk≤ σ m


We define the analogous periodic discrete Gaussian distribution DZmq ,σ,q as

                                                                             ̺σ,q (x)
                                             DZmq ,σ,q (x) =
                                                                             ∑  √
                                                                                         ̺σ,q (y)
                                                                   y∈Z m
                                                                       q ,kyk≤ σ m



                                                                        20
                                                        √
Lemma 14. Let m ∈ N, q ≥ 2 a modulus and let σ ∈ (0, q/ 8m). Consider the quantum states,
                        q                                      q
              |ψi = ∑     DZmq ,σ (x) |xi    and      |φ i = ∑   DZmq ,σ,q (x) |xi .
                           x∈Z m
                               q                                                   x∈Z m
                                                                                       q

Then, it holds that                                          r
                                                                            1
                                                                                          −1
                                                                                    2
                            k|ψihψ| − |φihφ|ktr ≤                1 − 1 + 2−( 2 (q/σ) −m)      .
Proof. We first bound the Hellinger distance,
                                                                        q
                           H 2 ( DZmq ,σ , DZmq ,σ,q ) = 1 − ∑              DZmq ,σ (x) · DZmq ,σ,q (x).           (4)
                                                              x∈Z m
                                                                  q

To this end, we define two normalization factors
                  Zσ =             ∑  √
                                            ̺σ (y)           and        Zσ,q =             ∑    √
                                                                                                      ̺σ,q (y).    (5)
                           y∈Z m
                               q ,kyk≤ mσ                                            y∈Z m
                                                                                         q ,kyk≤ mσ

                                                             q q
From Lemma 13, it follows for any x ∈ Z m ∩ (− 2 , 2 ]m with kxk < q/4 that
                                            1      2
                                                          −1
                         ̺2σ,q (x) · 1 + 2−( 2 (q/σ) −m)      ≤ ̺σ (x) · ̺σ,q (x).                                 (6)

Recall also that the truncated discrete Gaussian is supported on the finite set
                                                                      √
                                 supp( DZmq ,σ ) = {x ∈ Z m
                                                          q : kxk ≤     mσ}.
Plugging in Eq. (6), we can bound the Hellinger distance as follows:
                                                     q
                 H 2 ( DZmq ,σ , DZmq ,σ,q ) = 1 − ∑   DZmq ,σ (x) · DZmq ,σ,q (x)
                                                     x∈Z m
                                                         q
                                                     q                                     q
                                            = 1−         Zσ−1 · Zσ,q
                                                                 −1
                                                                                 ∑             ̺σ (x) · ̺σ,q (x)
                                                                                   √
                                                                        x∈Z m
                                                                            q ,kxk≤ mσ
                                                     s
                                                              Zσ−1 · Zσ,q
                                                                      −1
                                            ≤ 1−                    1        2             ∑          ̺σ,q (x)
                                                   1 + 2−( 2 (q/σ) −m) x∈Zmq ,kxk≤√mσ
                                                         1      2
                                                                      −1/2
                                            ≤ 1 − 1 + 2−( 2 (q/σ) −m)       .

Therefore, it holds that
                                                         q
                           k|ψihψ| − |φihφ|ktr ≤             1 − (1 − H 2 ( DZmq ,σ , DZmq ,σ,q ))2
                                                         r
                                                                        1
                                                                                      −1
                                                                                2
                                                     ≤       1 − 1 + 2−( 2 (q/σ) −m)      .



   The following result allows us to bound the total variation distance between a truncated discrete Gaussian
DZmq ,σ and its perturbation by a fixed vector e0 ∈ Z m .
Lemma 15 ( [BCM+ 21], Lemma 2.4). Let q ≥ 2 be a modulus, m ∈ N and σ > 0. Then, for any e0 ∈ Z m ,
                                                                −2π mke0 k 
                                                                    √

                       k DZq ,σ − ( DZq ,σ + e0 )kTV ≤ 2 · 1 − e
                           m          m                              σ        .

                                                              21
2.6 Cryptography
In this section, we review several definitions in cryptography.

Public-key encryption.

Definition 10 (Public-key encryption). A public-key encryption (PKE) scheme Σ = (KeyGen, Enc, Dec)
with plaintext space M is a triple of QPT algorithms consisting of a key generation algorithm KeyGen, an
encryption algorithm Enc, and a decryption algorithm Dec.

 KeyGen(1λ ) → (pk, sk) : takes as input the parameter 1λ and outputs a public key pk and secret key sk.

 Enc(pk, m) → CT : takes as input the public key pk and a plaintext m ∈ M, and outputs a ciphertext CT.

 Dec(sk, CT) → m′ or ⊥ : takes as input the secret key sk and ciphertext CT, and outputs m′ ∈ M or ⊥.

Definition 11 (Correctness of PKE). For any λ ∈ N, and for any m ∈ M:
                                                                  
                                               (pk,sk)←KeyGen(1λ )
                         Pr Dec(sk, CT) 6= m     CT←Enc(pk,m )
                                                                     ≤ negl(λ).

Definition 12 (IND-CPA security). Let Σ = (KeyGen, Enc, Dec) be a PKE scheme and let A be a QPT
adversary. We define the security experiment Expind-cpa
                                                Σ,A,λ ( b) between A and a challenger as follows:

   1. The challenger generates a pair (pk, sk) ← KeyGen(1λ ), and sends pk to A.

   2. A sends a plaintext pair (m0 , m1 ) ∈ M × M to the challenger.

   3. The challenger computes CTb ← Enc(pk, mb ), and sends CTb to A.

   4. A outputs a bit b′ ∈ {0, 1}, which is also the output of the experiment.

We say that the scheme Σ is IND-CPA-secure if, for any QPT adversary A, it holds that

               AdvΣ,A (λ) := | Pr[Expind-cpa                ind-cpa
                                     Σ,A,λ (0) = 1] − Pr[ExpΣ,A,λ (1) = 1]| ≤ negl( λ ).


2.7 The Short Integer Solution problem
The (inhomogenous) SIS problem was introduced by Ajtai [Ajt96] in his seminal work on average-case
lattice problems. The problem is defined as follows.

Definition 13 (Inhomogenous SIS problem, [Ajt96]). Let n, m ∈ N be integers, let q ≥ 2 be a modulus and
let β > 0 be a parameter. The Inhomogenous Short Integer Solution problem (ISIS) problem is to find a short
                                                                                     − Z nq ×m , y ←
solution x ∈ Z m with kxk2 ≤ β such that A · x = y (mod q) given as input a tuple (A ←             − Z nq ).
                                                                                      $             $


                                                                                       − Z nq ×m , 0 ∈ Z nq ).
                                                                                       $
The Short Integer Solution (SIS) problem is a homogenous variant of ISIS with input (A ←

    Micciancio and Regev [MR07] showed that the average-case SIS problem is as hard as approximating
worst-case lattice problems to within small factors. Gentry, Peikert and Vaikuntanathan [GPV07] sub-
            p an improved reduction showing that, for any m = poly(n), β = poly(n), and prime
sequently gave
q ≥ β · ω ( n log q ), the average-case problems SISn,m,q,β and ISISn,m,q,β are as hard as approximating the
                                                                                                     √
shortest independent vector problem (SIVP) problem in the worst case to within a factor γ = β · Õ( n).

                                                     22
2.8 The Learning with Errors problem
The Learning with Errors problem was introduced by Regev [Reg05] and serves as the primary basis of
hardness of post-quantum cryptosystems. The problem is defined as follows.

Definition 14 (“Search” LWE, [Reg05]). Let n, m ∈ N be integers, let q ≥ 2 be a modulus and let
α ∈ (0, 1) be a parameter. The Learning with Errors (LWE) problem is to find a secret vector s given as
input a sample (A, sA + e (mod q)) from the distribution LWEm                  − Z nq ×m and s ←
                                                                               $
                                                              n,q,αq , where A ←               − Z nq are
                                                                                               $


uniformly random, and where e ∼ DZm ,αq is sampled from the discrete Gaussian distribution.

Definition 15 (“Decisional” LWE, [Reg05]). Let n, m ∈ N be integers, let q ≥ 2 be a modulus and let
α ∈ (0, 1) be a parameter. The “decision” Learning with Errors (DLWE) problem is to distinguish between

                       − Z nq ×m , sA + e (mod q))                     − Z qn×m , u ←
                                                                                    − Zm
                       $                                               $            $
                    (A ←                                    and     (A ←               q ),


          − Z nq is uniformly random and where e ∼ DZm ,αq is a discrete Gaussian noise vector.
          $
where s ←
                                                                           √
     As shown in [Reg05], the LWEm  n,q,αq problem with parameter αq ≥ 2 n is at least as hard as approx-
imating the shortest independent vector problem (SIVP) to within a factor of γ = O     e (n/α) in worst case
lattices of dimension n. In this work we assume the subexponential hardness of LWEm     n,q,αq which relies on
the worst case hardness of approximating short vector problems in lattices to within a subexponential factor.


3 Primal and Dual Gaussian States
Our Dual-Regev-type encryption schemes with certified deletion in Section 7 and Section 9 rely on two
types of Gaussian superpositions, which we call primal and dual Gaussian states. The former (i.e., primal)
state corresponds to a quantum superposition of LWE samples with respect to a matrix A ∈ Z nq ×m , and (up
to a phase) can be thought of as a superposition of Gaussian balls around random lattice vectors in Λq (A).
The latter (i.e., dual) state corresponds to a Gaussian superposition over a particular coset,
                                  y
                                Λq (A) = {x ∈ Z m : A · x = y (mod q)},

of the q-ary lattice Λ⊥               m
                       q (A) = {x ∈ Z : A · x = 0 (mod q)} defined in Section 2.5.
    Our terminology regarding which state is primal and which state is dual is completely arbitrary. In fact,
the q-ary lattices Λq (A) and Λ⊥q (A) are both dual to each other (up to scaling), and satisfy


                          q · Λ⊥    ∗
                               q (A) = Λ q (A)        and     q · Λ q (A) ∗ = Λ ⊥
                                                                                q (A).

We choose to refer to the quantum superposition of LWE samples as the primal Gaussian state because it
corresponds directly to the ciphertexts of our encryption scheme, whereas the dual Fourier mode is only
used in order to prove deletion. We define primal and dual Gaussian states as follows.

Definition 16 (Gaussian states). Let m ∈ N, q ≥ 2 be an integer modulus and σ > 0. Then,

    • (primal Gaussian state:) for all A ∈ Z nq ×m and y ∈ Z m
                                                             q , we let

                                                                  −hs,yi
                            |ψA,y i = ∑       ∑ ̺q/σ (e) ωq                |sA + e (mod q)i ;
                                       s∈Z nq e∈Z m
                                                  q



                                                      23
    • (dual Gaussian state:) for all A ∈ Z nq ×m and y ∈ Z m
                                                           q , we let

                               |ψ̂A,y i =           ∑          ̺ σ ( x) | xi .
                                               x∈Z m
                                                   q
                                            Ax=y (mod q )


For simplicity, we oftentimes drop the subscript on A and write |ψy i and |ψ̂y i, respectively.

3.1 Duality lemma
The following lemma states that, up to negligible trace distance, the primal and dual Gaussian states in
Definition 16 are related via the q-ary quantum Fourier transform.
                                                                                      √        √
Lemma 16 (Duality lemma). Let m ∈ N, q ≥ 2 be a prime modulus and let σ ∈ ( 8m, q/ 8m ). Let
A ∈ Z nq ×m be a matrix whose columns generate Z nq and let y ∈ Z nq be arbitrary. Then, up to negligible
trace distance, the primal and dual Gaussian states are related via the quantum Fourier transform:

                 FTq |ψy i     ≈ε      |ψ̂y i =          ∑               ̺ σ ( x) | xi ;
                                                       x∈Z m
                                                           q
                                                    Ax=y (mod q )
                                                                                     −hs,yi
                 FT†q |ψ̂y i   ≈ε      |ψy i = ∑           ∑ ̺q/σ (e) ωq                        |sA + e (mod q)i ,
                                                    s∈Z nq e∈Z m
                                                               q


where ε : N → R + is a negligible function in the parameter m ∈ N.
Proof. Let y ∈ Z nq be an arbitrary vector and recall that the dual Gaussian coset |ψ̂y i is given by

                                          |ψ̂y i =             ∑              ̺ σ ( x) | xi .                         (7)
                                                          x∈Z m
                                                              q
                                                       Ax=y (mod q )

                 y
We denote by Λq (A) = {x ∈ Z m : Ax = y (mod q)} be the associated coset of the lattice Λ⊥       q (A).
                                                                       y
Consider now the Gaussian superposition over the entire lattice coset Λq (A) formally defined by

                                             |φ̂y i =          ∑
                                                               y
                                                                         ̺ σ ( x) | xi .                              (8)
                                                          x∈ Λ q ( A )
               √
Since σ < q/ 8m, it follows from the tail bound in Lemma 11 that the state in (7) is within negligible
trace distance of the state in Eq. (8). Applying the (inverse) quantum Fourier transform, we get
                                                                                
                                def                                       −hx,zi
                          |φy i = FT†q |φ̂y i = ∑          ∑ ̺ σ ( x) · ω q        | zi .          (9)
                                                       z∈Z m              y
                                                           q       x∈ Λ q ( A )

From the Poisson summation formula (Lemma 12) and a subsequent change of variables, it follows that
                                                                
                                                           hs,yi
                      |φy i = ∑       ∑ ̺q/σ,q (z + sA) · ωq |zi
                                    z∈Z m
                                        q    s∈Z nq
                                                                       −hs,yi
                                = ∑         ∑ ̺q/σ,q (e) · ωq                     |sA + e (mod q)i .                 (10)
                                    s∈Z nq e∈ Zqm



                                                               24
              √
Because σ >       8m it follows from Lemma 14 that there exists
                                            q
                                                                −1
                                     κ (m) = 1 − (1 + 2−3m ) ≥ 0

such that
                                                                   −hs,yi
                           |φy i ≈κ ∑         ∑ ̺q/σ (e) · ωq                |sA + e (mod q)i .          (11)
                                      s∈Z nq e∈ Zqm


Putting everything together, it follows from the triangle inequality that
                                                                                   −hs,yi
                       FT†q |ψ̂y i    ≈ε      |ψy i = ∑          ∑ ̺q/σ (e) ωq              |sA + ei ,
                                                          s∈Z nq e∈Z m
                                                                     q

                                                      p         √
where ε(m) = negl(m) + κ (m). Using that         1 − 1/(1 + x) ≤ x for all x > 0, we have
                                                      q
                                                                      −1
                                     ε(m) = negl(m) + 1 − (1 + 2−3m )
                                                                    3m
                                           ≤ negl(m) + 2− 2 .

Thus, we have that ε(m) ≤ negl(m). This proves the claim.
                                                        √         √
Corollary 1. Let m ∈ N, q ≥ 2 be a prime and σ ∈ ( 8m, q/ 8m). Let A ∈ Z nq ×m be a matrix whose
columns generate Z nq and let y ∈ Z nq be arbitrary. Then, there exists a negligible function ε(m) such that

                                 FTq Xvq |ψy i        ≈ε      Zvq |ψ̂y i ,      ∀v ∈ Z m
                                                                                       q.

Proof. From Lemma 6 it follows that FTq Xvq = Zvq FTq , for all v ∈ Z m    q . Moreover, Lemma 16 implies that
FTq |ψy i is within negligible trace distance of |ψ̂y i. This proves the claim.

3.2 Efficient state preparation
In this section, we give two algorithms that prepare the primal and dual Gaussian
                                                                             √ states from Definition 16.
                                                  m
We remark that Gaussian superpositions over Z q with parameter σ = Ω( m) can be efficiently imple-
mented using standard quantum state preparation techniques, for example using rejection sampling and the
Grover-Rudolph algorithm. We refer to [GR02, Reg05, Bra18, BCM+ 21]) for a reference.
    Our first algorithm (see Algorithm 1 in Figure 2) prepares the√dual Gaussian state from Definition 16
with respect to an input matrix A ∈ Z nq ×m and parameter σ = Ω( m), and is defined as follows.
    Our second algorithm (see Algorithm 2 in Figure  √ 3) prepares the primal Gaussian state with respect to
an input matrix A ∈ Z nq ×m and parameter σ = Ω( m). Here, in order for Lemma 16 to apply, it is crucial
that the columns of A generate Z nq . Fortunately, it follows from Lemma 9 that a uniformly random matrix
 − Z nq ×m satisfies this property with overwhelming probability.
 $
A←

3.3 Invariance under Pauli-Z dephasing
In this section, we prove a surprising property about the dual Gaussian state from Definition 16. We prove
Theorem 2, which says that the Pauli-Z dephasing channel with respect to the LWE distribution leaves the
dual Gaussian state approximately invariant.

                                                              25
  Algorithm 1: GenDual(A, σ)
                                                   √
   Input: Matrix A ∈ Z nq ×m and parameter σ = Ω( m).
   Output: Gaussian state |ψ̂y i and y ∈ Z nq .
 1 Prepare a Gaussian superposition in system X with parameter σ > 0:


                                               |ψ̂ i XY =     ∑ ̺ σ ( x) | xi X ⊗ | 0i Y .
                                                             x∈Z m
                                                                 q




 2 Apply the unitary UA : |xi |0i → |xi |A · x (mod q)i on systems X and Y:


                                    |ψ̂ i XY =      ∑ ̺σ (x) |xi X ⊗ |A · x (mod q)iY .
                                                   x∈Z m
                                                       q




 3 Measure system Y in the computational basis, resulting in the state


                                               |ψ̂y i XY =     ∑ ̺ σ ( x) | xi X ⊗ | y i Y .
                                                             x∈Z m
                                                                 q :
                                                             Ax=y



 4 Output the state |ψ̂y i in system X and the outcome y ∈ Z n
                                                             q in system Y.

                                                                                                  √
Figure 2: Quantum algorithm which takes as input a matrix A ∈ Z nq ×m and a width parameter σ = Ω( m),
and outputs the dual Gaussian state in Definition 16.


Theorem 2. Let n, m ∈ N be integers  √ and let√q ≥ 2 be a prime modulus, each parameterized        by the
                                                                                         n
security parameter λ ∈ N. Let σ ∈ ( 8m, q/ 8m ) be a function of λ. Let y ∈ Z q be any vector and
A ∈ Z nq ×m be any matrix whose columns generate Z nq , and let |ψ̂y i be the dual Gaussian state,

                                                |ψ̂y i =          ∑           ̺ σ ( x) | xi .
                                                                x∈Z m
                                                                    q
                                                             Ax=y (mod q )

Let ZLWEmn,q,αq be the Pauli-Z dephasing channel with respect to the LWEm                             n×m
                                                                        n,q,αq distribution for A ∈ Z q
and a noise ratio α ∈ (0, 1) with relative noise magnitude 1/α = σ · 2o(n) , i.e.
                                                                                      −( s0 ·A+e0 )
        ZLWEmn,q,αq (̺) =    ∑ ∑ q−n DZ ,αq (e0 ) Zsq ·A+e ̺ Zq
                                                       m
                                                       q
                                                                          0    0
                                                                                                      ,   ∀̺ ∈ L((C q )⊗m ).
                            s0 ∈Z nq e0 ∈Z m
                                           q


Then, there exists a negligible function ε(λ) such that

                                          ZLWEmn,q,αq ( ψ̂y ψ̂y ) ≈ε ψ̂y ψ̂y .

In other words, the Pauli-Z dephasing channel with respect to the LWE distribution leaves the dual Gaussian
state approximately invariant.

                                                                     26
  Algorithm 2: GenPrimal(A, σ)
                                                                                 √
   Input: Matrix A ∈ Z nq ×m whose columns generate Z nq , and a parameter σ = Ω( m).
   Output: Gaussian state |ψy i and y ∈ Z nq .
 1 Run GenDual(A, σ), resulting in the state


                                        |ψ̂y i XY =        ∑ ̺ σ ( x) | xi X ⊗ | y i Y .
                                                       x∈Z m
                                                           q :
                                                       Ax=y



 2 Apply the quantum Fourier transform FTq to system X.
 3 Output the state in system X, denoted by |ψy i, and the outcome y ∈ Z n
                                                                         q in system Y.

                                                                                            √
Figure 3: Quantum algorithm which takes as input a matrix A ∈ Z nq ×m and a parameter σ = Ω( m), and
outputs the primal Gaussian state in Definition 16.

Proof. Let y ∈ Z nq be an arbitrary vector and recall that the dual Gaussian state |ψ̂y i is given by
                                         |ψ̂y i =              ∑         ̺ σ ( x) | xi .                                       (12)
                                                          x∈Z m
                                                              q
                                                       Ax=y (mod q )

Consider a sample b = s0 · A + e0 (mod q)) ∼ LWEm      n,q,αq with s ←− Z nq and e0 ∼ DZmq ,αq . Because
                                                                      $

     √        √
σ ∈ ( 8m, q/ 8m ) and 1/α = σ · 2o(n) , there exist negligible η (λ) and κ (λ) such that
                  Zqs0 ·A+e0 |ψ̂y i = FTq Xsq0 ·A+e0 FT†q |ψ̂y i                                   (Lemma 6)
                                  ≈η FTq Xsq0 ·A+e0 |ψy i                                          (Lemma 16)
                                           hs ,yi
                                  ≈κ ωq 0 FTq |ψy i                                                (Lemma 15)
                                           hs ,yi
                                  ≈η ωq 0           |ψ̂y i .                                       (Lemma 16)
Here, |ψy i is the primal Gaussian state given by
                                                                    −hs,yi
                           |ψy i = ∑         ∑ ̺q/σ (e) ωq                   |sA + e (mod q)i .
                                    s∈Z nq e∈Z m
                                               q


In other words, |ψ̂y i in Eq. (12) is an approximate eigenvector of the generalized Pauli operator Zqs0 ·A+e0
                                                                                                     hs ,yi
with respect to the same matrix A ∈ Z nq ×m . Note that we can simply discard ωq 0                            ∈ C because it serves
as a global phase. Hence, there exists a negligible function ε(λ) such that
                                                                                                              −( s0 ·A+e0 )
            ZLWEmn,q,αq ( ψ̂y ψ̂y ) =     ∑ ∑ q−n DZ ,αq (e0 ) Zsq ·A+e ψ̂y ψ̂y Zq
                                                                     m
                                                                     q
                                                                                    0      0

                                        s0 ∈Z nq e0 ∈Z m
                                                       q
                                                            !                                 

                                    ≈ε        ∑ q−n            ·  ∑ DZmq ,αq (e0 ) ψ̂y ψ̂y
                                            s0 ∈Z nq                e0 ∈Z m
                                                                          q

                                    = ψ̂y ψ̂y .



                                                               27
4 Uncertainty Relation for Fourier Basis Projections
In this section, we prove an entropic uncertainty relation with respect to so-called Fourier basis projections.
Informally, we say that a projector Π  b is a Fourier basis projection, if Π
                                                                           b corresponds to a projector (onto a
             m
subset of Z q ) which is conjugated by the q-ary Fourier transform FTq . Notice that the deletion procedures of
our encryption schemes with certified deletion in Section 7 and Section 9 require a Fourier basis projection
onto a small set of solutions to the (inhomogenous) short integer solution (ISIS) problem. Another example
can be found in the work of Aaronson and Christiano [AC12] who used Hadamard basis projections (a
special case of the q-ary Fourier transform) onto small hidden subspaces to verify quantum money states.
    Our uncertainty relation captures the following intuitive property: any system which passes a Fourier
basis projection onto a small subset of Z mq (say, with high probability) must necessarily be unentangled with
any auxiliary system. We formalize this statement using the (smooth) quantum min-entropy (Definition 5).

4.1 Fourier basis projections
Definition 17 (Fourier basis projection). Let m ∈ N and let q ≥ 2 be an integer modulus. Let S ⊆ Z m
                                                                                                   q be
an arbitrary set and let ΠS be the associated projector onto S , where

                                                ΠS = ∑ |xihx|.
                                                        x∈S

Then, we define the associated Fourier basis projection onto S as the projector

                                               b S = FT†q ΠS FTq .
                                               Π

4.2 Uncertainty relation
In this section, our main result is the following.

Theorem 3 (Uncertainty relation for Fourier basis projections). Let m ∈ N, q ≥ 2 be a modulus,
{|ψx i}x∈Zmq be any family of normalized auxiliary states, and let |ψi AB be any state of the form

                         |ψi AB =    ∑ α x | xi A ⊗ | ψ x i B    s.t.    ∑ |αx |2 = 1.
                                    x∈Z m
                                        q                               x∈Z m
                                                                            q


Let S ⊆ Z m
          q be an arbitrary set and define the following projectors onto system A,


                               ΠS = ∑ |xihx|           and      b S = FT†q ΠS FTq .
                                                                Π
                                       x∈S

               b S ⊗ 1 B ) |ψi k2 = 1 − ε, for some ε ≥ 0. Then, it holds that
Suppose that k(Π              AB
                                      √
                                          ε
                                    Hmin ( X | B)̺ ≥ m · log q − 2 · log |S|.

Here, ̺XB results from a computational basis measurement of system A of the state |ψihψ| AB , i.e.

                           ̺XB =     ∑ |xihx|X ⊗ trA [(|xihx| A ⊗ 1 B )|ψihψ| AB ] .
                                    x∈Z m
                                        q




                                                         28
Proof. Suppose that |ψi AB satisfies k(Π  b S ⊗ 1 B ) |ψi k2 = 1 − ε, for some ε ≥ 0. From Lemma 2, it
                                                         AB
follows that there exists an ideal pure state,

                          b S ⊗ 1 B ) |ψi
                         (Π
           |ψ̄ i AB =
                          b
                                          AB
                                             = ∑ ᾱx |xi A ⊗ |ψx i B
                        k(ΠS ⊗ 1 B ) |ψi AB k x∈Zmq
                                                                                                                       s.t.         ∑ |ᾱx |2 = 1,
                                                                                                                                   x∈Z m
                                                                                                                                       q


with the property that
                                                                      √
                            k|ψihψ| − |ψ̄ihψ̄ |ktr ≤                          ε      and                   b S ⊗ 1 B ).
                                                                                                |ψ̄ i ∈ im(Π
                                                    b S ⊗ 1 B , we have
Because |ψ̄ i AB lies in the image of the projector Π

                         b S ⊗ 1 B ) |ψ̄ i = q−m                                                           hx,si       −hx′ ,si                 ′
             |ψ̄ i AB = (Π                AB                                      ∑ ∑ ᾱx′ · ωq                    ωq             | xi A ⊗ | ψ x i B .
                                                                                  ′
                                                                           x,x ∈Z m
                                                                                  q s∈S


Let us now analyze the ideal state ̺¯ XB which results from a computational basis measurement of system A
of the state |ψ̄ ihψ̄| AB . In other words, we consider the CQ state given by

                                ̺¯ XB =          ∑ |xihx|X ⊗ trA [(|xihx| A ⊗ 1 B )|ψ̄ihψ̄| AB ] .
                                              x∈Z m
                                                  q


By the definition of the guessing probability in Definition 6, we have
                                                                                                2
         pguess ( X | B)̺¯ = sup ∑                   (|xihx| A ⊗ MBx ) |ψ̄ i AB
                                   M Bx x ∈Z m
                                             q

                                                                                                                                                     2
                                                                                            hx,si −hx′ ,si                ′
                             = sup ∑ q−2m                         ∑ ∑               ᾱx′ · ωq ωq           |xi A ⊗ MBx |ψx i B
                                   M Bx x ∈Z m
                                             q                   x′ ∈Z m
                                                                       q s∈S

                                                                                                                                                         2
                                                                                                                       
                                                                                               hx,si        −hx′ ,si                            x′
                             = sup ∑ q−2m                           ∑ ᾱx′ · ∑ ωq                      ωq                     |xi A ⊗ MBx |ψ i B             .
                                   M Bx    x ∈Z m
                                                q
                                                                  ′
                                                                 x ∈Z m
                                                                      q                  s∈S


Using the Cauchy-Schwarz-inequality, we find that for any x ∈ Z m
                                                                q:


                                                                       
                                                    hx,si    −hx′ ,si                                  ′
                        ∑     ᾱx′ ·       ∑ ωq             ωq                |xi A ⊗ MBx |ψx i B
                      ′
                   x ∈Z m                  s∈S
                        q
                   v                                                                   v
                   u                                                               2 u                                                       2
                   u                                        hx,si     −hx′ ,si         u
                  ≤t ∑                 ᾱx′ ·       ∑ ωq            ωq                ·t ∑                    |xi A ⊗ MBx |ψx′ i B
                            x′ ∈Z m
                                  q                 s∈S                                        x′ ∈Z m
                                                                                                     q

                      s                                v
                                                       u                                                           2
                                                    2 u
                  ≤         |S|2        ∑       ᾱx′ · t ∑                        |xi A ⊗ MBx |ψx′ i B
                                      ′
                                   x ∈Z m
                                        q                        x′ ∈Z m
                                                                       q
                          v
                          u                                           2
                          u
                  = |S| · t ∑                    MBx |ψx′ i B             .                                                                                      (13)
                                    x′ ∈Z m
                                          q




                                                                                   29
Using the inequality in (13), we can now bound the guessing probability as follows:

                                |S|2                       ′                     2
          pguess ( X | B)̺¯ ≤     2m
                                     · sup ∑ ∑ MBx |ψx i B
                                q       M Bx x∈Z m x′ ∈Z m
                                                      q       q

                                |S|2                                        ′   2
                          =            ·        ∑ sup ∑           MBx |ψx i B
                                q2m           ′
                                           x ∈Z m M Bx x∈Z m
                                                q          q

                                |S|2
                          =          .                                                            (since ∑ MBx = 1 )
                                 qm                                                                      x

Because the purified distance is bounded above by the trace distance, it follows that
                                                                                    √
                    P(̺XB , ̺¯ XB ) ≤ k̺XB − ̺¯XB ktr ≤ k|ψihψ| − |ψ̄ ihψ̄|ktr ≤ ε.

Therefore, by the definition of (smooth) min-entropy (see Definition 5), we have
                                                                                          √
                                                                                              ε
                     Hmin ( X | B)̺¯ ≤                sup            Hmin ( X | B)σ = Hmin ( X | B)̺ .                 (14)
                                                        σXB     √
                                                P ( σXB ,̺ XB )≤ ε

Putting everything together, it follows from (14) and Theorem 1 that
                                      √
                                          ε
                                  Hmin ( X | B)̺ ≥ Hmin ( X | B)̺¯
                                                                                      
                                                          = − log pguess ( X | B)̺¯
                                                          ≥ m · log q − 2 · log |S|.

This proves the claim.


5 Gaussian-Collapsing Hash Functions
Unruh [Unr15] introduced the notion of collapsing hash functions in his seminal work on computationally
binding quantum commitments. This property is captured by the following definition.

Definition 18 (Collapsing hash function, [Unr15]). Let λ ∈ N be the security parameter. A hash function
family H = { Hλ }λ∈N is called collapsing if, for every QPT adversary A,

              | Pr[CollapseExpH,A,λ (0) = 1] − Pr[CollapseExpH,A,λ (1) = 1]| ≤ negl(λ).

Here, the experiment CollapseExpH,A,λ (b) is defined as follows:
                                                      $
                                                      − Hλ , and sends a description of h to A.
   1. The challenger samples a random hash function h ←

   2. A responds with a (classical) string y ∈ {0, 1}n(λ) and an m(λ)-qubit quantum state in system X.

   3. The challenger coherently computes h (into an auxiliary system Y) given the state in system X, and
      then performs a two-outcome measurement on Y indicating whether the output of h equals y. If h
      does not equal y the challenger aborts and outputs ⊥.


                                                                  30
   4. If b = 0, the challenger does nothing. Else, if b = 1, the challenge measures the m(λ)-qubit system
      X in the computational basis. Finally, the challenger returns the state in system X to A.

   5. A returns a bit b′ , which we define as the output of the experiment.

    Motivated by the properties of the dual Gaussian state from Definition 16, we consider a special class
of hash functions which are collapsing with respect to Gaussian superpositions. Informally, we say that a
hash function h is Gaussian-collapsing if it is computationally difficult to distinguish between a Gaussian
superposition of pre-images and a single (measured) Gaussian pre-image (of h). We formalize this below.

Definition 19 (Gaussian-collapsing hash function). Let λ ∈ N be the security parameter, m(λ), n(λ) ∈ N
and let q(λ) ≥ 2 be a modulus. Let σ > 0. A hash function family H = { Hλ }λ∈N with domain X = Z m   q
and range Y = Z nq is called σ-Gaussian-collapsing if, for every QPT adversary A,

        | Pr[GaussCollapseExpH,A,λ (0) = 1] − Pr[GaussCollapseExpH,A,λ (1) = 1]| ≤ negl(λ).

Here, the experiment GaussCollapseExpH,A,λ (b) is defined as follows:
                                                      $
                                                      − Hλ and prepares the quantum state
   1. The challenger samples a random hash function h ←

                                      |ψ̂ i XY =     ∑ ̺σ (x) |xi X ⊗ |h(x)iY .
                                                   x∈Z m
                                                       q



   2. The challenger measures system Y in the computational basis, resulting in the state

                                       |ψ̂y i XY =     ∑ ̺ σ ( x) | xi X ⊗ | y i Y .
                                                     x∈Z m
                                                         q :
                                                     h(x)=y


   3. If b = 0, the challenger does nothing. Else, if b = 1, the challenger measures system X of the
      quantum state |ψ̂y i in the computational basis. Finally, the challenger sends the outcome state in
      systems X to A, together with the string y ∈ Z nq and a classical description of the hash function h.

   4. A returns a bit b′ , which we define as the output of the experiment.

    The following follows immediately from the definition of Gaussian-collapsing hash functions, and the
fact that the dual Gaussian state can be efficiently prepared using Algorithm 1.

Claim 1. Let H = { Hλ }λ∈N be a hash function family with domain X = Z m                     n
                                                                           q and range Y = Z q , where
                                                                                        √
m(λ), n(λ) ∈ N. If H is collapsing, then H is also σ-Gaussian-collapsing, for any σ = Ω( m).

5.1 Ajtai’s hash function
Liu and Zhandry [LZ19] implicitly showed that the Ajtai hash function hA (x) = Ax (mod q) is collapsing
– and thus Gaussian-collapsing – via the notion of lossy functions and by assuming the superpolynomial
hardness of (decisional) LWE. In this section, we give a simple and direct proof that the Ajtai hash function
is Gaussian-collapsing assuming (decisional) LWE, which might be of independent interest.




                                                           31
Theorem√          ∈ N and q ≥ 2 be a prime modulus with m ≥ 2n log q, each parameterized by λ ∈ N.
         4. Let n √
Let σ ∈ ( 8m, q/ 8m ) be a function of λ. Then, the Ajtai hash function family H = { Hλ }λ∈N with
                       n                                                              o
                                                                                  n×m
                  Hλ = h A : Z m
                               q →   Z n
                                       q s.t. h A ( x ) = A · x ( mod q ) ; A ∈ Z q


is σ-Gaussian-collapsing assuming the quantum hardness of the decisional LWEm
                                                                            n,q,αq problem, for any
                                                              o
parameter α ∈ (0, 1) with relative noise magnitude 1/α = σ · 2 .( n )


Proof. Let A denote the QPT adversary in the experiment GaussCollapseExpH,A,λ (b) with b ∈ {0, 1}.
To prove the claim, we give a reduction from the decisional LWEm
                                                               n,q,αq assumption. We are given as input
                            × n , where b = s · A + e (mod q)) is either a sample from the LWE
                       − Zm
                       $
a sample (A, b) with A ←  q                  0       0
                                                                                         − Zm
                     − Z nq and e0 ∼ DZm ,αq , or where b is a uniformly random string u ←
                     $                                                                   $
distribution with s0 ←                                                                      q.
    Consider the distinguisher D that acts as follows on input 1λ and (A, b):

   1. D prepares a bipartite quantum state on systems X and Y with

                                  |ψ̂ i XY =      ∑ ̺σ (x) |xi X ⊗ |A · x (mod q)iY .
                                                x∈Z m
                                                    q



   2. D measures system Y in the computational basis, resulting in the state

                                           |ψ̂y i XY =      ∑ ̺ σ ( x) | xi X ⊗ | y i Y .
                                                           x∈Z m
                                                               q :
                                                           Ax=y


   3. D applies the generalized Pauli-Z operator Zbq on system X, resulting in the state
                                                                                        
                              (Zbq ⊗ 1Y ) |ψ̂y i XY =          ∑         ̺σ (x) Zbq |xi X ⊗ |yiY .
                                                              x∈Z m
                                                                  q :
                                                              Ax=y


   4. D runs the adversary A on input system X and classical descriptions of A ∈ Z nq ×m and y ∈ Z nq .

   5. D outputs whatever bit b′ ∈ {0, 1} the adversary A outputs.

Suppose that, for every λ ∈ N, there exists a polynomial p(λ) such that

                                                                                                            1
         | Pr[GaussCollapseExpH,A,λ (0) = 1] − Pr[GaussCollapseExpH,A,λ (1) = 1]| ≥                              .
                                                                                                           p( λ)

We now show that this implies that D succeeds at the decisional LWEm  n,q,αq experiment with advantage at
least 1/p(λ) − negl(λ). We distinguish between the following two cases.
    If (A, b) is a sample from the LWE distribution with b = s0 · A + e0 (mod q)), then the adversary A
receives as input the following quantum state in system X:
                                                                                                     −( s0 ·A+e0 )
          ZLWEmn,q,αq ( ψ̂y ψ̂y X ) =    ∑ ∑ q−n DZ ,αq (e0 ) Zsq ·A+e ψ̂y ψ̂y X Zq
                                                                     m           0    0
                                                                                                                     .
                                        s0 ∈Z nq e0 ∈Z m




                                                              32
From Theorem 2 it follows that there exists a negligible function ε(λ) such that

                                        ZLWEmn,q,αq ( ψ̂y ψ̂y X ) ≈ε ψ̂y ψ̂y X .

In other words, A receives as input a state in system X which is within negligible trace distance of the dual
Gaussian state |ψ̂y i, which corresponds precisely to the input in GaussCollapseExpH,A,λ (0).
                                                                               − Zm
                                                                               $
    If (A, b) is a uniformly random sample, where b is a random string u ←         q , then the adversary A
receives as input the following quantum state in system X:

                                 Z( ψ̂y ψ̂y X ) = q−m ∑ Zuq ψ̂y ψ̂y X Z− u
                                                                       q .
                                                                   u ∈Z m
                                                                        q


Because Z corresponds to the uniform Pauli-Z dephasing channel, it follows from Lemma 7 that
                                                                                    2
                                     Z( ψ̂y ψ̂y X ) =          ∑         hx|ψ̂y i       |xihx| X .
                                                              x∈Z m
                                                                  q


In other words, A receives as input a mixed state which is the result of a computational basis measurement
of the Gaussian state |ψ̂y i. Note that this corresponds precisely to the input in GaussCollapseExpH,A,λ (1).
    By assumption, the adversary A succeeds with advantage at least 1/p(λ). Therefore, the distinguisher
D succeeds at the decisional LWEm   n,q,αq experiment with probability at least 1/p( λ ) − negl( λ ).

Theorem 5. Let n ∈ N and q ≥ 2 √                √ modulus with m ≥ 2n log q, each
                                       be a prime                                       parameterized by the
security parameter λ ∈ N. Let σ ∈ ( 8m, q/ 8m) be a function of λ and A ←         $
                                                                                    Z n × m be a matrix.
                                                                                 − q
    Then, the following states are computationally indistinguishable assuming the quantum hardness of
decisional LWEmn,q,αq , for any parameter α ∈ (0, 1) with relative noise magnitude 1/α = σ · 2
                                                                                                o(n) :


    • For any (|ψ̂y i , y) ← GenDual(A, σ) in Algorithm 1:

                      |ψ̂y i =           ∑         ̺ σ ( x) | xi        ≈c     |x0 i :          x0 ∼ DΛyq (A), √σ .
                                                                                                                  2
                                      x∈Z m
                                          q
                                   Ax=y (mod q )


    • For any (|ψy i , y) ← GenPrimal(A, σ) in Algorithm 2:

                                             −hs,yi                                       −hu,x0 i
            |ψy i = ∑      ∑ ̺ ( e) ω q
                                    q
                                    σ
                                                      |sA + ei ≈c              ∑ ωq                  |u i :   x0 ∼ DΛyq (A), √σ .
                                                                                                                               2
                    s∈Z nq e∈Z m
                               q                                             u ∈Z m
                                                                                  q



Moreover, the distribution of y ∈ Z nq is negligibly close in total variation distance to the uniform distribution
                   y
over Z nq . Here, Λq (A) = {x ∈ Z m : Ax = y (mod q)} denotes a coset of the lattice Λ⊥        q (A).

                − Z nq ×m be a random matrix. From Lemma 9 it follows that the columns of A generate Z nq
                $
Proof. Let A ←
with overwhelming probability. Let us also recall the following simple facts about the discrete Gaussian.
According to Lemma 10, the distribution of the syndrome A · x = y     p(mod q) is statistically close to the
                               n
uniform distribution over Z q , whenever x ∼ DZ ,σ and σ = ω ( log m). Moreover, the conditional
                                                   m

distribution of x ∼ DZm ,σ given the syndrome y ∈ Z nq is a discrete Gaussian distribution DΛyq (A),σ .



                                                                   33
    Let us now show the first statement. Recall that in Theorem 4 we show that the Ajtai hash function
hA (x) = A · x (mod q) is σ-Gaussian-collapsing assuming the decisional LWEm       n,q,αq assumption and a
                       o ( n )                  n
noise ratio 1/α = σ · 2 . Therefore, for y ∈ Z q , the (normalized variant of the) dual Gaussian state,

                                                   |ψ̂y i =          ∑          ̺ σ ( x) | xi
                                                                   x∈Z m
                                                                       q :
                                                                Ax=y (mod q )

is computationally indistinguishable from the (normalized) classical mixture,
                                                            −1

                            2                                                
             ∑      hx|ψ̂y i |xihx| = 
                                                        ∑           ̺σ/√2 (z)
                                                                                                ∑        ̺σ/√2 (x) |xihx| ,
            x∈Z m
                q                                      z∈Z m
                                                           q :                                  x∈Z m
                                                                                                    q :
                                                   Az=y (mod q )                         Ax=y (mod q )
                                                                                    √        √
which is the result of a computational basis measurement of |ψ̂y i.4 Since σ ∈ ( 8m, q/ 8m), the tail
bound in Lemma 11 implies that the above mixture is statistically close to the discrete Gaussian DΛyq (A), √σ .
                                                                                                                               2
    The second statement follows immediately by applying the (inverse) Fourier transform to both of the
states above. Note that in Lemma 16 we showed that the primal Gaussian state
                                                                                −hs,yi
                                            |ψy i = ∑           ∑ ̺ ( e) ω q
                                                                      q
                                                                      σ
                                                                                         |sA + ei
                                                      s∈Z nq e∈Z m
                                                                 q


is within negligible trace distance of FT†q |ψ̂y i. This proves the claim.


5.2 Strong Gaussian-collapsing conjecture
Our quantum encryption schemes with certified deletion in Section 7 and Section 9 rely on the assumption
that Ajtai’s hash function satisfies a strong Gaussian-collapsing property in the presence of leakage. We
formalize the property as the following simple and falsifiable conjecture.
Conjecture (Strong Gaussian-Collapsing Conjecture).
Let λ ∈ N be
          √ the security parameter, n(λ) ∈ N, q(λ) ≥ 2 be a modulus and m ≥ 2n log q be an integer.
Let σ = Ω( m) be a parameter and let H = { Hλ }λ∈N be the Ajtai hash function family with
                       n                                                              o
                                                                                  n×m
                 Hλ = h A : Z mq  →  Z n
                                       q s.t. h A ( x ) = A · x ( mod q ) ; A ∈ Z q     .

The Strong Gaussian-Collapsing Conjecture (SGCn,m,q,σ ) states that, for every QPT adversary A,
 | Pr[StrongGaussCollapseExpH,A,λ (0) = 1] − Pr[StrongGaussCollapseExpH,A,λ (1) = 1]| ≤ negl(λ).
Here, the experiment StrongGaussCollapseExpH,A,λ (b) is defined as follows:
                                $                  n ×( m −1)
   1. The challenger samples Ā ←
                                − Zq                            and prepares the quantum state
                                            |ψ̂ i XY =    ∑ ̺σ (x) |xi X ⊗ |A · x (mod q)iY ,
                                                         x∈Z m
                                                             q


                                                                   − {0, 1}m−1 .
      where A = [Ā|Ā · x̄ (mod q)] ∈ Z nq ×m is a matrix with x̄ ←
                                                                   $


  4 Here, the additional factor 1/
                                     √
                                         2 arises from the normalization of the dual Gaussian state | ψ̂y i.


                                                                      34
   2. The challenger measures system Y in the computational basis, resulting in the state

                                         |ψ̂y i XY =        ∑          ̺ σ ( x) | xi X ⊗ | y i Y .
                                                          x∈Z m
                                                              q :
                                                       Ax=y (mod q )


   3. If b = 0, the challenger does nothing. Else, if b = 1, the challenger measures system X of the
      quantum state |ψ̂y i in the computational basis. Finally, the challenger sends the outcome state in
      systems X to A, together with the matrix A ∈ Z nq ×m and the string y ∈ Z nq .

   4. A sends a classical witness w ∈ Z m
                                        q to the challenger.
                                                                    √      √
   5. The challenger checks whether A · w = y (mod q) and kwk ≤ mσ/ 2. If w passes both checks,
      the challenger sends t = (x̄, −1) ∈ Z m
                                            q to A with A · t = 0 (mod q). Else, the challenger aborts.

   6. A returns a bit b′ , which we define as the output of the experiment.
                                                                                               N
Remark. We also consider an N-fold variant of SGCn,m,q,σ, which we denote by SGCn,m,q,σ                  , where the
challenger prepares N independent states |ψ̂y1 i ⊗ · · · ⊗ |ψ̂y N i in Steps 2–3, for outcomes y1 , . . . , y N ∈ Z nq .
                                          N
A simple hybrid argument shows that SGCn,m,q,σ    is implied by SGCn,m,q,σ, for any N = poly(λ).

Towards a proof of the strong-Gaussian-collapsing conjecture. Unfortunately, we currently do not
know how to prove Conjecture 5.2 from standard assumptions, such as LWE or ISIS. The difficulty emerges
when we attempt to reduce the security to the LWE (or ISIS) problem with respect to the same matrix
A ∈ Z nq ×m . In order to simulate the experiment StrongGaussCollapseExpH,A,λ with respect to an adver-
sary A, we have to eventually forward a short trapdoor vector t ∈ Z m in order to simulate the second phase
of the experiment once A has produced a valid witness. Notice, however, that the reduction has no way of
obtaining a short vector t in the kernel of A as it is trying to break the underlying LWE (or ISIS) problem
with respect to A in the first place. Therefore, any successful security proof must necessarily exploit the
fact that there is interaction between the challenger and the adversary A, and that a short trapdoor vector t
is only revealed after A has already produced a valid short pre-image of y ∈ Z nq .
    When trying to distinguish between the state |ψ̂y i and a single Gaussian pre-image |x0 i with the property
that A · x0 = y (mod q), it is useful to work with the Fourier basis. Without loss of generality, we can
assume that A instead receives one of the following states during in Step 3; namely
                                             −hs,yi                                         −hu,x0 i
                       ∑ ∑ ̺ ( e) ω qq
                                     σ
                                                      |sA + ei X        or         ∑ ωq                |u i X .
                      s∈Z nq e∈Z m
                                 q                                               u ∈Z m
                                                                                      q


    One natural approach is prepare an auxiliary system, say B, which could later help the adversary deter-
mine whether X corresponds to a superposition of LWE samples or a superposition of uniform samples once
the trapdoor t is revealed (ideally, without disturbing X so as to allow for a Fourier basis measurement).
Because finding a valid witness w to the ISIS problem specified by (A, y) now amounts to a Fourier basis
projection (as in Definition 17), the entropic uncertainty relation in Theorem 3 immediately rules out large
class of attacks, including the shift-by-LWE-sample attack we described in Section 1.2. There, the idea is to
reversibly shift system X by a fresh LWE sample into an auxiliary system B. If system X corresponds to a
superposition of LWE samples, we obtain a separate LWE sample which is re-randomized, whereas, if X is
a superposition of uniform samples, the outcome remains random. Hence, if the aforementioned procedure


                                                             35
succeeded without disturbing system X, we could potentially find a valid witness w and simultaneously
distinguish the auxiliary system B with access to the trapdoor t. As we observed before, however, such an
attack must necessarily entangle the two systems X and B in a way that prevents it from finding a solution
to the ISIS problem specified by (A, y). Intuitively, if the state in system X yields a short-pre image w with
high probability via a Fourier basis measurement, then system X cannot be entangled with any auxiliary
systems. Because the set S of valid short pre-images (i.e. the set of√solution to the ISIS problem specified
by A and y) is much smaller than the size of Z m q (in particular, if σ m ≪ q), Theorem 3 tells us that the
min-entropy of system X (once it is measured in the computational basis) given system B must necessarily
be large. We remark that this statement holds information-theoretically, and does not rely on the hardness
of LWE. This suggests that, even if the trapdoor t is later revealed, system B cannot contain any relevant
information about whether system X initially corresponded to a superposition of LWE samples, or to a su-
perposition of uniform samples. While this argument is not sufficient to prove Conjecture 5.2, it captures the
inherent difficulty in extracting information encoded in two mutually unbiased bases, i.e. the computational
basis and the Fourier basis.


6 Public-Key Encryption with Certified Deletion
In this section, we formalize the notion of public-key encryption with certified deletion.

6.1 Definition
In this work, we consider public-key encryption schemes with certified deletion for which verification of a
deletion certificate is public; meaning anyone with access to the verification key can verify that deletion has
taken place. We first introduce the following definition.

Definition 20 (Public-key encryption with certified deletion). A public-key encryption scheme with certified
deletion (PKECD ) Σ = (KeyGen, Enc, Dec, Del, Vrfy) with plaintext space M consists of a tuple of QPT
algorithms, a key generation algorithm KeyGen, an encryption algorithm Enc, and a decryption algorithm
Dec, a deletion algorithm Del, and a verification algorithm Vrfy.

 KeyGen(1λ ) → (pk, sk) : takes as input the parameter 1λ and outputs a public key pk and secret key sk.

 Enc(pk, m) → (vk, CT) : takes as input the public key pk and a plaintext m ∈ M, and outputs a classical
     (public) verification key vk together with a quantum ciphertext CT.

 Dec(sk, CT) → m′ or ⊥ : takes as input the secret key sk and ciphertext CT, and outputs m′ ∈ M or ⊥.

 Del(CT) → π : takes as input a ciphertext CT and outputs a classical certificate π.

 Vrfy (vk, π ) → ⊤ or ⊥ : takes as input the verification key vk and certificate π, and outputs ⊤ or ⊥.

Definition 21 (Correctness of PKECD ). We require two separate kinds of correctness properties, one for
decryption and one for verification.

 (Decryption correctness:) For any λ ∈ N, and for any m ∈ M:
                                                                    
                                                       )←KeyGen(1λ )
                            Pr Dec(sk, CT) 6= m (pk,sk
                                                    CT←Enc(pk,m )
                                                                       ≤ negl(λ).


                                                      36
 (Verification correctness:) For any λ ∈ N, and for any m ∈ M:
                                                                      
                                                   (pk,sk)←KeyGen(1λ )
                              Pr Vrfy(vk, π ) = ⊥ (vk,CT)←Enc(pk,m) ≤ negl(λ).
                                                           π ←Del(CT)


   The notion of IND-CPA-CD security for public-key encryption was first introduced by Hiroka, Morimae,
Nishimaki and Yamakawa [HMNY21b].

6.2 Certified deletion security
In terms of security, we adopt the following definition.

Definition 22 (Certified deletion security for PKE). Let Σ = (KeyGen, Enc, Dec, Del, Vrfy) be a PKECD
scheme and let A be a QPT adversary (in terms of the security parameter λ ∈ N). We define the security
experiment Exppk -cert-del (b) between A and a challenger as follows:
               Σ,A,λ

   1. The challenger generates a pair (pk, sk) ← KeyGen(1λ ), and sends pk to A.

   2. A sends a plaintext pair (m0 , m1 ) ∈ M × M to the challenger.

   3. The challenger computes (vk, CTb ) ← Enc(pk, mb ), and sends CTb to A.

   4. At some point in time, A sends the certificate π to the challenger.

   5. The challenger computes Vrfy(vk, π ) and sends sk to A, if the output is ⊤, and sends ⊥ otherwise.

   6. A outputs a guess b′ ∈ {0, 1}, which is also the output of the experiment.

We say that the scheme Σ is IND-CPA-CD-secure if, for any QPT adversary A, it holds that

         Advpk -cert-del (λ) := | Pr[Exppk-cert-del (0) = 1] − Pr[Exppk-cert-del (1) = 1]| ≤ negl(λ).
            Σ,A                         Σ,A,λ                        Σ,A,λ


7 Dual-Regev Public-Key Encryption with Certified Deletion
In this section, we consider the Dual-Regev PKE scheme due to Gentry, Peikert and Vaikuntanathan
[GPV07]. Unlike Regev’s original PKE scheme in [Reg05], the Dual-Regev PKE scheme has the useful
property that the ciphertext takes the form of a regular sample from the LWE distribution together with an
additive shift which depends on the plaintext.

7.1 Construction
Parameters. Let λ ∈ N be the security parameter. We choose the following set of parameters for our
Dual-Regev PKE scheme with certified deletion (each parameterized by λ).

    • an integer n ∈ N.

    • a prime modulus q ≥ 2.

    • an integer m ≥ 2n log q.


                                                     37
                                                p                             q
    • a noise ratio α ∈ (0, 1) such that            8(m + 1) ≤ α1 ≤ √                   .
                                                                            8( m + 1)

Construction 1 (Dual-Regev PKE with Certified Deletion). Let λ ∈ N. The Dual-Regev PKE scheme
DualPKECD = (KeyGen, Enc, Dec, Del, Vrfy) with certified deletion is defined as follows:
                                                    − Z nq ×m and a vector x̄ ←
 KeyGen(1λ ) → (pk, sk) : sample a random matrix Ā ←                         − {0, 1}m and choose
                                                    $                         $

                                                                                    n ×( m +1)
      A = [Ā|Ā · x̄ (mod q)]. Output (pk, sk), where pk = A ∈ Z q                              and sk = (−x̄, 1) ∈ Z qm+1 .
 Enc(pk, x) → (vk, |CTi): parse A ← pk and run (|ψy i , y) ← GenPrimal(A, 1/α) in Algorithm 2,
     where y ∈ Z nq . To encrypt a single bit b ∈ {0, 1}, output the pair
                                                                                       q         
                                       n ×( m +1)                         (0,...,0,b ·⌊ 2 ⌋)
                         vk ← (A ∈ Z q            , y ∈ Z nq ), |CTi ← Xq                    |ψy i ,

      where vk is the public verification key and |CTi is an (m + 1)-qudit quantum ciphertext.
 Dec(sk, |CTi) → {0, 1} : to decrypt, measure the ciphertext |CTi in the computational basis with outcome
                                                                                q
     c ∈ Zm             T
           q . Compute c · sk ∈ Z q and output 0, if itis closer to 0 than to ⌊ 2 ⌋, and output 1, otherwise.

 Del(|CTi) → π : Measure |CTi in the Fourier basis and output the measurement outcome π ∈ Z qm+1 .

 Vrfy (vk, π ) → {⊤, ⊥} : to verify a deletion certificate π ∈ Z qm+1 , parse (A, y) ← vk and output ⊤, if
                                       √         √
       A · π = y (mod q) and kπ k ≤ m + 1/ 2α, and output ⊥, otherwise.

Proof of correctness.    Let us now establish the correctness properties of DualPKECD in Construction 1.
Lemma 17 (Correctness of decryption). Let n ∈ N and q ≥ 2 be a primepmodulus with m ≥ 2n log q,
                                                                                            q
each parameterized by the security parameter λ ∈ N. Let α be a ratio with 8(m + 1) ≤ α1 ≤ √   .
                                                                                                                       8( m + 1)
Then, for b ∈ {0, 1}, the scheme DualPKECD = (KeyGen, Enc, Dec, Del, Vrfy) in Construction 1 satisfies:
                                                               
                                            (pk,sk)←KeyGen(1λ )
                       Pr Dec(sk, |CTi) = b (vk,|CTi)←Enc(pk,b) ≥ 1 − negl(λ).

Proof. By the Leftover Hash Lemma (Lemma 4), the distribution of A = [Ā|Ā · x̄ (mod q)] is within
                                                                       n ×( m +1)
negligible total variation distance of the uniform distribution over Z q          . Moreover, from Lemma 9 it
                                             n
follows that the columns of A generate Z q with overwhelming probability. Since the noise ratio α ∈ (0, 1)
         p                          q
satisfies 8(m + 1) ≤ α1 ≤ √              , it then follows from Corollary 1 that the ciphertext |CTi is within
                                    8( m + 1)
negligible trace distance of the state
                                                       −hs,yi                                 q
                             ∑ ∑             ̺αq (e) ωq         |sA + e + (0, . . . , 0, b · ⌊ ⌋)i
                                                                                              2
                          s∈Z nq e∈Z qm +1

A measurement in computational basis yields an outcome c such that
                                                                q
                            c = s0 A + e0 + (0, . . . , 0, b · ⌊ ⌋) ∈ Z qm+1 ,
                                                                2
          − Z nq is random and where e0 ∼ DZmq +1, √αq is a sample from the (truncated) discrete Gaussian
           $
where s0 ←
                      q                              2
                               q                                                    q q
such that ke0 k ≤ αq m2+1 < ⌊ 4 ⌋. Since Dec(sk, |CTi) computes cT · sk ∈ Z ∩ (− 2 , 2 ] and outputs 0, if
                         q
it is closer to 0 than to ⌊ 2 ⌋ over , and 1 otherwise, it succeeds with overwhelming probability.


                                                                38
    Let us now prove the following property.

Lemma 18 (Correctness of verification). Let n ∈ N and q ≥ 2 be a primepmodulus with m ≥ 2n log q,
                                                                                            q
each parameterized by the security parameter λ ∈ N. Let α be a ratio with 8(m + 1) ≤ α1 ≤ √     .
                                                                                                      8( m + 1)
Then, for b ∈ {0, 1}, the scheme DualPKECD = (KeyGen, Enc, Dec, Del, Vrfy) in Construction 1 satisfies:
                                                                
                                             (pk,sk)←KeyGen(1λ )
                       Pr Verify(vk, π ) = ⊤ (vk,|CTi)←Enc(pk,b) ≥ 1 − negl(λ).
                                                          π ←Del(|CTi)

Proof. By the Leftover Hash Lemma (Lemma 4), the distribution of A = [Ā|Ā · x̄ (mod q)] is within
                                                                         n ×( m +1)
negligible total variation distance of the uniform distribution over Z q            . From Lemma 9 it follows
that the columns of A generate Z nq with overwhelming probability. Since α ∈ (0, 1) is a ratio parameter
      p                         q
with 8(m + 1) ≤ α1 ≤ √              , Corollary 1 implies that the Fourier transform of the ciphertext |CTi is
                             8( m + 1)
within negligible trace distance of the state

                              ci =                                 hx,(0,...,0,b ·⌊ 2q ⌋)i
                             |CT              ∑          ̺1/α (x) ωq                         | xi .
                                           x∈Z m +1 :
                                               q
                                         Ax=y (mod q )

From Lemma 11, it follows that the distribution of computational basis
                                                                   √ measurement
                                                                          √      outcomes is within
negligible total variation distance of π ∼ DΛyq (A), √1 with kπ k ≤ m + 1/ 2α. This proves the claim.
                                                           2α




7.2 Proof of security
Let us now analyze the security of our Dual-Regev PKE scheme with certified deletion in Construction 1.

IND-CPA security of DualPKECD . We first prove that our public-key encryption scheme DualPKECD in
Construction 1 satisfies the notion IND-CPA security according to Definition 12. The proof follows from
Theorem 5 and assumes the hardness of (decisional) LWE (Definition 15). We add it for completeness.

Theorem 6. Let n ∈ N and q ≥ 2 be a prime modulus with m ≥ 2n logpq, each parameterized by the
                                                                                           q
security parameter λ ∈ N. Let α ∈ (0, 1) be a noise ratio parameter with 8(m + 1) ≤ α1 ≤ √   .
                                                                                                      8( m + 1)
Then, the scheme DualPKECD in Construction 1 is IND-CPA-secure assuming the quantum hardness of the
decisional LWEmn,q,βq problem, for any β ∈ (0, 1) with α/β = λ
                                                               ω ( 1) .


Proof. Let Σ = DualPKECD . We need to show that, for any QPT adversary A, it holds that

               AdvΣ,A (λ) := | Pr[Expind-cpa                ind-cpa
                                     Σ,A,λ (0) = 1] − Pr[ExpΣ,A,λ (1) = 1]| ≤ negl( λ ).


Consider the experiment Expind-cpa
                           Σ,A,λ ( b) between the adversary A and a challenger taking place as follows:

   1. The challenger generates a pair (pk, sk) ← KeyGen(1λ ), and sends pk to A.

   2. A sends a distinct plaintext pair (m0 , m1 ) ∈ {0, 1} × {0, 1} to the challenger.

   3. The challenger computes (vk, CTb ) ← Enc(pk, mb ), and sends |CTb i to A.

                                                           39
   4. A outputs a guess b′ ∈ {0, 1}, which is also the output of the experiment.
                                                                                              n ×( m +1)
Recall that the procedure Enc(pk, mb ) outputs a pair (vk, |CTb i), where (A ∈ Z q            , y ∈ Z nq ) ← vk
is the verification key and where the ciphertext |CTb i is within negligible trace distance of
                                              −hs,yi
                   ∑ ∑              ̺αq (e) ωq          |sA + e + (0, . . . , 0, mb · ⌊q/2⌋) (mod q)i      (15)
                  s∈Z nq e∈Z m
                             q
                               +1



Let β ∈ (0, 1) be such that α/β = λω (1) . From Theorem 5 it follows that, under the (decisional) LWEm
                                                                                                     n,q,βq
assumption, the quantum ciphertext |CTb i is computationally indistinguishable from the state
                                                   −hu,x0 i
                                        ∑         ωq          |u i ,    x0 ∼ DΛyq (A), √1 .
                                                                                        2α
                                                                                                           (16)
                                             +1
                                      u ∈Z m
                                           q


Because the state in Eq. (19) is completely independent of b ∈ {0, 1}, it follows that

               AdvΣ,A (λ) := | Pr[Expind-cpa                ind-cpa
                                     Σ,A,λ (0) = 1] − Pr[ExpΣ,A,λ (1) = 1]| ≤ negl( λ ).

This proves the claim.

IND-CPA-CD security of DualPKECD . In this section, we prove that our public-key encryption scheme
DualPKECD in Construction 1 satisfies the notion of certified deletion security assuming the Strong
Gaussian-Collapsing (SGC) Conjecture (see Conjecture 5.2). This is a strengthening of the Gaussian-
collapsing property which we proved under the (decisional) LWE assumption (see Theorem 4).
Theorem 7. Let n ∈ N and p q ≥ 2 be a prime modulus with m ≥ 2n log q, each parameterized by λ ∈ N.
                                              q
Let Let α be a ratio with 8(m + 1) ≤ α1 ≤ √       . Then, the scheme DualPKECD in Construction 1 is
                                                            8( m + 1)
IND-CPA-CD-secure assuming the Strong Gaussian-Collapsing property SGCn,m+1,q, 1 from Conjecture 5.2.
                                                                                                 α

Proof. Let Σ = DualPKECD . We need to show that, for any QPT adversary A, it holds that

         Advpk-cert-del (λ) := | Pr[Exppk-cert-del (0) = 1] − Pr[Exppk-cert-del (1) = 1]| ≤ negl(λ).
            Σ,A                        Σ,A,λ                        Σ,A,λ

    We consider the following sequence of hybrids:

 H0 : This is the experiment Exppk-cert-del (0) between A and a challenger:
                                Σ,A,λ

                                                        − Z nq ×m and a vector x̄ ←
                                                                                  − {0, 1}m and chooses
                                                        $                         $
        1. The challenger samples a random matrix Ā ←
           A = [Ā|Ā · x̄ (mod q)]. The challenger chooses the secret key sk ← (−x̄, 1) ∈ Z qm+1 and the
                                           n ×( m +1)
            public key pk ← A ∈ Z q                     .
        2. A sends a distinct plaintext pair (m0 , m1 ) ∈ {0, 1} × {0, 1} to the challenger. (Note: Without
           loss of generality, we can just assume that m0 = 0 and m1 = 1).
        3. The challenger runs (|ψy i , y) ← GenPrimal(A, 1/α) in Algorithm 2, and outputs
                                                                                    
                                              n ×( m +1)
                                vk ← (A ∈ Z q            , y ∈ Z nq ), |CT0 i ← |ψy i .

        4. At some point in time, A returns a certificate π to the challenger.

                                                                  40
                                                                                          √         √
        5. The challenger verifies π and outputs ⊤, if A · π = y (mod q) and kπ k ≤ m + 1/ 2α,
           and output ⊥, otherwise. If π passes the test with outcome ⊤, the challenger sends sk to A.
        6. A outputs a guess b′ ∈ {0, 1}, which is also the output of the experiment.

 H1 : This is same experiment as in H0 , except that (in Step 3) the challenger prepares the ciphertext in the
      Fourier basis rather than the standard basis. In other words, A receives the pair
                                                                                      
                                            n ×( m +1)
                              vk ← (A ∈ Z q            , y ∈ Z nq ), |CT0 i ← FTq |ψy i .

 H2 : This is the experiment StrongGaussCollapseExpH,D,λ (0) in Conjecture 5.2:

                                                        − Z nq ×m and a vector x̄ ←
                                                                                  − {0, 1}m and chooses
                                                          $                       $
        1. The challenger samples a random matrix Ā ←
           A = [Ā|Ā · x̄ (mod q)] and t = (−x̄, 1) ∈ Z qm+1 .
        2. The challenger runs (|ψ̂y i , y) ← GenDual(A, σ) in Algorithm 1, where y ∈ Z nq , and sends the
           triplet (|ψ̂y i , A, y) to the adversary A.
        3. At some point in time, A returns a certificate π to the challenger.
                                                                                          √         √
        4. The challenger verifies π and outputs ⊤, if A · π = y (mod q) and kπ k ≤ m + 1/ 2α,
           and output ⊥, otherwise. If π passes the test with outcome ⊤, the challenger sends t to A.
        5. A outputs a guess b′ ∈ {0, 1}, which is also the output of the experiment.

 H3 : This is the experiment StrongGaussCollapseExpH,D,λ (1) in Conjecture 5.2; it is the same as H2 ,
      except that the state |ψ̂y i (in Step 2) is measured in the computational basis before it is sent to A.

 H4 : This is same experiment as H3 , except that (in Step 2) the challenger additionally applies the Pauli
                                q
                      (0,...,0,⌊ 2 ⌋)
      operator Zq                       to the state |ψ̂y i before it is measured in the computational basis.

 H5 : This is same experiment as H4 , except that (in Step 2) A receives the triplet
                                                (0,...,0,⌊ 2q ⌋)                         n ×( m +1)
                                             (Zq                   |ψ̂y i ,      A ∈ Zq               ,       y ∈ Z nq ).

 H6 : This is same experiment as H5 , except that (in Step 2) the challenger prepares the quantum state
       (0,...,0,⌊ 2q ⌋)
      Zq                  |ψ̂y i in the (inverse) Fourier basis instead. In other words, A receives the triplet

                                                   (0,...,0,⌊ 2q ⌋)                        n ×( m +1)
                                           (FT†q Zq                   |ψ̂y i ,        A ∈ Zq              ,     y ∈ Z nq ).

 H7 : This is the experiment Exppk-cert-del (1).
                                Σ,A,λ

   We now show that the hybrids are indistinguishable.
Claim 2.
                                              Pr[Exppk-cert-del (0) = 1] = Pr[H = 1].
                                                    Σ,A,λ                      1

Proof. Without loss of generality, we can assume that the challenger applies the inverse Fourier transform
before sending the ciphertext to A. Therefore, the success probabilities are identical in H0 and H1 .


                                                                                 41
Claim 3.
                                                                Pr[H1 = 1] = Pr[H2 = 1].

Proof. Because the challenger in H1 always sends the ciphertext |CT0 i corresponding to m0 = 0 to the
adversary A, the two hybrids H1 and H2 are identical.

Claim 4. Under the Strong Gaussian-Collapsing property SGCn,m+1,q, 1 , it holds that
                                                                                                 α

                                                    | Pr[H2 = 1] − Pr[H3 = 1]| ≤ negl(λ).
Proof. This follows directly from Conjecture 5.2.

Claim 5.
                                                                Pr[H3 = 1] = Pr[H4 = 1].

Proof. Because the challenger measures the state |ψ̂y i in Step 2 in the computational basis, applying the
                        (0,...,0,⌊ 2q ⌋)
phase operator Zq                          before the measurement does not affect the measurement outcome.

Claim 6. Under the Strong Gaussian-Collapsing property SGCn,m+1,q, 1 , it holds that
                                                                                                 α

                                                    | Pr[H4 = 1] − Pr[H5 = 1]| ≤ negl(λ).
Proof. This follows from Conjecture 5.2 since, without loss of generality, we can assume that the challenger
                                                       q
                                             (0,...,0,⌊ 2 ⌋)
applies the phase operator Zq                                  before sending the state |ψ̂y i to A.

Claim 7.
                                                                Pr[H5 = 1] = Pr[H6 = 1].

Proof. Without loss of generality, we can assume that the challenger applies the Fourier transform to
           q
 (0,...,0,⌊ 2 ⌋)
Zq                 |ψ̂y i before sending it to A. Therefore, the success probabilities are identical in H5 and H6 .
Claim 8.
                                           | Pr[H6 = 1] − Pr[Exppk-cert-del (1) = 1]| ≤ negl(λ).
                                                                Σ,A,λ

Proof. From Lemma 6, we have FTq Xvq = Zvq FTq , for all v ∈ Z m      q . Hence, in H6 , we can instead assume
that the challenger runs (|ψy i , y) ← GenPrimal(A, 1/α) in Algorithm 2 and sends the following to A:
                                                                                    q         
                                      n ×( m +1)                          (0,...,0,⌊ 2 ⌋)
                       vk ← (A ∈ Z q             , y ∈ Z nq ), |CT1 i ← Xq                |ψy i .

From Corollary 1, we have that FT†q Zvq |ψ̂y i and Xvq |ψy i are within negligible trace distance, for all v ∈ Z m
                                                                                                                 q.
Because the challenger in H7 always sends the ciphertext |CT1 i corresponding to m1 = 1 to the adversary
A, it follows that the distinguishing advantage between H6 and H7 = Exppk         -cert-del (1) is negligible.
                                                                                Σ,A,λ

     Because the hybrids H0 and H7 are indistinguishable, this implies that

                                                               Advpk-cert-del (λ) ≤ negl(λ).
                                                                  Σ,A




    Next, we show how to extend our Dual-Regev PKE scheme with certified deletion in Construction 1 to
a fully homomorphic encryption scheme of the same type.

                                                                             42
8 Fully Homomorphic Encryption with Certified Deletion
In this section, we formalize the notion of homomorphic encryption with certified deletion which enables
an untrusted quantum server to compute on encrypted data and, if requested, to simultaneously prove data
deletion to a client. We also provide several notions of certified deletion security.

8.1 Definition
We begin with the following definition.

Definition 23 (Homomorphic encryption with certified deletion). A homomorphic encryption scheme with
certified deletion is a tuple HECD = (KeyGen, Enc, Dec, Eval, Del, Vrfy) of QPT algorithms (in the secu-
rity parameter λ ∈ N), a key generation algorithm KeyGen, an encryption algorithm Enc, a decryption
algorithm Dec, an evaluation algorithm Eval, a deletion algorithm Del, and a verification algorithm Vrfy.

 KeyGen(1λ ) → (pk, sk) : takes as input 1λ and outputs a public key pk and secret key sk.

 Enc(pk, x) → (vk, CT) : takes as input the public key pk and a plaintext x ∈ {0, 1}, and outputs a
     classical verification key vk together with a quantum ciphertext CT.

 Dec(sk, CT) → x′ or ⊥ : takes as input a key sk and ciphertext CT, and outputs x′ ∈ {0, 1} or ⊥.

 Eval(C, CT, pk) → f
                   CT: takes as input a key pk and applies a circuit C : {0, 1}ℓ → {0, 1} to a product of
                                                                      f
     quantum ciphertexts CT = CT1 ⊗ · · · ⊗ CTℓ resulting in a state CT.

 Del(CT) → π : takes as input a ciphertext CT and outputs a classical certificate π.

 Vrfy (vk, π ) → ⊤ or ⊥ : takes as input a key vk and certificate π, and outputs ⊤ or ⊥.

    We remark that we frequently overload the functionality of the encryption and decryption procedures
by allowing both procedures to take multi-bit messages as input, and to generate or decrypt a sequence of
quantum ciphertexts bit-by-bit.

Definition 24 (Compactness and full homomorphism). A homomorphic encryption scheme with certified
deletion HECD = (KeyGen, Enc, Dec, Eval, Del, Vrfy) is fully homomorphic if, for any efficienty (in λ ∈ N)
computable circuit C : {0, 1}ℓ → {0, 1} and any set of inputs x = ( x1 , . . . , xℓ ) ∈ {0, 1}ℓ , it holds that
                      "                                                          #
                                                             (pk,sk)←KeyGen(1λ )
                   Pr Dec(sk, f CT) 6= C ( x1 , . . . , xℓ ) (vk,CT)←Enc(pk,x ) ≤ negl(λ).
                                                           f ←Eval( C,CT,pk)
                                                           CT


We say that a fully homomorphic encryption scheme with certified deletion (FHECD ) is compact if its de-
cryption circuit is independent of the circuit C. The scheme is leveled fully homomorphic if it takes 1L as an
additional input for its key generation procedure and can only evaluate depth L Boolean circuits.

Definition 25 (Correctness of verification). A homomorphic encryption scheme with certified deletion
HECD = (KeyGen, Enc, Dec, Eval, Del, Vrfy) has correctness of verification if the following property holds
for any integer λ ∈ N and any set of inputs x = ( x1 , . . . , xℓ ) ∈ {0, 1}ℓ
                                                                      
                                                (pk,sk)←KeyGen(1λ )
                        Pr Vrfy(vk, π ) = ⊥ (vk,CT)←Enc(pk,x ) ≤ negl(λ).
                                                      π ←Del(CT)


                                                      43
    Recall that a fully homomorphic encryption scheme with certified deletion enables an untrusted quantum
server to compute on encrypted data and to also prove data deletion to a client. In this context, it is desirable
for the client to be able to extract (i.e., to decrypt) the outcome of the computation without irreversibly
affecting the ability of the server to later prove deletion. We use the following definition.
Definition 26 (Extractable FHE scheme with certified deletion). A fully homomorphic encryption scheme
with certified deletion Σ = (KeyGen, Enc, Dec, Eval, Extract, Del, Vrfy) is called extractable, if
    • Eval(C, CT1 , . . . , CTℓ , pk) additionally outputs a circuit transcript tC besides f
                                                                                           CT;
    • ExtracthS(̺, tC ), R(sk)i is an interactive protocol between a sender S (which takes as input a state
      ̺ and a circuit transcript tC ) and a receiver R (which takes as input a key sk) with the property that,
      once the protocol is complete, S obtains a state ̺e and R obtains a bit y ∈ {0, 1};
such that for any efficiently computable circuit C : {0, 1}ℓ → {0, 1} of depth L and any input x ∈ {0, 1}ℓ :
                                                             λ L
                                                                      
                                                          (pk,sk)←KeyGen(1 ,1 )
                                                            (vk,CT)←Enc(pk,x )
                   Pr y 6= C ( x1 , . . . , xℓ )         (f
                                                           CT,tC )←Eval( C,CT,pk)
                                                                                       ≤ negl(λ),   and
                                                                       f
                                                    ( ̺e,y)←ExtracthS (CT,tC ),R(sk)i
                                                         (pk,sk)←KeyGen(1λ ,1L )
                                                                                 
                                                            (vk,CT)←Enc(pk,x )
                                                                                     
                    Pr Vrfy(vk, π ) = ⊥                  (f
                                                           CT,tC )←Eval( C,CT,pk)      ≤ negl(λ).
                                                                       f
                                                    ( ̺e,y)←ExtracthS (CT,tC ),R(sk)i
                                                                 π ←Del( ̺e)

Remark (Compactness of an extractable FHE scheme). Our notion of an extractable FHE scheme with
certified deletion in Definition 26 requires the evaluator to keep a transcript of the circuit that is being
applied, which at first sight seems to violate the usual notion of compactness in Definition 24. However, the
action of the decryptor during the interactive protocol Extract is still independent of the circuit that is being
applied, and so it is possible to recover an analogous form of compactness as before.

8.2 Certified deletion security
Our notion of certified deletion security for homomorphic encryption (HE) schemes is similar to the notion
of IND-CPA-CD security for public-key encryption schemes in Definition 22.
Definition 27 (Certified deletion security for HE). Let Σ = (KeyGen, Enc, Dec, Eval, Del, Vrfy) be a homo-
morphic encryption scheme with certified deletion and let A be a QPT adversary. We define the security
experiment Exphe -cert-del (b) between A and a challenger as follows:
               Σ,A,λ

   1. The challenger generates a pair (pk, sk) ← KeyGen(1λ ), and sends pk to A.
   2. A sends a distinct plaintext pair (m0 , m1 ) ∈ {0, 1}ℓ × {0, 1}ℓ to the challenger.
   3. The challenger computes (vk, CTb ) ← Enc(pk, mb ), and sends |CTb i to A.
   4. At some point in time, A sends a certificate π to the challenger.
   5. The challenger computes Vrfy(vk, π ) and sends sk to A, if the output is 1, and 0 otherwise.
   6. A outputs a guess b′ ∈ {0, 1}, which is also the output of the experiment.
We say that the scheme Σ is IND-CPA-CD-secure if, for any QPT adversary A, that
         Advhe-cert-del (λ) := | Pr[Exppk-cert-del (0) = 1] − Pr[Exphe-cert-del (1) = 1]| ≤ negl(λ).
             Σ,A                              Σ,A,λ                            Σ,A,λ


                                                               44
9 Dual-Regev Fully Homomorphic Encryption with Certified Deletion
In this section, we describe the main result of this work. We introduce a protocol that allows an untrusted
quantum server to perform homomorphic operations on encrypted data, and to simultaneously prove data
deletion to a client. Our FHE scheme with certified deletion supports the evaluation of polynomial-sized
Boolean circuits composed entirely of NAND gates (see Figure 4) – an assumption we can make without loss
of generality, since the NAND operation is universal for classical computation. Note that, for a, b ∈ {0, 1},
the logical NOT-AND (NAND) operation is defined by

                                     NAND( a, b) = a ∧ b = 1 − a · b.

Recall also that a Boolean circuit with input x ∈ {0, 1}n is a directed acyclic graph G = (V, E) in which




                                                    a        b

                                           Figure 4: NAND gate.

each node in V is either an input node (corresponding to an input bit xi ), an AND (∧) gate, an OR (∨) gate,
or a NOT (¬) gate. We can naturally identify a Boolean circuit with a function f : {0, 1}n → {0, 1} which
it computes. Due to the universality of the NAND operation, we can represent every Boolean circuit (and
the function it computes) with an equivalent circuit consisting entirely of NAND gates. In Figure 5, we give
an example of a Boolean circuit composed of three NAND gates that takes as input a string x ∈ {0, 1}4 .

                                                    C ( x)




                                            x1 x2                x3 x4

Figure 5: A Boolean circuit C made up of three NAND gates which takes as input a binary string of the form
x ∈ {0, 1}4 . The top-most NAND gate is the designated output node with outcome C ( x) ∈ {0, 1}.


9.1 Construction
In this section, we describe our fully homomorphic encryption scheme with certified deletion. In order to
define our construction, we require a so-called flattening operation first introduced by Gentry, Sahai and
Waters [GSW13] in the context of homomorphic encryption and is also featured in the Dual-Regev FHE
scheme of Mahadev [Mah18]. Let n ∈ N, q ≥ 2 be a prime modulus and m ≥ 2n log q. We define a linear
                 ( m +1)× N
operator G ∈ Z q            called the gadget matrix, where N = (n + 1) · ⌈log q⌉. The operator G converts a

                                                        45
binary representation of a vector back to its original vector representation over the ring Z q . More precisely,
for any binary vector a = ( a1,0 , . . . , a1,l −1 , . . . , am+1,0 , . . . , am+1,l −1 ) of length N with ℓ = ⌈log q⌉, the
matrix G produces a vector in Z qm+1 as follows:

                                                                                                       !
                                          ⌈log q ⌉−1                        ⌈log q ⌉−1
                                                        j                                 j
                              G ( a) =        ∑        2 · a1,j , . . . ,      ∑         2 · am+1,j         .                      (17)
                                              j=0                              j=0


We also define the associated (non-linear) inverse operation G−1 which converts a vector a ∈ Z qm+1 to its
binary representation in {0, 1} N . In other words, we have that G−1 · G = 1 acts as the identity operation.
    Our (leveled) FHE scheme with certified deletion is based on the (leveled) Dual-Regev FHE scheme
introduced by Mahadev [Mah18] which is a variant of the LWE-based FHE scheme proposed by Gentry,
Sahai and Waters [GSW13]. We base our choice of parameters on the aforementioned two works.
    Let us first recall the Dual-Regev FHE scheme below.

Construction 2 (Dual-Regev leveled FHE). Let λ ∈ N be the security parameter. The Dual-Regev leveled
FHE scheme DualFHE = (KeyGen, Enc, Dec, Eval) consists of the following PPT algorithms:

                                                              − Z nq ×m and vector x̄ ←
 KeyGen(1λ ) → (pk, sk) : sample a uniformly random matrix Ā ←                       − {0, 1}m and let
                                                              $                       $

                                                                                              ( m +1)× n
       A = [Ā|Ā · x̄ (mod q)] T . Output (pk, sk), where pk = A ∈ Z q                                    and sk = (−x̄, 1) ∈ Z qm+1 .
                                                            ( m +1)× n
                                                                                        − Z nq × N and E ∼ DZ(m+1)× N, αq
                                                                                        $
 Enc(pk, x) : to encrypt x ∈ {0, 1}, parse A ∈ Z q                       ← pk, sample S ←
                                                                     ( m +1)× N
       and output CT = A · S + E + x · G (mod q) ∈ Z q                               , where G is the gadget matrix in Eq. (17).

 Eval(C, CT) : apply the circuit C composed of NAND gates on a ciphertext tuple CT as follows:

           • parse the ciphertext tuple as (CT1 , . . . , CTℓ ) ← CT.
           • repeat for every NAND gate in C: to apply a NAND gate on a ciphertext pair (CTi , CT j ), parse
                                                                                 ( m +1)× N
             matrices Ci ← CTi and C j ← CT j with Ci , C j ∈ Z q                                 and generate

                                               Cij = G − Ci · G−1 (C j ) (mod q).

             Let CTij ← Cij denote the outcome ciphertext.
                                 ( m +1)× N                                                                     q q
 Dec(sk, CT) : parse C ∈ Z q         ← CT and compute c = skT · cN ∈ Z ∩ (− 2 , 2 ], where cN ∈ Z qm+1
                                                                               q
     is the N-th column of C, and then output 0, if c is closer to 0 than to ⌊ 2 ⌋, and output 1, otherwise.

     The Dual-Regev FHE scheme supports the homomorphic evaluation of a NAND gate in the following
sense. If CT0 and CT1 are ciphertexts that encrypt two bits x0 and x1 , respectively, then the resulting
outcome CT = G − CT0 · G−1 (CT1 ) (mod q) is an encryption of NAND( x0 , x1 ) = 1 − x0 · x1 , where
G is the gadget matrix that converts a binary representation of a vector back to its original representation
over the ring Z q . Moreover, the new ciphertext CT maintains the form of an LWE sample with respect to
the same public key pk, albeit for a new LWE secret and a new (non-necessarily Gaussian) noise term of
bounded magnitude. This property is crucial, as knowledge of the secret key sk (i.e., a short trapdoor vector)
still allows for the decryption of the ciphertext CT once a NAND gate has been applied.
     The following result is implicit in the work of Mahadev [Mah18, Theorem 5.1].


                                                                46
Theorem 8 ( [Mah18]). Let λ ∈ N be the security parameter. Let n ∈ N, let q ≥ 2 be a prime modulus
and m ≥ 2n log q. Let N = (n + 1) · ⌈log q⌉ be an integer and let L be an upper bound on the depth of
the polynomial-sized Boolean circuit which is to be evaluated. Let α ∈ (0, 1) be a ratio such that
                                   √                            q
                                  2 n ≤ αq ≤                                   .
                                                    4( m + 1) · N · ( N + 1) L

Then, the scheme in Construction 2 is an IND-CPA-secure leveled fully homomorphic encryption scheme
              ( m +1)× N
under the LWEn,q,αq      assumption.

    Note that the Dual-Regev FHE scheme is leveled in the sense that an apriori upper bound L on the
NAND-depth of the circuit is required to set the parameters appropriately. We remark that a proper (non-
leveled) FHE scheme can be obtained under an additional circular security assumption [BV11a].
    The leveled Dual-Regev FHE scheme inherits a crucial property from its public-key counterpart.
Namely, in contrast to the FHE scheme in [GSW13], the ciphertext takes the form of a regular sample
from the LWE distribution together with an additive shift x · G that depends on the plaintext x ∈ {0, 1}. In
particular, if a Boolean circuit C of polynomial NAND-depth L is applied to the ciphertext corresponding to a
plaintext x ∈ {0, 1}ℓ in Construction 2, then the resulting final ciphertext is of the form A · S + E + C ( x)G,
                              ( m +1)× N                 p
where S ∈ Z nq × N , E ∈ Z q             and kEk∞ ≤ αq (m + 1) N · ( N + 1) L (see [GSW13] for details).
Choosing 1/α to be sub-exponential in N as in [GSW13], we can therefore allow for homomorphic com-
putations of arbitrary polynomial-sized Boolean circuits of NAND-depth at most L. It is easy to see that the
decryption procedure of the leveled Dual-Regev FHE scheme is successful as long as the cumulative error
                                           q
E satisfies the condition kEk∞ ≤ √             .
                                   4   ( m + 1) N
    This property is essential as it allows us to extend Dual-Regev PKE scheme with certified deletion
towards a leveled FHE scheme, which we denote by FHECD . Using Gaussian coset states, we can again
encode Dual-Regev ciphertexts for the purpose of certified deletion while simultaneously preserving their
cryptographic functionality.

Dual-Regev leveled FHE with certified deletion. Let us now describe our (leveled) FHE scheme with
certified deletion. We base our choice of parameters on the Dual-Regev FHE scheme of Mahadev [Mah18]
which is a variant of the scheme due to Gentry, Sahai and Waters [GSW13].

Parameters. Let λ ∈ N be the security parameter and let n ∈ N. Let L be an upper bound on the depth
of the polynomial-sized Boolean circuit which is to be evaluated. We choose the following set of parameters
for the Dual-Regev leveled FHE scheme (each parameterized by the security parameter λ).

    • a prime modulus q ≥ 2.

    • an integer m ≥ 2n log q.

    • an integer N = (n + 1) · ⌈log q⌉.

    • a noise ratio α ∈ (0, 1) such that
                               q
                                                                         q
                                  8(m + 1) N ≤ αq ≤ √                                      .
                                                             8 ( m + 1) · N · ( N + 1) L



                                                        47
Construction 3 (Dual-Regev leveled FHE scheme with certified deletion). Let λ ∈ N be a parameter and
DualFHE = (KeyGen, Enc, Dec, Eval) be the scheme in Construction 2. The Dual-Regev (leveled) FHE
scheme DualFHECD = (KeyGen, Enc, Dec, Eval, Del, Vrfy) with certified deletion is defined by:
 KeyGen(1λ ) → (pk, sk) : generate (pk, sk) ← DualFHE.KeyGen(1λ ) and output (pk, sk).
                                                                           ( m +1)× n
 Enc(pk, x) → (vk, |CTi) : to encrypt a bit x ∈ {0, 1}, parse A ∈ Z q                  ← pk and, for i ∈ [ N ], run
     (|ψyi i , yi ) ← GenPrimal(AT , 1/α) in Algorithm 2, where yi ∈ Z nq , and output the pair
                                                                                                               
                         ( m +1)× n                                            x ·g                  x ·g
         vk ← (A ∈ Z q              , (y1 | . . . |y N ) ∈ Z nq × N ), |CTi ← Xq 1 |ψy1 i ⊗ · · · ⊗ Xq N |ψy N i ,
                                                                            ( m +1)× N
      where (g1 , . . . , g N ) are the columns of the gadget matrix G ∈ Z q             in Eq. (17).

 Eval(C, |CTi) → (|CT f i , tC ): apply the Boolean circuit C composed of NAND gates to the ciphertext
      |CTi in system Cin = C1 · · · Cℓ as follows: For every gate NANDij in the circuit C between a
     ciphertext pair in systems Ci and Cj , repeat the following two steps:
          • apply UNAND from Definition 28 to systems Ci Cj of the ciphertext CT by appending an auxiliary
            system Cij . This results in a new ciphertext state CT which contains the additional system Cij .
          • add the gate NANDij to the circuit transcript tC .

      Output (| f
               CTi , tC ), where | f
                                  CTi is the final post-evaluation state in systems Cin Caux Cout and
          • Cin = C1 · · · Cℓ denotes the initial ciphertext systems of |CT1 i ⊗ · · · ⊗ |CTℓ i.
          • Caux denotes all intermediate auxiliary ciphertext systems.
          • Cout denotes the final ciphertext system corresponding to the output of the circuit C.
 Dec(sk, |CTi) → {0, 1}µ or ⊥ : measure the ciphertext |CTi in the computational basis to obtain an
     outcome C and output x′ ← DualFHE.Dec(sk, C).
                                                                                                        ( m +1)× N
 Del(|CTi) → π : measure |CTi in the Fourier basis with outcomes π = (π1 | . . . |π N ) ∈ Z q                        .

 ExtracthS(| f
            CT i , tC ), R(sk)i → (̺, y) this is the following interactive protocol between a sender S with
            f
     input |CTi in systems Cin Caux Cout and transcript tC , and a receiver R with input sk:
          • S and R run the rewinding protocol Π = hS(| f  CT i , tC ), R(sk)i in Protocol 1.
          • Once Π is complete, S obtains a state ̺ in system Cin and R obtains a bit y ∈ {0, 1}.
                                                                                                    ( m +1)× N
 Vrfy (vk, pk, π ) → {0, 1} : to verify the deletion certificate π = (π1 | . . . |π N ) ∈ Z q                    , parse
             ( m +1)× n
      (A ∈ Z q          , (y1 | . . . |y N ) ∈ Z nq × N ) ← vk and output ⊤, if both AT · πi = yi (mod q) and
                 √         √
      kπ i k ≤       m + 1/ 2α for every i ∈ [ N ], and output ⊥, otherwise.

Protocol 1 (Rewinding Protocol). Let DualFHE = (KeyGen, Enc, Dec, Eval) be the Dual-Regev FHE
scheme in Construction 2. Consider the following interactive protocol Π = hS(̺, tC ), R(sk)i between a
sender S which takes as input state ̺ in systems Cin Caux Cout and a transcript tC of a Boolean circuit C,
as well as a receiver R which takes as input a secret key sk.

    1. S sends system Cout of the state ̺ associated with the encrypted output of the circuit C to R.


                                                        48
    2. R runs UDualFHE.Decsk (with the key sk hard coded) to reversibly decrypt system Cout , where

                     UDualFHE.Decsk :        |CiCout ⊗ |0i M → |CiCout ⊗ |DualFHE.Decsk (C)i M ,
                                ( m +1)× N
       for any matrix C ∈ Z q         . R then measures system M to obtain a bit y ∈ {0, 1} (the supposed
                                                                †
       output of the Boolean circuit C). Afterwards, R applies UDualFHE.Dec   , discards the ancillary system
                                                                           sk
                                                         g
       M, and sends back the post-measurement system Cout of the resulting ciphertext ̺e to S .

    3. S repeats the following two steps in order to uncompute the systems Caux C  g                   e:
                                                                                    out from the state ̺
       For every gate NANDij ∈ tC , where i and j denote the respective ciphertext systems Ci and Cj , in
       decreasing order starting from the last gate in the circuit transcript tC :
                        †
           • S applies UNAND from Definition 28 to systems Ci Cj Cij of ̺e to uncompute system Cij .
           • S repeats the procedure starting from the new outcome state ̺e.

    Let us now define how to perform the homomorphic NAND gate in Construction 3 in more detail.

Definition 28 (Homomorphic NAND gate). Let q ≥ 2 be a modulus, and let m and N be integers. Let
            ( m +1)× N
X, Y, Z ∈ Z q          be arbitrary matrices. We define the homomorphic NAND gate as the unitary

       UNAND :      |X i X ⊗ |Y i Y ⊗ |Z i Z    →          |Xi X ⊗ |YiY ⊗ |Z + G − X · G−1 (Y) (mod q)i Z ,
              ( m +1)× N
where G ∈ Z q              is the gadget matrix in Eq. (17).

    To illustrate the action of our homomorphic NAND gate, we consider a simple example.

Example. Consider a pair of two ciphertexts |CTi i ⊗ |CT j i which encrypt two bits xi , x j ∈ {0, 1} as in
Construction 3. Let UNANDij denote the homomorphic NAND gate applied to systems Ci and Cj . Then,

                        UNANDij :      |CTi iCi ⊗ |CT j iC ⊗ |0i Cij          →       |CTij iC C C .
                                                               j                                i   j ij


Here, |CTij i is the resulting ciphertext in systems Ci Cj Cij . Note that UNANDij is reversible in the sense that
                         †
                        UNANDij
                                :      |CTij iC C C         →      |CTi iCi ⊗ |CT j iC ⊗ |0i Cij .
                                                i   j ij                                j


Let us now analyze how UNAND acts on the basis states of a pair of ciphertexts |CTi i ⊗ |CT j i that encode
LWE samples as in Construction 3. In the following, Ei , E j ∼ DZ(m+1)× N, √αq have a (truncated) discrete
                                                                                  q         2
Gaussian distribution as part of the superposition. Then,

        UNANDij :     |ASi + Ei + xi GiCi ⊗ |AS j + E j + x j GiC ⊗ |0i Cij
                                                                          j

                 → |ASi + Ei + xi GiCi ⊗ |AS j + E j + x j GiC ⊗ |ASij + Eij + (1 − xi x j )GiC ,
                                                                          j                                ij


where introduced the following matrices

                             Sij := −Si · G−1 (AS j + E j + x j G) − xi Si (mod q)
                             Eij := −Ei · G−1 (AS j + E j + x j G) − xi E j (mod q).


                                                              49
                                                                             p
Because the initial error terms have the property that kEi k∞ , kE j k∞ ≤ αq (m + 1) N/2, it follows that
the resulting error after a single NAND gate is at most (see also [GSW13, Mah18] for more details)
                                                 r
                                                    ( m + 1) N
                                    kEij k∞ ≤ αq                · ( N + 1) .
                                                         2
In other words, the cumulative error term remains short relative to the modulus q after every application of
a homomorphic NAND gate, exactly as in the Dual-Regev FHE scheme of Mahadev [Mah18].

                               |CT12,34 iC1 C2 C3 C4 C12 C34 C12,34                       Cout = C12,34




                                            UNAND




            |CT12 iC1 C2 C12                                          |CT34 iC3 C4 C34    Caux = C12 C34




                    UNAND                                             UNAND




                                                                                         Cin = C1 C2 C3 C4
              |CT1 iC1     |CT2 iC2                        |CT3 iC3        |CT4 iC4

Figure 6: Homomorphic evaluation of a Boolean circuit C composed entirely of three NAND gates. Here,
the input is the quantum ciphertext |CT1 i ⊗ |CT2 i ⊗ |CT3 i ⊗ |CT4 i which corresponds to an encryption
of the plaintext x = ( x1 , . . . , x4 ) ∈ {0, 1}4 as in Construction 3. The resulting ciphertext |CT12,34 i lives on
a system C1 C2 C3 C4 C12 C34 C12,34 of which the last system C12,34 contains an encryption of C ( x) ∈ {0, 1}.


9.2 Rewinding lemma
Notice that the procedure DualFHECD .Eval in Construction 3 produces a highly entangled state since the
unitary operation UNAND induces entanglement between the Gaussian noise terms. In the next lemma, we
show that it is possible to rewind the evaluation procedure to be able to prove data deletion to a client.



                                                                 50
Lemma 19 (Rewinding lemma). Let λ ∈ N be the security parameter. Let n ∈ N, let q ≥ 2 be a prime
modulus and m ≥ 2n log q. Let N = (n + 1) · ⌈log q⌉ be an integer and let L be an upper bound on the
depth of the polynomial-sized Boolean circuit which is to be evaluated. Let α ∈ (0, 1) be a ratio such that
                           q
                                                                 q
                              8(m + 1) N ≤ αq ≤ √                                .
                                                     8 ( m + 1) · N · ( N + 1) L

Let DualFHECD = (KeyGen, Enc, Dec, Eval, Del, Vrfy) be the Dual-Regev (leveled) FHE scheme with certi-
fied deletion in Construction 3 and let Π be the interactive protocol in Protocol 1. Then, the following holds
for any parameter λ ∈ N, plaintext x ∈ {0, 1}ℓ and any polynomial-sized Boolean circuit C:
    After the interactive protocol Π = hS(|CT   f i , tC ), R(sk)i between the sender S and receiver R is
complete, the sender S is in possession of a quantum state ̺ in system Cin that satisfies

                                       k̺ − |CTihCT|ktr ≤ negl(λ),
        f i , tC ) ← DualFHECD .Eval(C, |CTi) is the post-evaluation state |CT
where (|CT                                                                  f i in systems Cin Caux Cout
and where |CTi ← DualFHECD .Enc(pk, x) is the initial state for (pk, sk) ← DualFHECD .KeyGen(1λ ).
Proof. Let λ ∈ N, x ∈ {0, 1}ℓ be a plaintext and C be any Boolean circuit of NAND-depth L = poly(λ).
Let (| f
       CTi , tC ) ← DualFHECD .Eval(C, |CTi) be the post-evaluation state | f   CTi in systems Cin Caux Cout
with circuit transcript tC and let ̺ be the outcome of the interactive protocol Π = hS(|CTf i , tC ), R(sk)i.
Recall that, in Lemma 20, we established that there exists a negligible ε(λ) such that DualFHE.Decsk de-
crypts system Cout of |CT f i with probability at least 1 − ε. By the ”Almost As Good As New Lemma“
(Lemma 1), performing the operation UDualFHE.Decsk , measuring the ancillary register M and rewinding the
                                                                       √
                                                                                                        f i.
computation, results in a mixed state ̺e that is within trace distance ε of the post-evaluation state |CT
Notice that, by reversing the sequence UtC of homomorphic NAND gates according to the transcript tC
                  f i, we recover the initial ciphertext |CTihCT| = Ut† |CT
with respect to |CT                                                         f ihCT
                                                                                 f | Ut in system Cin . By
                                                                          C             C

definition, we also have that ̺ = Ut†C ̺e UtC . Therefore,
                                                                                            q
                                    †             † f      f                 f    f
         k̺ − |CTihCT|ktr = kUtC ̺e UtC − UtC |CTihCT| UtC ktr = k̺e − |CTihCT|ktr ≤ ε(λ),

where we used that the trace distance is unitarily invariant. Since ε(λ) = negl(λ), this proves the claim.

Proof of correctness.    Let us now verify the correctness of decryption and verification of Construction 3.
Lemma 20 (Compactness and full homomorphism of DualFHECD ). Let λ ∈ N be the security parameter.
Let n ∈ N, let q ≥ 2 be a prime and m ≥ 2n log q. Let N = (n + 1) · ⌈log q⌉ and let L be an upper bound
on the depth of the polynomial-sized Boolean circuit which is to be evaluated. Let α ∈ (0, 1) be a ratio with
                           q
                                                                  q
                             8(m + 1) N ≤ αq ≤ √                                  .
                                                      8 ( m + 1) · N · ( N + 1) L

Then, the scheme DualFHECD = (KeyGen, Enc, Dec, Eval, Del, Vrfy) in Construction 3 is a compact and
fully homomorphic encryption scheme with certified deletion. In other words, for any efficienty (in λ ∈ N)
computable circuit C : {0, 1}ℓ → {0, 1} and any set of inputs x = ( x1 , . . . , xℓ ) ∈ {0, 1}ℓ , it holds that:
        "                                                                                       #
                                                             (pk,sk)←DualFHECD .KeyGen(1λ ,1L )
     Pr DualFHECD .Dec(sk, |CT f i) 6= C ( x1 , . . . , xℓ )  (vk,|CTi)←DualFHECD .Enc(pk,x )     ≤ negl(λ).
                                                           (| f
                                                             CTi,tC )←DualFHECD .Eval( C,|CTi,pk)


                                                      51
Proof. Let |CTi be the ciphertext output by DualFHECD .Enc(pk, x), where x ∈ {0, 1}ℓ denotes the plain-
                 f i , tC ) ← DualFHECD .Eval(C, |CTi) be the output of the evaluation procedure. Let us
text, and let (|CT
first consider the case when tC = ∅, i.e. not a single NAND gate has been applied to the ciphertext. In
this case, the claim follows from the fact that the truncated discrete Gaussian DZ(m+1)× N, √αq is supported on
                                                                                    q         2
          ( m +1)× N                p
{X ∈ Z q             : kXk∞ ≤ αq N (m + 1)/2}. Recall that DualFHECD .Dec(sk, | f         CTi) measures the
                                                                                                   ( m +1)× N
ciphertext | fCTi in the computational basis with outcome C = (C1 , . . . , Cℓ ), where Ci ∈ Z q              is a
                        ′
matrix, and outputs x ← DualFHE.Dec(sk, C). By our choice of parameters, each error term satisfies
                                        r
                                          N ( m + 1)            q
                            kEi k∞ ≤ αq                < p              , ∀i ∈ [ℓ].
                                               2         4 ( m + 1) N
Hence, decryption correctness is preserved if tC = ∅. Let us now consider the case when tC 6= ∅, i.e.
the Boolean circuit C consists of at least one NAND gate which has been applied to the ciphertext |CTi.
   this case, the cumulative error in system Cout after L applications of UNAND in Definition 28 is at most
In p
                                                        q
αq (m + 1) N/2( N + 1) L , which is less than √               by our choice of parameters. Therefore, the
                                                     4   ( m + 1) N
                                                                                          f i correctly
procedure DualFHE.Decsk decrypts a computational basis state in system Cout of the state |CT
with probability at least 1 − negl(λ). Furthermore, because the procedure DualFHECD .Dec is independent
of the circuit C and its depth L, the scheme DualFHECD is compact. This proves the claim.

    Let us now verify the correctness of verification of the scheme DualFHECD in Construction 3 according
to Definition 25. We show the following.
Lemma 21 (Correctness of verification). Let λ ∈ N be the security parameter. Let n ∈ N, let q ≥ 2 be a
prime modulus and m ≥ 2n log q. Let N = (n + 1) · ⌈log q⌉ be an integer and let L be an upper bound on
the depth of the polynomial-sized Boolean circuit which is to be evaluated. Let α ∈ (0, 1) be a ratio with
                           q
                                                                 q
                              8(m + 1) N ≤ αq ≤ √                                .
                                                     8 ( m + 1) · N · ( N + 1) L
Then, the Dual-Regev FHE scheme DualFHECD = (KeyGen, Enc, Dec, Eval, Del, Vrfy) with certified dele-
tion in Construction 3 satisfies verification correctness. In other words, for any λ ∈ N, any plaintext
x ∈ {0, 1}ℓ and any polynomial-sized Boolean circuit C entirely composed of NAND gates:
                                                                    
                                                 (pk,sk)←KeyGen(1λ )
                       Pr Verify (vk, π ) = 1 (vk,|CTi)←Enc(pk,x ) ≥ 1 − negl(λ).
                                                      π ←Del(|CTi)

                                                                                                         ( m +1)× n
Proof. Consider a bit x ∈ {0, 1} and a public key pk given by A = [Ā|Ā · x̄ (mod q)] ∈ Z q            ,
       $       m
       − {0, 1} . By the Leftover Hash Lemma (Lemma 4), the distribution of A is within negligible total
for x̄ ←
                                                      ( m +1)× n
variation distance of the uniform distribution over Z q          . Lemma 9 implies that the columns of A
           n
generate Z q with overwhelming probability. We consider the ciphertext |CTi output by Enc(pk, x), where
                                              x ·g                    x ·g
                                  |CTi ← Xq 1 |ψ̂y1 i ⊗ · · · ⊗ Xq N |ψ̂y N i ,
                                                                             ( m +1)× N
and where (g1 , . . . , g N ) are the columns of the gadget matrix G ∈ Z q           in Eq. (17). Given our choice,
                                 q
                                                                        q
                                    8(m + 1) N ≤ αq ≤ √                                 ,
                                                            8 ( m + 1) · N · ( N + 1) L

                                                         52
Corollary 1 implies that the Fourier transform of |CTi is within negligible trace distance of the state

       ci =                                   hx ,x ·g1 i                                                      hx ,x ·g N i
      |CT             ∑            ̺ 1 (x1 ) ωq 1
                                    α
                                                            |x1 i ⊗ · · · ⊗          ∑             ̺ 1 (x N ) ω q N
                                                                                                    α
                                                                                                                              |x N i .
                   x1 ∈Z m +1 :                                                   x N ∈Z m +1 :
                         q                                                               q
                Ax1 =y1 (mod q )                                              Ax N =y N (mod q )

From Lemma 11, it follows that the distribution of computational basis measurement outcomes is within
negligible total variation distance of the sample

                           π = (π1 , . . . , π N ) ∼ DΛyq 1 (A), √1 × · · · × DΛyq N (A), √1 ,
                                                                        2α                              2α

                √         √
where kπi k ≤       m + 1/ 2α for every i ∈ [ N ]. This proves the claim.

    We now show that our scheme DualFHECD in Construction 3 is extractable according to Definition 26.

Lemma 22 (Extractability of DualFHECD ). Let λ ∈ N be the security parameter. Let n ∈ N, let q ≥ 2 be
a prime modulus and m ≥ 2n log q. Let N = (n + 1) · ⌈log q⌉ and let L be an upper bound on the depth
of the polynomial-sized Boolean circuit which is to be evaluated. Let α ∈ (0, 1) be a noise ratio with
                          q
                                                                  q
                             8(m + 1) N ≤ αq ≤ √                                  .
                                                      8 ( m + 1) · N · ( N + 1) L

Then, the Dual-Regev FHE scheme Σ = DualFHECD with certified deletion in Construction 3 is extractable.
In other words, for any efficiently computable circuit C : {0, 1}ℓ → {0, 1} and any input x ∈ {0, 1}ℓ :
                                                               λ L
                                                                      
                                                          (pk,sk)←KeyGen(1 ,1 )
                                                           (vk,|CTi)←Enc(pk,x )
                 Pr y 6= C ( x1 , . . . , xℓ )           f i,tC )←Eval( C,|CTi,pk)
                                                        (|CT
                                                                                        ≤ negl(λ),             and
                                                                       f i,tC ),R(sk)i
                                                    ( ̺,y)←ExtracthS (|CT
                                                         (pk,sk)←KeyGen(1λ ,1L )
                                                                                         
                                                           (vk,|CTi)←Enc(pk,x )
                                                         f i,tC )←Eval( C,|CTi,pk) 
                    Pr Vrfy (vk, π ) = ⊥               (|CT                            ≤ negl(λ).
                                                                       f i,tC ),R(sk)i
                                                    ( ̺,y)←ExtracthS (|CT
                                                                 π ←Del( ̺)

Proof. Let C : {0, 1}ℓ → {0, 1} be an efficiently computable circuit and let x ∈ {0, 1}ℓ be any input.
Let (̺, y) ← ExtracthS(|CT          f i , tC ), R(sk)i denote the outcome of the interactive protocol between the
sender S and the receiver R, where (|CT           f i , tC ) ← Eval(C, |CTi , pk) is the post-evaluation state and
CT ← Enc(pk, x) is the initial ciphertext for (pk, sk) ← KeyGen(1λ ). Recall that the receiver R reversibly
performs the decryption procedure Dec (with the secret key sk hard-coded) during the execution of the
protocol Π = hS(|CT       f i , tC ), R(sk)i in Protocol 1. Therefore, it follows that the measurement outcome y
is equal to C ( x1 , . . . , xℓ ) with overwhelming probability due Lemma 20. This shows the first property.
    To show the second property, we can use the Rewinding Lemma (Lemma 19) to argue that after the
interactive protocol Π = hS(CT,       f tC ), R(sk)i between the sender S and receiver R is complete, the sender
S is in possession of a quantum state ̺ in system Cin that satisfies

                                             k̺ − |CTihCT|ktr ≤ negl(λ).

Therefore, the claim follows immediately from the verification correctness of Σ shown in Lemma 21.


                                                                  53
9.3 Proof of security
Let us now analyze the security of our FHE scheme with certified deletion in Construction 3. Note that
the results in this section all essentially carry over from Section 7.2, where we analyzed the security of our
Dual-Regev PKE scheme with certified deletion.

IND-CPA security of DualFHECD . We first prove that our scheme FHECD in Construction 3 satisfies the
notion IND-CPA security according to Definition 12. The proof is identical to the proof of IND-CPA-security
of our DualPKE scheme in Theorem 6. We add it for completeness.
Theorem 9. Let n ∈ N, let q ≥ 2 be a modulus, let m ≥ 2n log q and let N = (n + 1)⌈log q⌉, each
parameterized
p             by the security parameter λ ∈ N. Let α ∈ (0, 1) be a noise ratio parameter such that
                            q
  8(m + 1) N ≤ α1 ≤ √            . Then, the scheme DualFHECD in Construction 3 is IND-CPA-secure
                                   8( m + 1) N
                                                                      ( m + 1) N
assuming the quantum hardness of (decisional) LWEn,q,βq , for any β ∈ (0, 1) with α/β = λω (1) .
Proof. Let Σ = DualFHECD . We need to show that, for any QPT adversary A, it holds that
             Adv (λ) := | Pr[Expind-cpa (0) = 1] − Pr[Expind-cpa (1) = 1]| ≤ negl(λ).
                      Σ,A                            Σ,A,λ                             Σ,A,λ

Consider the experiment Expind-cpa
                           Σ,A,λ ( b) between the adversary A and a challenger taking place as follows:

   1. The challenger generates a pair (pk, sk) ← KeyGen(1λ ), and sends pk to A.
   2. A sends a distinct plaintext pair (m0 , m1 ) ∈ {0, 1}ℓ × {0, 1}ℓ to the challenger.
   3. The challenger computes (vk, CTb ) ← DualFHECD .Enc(pk, mb ), and sends |CTb i to A.
   4. A outputs a guess b′ ∈ {0, 1}, which is also the output of the experiment.
Recall that the procedure Enc(pk, mb ) outputs a pair (vk, |CTb i), where
                                                                               
                                      ( m +1)× n
                               A ∈ Zq            , (y1 | . . . |y N ) ∈ Z nq × N ← vk

is the verification key and where the ciphertext |CTb i is within negligible trace distance of
                                                               −Tr[S T Y]
                          ∑             ∑            ̺αq (E) ωq             |A · S + E + mb · G (mod q)i .                             (18)
                       S∈Z nq × N E∈Z (qm +1)× N

Here, Y ∈ Z nq × N is the matrix composed of the columns y1 , . . . , y N . Let β ∈ (0, 1) be any parameter with
                                                                                                            ( m + 1) N
α/β = λω (1) . Then, it follows from Theorem 5 that, under the (decisional) LWEn,q,βq                                    assumption, |CTb i
is computationally indistinguishable from the state
                               Tr[U T X̄]
                 ∑            ωq            |U i ,     X̄ = (x̄1 , . . . , x̄N ) ∼ DΛyq 1 (A), √1 × · · · × DΛyq N (A), √1 .
                                                                                                  2α                         2α
                                                                                                                                       (19)
                 ( m +1)× N
            U ∈Z q

                                                                                   ( m +1)× N
Here (x̄1 , . . . , x̄N ) refer to the columns of the matrix X̄ ∈ Z q                           . Finally, because the state in Eq. (19)
is completely independent of the bit b ∈ {0, 1}, it follows that

                AdvΣ,A (λ) := | Pr[Expind-cpa                ind-cpa
                                      Σ,A,λ (0) = 1] − Pr[ExpΣ,A,λ (1) = 1]| ≤ negl( λ ).

This proves the claim.

                                                                      54
IND-CPA-CD security of DualFHECD . Let us now analyze the security of our Dual-Regev homomorphic
encryption scheme DualFHECD in Construction 3. We prove that it satisfies certified deletion security as-
suming the Strong Gaussian-Collapsing (SGC) Conjecture (see Conjecture 5.2). This is a strengthening of
the Gaussian-collapsing property which we proved under the (decisional) LWE assumption (see Theorem 4).
The proof is similar to the proof of Theorem 7. We add it for completeness.
Theorem 10. Let λ ∈ N be the security parameter. Let n ∈ N, let q ≥ 2 be a prime modulus and
m ≥ 2n log q. Let N = (n + 1) · ⌈log q⌉ be an integer and let L be an upper bound on the depth of the
polynomial-sized Boolean circuit which is to be evaluated. Let α ∈ (0, 1) be a noise ratio such that
                          q
                                                                 q
                            8(m + 1) N ≤ αq ≤ √                                  .
                                                     8 ( m + 1) · N · ( N + 1) L
Then, the Dual-Regev homomorphic encryption scheme DualFHECD in Construction 3 is IND-CPA-CD-
                                                           N
secure assuming the Strong Gaussian-Collapsing property SGCn, ( m +1),q, 1
                                                                           from Conjecture 5.2.
                                                                              α

Proof. Let Σ = DualFHECD . We need to show that, for any QPT adversary A, it holds that

         Advhe -cert-del (λ) := | Pr[Exphe-cert-del (0) = 1] − Pr[Exphe-cert-del (1) = 1]| ≤ negl(λ).
            Σ,A                         Σ,A,λ                        Σ,A,λ

We consider the following sequence of hybrids:

 H0 : This is the experiment Exphe-cert-del (0) between A and a challenger:
                                Σ,A,λ

                                                          − Z nq ×m and a vector x̄ ←
                                                                                    − {0, 1}m and chooses
                                                          $                         $
         1. The challenger samples a random matrix Ā ←
            A = [Ā|Ā · x̄ (mod q)] T . The challenger chooses the secret key sk ← (−x̄, 1) ∈ Z qm+1 and
                                           ( m +1)× n
            the public key pk ← A ∈ Z q                 .
         2. A sends a distinct plaintext pair (m0 , m1 ) ∈ {0, 1} × {0, 1} to the challenger. (Note: Without
            loss of generality, we can just assume that m0 = 0 and m1 = 1).
         3. The challenger runs (|ψyi i , yi ) ← GenPrimal(AT , σ) in Algorithm 2, for i ∈ [ N ], and outputs
                                                                                                              
                                ( m +1)× n
                  vk ← (A ∈ Z q            , (y1 | . . . |y N ) ∈ Z nq × N ), |CT0 i ← |ψy1 i ⊗ · · · ⊗ |ψy N i .

         4. At some point in time, A returns a certificate π = (π1 , . . . , π N ) to the challenger.
                                                                                     √          √
         5. The challenger outputs ⊤, if AT · πi = yi (mod q) and kπi k ≤ m + 1/ 2α for i ∈ [ N ],
            and outputs ⊥, otherwise. If π passes the test with outcome ⊤, the challenger sends sk to A.
         6. A outputs a guess b′ ∈ {0, 1}, which is also the output of the experiment.

 H1 : This is same experiment as in H0 , except that (in Step 3) the challenger prepares the ciphertext in the
      Fourier basis rather than the standard basis. In other words, A receives the pair
                                                                                                                 
                          ( m +1)× n
          vk ← (A ∈ Z q              , (y1 , . . . , y N ) ∈ Z nq × N ), |CT0 i ← FTq |ψy1 i ⊗ · · · ⊗ FTq |ψy N i .

 H2 : This experiment is an N-fold variant of StrongGaussCollapseExpH,D,λ (0) in Conjecture 5.2:

                                                         − Z nq ×m and a vector x̄ ←
                                                                                   − {0, 1}m and chooses
                                                           $                       $
         1. The challenger samples a random matrix Ā ←
            A = [Ā|Ā · x̄ (mod q)] and t = (−x̄, 1) ∈ Z qm+1 .

                                                            55
         2. The challenger runs (|ψ̂yi i , yi ) ← GenDual(AT , σ) in Algorithm 1, for i ∈ [ N ], and sends the
            following tiplet to the adversary A:
                                                                                                        
                                                           n ×( m +1)
                       |ψ̂y1 i ⊗ · · · ⊗ |ψ̂y N i , AT ∈ Z q          , Y = (y1 | . . . |y N ) ∈ Z nq × N .

         3. At some point in time, A returns a certificate π to the challenger.
                                                                               √         √
         4. The challenger outputs ⊤, if AT · πi = yi (mod q) and kπi k ≤ m + 1/ 2α for i ∈ [ N ],
            and outputs ⊥, otherwise. If π passes the test with outcome ⊤, the challenger sends sk to A.
         5. A outputs a guess b′ ∈ {0, 1}, which is also the output of the experiment.

 H3 : This is an N-fold variant of the experiment in StrongGaussCollapseExpH,D,λ (1) in Conjecture 5.2;
      it is the same as H2 , except that the states |ψ̂y1 i ⊗ · · · ⊗ |ψ̂y N i (in Step 2) are measured in the
      computational basis before they are sent to A.

 H4 : This is same experiment as H3 , except that (in Step 2) the challenger additionally applies the Pauli
                 g              g
      operators Zq 1 ⊗ · · · ⊗ Zq N to the states |ψ̂y1 i ⊗ · · · ⊗ |ψ̂y N i before they are measured in the compu-
                                                                                           ( m +1)× N
      tational basis, where (g1 , . . . , g N ) are the rows of the gadget matrix G ∈ Z q               in Eq. (17).

 H5 : This is same experiment as H4 , except that (in Step 2) A receives the triplet
                                                                                                            
                  g                      g                     n ×( m +1)
                 Zq 1 |ψ̂y1 i ⊗ · · · ⊗ Zq N |ψ̂y N i , AT ∈ Z q          , y = (y1 | . . . |y N ) ∈ Z nq × N .

 H6 : This is same experiment as H5 , except that (in Step 2) the challenger prepares the quantum states in
      the Fourier basis instead. In other words, A receives the triplet
                                                                                                                 
                  g                           g                     n ×( m +1)
            FT†q Zq 1 |ψ̂y1 i ⊗ · · · ⊗ FT†q Zq N |ψ̂y N i , AT ∈ Z q          , y = (y1 | . . . |y N ) ∈ Z nq × N .

 H7 : This is the experiment Exphe-cert-del (1).
                                Σ,A,λ

   We now show that the hybrids are indistinguishable.
Claim 9.
                                    Pr[Exphe-cert-del (0) = 1] = Pr[H = 1].
                                          Σ,A,λ                      1

Proof. Without loss of generality, we can assume that the challenger applies the inverse Fourier transform
before sending the ciphertext to A. Therefore, the success probabilities are identical in H0 and H1 .

Claim 10.
                                            Pr[H1 = 1] = Pr[H2 = 1].

Proof. Because the challenger in H1 always sends the ciphertext |CT0 i corresponding to m0 = 0 to the
adversary A, the two hybrids H1 and H2 are identical.
                                                           N
Claim 11. Under the Strong Gaussian-Collapsing property SGCn, ( m +1),q, 1
                                                                           , it holds that
                                                                                  α


                                    | Pr[H2 = 1] − Pr[H3 = 1]| ≤ negl(λ).

Proof. This follows from Conjecture 5.2.

                                                          56
Claim 12.
                                           Pr[H3 = 1] = Pr[H4 = 1].

Proof. Because the challenger measures the state |ψ̂y1 i ⊗ · · · ⊗ |ψ̂y N i in Step 2 in the computational basis,
                              g              g
applying the phase operators Zq 1 ⊗ · · · ⊗ Zq N before the measurement does not affect the outcome.
                                                           N
Claim 13. Under the Strong Gaussian-Collapsing property SGCn, ( m +1),q, 1
                                                                           , it holds that
                                                                                α


                                   | Pr[H4 = 1] − Pr[H5 = 1]| ≤ negl(λ).

Proof. This follows from Conjecture 5.2 since, without loss of generality, we can assume that the challenger
                             g              g
applies the phase operators Zq 1 ⊗ · · · ⊗ Zq N before sending the states |ψ̂y1 i ⊗ · · · ⊗ |ψ̂y N i to A as input.

Claim 14.
                                           Pr[H5 = 1] = Pr[H6 = 1].

Proof. Without loss of generality, we can assume that the challenger applies the Fourier transform to the
       g                      g
state Zq 1 |ψ̂y1 i ⊗ · · · ⊗ Zq N |ψ̂y N i before sending it to the adversary A. Therefore, the success probabilities
in H5 and H6 are identical.

Claim 15.
                            | Pr[H6 = 1] − Pr[Exppk-cert-del (1) = 1]| ≤ negl(λ).
                                                 Σ,A,λ

Proof. From Lemma 6, we have FTq Xvq = Zvq FTq , for all v ∈ Z m            q . Hence, in H6 , we can instead assume
                                                                 T
that the challenger runs (|ψyi i , yi ) ← GenPrimal(A , 1/α) in Algorithm 2, for i ∈ [ N ], and then sends
the following to A:
                                                                                                               
                       ( m +1)× n                                                g                   g
         vk ← (A ∈ Z q            , (y1 | . . . |y N ) ∈ Z nq × N ), |CT1 i ← Xq 1 |ψy1 i ⊗ · · · ⊗ Xq N |ψy N i .

From Corollary 1, it follows that the states FT†q Zvq |ψ̂y i and Xvq |ψy i are within negligible trace distance, for
all v ∈ Z mq . Because the challenger in H7 always sends |CT1 i corresponding to m1 = 1 to the adversary
A, it follows that the distinguishing advantage between H6 and H7 = Exphe          -cert-del (1) is negligible.
                                                                                 Σ,A,λ

    Because the hybrids H0 and H7 are indistinguishable, this implies that

                                          Advhe-cert-del (λ) ≤ negl(λ).
                                             Σ,A




References
[Aar16]        Scott Aaronson. The complexity of quantum states and transformations: From quantum
               money to black holes, 2016.

[AC12]         Scott Aaronson and Paul Christiano. Quantum money from hidden subspaces, 2012.

[AJOP20]       Gorjan Alagic, Stacey Jeffery, Maris Ozols, and Alexander Poremba. On quantum chosen-
               ciphertext attacks and learning with errors. Cryptography, 4(1), 2020.


                                                         57
[Ajt96]     Miklós Ajtai. Generating hard instances of lattice problems (extended abstract). In Gary L.
            Miller, editor, Proceedings of the Twenty-Eighth Annual ACM Symposium on the Theory of
            Computing, Philadelphia, Pennsylvania, USA, May 22-24, 1996, pages 99–108. ACM, 1996.

[AP20]      Prabhanjan Ananth and Rolando L. La Placa. Secure software leasing, 2020.

[Ban93]     W. Banaszczyk. New bounds in some transference theorems in the geometry of numbers.
            Mathematische Annalen, 296(4):625–636, 1993.

[BB84]      C. H. Bennett and G. Brassard. Quantum cryptography: Public key distribution and coin
            tossing. In Proceedings of IEEE International Conference on Computers, Systems, and Signal
            Processing, page 175, India, 1984.

[BCM+ 21]   Zvika Brakerski, Paul Christiano, Urmila Mahadev, Umesh Vazirani, and Thomas Vidick. A
            cryptographic test of quantumness and certifiable randomness from a single quantum device,
            2021.

[BGG+ 14]   Dan Boneh, Craig Gentry, Sergey Gorbunov, Shai Halevi, Valeria Nikolaenko, Gil Segev,
            Vinod Vaikuntanathan, and Dhinakaran Vinayagamurthy. Fully key-homomorphic encryp-
            tion, arithmetic circuit abe, and compact garbled circuits. Cryptology ePrint Archive, Paper
            2014/356, 2014. https://eprint.iacr.org/2014/356.

[BI20]      Anne Broadbent and Rabib Islam. Quantum encryption with certified deletion. Lecture Notes
            in Computer Science, page 92–122, 2020.

[BK22]      James Bartusek and Dakshita Khurana. Cryptography with certified deletion, 2022.

[BPTG14]    Raphael Bost, Raluca Ada Popa, Stephen Tu, and Shafi Goldwasser. Machine learning clas-
            sification over encrypted data. IACR Cryptology ePrint Archive, 2014:331, 2014.

[Bra18]     Zvika Brakerski. Quantum fhe (almost) as secure as classical. Cryptology ePrint Archive,
            Report 2018/338, 2018. https://ia.cr/2018/338.

[BV11a]     Zvika Brakerski and Vinod Vaikuntanathan. Efficient fully homomorphic encryption from
            (standard) lwe. In Proceedings of the 2011 IEEE 52nd Annual Symposium on Foundations of
            Computer Science, FOCS ’11, page 97–106, USA, 2011. IEEE Computer Society.

[BV11b]     Zvika Brakerski and Vinod Vaikuntanathan.   Efficient fully homomorphic encryp-
            tion from (standard) lwe.   Cryptology ePrint Archive, Paper 2011/344, 2011.
            https://eprint.iacr.org/2011/344.

[CFGN96]    Ran Canetti, Uri Feige, Oded Goldreich, and Moni Naor. Adaptively secure multi-party com-
            putation. In Proceedings of the Twenty-Eighth Annual ACM Symposium on Theory of Com-
            puting, STOC ’96, page 639–648, New York, NY, USA, 1996. Association for Computing
            Machinery.

[CLLZ21]    Andrea Coladangelo, Jiahui Liu, Qipeng Liu, and Mark Zhandry. Hidden cosets and applica-
            tions to unclonable cryptography, 2021.

[CLZ21]     Yilei Chen, Qipeng Liu, and Mark Zhandry. Quantum algorithms for variants of average-case
            lattice problems via filtering, 2021.

                                                 58
[CMP20]      Andrea Coladangelo, Christian Majenz, and Alexander Poremba. Quantum copy-protection
             of compute-and-compare programs in the quantum random oracle model, 2020.

[CRW19]      Xavier Coiteux-Roy and Stefan Wolf. Proving erasure. 2019 IEEE International Symposium
             on Information Theory (ISIT), Jul 2019.

[DKW11]      Stefan Dziembowski, Tomasz Kazana, and Daniel Wichs. One-time computable self-erasing
             functions. In Theory of Cryptography - 8th Theory of Cryptography Conference, TCC 2011,
             volume 6597 of Lecture Notes in Computer Science, page 125. Springer, 2011.

[FM18]       Honghao Fu and Carl A. Miller. Local randomness: Examples and application. Physical
             Review A, 97(3), Mar 2018.

[Gen09]      Craig Gentry. A fully homomorphic encryption scheme. PhD thesis, Stanford University,
             2009. crypto.stanford.edu/craig.

[GGV20]      Sanjam Garg, Shafi Goldwasser, and Prashant Nalini Vasudevan. Formalizing data deletion
             in the context of the right to be forgotten. IACR Cryptol. ePrint Arch., page 254, 2020.

[GKZ19]      Alex B. Grilo, Iordanis Kerenidis, and Timo Zijlstra. Learning-with-errors problem is easy
             with quantum samples. Physical Review A, 99(3), Mar 2019.

[GMP22]      Alexandru Gheorghiu, Tony Metger, and Alexander Poremba. Quantum cryptography with
             classical communication: parallel remote state preparation for copy-protection, verification,
             and more, 2022.

[GPV07]      Craig Gentry, Chris Peikert, and Vinod Vaikuntanathan. Trapdoors for hard lattices and
             new cryptographic constructions. Cryptology ePrint Archive, Report 2007/432, 2007.
             https://eprint.iacr.org/2007/432.

[GR02]       Lov K. Grover and Terry Rudolph. Creating superpositions that correspond to efficiently
             integrable probability distributions. arXiv: Quantum Physics, 2002.

[GSW13]      Craig Gentry, Amit Sahai, and Brent Waters. Homomorphic encryption from learning
             with errors: Conceptually-simpler, asymptotically-faster, attribute-based. Cryptology ePrint
             Archive, Report 2013/340, 2013. https://ia.cr/2013/340.

[HH00]       L. Hales and S. Hallgren. An improved quantum fourier transform algorithm and applications.
             In Proceedings 41st Annual Symposium on Foundations of Computer Science, pages 515–525,
             2000.

[HILL88]     Johan Håstad, Russell Impagliazzo, Leonid A. Levin, and Michael Luby. Pseudo-random
             generation from one-way functions. In PROC. 20TH STOC, pages 12–24, 1988.

[HMNY21a] Taiga Hiroka, Tomoyuki Morimae, Ryo Nishimaki, and Takashi Yamakawa. Certified ever-
          lasting zero-knowledge proof for qma, 2021.

[HMNY21b] Taiga Hiroka, Tomoyuki Morimae, Ryo Nishimaki, and Takashi Yamakawa. Quantum en-
          cryption with certified deletion, revisited: Public key, attribute-based, and classical commu-
          nication, 2021.


                                                   59
[JL00]     Stanisław Jarecki and Anna Lysyanskaya. Adaptively secure threshold cryptography: Intro-
           ducing concurrency, removing erasures. In Proceedings of the 19th International Conference
           on Theory and Application of Cryptographic Techniques, EUROCRYPT’00, page 221–242,
           Berlin, Heidelberg, 2000. Springer-Verlag.

[KNTY18]   Fuyuki Kitagawa, Ryo Nishimaki, Keisuke Tanaka, and Takashi Yamakawa. Adap-
           tively secure and succinct functional encryption:  Improving security and ef-
           ficiency, simultaneously.  Cryptology ePrint Archive, Paper 2018/974, 2018.
           https://eprint.iacr.org/2018/974.

[KNY21]    Fuyuki Kitagawa, Ryo Nishimaki, and Takashi Yamakawa. Secure software leasing from
           standard assumptions, 2021.

[KRS09]    Robert Konig, Renato Renner, and Christian Schaffner. The operational meaning of min- and
           max-entropy. IEEE Transactions on Information Theory, 55(9):4337–4347, sep 2009.

[LZ19]     Qipeng Liu and Mark Zhandry. Revisiting post-quantum fiat-shamir. Cryptology ePrint
           Archive, Paper 2019/262, 2019. https://eprint.iacr.org/2019/262.

[Mah18]    Urmila Mahadev. Classical verification of quantum computations, 2018.

[MQU07]    Jörn Müller-Quade and Dominique Unruh. Long-term security and universal composability.
           In Salil P. Vadhan, editor, Theory of Cryptography, pages 41–60, Berlin, Heidelberg, 2007.
           Springer Berlin Heidelberg.

[MR04]     D. Micciancio and O. Regev. Worst-case to average-case reductions based on gaussian mea-
           sures. In 45th Annual IEEE Symposium on Foundations of Computer Science, pages 372–381,
           2004.

[MR07]     Daniele Micciancio and Oded Regev. Worst-case to average-case reductions based on gaus-
           sian measures. SIAM J. Comput., 37(1):267–302, 2007.

[NC11]     Michael A. Nielsen and Isaac L. Chuang. Quantum Computation and Quantum Information:
           10th Anniversary Edition. Cambridge University Press, USA, 10th edition, 2011.

[PT10]     Daniele Perito and Gene Tsudik.   Secure code update for embedded devices via
           proofs of secure erasure.   Cryptology ePrint Archive, Report 2010/217, 2010.
           https://ia.cr/2010/217.

[RAD78]    R L Rivest, L Adleman, and M L Dertouzos. On data banks and privacy homomorphisms.
           Foundations of Secure Computation, Academia Press, pages 169–179, 1978.

[Reg05]    Oded Regev. On lattices, learning with errors, random linear codes, and cryptography. Journal
           of the ACM, 56(6):34:1–34:40, 2005.

[Rob19]    Bhaskar Roberts. Toward secure quantum money. Princeton University Senior Thesis, 2019.
           http://arks.princeton.edu/ark:/88435/dsp01nc580q51r.

[SSTX09]   Damien Stehlé, Ron Steinfeld, Keisuke Tanaka, and Keita Xagawa. Efficient public key
           encryption based on ideal lattices. Cryptology ePrint Archive, Paper 2009/285, 2009.
           https://eprint.iacr.org/2009/285.

                                                 60
[TL17]    Marco Tomamichel and Anthony Leverrier. A largely self-contained and complete security
          proof for quantum key distribution. Quantum, 1:14, July 2017.

[Unr13]   Dominique Unruh. Revocable quantum timed-release encryption. Cryptology ePrint Archive,
          Report 2013/606, 2013. https://ia.cr/2013/606.

[Unr15]   Dominique Unruh. Computationally binding quantum commitments. Cryptology ePrint
          Archive, Paper 2015/361, 2015. https://eprint.iacr.org/2015/361.

[Wat06]   John Watrous. Zero-knowledge against quantum attacks. In Proceedings of the Thirty-Eighth
          Annual ACM Symposium on Theory of Computing, STOC ’06, page 296–305, New York, NY,
          USA, 2006. Association for Computing Machinery.

[Wil13]   Mark M. Wilde. Quantum Information Theory. Cambridge University Press, USA, 1st edition,
          2013.

[WZ82]    W. K. Wootters and W. H. Zurek. A single quantum cannot be cloned. Nature, 299(5886):802–
          803, October 1982.




                                              61

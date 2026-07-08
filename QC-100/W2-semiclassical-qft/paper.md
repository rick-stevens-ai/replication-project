# Semiclassical Fourier Transform for Quantum Computation

Robert B. Griffiths <sup>∗</sup> and Chi-Sheng Niu † Department of Physics Carnegie Mellon University Pittsburgh, PA 15213, U.S.A.

Version of 3 Nov. 1995

#### Abstract

Shor's algorithms for factorization and discrete logarithms on a quantum computer employ Fourier transforms preceding a final measurement. It is shown that such a Fourier transform can be carried out in a semi-classical way in which a "classical" (macroscopic) signal resulting from the measurement of one bit (embodied in a twostate quantum system) is employed to determine the type of measurement carried out on the next bit, and so forth. In this way the two-bit gates in the Fourier transform can all be replaced by a smaller number of one-bit gates controlled by classical signals. Success in simplifying the Fourier transform suggests that it may be worthwhile looking for other ways of using semi-classical methods in quantum computing.

Recently Shor[[1](#page-4-0), [2\]](#page-4-0) has shown that a quantum computer[[3\]](#page-4-0), if it could be built, would be capable of solving certain problems, such as factoring long numbers, much more rapidly than is possible using currently available algorithms on a conventional computer. This has stimulated a lot of interest in the subject[[4, 5](#page-4-0), [6\]](#page-4-0), and various proposals have been made for actually constructing such a computer[[7](#page-4-0), [8](#page-4-0), [9](#page-4-0), [10, 11\]](#page-4-0). The basic idea is that bits representing numbers can be embodied in two-state quantum systems, for example, in the spin degree of freedom of a spin half particle, and the computation proceeds by manipulating these bits using appropriate gates. It turns out that quantum computations can be carried out using circuits employing one-bit gates, which produce a unitary transformation on the twodimensional Hilbert space representing a single bit, together with two-bit gates producing appropriate unitary transformations on a four-dimensional Hilbert space [\[12](#page-5-0), [13, 14, 15\]](#page-5-0).

One-bit gates should be much easier to construct than two-bit gates, since, for example, an arbitrary unitary transformation on the spin degree of freedom of a spin half particle can be produced by subjecting it to a suitable time-dependent macroscopic magnetic field. On the other hand, a two-bit gate requires that one of the bits influence the other in a

<sup>∗</sup>Electronic mail: rgrif+@cmu.edu

†Electronic mail: cn28+@andrew.cmu.edu

<span id="page-1-0"></span>non-trivial way, and this without leaving any record in the environment, since the computer utilizes coherent quantum states.

In this letter we shall show how the quantum Fourier transforms which in Shor's algorithms immediately precede a final measurement can be carried out in a semi-classical fashion which requires no two-bit gates. The trick is to measure a particular bit and then use the result to produce a classical signal which controls a one-bit transformation carried out on the next bit just before it is measured, and so forth. It is of interest for at least three reasons. First, it represents a completely new (so far as we know) technique for quantum computation, in which the results of certain measurements, converted into "classical" signals (imagine a pulse of several volts traveling down a coaxial cable), can be used to influence a later step in the computation [16]. Second, computing the Fourier transform is considerably simplified in the sense that it requires no two-bit gates. Third, a simple way of seeing why the semi-classical method actually works is to adopt a point of view—in technical terms, a particular family of consistent histories—in which the results of a measurement are used to infer the state of a quantum system before the measurement was carried out. This perspective may prove useful in thinking about other issues in quantum computing, quantum optics, and quantum effects in atomic physics.

Since Shor has described his algorithms in considerable detail in his publications [1, 2], we shall not discuss them here. It will be sufficient to note that after a certain number of steps of the quantum computation have been carried out, the relevant quantum state  $|\psi\rangle$  is a coherent superposition [17] of different states  $|a\rangle$  labeled by an integer a between 0 and q-1, where  $q=2^{s+1}$ . The state  $|\psi\rangle$  is then subjected to a unitary transformation F, a sort of discrete Fourier transform, which carries each basis state  $|a\rangle$  of the q-dimensional Hilbert space into

$$F|a\rangle = \frac{1}{\sqrt{q}} \sum_{c=0}^{q-1} e^{2\pi i a c/q} |c\rangle. \tag{1}$$

This is followed by a measurement of the integer c, that is, a measurement of each of its s+1 bits.

A set of gates which carries out this Fourier transform [18] is shown in Fig. 1 for s=3. The bits to be transformed enter from the left. One can imagine that they are spin 1/2 particles, with the results of the preceding computation embodied (as a coherent superposition) in their collective spin degrees of freedom. These particles then move through a series of gates, indicated by circles, and eventually arrive at measuring devices, shown as squares, where a particular component of spin, say  $S_z$ , is measured by a Stern-Gerlach device, with  $S_z = 1/2$  in units of  $\hbar$  interpreted as the bit  $|1\rangle$ , and  $S_z = -1/2$  as the bit  $|0\rangle$ .

If the binary representation of the number a is

$$a = \sum_{j=0}^{s} a_j 2^j, (2)$$

with each  $a_j$  zero or one, the state  $|a\rangle$  can be conveniently written as a tensor product

$$|a\rangle = |a_s a_{s-1} \dots a_0\rangle = |a_s\rangle_s \otimes \dots |a_1\rangle_1 \otimes |a_0\rangle_0.$$
(3)

Using the same notation for  $|c\rangle$ , we can rewrite (1) in the form

$$F|a\rangle = \prod_{j=0}^{s} \otimes |p(\phi_j)\rangle_j, \tag{4}$$

<span id="page-2-0"></span>where the state

$$|p(\phi)\rangle = (|0\rangle + e^{2\pi i\phi}|1\rangle)/\sqrt{2} \tag{5}$$

will be said to have a phase  $\phi$  between 0 and 1. The phases  $\phi_j$  in (4) take the values:

$$\phi_j = \sum_{k=0}^{s-j} a_k 2^{j+k-s-1}.$$
 (6)

In terms of our picture of a spin half particle,  $|p(\phi)\rangle$  represents a spin component of 1/2 in a direction in the x, y plane determined by  $\phi$ .

The one-bit gates in the top row of Fig. 1 transform the bit entering on the left to one leaving on the right through:

$$|0\rangle \to (|0\rangle + |1\rangle)/\sqrt{2} = |p(0)\rangle, |1\rangle \to (|0\rangle - |1\rangle)/\sqrt{2} = |p(1/2)\rangle.$$
(7)

(In a spin picture, the spin is rotated by  $90^{\circ}$  about the y axis.) The two bit gate labeled with an integer m converts the bits entering on the left into those leaving on the right according to the scheme:

$$|00\rangle \to |00\rangle, \quad |01\rangle \to |01\rangle, |10\rangle \to |10\rangle, \quad |11\rangle \to \exp[2\pi i/2^m]|11\rangle.$$
(8)

Here we use the convention that the left element in each ket  $|\rangle$  in (8) is the bit which in Fig. 1 enters the two-bit gate at a point marked by a black dot and also leaves at a black dot, while the right element in each ket denotes the bit which enters and leaves the gate at a point labeled by a circle.

It is helpful to think of (8) as a transformation in which one bit acts as a "control" which enters and leaves the gate as a zero or one, while the other "target" bit enters as  $|p(\phi)\rangle$  and undergoes a phase shift, so that it leaves as  $|p(\phi')\rangle$ , where  $\phi' = \phi + 2^{-m}$ . From this perspective it is easy to see how the network in Fig. 1 produces the desired result. Suppose that the bit  $a_3$  enters the left-most one-bit gate in Fig. 1 in the state  $|0\rangle$ . It emerges at the point B in the state  $|p(0)\rangle$ . As it passes downwards through the successive two bit gates its phase is shifted by the bits  $a_2$ ,  $a_1$ , and  $a_0$ , acting as control bits, by an amount

$$\Delta \phi = a_0 / 16 + a_1 / 8 + a_2 / 4. \tag{9}$$

If, on the other hand,  $a_3$  arrives as  $|1\rangle$ , the one-bit gate converts it to  $|p(1/2)\rangle$ , so that the bit which emerges as  $c_0$  has a phase  $\Delta \phi + a_3/2$ , in agreement with (6). The same sort of analysis can be applied to the rest of the circuit.

However, one can equally well regard the bits entering and leaving the gates through the black dots in Fig. 1 as the control bits, and it is this point of view which is useful for constructing the semiclassical Fourier transform. Suppose that the final measurement reveals that the bit  $c_0$  is 1, corresponding to  $|1\rangle$ . Then, since a control bit enters and leaves the two-bit gates unchanged, we conclude that this bit was also in the state  $|1\rangle$  at point B, just after emerging from the first one-bit gate. Similarly, if the measurement yields  $c_0 = 0$ , we conclude that the bit was in the state  $|0\rangle$  at the point B. Hence the circuit would work equally well if the measurement on this bit were actually carried out at the point B in Fig. 1, were it not for the fact that this bit is also needed in order to influence  $a_2$ ,  $a_1$ , and  $a_0$ , now

regarded as target bits, as they pass through the two-bit gates controlled by  $c_0$ . However, if  $c_0$  is measured at B and the result is converted to a classical signal, this signal can be used to determine the action of a corresponding set of one-bit gates acting upon  $a_2$ ,  $a_1$ , and  $a_0$ .

Applying this type of analysis to the other parts of Fig. 1, one is led to the arrangement shown in Fig. 2, where all the two bit gates in Fig. 1 have been eliminated, and their work taken over by one-bit gates controlled by classical signals (double lines) and followed by measurements. Each of the boxes in Fig. 2 performs the following operations. The incoming bit is first subjected to a unitary transformation, equivalent to a phase shift followed by (7):

$$|0\rangle \to (|0\rangle + |1\rangle)/\sqrt{2}, |1\rangle \to e^{2\pi i\phi}(|0\rangle - |1\rangle)/\sqrt{2},$$
(10)

where  $\phi$  is the phase transmitted as a classical signal from the previous box. The bit is then measured to yield the result c=0 or 1. The outputs are two classical signals represented by double lines: one is the result of the measurement, and the other represents a phase

$$\phi' = \phi/2 + c/4 \tag{11}$$

which is sent to the next box. The very first box uses  $\phi = 0$  in (10).

Readers unfamiliar with the rules which allow one to use the results of a measurement to infer the state of a quantum system prior to the measurement are referred to the relevant literature [19, 20, 21, 22, 23]. The basic idea is that one can add to a quantum history, consisting of an initial state and the result of a measurement, a projector, for example

$$P = |c_0 = 1\rangle\langle c_0 = 1|, \tag{12}$$

representing property of the quantum system at a time just prior to the measurement. The conditional probability of P is one, given that the measurement yields  $c_0 = 1$ . But in the situation shown in Fig. 1, P commutes with the unitary transformations corresponding to the three 2-bit gates which precede the measurement of  $c_0$ , and therefore one can "push" the corresponding property backwards in time to the point B in Fig. 1, and again conclude that it occurred with probability one. Anyone who feels uncomfortable with this method of reasoning can, of course, use traditional techniques to verify that the arrangement in Fig. 2 will yield the same probability to observe a number c as that in Fig. 1. (Note that it is necessary to check this for an initial state  $|\psi\rangle$  which is an arbitrary linear combination of the different  $|a\rangle$  states.)

The scheme in Fig. 2 should be quite a bit simpler to realize than that in Fig. 1, because it only requires one-bit operations controlled by classical signals rather than the more difficult and more numerous two-bit operations indicated in Fig. 1. However, the need to carry out a measurement on one bit before beginning to measure another could be a disadvantage if the physical elements representing the bits are short lived or decohere rapidly on the time scale required to carry out a measurement and convert it into a classical signal. If this turns out to be a problem, a possible remedy might be to arrange the earlier part of the quantum computation in such a way that the more significant bits of a are produced earlier than the less significant bits.

An important question is whether other parts of Shor's algorithms (or other applications of quantum computing) can make use of similar semi-classical operations. We have no specific proposals, but we think the idea is worth further study. There are bits other than

<span id="page-4-0"></span>those entering the final Fourier transform which are produced elsewhere in the computation, and it is conceivable that measuring some of these could be used in modify later steps in the calculation, or perhaps for the non-trivial task of correcting errors. In connection with the latter, see [\[24](#page-5-0)].

Finally, we note that adopting alternative perspectives or points of view about what is going on in a quantum computation can yield useful insights. The traditional perspective, represented in almost all work on quantum computing up till now, in which the "wave function of the computer" develops unitarily in time until a measurement is made, has demonstrated its value through the work of various people who have brought quantum computation to its current state of development. In this letter we have shown that an alternative point of view, in which the results of measurements are traced backwards in time, can also be valuable. The general principles of quantum mechanics allow for a variety of viewpoints or, to use the technical term, consistent families, and recent developments in the foundations of quantum theory[[25\]](#page-5-0) permit one to make effective use of these without becoming entangled in paradoxes, mysterious long-range influences, and the like.

## Acknowledgements

We are grateful to Dr. D. DiVincenzo for some helpful comments on the manuscript. Financial support for this research has been provided by the National Science Foundation through grant PHY-9220726.

## References

- [1] P. W. Shor, in Proceedings of the 35th Annual Symposium on Foundations of Computer Science, Santa Fe, 1994, edited by S. Goldwasser (IEEE Computer Society Press, Los Alamitos, California, 1994), p. 124.
- [2] P. W. Shor, preprint ([quant-ph/9508027\)](http://arxiv.org/abs/quant-ph/9508027), submitted to SIAM J. Computing.
- [3] D. Deutsch, Proc. R. Soc. London, Ser. A 400, 97 (1985); Proc. R. Soc. London, Ser. A 425, 73 (1989)
- [4] C. H. Bennett, Phys. Today 48, 24 (Oct. 1995).
- [5] D. P. DiVincenzo, Science 270, 255 (1995).
- [6] S. Lloyd, Sci. Am. Oct. 1995, 140 (1995).
- [7] S. Lloyd, Science 261, 1569 (1993).
- [8] A. Barenco, D. Deutsch, A. Ekert and R. Jozsa Phys. Rev. Lett. 74, 4083 (1995).
- [9] T. Sleator and H. Weinfurter, Phys. Rev. Lett. 74, 4087 (1995).
- [10] J. I. Cirac and P. Zoller, Phys. Rev. Lett. 74, 4091 (1995).
- [11] I. L. Chuang and Y. Yamamoto, preprint [\(quant-ph/9505011](http://arxiv.org/abs/quant-ph/9505011)).

- <span id="page-5-0"></span>[12] D. P. DiVincenzo, Phys. Rev. A 51, 1015 (1995).
- [13] D. Deutsch, A. Barenco and A Ekert, Proc. R. Soc. Lond. A 449, 669 (1995).
- [14] S. Lloyd, Phys. Rev. Lett. 75, 346 (1995).
- [15] A. Barenco et al., Phys. Rev. A 52, 3457 (1995).
- [16] Using the result of a classical measurement to determine a subsequent unitary transformation on a quantum system has been proposed in connection with teleportation; see C. H. Bennett et al., Phys. Rev. Lett. 70, 1895 (1993), as pointed out to us by D. DiVincenzo.
- [17] Or, if one prefers, a reduced density matrix; this makes no difference for the following discussion.
- [18] According to [\[2](#page-4-0)], this scheme was invented independently by D. Coppersmith, IBM Research Report RC 19642 (1994) and by D. Deutsch (unpublished).
- [19] R. B. Griffiths, J. Stat. Phys. 36, 219 (1984). See, in particular, Sec. 5.
- [20] R. B. Griffiths, in New Techniques and Ideas in Quantum Measurement Theory, edited by D. M. Greenberger (New York Academy of Sciences, New York, 1986) p. 512.
- [21] R. Omn`es, Rev. Mod. Phys. 64, 339 (1992).
- [22] R. B. Griffiths, Phys. Rev. Lett. 70, 2201 (1993).
- [23] R. Omn`es, The Interpretation of Quantum Mechanics (Princeton University Press, Princeton, 1994).
- [24] P. W. Shor, Phys. Rev. A 52 2493 (1995).
- [25] For a compact review, see R. B. Griffiths, in Symposium on the Foundations of Modern Physics 1994, edited by K. V. Laurikainen, C. Montonen and K. Sunnarborg (Editions Fronti`eres, Gif-sur-Yvette, France, 1994) p. 85.

#### Figure Captions

Figure 1: Arrangement of quantum gates to carry out the discrete Fourier transform [\(4](#page-1-0)) on numbers consisting of four bits.

Figure 2: Semiclassical procedure which produces the same result as the circuit in Fig. 1. The double lines represent classical signals.

![](_page_6_Figure_0.jpeg)

Figure 1

![](_page_6_Figure_2.jpeg)

Figure 2
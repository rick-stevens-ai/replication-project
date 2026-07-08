# Hamiltonian Simulation Using Linear Combinations of Unitary Operations

Andrew M. Childs<sup>1,2</sup> and Nathan Wiebe<sup>2</sup>

<sup>1</sup>Department of Combinatorics & Optimization, University of Waterloo, Ontario N2L 3G1, Canada <sup>2</sup>Institute for Quantum Computing, University of Waterloo, Ontario N2L 3G1, Canada

We present a new approach to simulating Hamiltonian dynamics based on implementing linear combinations of unitary operations rather than products of unitary operations. The resulting algorithm has superior performance to existing simulation algorithms based on product formulas and, most notably, scales better with the simulation error than any known Hamiltonian simulation technique. Our main tool is a general method to nearly deterministically implement linear combinations of nearby unitary operations, which we show is optimal among a large class of methods.

### I. INTRODUCTION

Simulating the time evolution of quantum systems is a major potential application of quantum computers. While quantum simulation is apparently intractable using classical computers, quantum computers are naturally suited to this task. Even before a fault-tolerant quantum computer is built, quantum simulation techniques can be used to prove equivalence between Hamiltonian-based models of quantum computing (such as adiabatic quantum computing [1] and continuous-time quantum walks [2]) and to develop novel quantum algorithms [3–7].

In recent years there has been considerable interest in optimizing quantum simulation algorithms. The original approach to quantum simulation, based on product formulas, was proposed by Lloyd for time-independent local Hamiltonians [8]. This work was later generalized to give efficient simulations of sparse time-independent Hamiltonians that need not have tensor-product structure [4, 9]. Further refinements of these schemes have yielded improved performance [10–13] and the techniques have been extended to cover time-dependent Hamiltonians [14, 15]. Recently a new paradigm has been proposed that uses quantum walks rather than product formulas [16, 17]. This approach is superior to the product formula approach for simulating sparse time-independent Hamiltonians with constant accuracy (and in addition, can be applied to non-sparse Hamiltonians), whereas the product formula approach is superior for generating highly accurate simulations of sparse Hamiltonians.

The performance of simulation algorithms based on product formulas is limited by the fact that high-order approximations are needed to optimize the algorithmic complexity. The best known high-order product formulas, the Lie-Trotter-Suzuki formulas, approximate the time evolution using a product of unitary operations whose length scales exponentially with the order of the formula [18]. In contrast, classical methods known as multi-product formulas require a sum of only polynomially many unitary operations to achieve the same accuracy [19] (although of course the overall cost of classical simulations based on multi-product formulas remains exponential in the number of qubits used to represent the Hilbert space). However, these methods cannot be directly implemented on a quantum computer because unitary operations are not closed under addition.

Our work addresses this by presenting a non-deterministic algorithm that can be used to perform linear combinations of unitary operators on quantum computers. We achieve high success probabilities provided the operators being combined are near each other. We apply this tool to quantum simulation and thereby improve upon existing quantum algorithms for simulating Hamiltonian dynamics. Our main result is as follows.

<span id="page-0-1"></span>**Theorem 1.** Let the system Hamiltonian be  $H = \sum_{j=1}^m H_j$  where each  $H_j \in \mathbb{C}^{2^n \times 2^n}$  is Hermitian and satisfies  $\|H_j\| \leq h$  for a given constant h. Then the Hamiltonian evolution  $e^{-iHt}$  can be simulated on a quantum computer with failure probability and error at most  $\epsilon$  as a product of linear combinations of unitary operators. In the limit of large  $m, ht, 1/\epsilon$ , this simulation uses

<span id="page-0-0"></span>
$$\tilde{O}\left(m^2 h t e^{1.6\sqrt{\log(mht/\epsilon)}}\right) \tag{1}$$

elementary operations and exponentials of the  $H_i$ s.

Although we have not specified the method used to simulate the exponential of each  $H_j$ , there are well-known techniques to simulate simple Hamiltonians. In particular, if  $H_j$  is 1-sparse (i.e., has at most one non-zero matrix element in each row and column), then it can be simulated using O(1) elementary operations [4, 9], so (1) gives an upper bound on the complexity of simulating sparse Hamiltonians.

Our simulation is superior to the previous best known simulation algorithms based on product formulas. Previous methods have scaling of the same form, but with the coefficient 1.6 replaced by 2.54 [11, Theorem 1] or 2.06 [20, Theorem 1]. Also note that Theorem 1 of [12] gives a similar scaling as in [20], except the term in the exponential depends on the second-largest  $||H_j||$  rather than h.

Perhaps more significant than the quantitative improvement to the complexity of Hamiltonian simulation is that our approach demonstrates a new class of simulation protocols going beyond the Lie–Trotter–Suzuki paradigm, the approach used in most previous simulation algorithms. It remains unknown how efficiently one can perform quantum simulation as a function of the allowed error  $\epsilon$ , and we hope our work will lead to a better understanding of this question.

The remainder of this article is organized as follows. In Section II, we provide a general method for implementing linear combinations of unitary operators using quantum computers and lower bound its success probability. This method is optimal among a large class of such protocols, as shown in the appendix. In Section III, we provide a brief review of Lie–Trotter–Suzuki formulas and multi-product formulas and then show how to implement multi-product formulas on quantum computers. Error bounds and overall success probabilities of our simulations are derived in Section IV. We then bound the number of quantum operations used in our simulation in Lemma 12, from which Theorem 1 follows. We conclude in Section V with a summary of our results and a discussion of directions for future work.

# <span id="page-1-0"></span>II. ADDING AND SUBTRACTING UNITARY OPERATIONS USING QUANTUM COMPUTERS

In this section we describe basic protocols for implementing linear combinations of unitary operations. Lemma 2 shows that a quantum computer can nearly deterministically perform a weighted average of two nearby unitary operators. (Our approach is reminiscent of a technique for implementing fractional quantum queries using discrete queries [21].) We build upon Lemma 2 in Theorem 3, showing that a quantum computer can non-deterministically implement an arbitrary linear combination of a set of unitary operators.

<span id="page-1-1"></span>**Lemma 2.** Let  $U_a, U_b \in \mathbb{C}^{2^n \times 2^n}$  be unitary operations and let  $\Delta = \|U_a - U_b\|$ . Then for any  $\kappa \geq 0$ , there exists a quantum algorithm that can implement an operator proportional to  $\kappa U_a + U_b$  with failure probability at most  $\Delta^2 \kappa / (\kappa + 1)^2 \leq 4\kappa / (\kappa + 1)^2$ .

Proof. Let

$$V_{\kappa} := \begin{pmatrix} \sqrt{\frac{\kappa}{\kappa+1}} & \frac{-1}{\sqrt{\kappa+1}} \\ \frac{1}{\sqrt{\kappa+1}} & \sqrt{\frac{\kappa}{\kappa+1}} \end{pmatrix}. \tag{2}$$

Our protocol for implementing the weighted average of  $U_a$  and  $U_b$  works as follows (see Figure 1). First, we perform  $V_{\kappa}$  on an ancilla qubit. Second, we perform a zero-controlled  $U_a$  gate and a controlled  $U_b$  gate on the state  $|\psi\rangle$  using the ancilla as the control. Finally, we apply  $V_{\kappa}^{\dagger}$  to the ancilla qubit and measure it in the computational basis. This protocol performs the following transformations:

$$|0\rangle|\psi\rangle \mapsto \left(\sqrt{\frac{\kappa}{\kappa+1}}|0\rangle + \frac{1}{\sqrt{\kappa+1}}|1\rangle\right)|\psi\rangle$$

$$\mapsto \left(\sqrt{\frac{\kappa}{\kappa+1}}|0\rangle U_{a}|\psi\rangle + \frac{1}{\sqrt{\kappa+1}}|1\rangle U_{b}|\psi\rangle\right)$$

$$\mapsto |0\rangle \left(\frac{\kappa}{\kappa+1}U_{a} + \frac{1}{\kappa+1}U_{b}\right)|\psi\rangle + |1\rangle \frac{\sqrt{\kappa}}{\kappa+1}(U_{b} - U_{a})|\psi\rangle. \tag{3}$$

If the first qubit is measured and a result of 0 is observed, then this protocol performs  $|\psi\rangle \mapsto (\kappa U_a + U_b)|\psi\rangle$  (up to normalization). If the measurement yields 1 then the algorithm fails. The probability of this failure,  $P_+$ , is

$$P_{+} \le \frac{\|U_{b} - U_{a}\|^{2} \kappa}{(\kappa + 1)^{2}} = \frac{\Delta^{2} \kappa}{(\kappa + 1)^{2}}.$$
(4)

Since  $\Delta \leq 2$ , this is at most  $\frac{4\kappa}{(\kappa+1)^2}$ .

By substituting  $U_b \to -U_b$ , Lemma 2 also shows that unitary operations can be subtracted. (Alternatively, replacing  $V_{\kappa}^{\dagger}$  with  $V_{\kappa}$  in Figure 1 also simulates  $U_a - U_b$ .) Similarly, we could make the weights of each unitary complex by multiplying  $U_0$  and  $U_1$  by phases, although we will not need to make use of this freedom.

General linear combinations of unitary operators can be performed by iteratively applying Lemma 2. The following theorem gives constructs such a simulation and provides bounds on the probabilities of failure.

<span id="page-2-1"></span>![](_page_2_Picture_1.jpeg)

FIG. 1: Quantum circuit for non-deterministically performing an operator proportional to  $\kappa U_a + U_b$  given a measurement outcome of zero.

<span id="page-2-0"></span>**Theorem 3.** Let  $V:=\sum_{q=1}^{k+1}C_qU_q$  for  $k\geq 1$  where  $C_q\neq 0$ ,  $\|U_q\|=1$ , and  $\max_{q\neq q'}\|U_q-U_{q'}\|\leq \Delta$ . Let  $\kappa:=(\sum_{q:\ C_q>0}C_q)/(\sum_{q:\ C_q<0}|C_q|)$ . Then there exists a quantum algorithm that implements an operator proportional to V with probability of failure  $P_++P_-$  with

$$P_{+} \le \frac{k\Delta^{2}}{4},\tag{5}$$

$$P_{-} \le \frac{4\kappa}{(\kappa+1)^2},\tag{6}$$

where  $P_{+}$  is the probability of failing to add some pair of operators and  $P_{-}$  is the probability of failing to perform the subtraction.

Proof. Let

$$A := \frac{1}{\sum_{q:C_q > 0} C_q} \sum_{q:C_q > 0} C_q U_q, \tag{7}$$

$$B := \frac{1}{\sum_{q:C_q < 0} |C_q|} \sum_{q:C_q < 0} |C_q| U_q. \tag{8}$$

We implement  $V \propto \kappa A - B$  using circuits that non-deterministically implement operators proportional to A and B. We recursively perform these sums by using the circuits given in Lemma 2, except that we defer measurement of the output until the algorithm is complete. We then implement  $\kappa A - B$  by using our addition circuit, with  $U_a$  taken to be the circuit that implements A and  $U_b$  taken to be the circuit that implements -B. Then we measure each of the control qubits for the addition steps. Finally, if all the measurement results are zero (indicating success), we measure the control qubit for the subtraction step. If that qubit is zero, then we know from prior analysis that the non-unitary operation V is implemented successfully.

The operators A and B are implemented by recursively adding terms. For example, the sum  $U_1 + U_2 + U_3 + U_4$  is implemented as  $(((U_1 + U_2) + U_3) + U_4)$ . Implementing the sums in A and B requires k - 1 addition operations, so V can be implemented using k - 1 addition operations and one subtraction operation (assuming that all the control qubits are measured to be zero at the end of the protocol).

According to Lemma 2, the probability of failing to implement V, given that we successfully implement A and B, is

$$P_{-} \le \frac{4\kappa}{(\kappa+1)^2}.\tag{9}$$

The probability of failing to perform the k-1 sums needed to construct A and B obeys

$$P_{+} \le (k-1)\frac{\Delta^{2}\kappa}{(\kappa+1)^{2}} \le \frac{k\Delta^{2}}{4},\tag{10}$$

where the last step follows from the fact that we can take  $\kappa \geq 1$  without loss of generality.

These results show that we can non-deterministically implement linear combinations of unitary operators with high probability provided that  $\kappa \gg 1$  and  $\Delta \ll 1$ . As we will see shortly, this situation can naturally occur in quantum simulation problems.

Note that it is not possible to increase the success probability of the algorithm by replacing the single-qubit unitary  $V_{\kappa}$  with a different unitary, even if that unitary is allowed to act on all of the ancilla qubits simultaneously. We present this argument in Appendix A.

### <span id="page-3-0"></span>III. IMPLEMENTING MULTI-PRODUCT FORMULAS ON QUANTUM COMPUTERS

In this section we present a new approach to quantum simulation: we approximate the time evolution using a sequence of non-unitary operators that are each a linear combination of product formulas. Such sums of product formulas are known in the numerical analysis community as multi-product formulas, and can be more efficient than product formulas for classical computations [19, 22]. We show how to implement multi-product formulas using quantum computers by leveraging our method for non-deterministically performing linear combinations of unitary operators.

#### A. Review of Lie-Trotter-Suzuki and Multi-Product Formulas

Product formula approximations can be used to accurately approximate an operator exponential as a product of operator exponentials that can be easily implemented. Apart from their high degree of accuracy, these approximations are useful because they approximate a unitary operator with a sequence of unitary operators, making them ideally suited for quantum computing applications.

The most accurate known product formula approximations are the Lie–Trotter–Suzuki formulas, which approximate  $e^{-iHt}$  for  $H = \sum_{j=1}^{m} H_j$  as a product of the form

$$e^{-iHt} pprox \prod_{k=1}^{N_{\text{exp}}} e^{-iH_{j_k}t_k}.$$

These formulas are recursively defined for any integer  $\chi > 0$  by [18]

$$S_{1}(t) = \prod_{j=1}^{m} e^{-iH_{j}t/2} \prod_{j=m}^{1} e^{-iH_{j}t/2},$$

$$S_{\chi}(t) = \left(S_{\chi-1}(s_{\chi-1}t)\right)^{2} S_{\chi-1}([1-4s_{\chi-1}]t) \left(S_{\chi-1}(s_{\chi-1}t)\right)^{2},$$
(11)

where  $s_p = (4 - 4^{1/(2p+1)})^{-1}$  for any integer p > 0. This choice of  $s_p$  is made to ensure that the Taylor series of  $S_{\chi}$  matches that of  $e^{-iHt}$  to  $O(t^{2\chi+1})$ . Consequently, the approximation can be made arbitrarily accurate for suitably large values of  $\chi$  and small values of t.

The advantage of these formulas is clear: they are highly accurate and approximate  $U(t) := e^{-iHt}$  by a sequence of unitary operations, which can be directly implemented using a quantum computer. The primary disadvantage is that they require  $O(5^k)$  exponentials to construct an  $O(t^{2k+1})$  approximation. This scaling leads to quantum simulation algorithms with complexity  $(\|H\|t)^{1+o(1)}$ . A product formula requiring significantly fewer exponentials could result in a substantial performance improvement over existing product formula-based quantum simulation algorithms.

In the context of classical simulation, multi-product approximations were introduced to address these problems [19, 22]. Multi-product formulas generalize the approximation-building procedure used to construct  $S_{\chi}$  to allow sums of product formulas. The resulting formulas are simpler since it is easier to construct a Taylor series by adding polynomials than by multiplication alone. Specifically, multi-product formulas only need  $O(k^2)$  exponentials to construct an approximation of U(t) to  $O(t^{2k+1})$ .

We consider multi-product formulas of the form

<span id="page-3-1"></span>
$$M_{k,\chi}(t) = \sum_{q=1}^{k+1} C_q S_{\chi}(t/\ell_q)^{\ell_q},$$
(12)

where the formula is accurate to  $O(t^{2(k+\chi)+1})$ . Here  $\ell_1, \ldots, \ell_{k+1}$  are distinct natural numbers and  $C_1, \ldots, C_{k+1} \in \mathbb{R}$  satisfy  $\sum_{q=1}^{k+1} C_q = 1$ . Explicit expressions for the coefficients  $C_q$  are known for the case  $\chi = 1$  [22]:

<span id="page-3-2"></span>
$$C_q = \prod_{j=\{1,\dots,k+1\}\backslash q} \frac{\ell_q^2}{\ell_q^2 - \ell_j^2}.$$
 (13)

We will show later that the same expressions for  $C_q$  also apply for  $\chi > 1$ .

For classical simulations, the most numerically efficient formulas correspond to  $\ell_q = q$  and  $\chi = 1$ . The simplest example of a multi-product formula is the Richardson extrapolation formula for  $S_1$  [23]:

$$U(t) = \frac{4S_1(t/2)^2 - S_1(t)}{3} + O(t^5). \tag{14}$$

Even though the above expression is non-unitary, it is very close to a unitary operator. In fact, there exists a unitary operator within distance  $O(t^{10})$  of the multi-product formula. In general, Blanes, Casas, and Ros show that if a multi-product formula  $M_{k,\chi}$  is accurate to  $O(t^{2(k+\chi)+1})$  then it is unitary to  $O(t^{4(k+\chi)+2})$  [19]; therefore such formulas are practically indistinguishable from unitary operations in many applications [19, 22].

The principal drawback of these formulas is that they are less numerically stable than Lie–Trotter–Suzuki formulas. Because they involve sums that nearly perfectly cancel, substantial roundoff errors can occur in their computation. Such errors can be mitigated by using high numerical precision or by summing the multi-product formula in a way that minimizes roundoff error.

An additional drawback is that linear combinations of unitary operators are not natural to implement on a quantum computer. Furthermore, our previous discussion alludes to a sign problem for the integrators: the more terms of the multi-product formula that have negative coefficients, the lower the success probability of the implementation of Theorem 3. This sign problem cannot be resolved completely because, as shown by Sheng [24], it is impossible to construct a high-order multi-product formula of the form in (12) without using negative  $C_q$ . Nevertheless, we show that this problem is not fatal and that multi-product formulas can be used to surpass what is possible with previous simulations based on product formulas.

# B. Implementing Multi-Product Formulas Using Quantum Computers

We now discuss how to implement multi-product formulas using quantum computers. The main obstacle is that the multi-product formulas most commonly used in classical algorithms have a value of  $\kappa$  (as defined in Theorem 3) that approaches 1 exponentially quickly as k increases. Thus the probability of successfully implementing such multi-product formulas using Theorem 3 is exponentially small.

Instead, we seek a multi-product formula  $M_{k,\chi}$ , with a large value of  $\kappa$ , such that  $||M_{k,\chi}(\lambda) - U(\lambda)|| \in O(\lambda^{2(k+\chi)+1})$ . Although many choices are possible, we take our multi-product formulas to be of the following form because they yield a large value of  $\kappa$  while consisting of relatively few exponentials.

<span id="page-4-0"></span>**Definition 1.** Let  $k \geq 0$  and  $\chi \geq 1$  be integers,  $\gamma$  a real number such that  $e^{\gamma(k+1)}$  is an integer, and  $S_{\chi}(\lambda)$  a symmetric product formula approximation to  $U(\lambda)$  obeying  $||S_{\chi}(\lambda) - U(\lambda)|| \in O(\lambda^{2\chi+1})$ . Then for any  $t \in \mathbb{R}$  we define the multi-product formula  $M_{k,\chi}(t)$  as

$$M_{k,\chi}(t) := \sum_{q=1}^{k+1} C_q S_{\chi}(t/\ell_q)^{\ell_q}$$
(15)

where

<span id="page-4-2"></span>
$$\ell_q := \begin{cases} q & \text{if } q \le k \\ e^{\gamma(k+1)} & \text{if } q = k+1 \end{cases}$$
 (16)

and

<span id="page-4-1"></span>
$$C_{q} := \begin{cases} \frac{q^{2}}{q^{2} - e^{2\gamma(k+1)}} \prod_{\substack{j \neq q \\ q^{2} - j^{2}}}^{k} & \text{if } q \leq k \\ \prod_{j=1}^{k} \frac{e^{2\gamma(k+1)}}{e^{2\gamma(k+1)} - j^{2}} & \text{if } q = k+1. \end{cases}$$

$$(17)$$

We choose these values of  $\ell_q$  because for sufficiently large  $\gamma$  they guarantee that  $C_{k+1}$  is much larger in absolute value than all other coefficients. This ensures a high success probability in Theorem 3 because  $\kappa \geq |C_{k+1}|/\sum_{q=1}^k |C_q|$  is large if  $|C_{k+1}|$  exceeds the sum of all other  $|C_q|$ .

The following lemma shows that  $M_{k,\chi}$  is a higher-order integrator than  $S_k$ . Quantitative error bounds are proven in the next section.

<span id="page-4-3"></span>**Lemma 4.** Let  $M_{k,\chi}$  be a multi-product formula constructed according to Definition 1. Then for  $\lambda \ll 1$  we have

$$||M_{k,\chi}(\lambda) - U(\lambda)|| \in O(\lambda^{2(k+\chi)+1}).$$
(18)

*Proof.* We follow the steps outlined in Chin's proof for the case where  $\chi=1$  [22]. As shown in [19], a sufficient condition for a multi-product formula of the form  $M_{k,\chi}(\lambda)=\sum_p C_p S_\chi(\lambda/\ell_p)^{\ell_p}$  to satisfy  $\|U(\lambda)-M_{k,\chi}(\lambda)\|\in O(\lambda^{2(k+\chi)+1})$  is

for C to satisfy the following matrix equation:

$$\begin{pmatrix}
1 & 1 & 1 & \cdots & 1 \\
\ell_1^{-2\chi} & \ell_2^{-2\chi} & \ell_3^{-2\chi} & \cdots & \ell_{k+1}^{-2\chi} \\
\ell_1^{-2\chi-2} & \ell_2^{-2\chi-2} & \ell_3^{-2\chi-2} & \cdots & \ell_{k+1}^{-2\chi-2} \\
\vdots & \vdots & \vdots & \ddots & \vdots \\
\ell_1^{-2(k+\chi-1)} & \ell_2^{-2(k+\chi-1)} & \ell_3^{-2(k+\chi-1)} & \cdots & \ell_{k+1}^{-2(k+\chi-1)}
\end{pmatrix}
\begin{pmatrix}
C_1 \\
C_2 \\
C_3 \\
\vdots \\
C_{k+1}
\end{pmatrix} = \begin{pmatrix}
1 \\
0 \\
0 \\
\vdots \\
0
\end{pmatrix}.$$
(19)

This ensures that the sum of all  $C_q$  is 1 and the coefficients of all the error terms in the multi-product formula are zero up to  $O(\lambda^{2(k+\chi)-1})$ . Denoting the matrix in the above equation by V, the vector C is then the first column of  $V^{-1}$ . The matrix V is a generalized Vandermonde matrix, which can be explicitly inverted [25]. The entries of C correspond to (13), which coincides with the values of  $C_q$  given in (17) for the values of  $\ell_q$  in (16). Therefore the result of [19] shows that these values of  $C_q$  extrapolate an  $O(\lambda^{2\chi+1})$  symmetric product formula into an  $O(\lambda^{2(k+\chi)+1})$  multi-product formula, as claimed.

The following upper bound on the coefficients of the multi-product formula will be useful.

<span id="page-5-5"></span>**Lemma 5.** If  $e^{2\gamma(k+1)} \ge 2k^2$ , then for all  $1 \le q < k+1$ , the coefficients  $C_q$  from Definition 1 satisfy

<span id="page-5-3"></span>
$$|C_q| \le \sqrt{2} k^{3/2} e^{2k(1 + \log(\eta)/2 - \gamma)}$$
 (20)

where

<span id="page-5-4"></span>
$$\eta := \max_{\lambda \in [0,1)} \frac{\lambda^2}{(1+\lambda)^{1+\lambda}(1-\lambda)^{1-\lambda}} \approx 0.3081. \tag{21}$$

*Proof.* For any q < k + 1, Definition 1 gives

$$C_{q} = \frac{q^{2}}{q^{2} - e^{2\gamma(k+1)}} \prod_{j \in \{1, \dots, k\} \setminus q} \frac{q^{2}}{q^{2} - j^{2}}$$

$$= \frac{q^{2}}{q^{2} - e^{2\gamma(k+1)}} \prod_{j \in \{1, \dots, k\} \setminus q} \frac{q^{2}}{(q+j)(q-j)}$$

$$= \frac{q^{2}}{q^{2} - e^{2\gamma(k+1)}} q^{2(k-1)} \frac{2q \cdot q!}{(q+k)!} \frac{(-1)^{k-q}}{(q-1)!(k-q)!}$$

$$= \frac{(-1)^{k-q} 2q^{2k+2}}{(k+q)!(k-q)!(q^{2} - e^{2\gamma(k+1)})}.$$
(22)

Using  $e^{2\gamma(k+1)} \ge 2k^2 \ge 2q^2$ , we have the bound

<span id="page-5-1"></span>
$$|C_q| \le \frac{4q^{2k+2}e^{-2\gamma(k+1)}}{(k+q)!(k-q)!}. (23)$$

We proceed by using the lower bound [26]

<span id="page-5-2"></span><span id="page-5-0"></span>
$$n! \ge \sqrt{2\pi n} \, n^n e^{-(n+1/13)}. \tag{24}$$

We will use this bound differently to estimate  $|C_q|$  for the cases where q < k and q = k. Using (24), we lower bound both factorial functions in (23) as follows:

$$|C_q| \le \frac{4q^{2k+2}e^{-2\gamma(k+1)+2k+2/13}}{2\pi\sqrt{k}(k+q)^{k+q}(k-q)^{k-q}}.$$
(25)

Here we have used the fact that  $\sqrt{(k+q)(k-q)} \ge \sqrt{k}$  for  $q \le k-1$ . Now introduce a parameter  $\lambda$  such that  $q = k\lambda$ . We simplify (25) using this substitution and divide the numerator and denominator of (25) by  $k^{2k}$  to find

$$|C_q| \le \frac{2k^{3/2}e^{2k(1-\gamma)-2\gamma+2/13}}{\pi} \left(\frac{\lambda^2}{(1+\lambda)^{1+\lambda}(1-\lambda)^{1-\lambda}}\right)^k$$

$$\le \frac{2k^{3/2}e^{2k(1-\gamma)-2\gamma+2/13}}{\pi} \eta^k.$$
(26)

We then simplify this expression and find that

<span id="page-6-0"></span>
$$|C_q| \le \frac{2k^{3/2}e^{2k(1+\log(\eta)/2-\gamma)}}{\pi e^{2\gamma-2/13}},$$
 (27)

which for  $\gamma > 0$  is bounded above by

$$|C_q| \le k^{3/2} e^{2k(1 + \log(\eta)/2 - \gamma)} < \sqrt{2} k^{3/2} e^{2k(1 + \log(\eta)/2 - \gamma)}.$$
 (28)

Our bound for the case where q = k is found using similar (but simpler) reasoning. We first substitute q = k into (23), use the lower bound in (24) to remove the factorial function, and simplify the result to find

$$|C_k| \le 2k^{3/2}e^{2k(1-\log(2)-\gamma)}/\sqrt{\pi} < \sqrt{2}k^{3/2}e^{2k(1-\log(2)-\gamma)},$$
 (29)

which is less than the value in (28) because  $-0.6931 \approx -\log 2 < \log(\eta)/2 \approx -0.5886$ . Therefore (20) holds for all  $q \leq k$  as required.

The value of  $\gamma$  used in  $M_{k,\chi}$  can be chosen to minimize the probability of a subtraction error. The following lemma relates the value of  $\kappa$  to  $\gamma$ , allowing us to use Theorem 3 to find a value of  $\gamma$  that ensures a sufficiently small probability of a subtraction error.

Henceforth we assume that  $k \ge 1$ . This is because k = 0 corresponds to an ordinary product formula and the bounds that we prove for multi-product formulas can tightened by excluding this case, which is also already well analyzed [11, 18].

<span id="page-6-3"></span>**Lemma 6.** Let  $M_{k,\chi}$  be a multi-product formula as in Definition 1 and let  $\kappa$  be defined for  $M_{k,\chi}$  as in Theorem 3. Then if  $2k^2 \leq e^{2\gamma(k+1)}$  and k > 0, we have

$$\kappa \ge 2^{-1/2} e^{-2k(1 + \log(\eta)/2 - \gamma) - \log(k^{5/2})} \tag{30}$$

where  $\eta$  is defined in (21).

*Proof.* According to Theorem 3, we have  $\kappa = \Sigma_+/\Sigma_-$ , where  $\Sigma_+$  is the sum of all  $C_q$  with positive coefficients and  $\Sigma_-$  is the absolute value of the corresponding negative sum. A lower bound on  $\kappa$  is therefore found by dividing a lower bound on  $\Sigma_+$  by an upper bound on  $\Sigma_-$ .

Using the expression for  $C_q$  from Definition 1, we have

$$C_{k+1} = \prod_{j=1}^{k} \frac{e^{2\gamma(k+1)}}{e^{2\gamma(k+1)} - j^2} = \prod_{j=1}^{k} \frac{1}{1 - j^2 e^{-2\gamma(k+1)}}.$$
 (31)

The denominators on the right hand side of (31) are positive under the assumption that  $2k^2 \leq e^{2\gamma(k+1)}$ , which ensures that  $k^2e^{-2\gamma(k+1)} < 1$  and simplifies the subsequent results of Corollary 7. We also have  $C_{k+1} \geq 1$  because each denominator is less than 1. Since  $C_{k+1} > 0$ , we have  $\Sigma_+ \geq C_{k+1} \geq 1$ , and therefore

<span id="page-6-2"></span><span id="page-6-1"></span>
$$\kappa \ge \frac{1}{\Sigma_{-}}.\tag{32}$$

Next we provide an upper bound for  $\Sigma_{-}$ . Since  $C_{k+1} > 0$ , we have

$$\Sigma_{-} \le \sum_{q=1}^{k} |C_q|. \tag{33}$$

An upper bound for  $\Sigma_{-}$  can then be obtained directly from upper bounds for  $\max_{q < k+1} |C_q|$ . Using Lemma 5, we have

<span id="page-6-4"></span>
$$\Sigma_{-} \le \sum_{q=1}^{k} \sqrt{2} k^{3/2} e^{2k(1 + \log(\eta)/2 - \gamma)} < \sqrt{2} k^{5/2} e^{2k(1 + \log(\eta)/2 - \gamma)}. \tag{34}$$

We substitute this inequality into (32) to obtain

$$\kappa \ge 2^{-1/2} k^{-5/2} e^{-2k(1 + \log(\eta)/2 - \gamma)} \tag{35}$$

as claimed.  $\Box$ 

In fact, the bound of Lemma 6 is nearly tight, in that  $\kappa$  decays exponentially with k if  $\gamma < 1 + \log(\eta)/2$ , as we discuss in more detail below. Thus the success probability of our algorithm decays exponentially if  $\gamma$  is too small. Consequently, we will find that unlike the classical case, our quantum algorithm does not provide poly-logarithmic error scaling.

The following corollary provides a sufficient value of  $\gamma$  to ensure that the probability of our algorithm making a subtraction error is small.

<span id="page-7-1"></span>Corollary 7. Let  $M_{k,\chi}$  be a multi-product formula as in Definition 1, let  $\kappa$  be defined for  $M_{k,\chi}$  as in Theorem 3, and let  $\delta \leq 1$ . Furthermore, suppose k > 0 and

$$\gamma \ge 1 + \frac{\log(\eta)}{2} + \frac{1}{2k} \log\left(\frac{(2k)^{\frac{5}{2}}}{\delta}\right).$$

Then  $P_{-} \leq \delta$  and  $k^2 e^{-2\gamma(k+1)} \leq 1/2$ .

*Proof.* Without loss of generality, we can take  $\kappa \geq 1$  for our subtraction step because  $\sum_q C_q = 1$  and hence  $\kappa = \Sigma_+/\Sigma_- \geq 1$ . This observation and the result of Theorem 3 imply that the probability of failing to perform the subtraction step in our implementation of  $M_{k,\chi}$  satisfies

<span id="page-7-2"></span>
$$P_{-} \le 4/\kappa. \tag{36}$$

Eq. (36) and the bounds on  $\kappa$  in Lemma 6 give  $P_{-} \leq \delta$  provided

<span id="page-7-3"></span>
$$4\sqrt{2}e^{2k(1+\log(\eta)/2-\gamma)+\log(k^{5/2})} \le \delta. \tag{37}$$

We obtain our sufficient value of  $\gamma$  by solving (37) for  $\gamma$ , giving

<span id="page-7-4"></span>
$$\gamma \ge 1 + \log(\eta)/2 + \frac{1}{2k} \log\left(\frac{(2k)^{\frac{5}{2}}}{\delta}\right). \tag{38}$$

Eq. (38) also implies that  $k^2e^{-2\gamma(k+1)} \le 1/2$ . For  $0 < \delta \le 1$  and  $\gamma$  saturating (38), it is easy to see that  $k^2e^{-2\gamma(k+1)}$  is a monotonically decreasing function of k, and therefore achieves its maximum value at k = 1, the smallest possible value of k. We find that  $k^2e^{-2\gamma(k+1)} < 1/2$  at k = 1 for  $\delta = 1$ , and therefore the condition  $k^2e^{-2\gamma(k+1)} \le 1/2$  is automatically implied by our choice of  $\gamma$  in (38).

The value of  $\gamma$  given by Corollary 7 is tight up to  $O(k^{-1} \log k)$ . This is illustrated in Figure 2, which shows  $\kappa$  as a function of k for  $\gamma = \gamma_c := 1 + \log(\eta)/2$  and two slightly perturbed values of  $\gamma$  centered around  $\gamma_c$ . We see that small deviations away from  $\gamma = \gamma_c$  lead to either exponential growth of  $\kappa$  or exponential convergence of  $\kappa$  to 1. Thus our lower bound for  $\gamma$  cannot be significantly improved.

### <span id="page-7-0"></span>IV. ANALYSIS OF SIMULATION AND ERRORS IN MULTI-PRODUCT FORMULAS

The results of the previous section show how  $\kappa$  scales with the number of terms in the multi-product formula used in the simulation. We now expand on these results by bounding the approximation errors incurred by using the multi-product formula. We also present an error correction method to ensure that our implementation fails at most a constant fraction of the time. Our error bounds are established as follows. First, we estimate the error in multi-product formulas that utilize high-order Lie-Trotter-Suzuki formulas. Second, we discuss how these multi-product formulas are implemented. Finally, we estimate the inversion error for the resulting multi-product formulas and bound the average error resulting from a given step.

<span id="page-7-5"></span>**Lemma 8.** Let  $M_{k,k}(\lambda)$  satisfy Definition 1 for evolution time  $\lambda \geq 0$ , let  $|C_q| \leq 2$  for all  $q = 1, \ldots, k+1$ , and let  $h\lambda \leq \frac{3\log(2)}{4mk(5/3)^{k-1}}$ . Then

$$||U(\lambda) - M_{k,k}(\lambda)|| \le (2m(5/3)^{k-1}h\lambda)^{4k+1}.$$
(39)

The proof of Lemma 8 requires upper bounds on the remainder terms of Taylor series expansions. Let  $\mathbf{R}_{\ell}(f)$  denote the remainder term of the Taylor series of a function f truncated at order  $\ell$ . The following lemma bounds the remainder term for an operator exponential.

<span id="page-8-0"></span>![](_page_8_Figure_1.jpeg)

FIG. 2: Scaling of  $\kappa$  with k for three values of  $\gamma$  centered around  $\gamma_c := 1 + \log(\eta)/2$ . The data show that  $\kappa$  approaches 1 polynomially quickly if  $\gamma = \gamma_c$ , whereas a slight increase in  $\gamma$  causes  $\kappa$  to grow exponentially and a slight decrease causes  $\kappa$  to converge to 1 exponentially with k.

<span id="page-8-1"></span>**Lemma 9.** Let  $a_j \in \mathbb{R}$  for j = 1, ..., M and suppose  $||H_j|| \le h$ . Then

$$\left\| \mathbf{R}_{\ell} \left( \prod_{j=1}^{M} e^{-ia_{j}H_{j}t} \right) \right\| \leq \frac{\left( \sum_{j=1}^{M} |a_{j}|ht \right)^{\ell+1}}{(\ell+1)!} \exp \left( \sum_{q=1}^{M} |a_{q}|ht \right).$$
 (40)

*Proof.* Using the triangle inequality and sub-multiplicativity of the norm, we find

$$\left\| \mathbf{R}_{\ell} \left( \prod_{j=1}^{M} e^{-ia_{j}H_{j}t} \right) \right\| = \left\| \mathbf{R}_{\ell} \left( \prod_{j=1}^{M} \left( \sum_{p=0}^{\infty} (-ia_{j}H_{j}t)^{p}/p! \right) \right) \right\|$$

$$\leq \mathbf{R}_{\ell} \left( \prod_{j=1}^{M} \left( \sum_{p=0}^{\infty} (|a_{j}|ht)^{p}/p! \right) \right)$$

$$= \mathbf{R}_{\ell} \left( \exp \left( \sum_{j=1}^{M} |a_{j}|ht \right) \right)$$

$$= \sum_{p=\ell+1}^{\infty} \frac{\left( \sum_{j=1}^{M} |a_{j}|ht \right)^{p}}{p!}$$

$$\leq \frac{\left( \sum_{j=1}^{M} |a_{j}|ht \right)^{\ell+1}}{(\ell+1)!} \exp \left( \sum_{j=1}^{M} |a_{j}|ht \right)$$

$$(42)$$

as claimed.  $\hfill\Box$ 

Now we are ready to prove Lemma 8.

Proof of Lemma 8. Lemma 4 implies that

$$||M_{k,k}(\lambda) - U(\lambda)|| \in O(\lambda^{4k+1}), \tag{43}$$

so the approximation error is entirely determined by the terms of order  $\lambda^{4k+1}$  in  $M_{k,k}$  and U. If we remove the terms in the Taylor series of  $M_{k,k}$  and U that cancel, the remainders,  $\mathbf{R}_{4k}(M_{k,k}(\lambda))$  and  $\mathbf{R}_{4k}(U(\lambda))$ , determine the error via

$$||M_{k,k}(\lambda) - U(\lambda)|| = ||\mathbf{R}_{4k}(M_{k,k}(\lambda)) - \mathbf{R}_{4k}(U(\lambda))||$$

$$\leq ||\mathbf{R}_{4k}(M_{k,k}(\lambda))|| + ||\mathbf{R}_{4k}(U(\lambda))||.$$
(44)

Lemma 9 implies that

<span id="page-9-2"></span><span id="page-9-0"></span>
$$\|\mathbf{R}_{4k}(U(\lambda))\| \le \frac{(mh\lambda)^{4k+1}}{(4k+1)!} e^{mh\lambda} < \left(\frac{4}{3}m(5/3)^{k-1}h\lambda\right)^{4k+1}.$$
(45)

The second inequality in (45) follows from the assumption that  $h\lambda \leq \frac{3\log(2)}{4mk(5/3)^{k-1}}$ , which implies that  $\exp(mh\lambda)/(4k+1)! \leq 2^{3/4}/5! < 1$ .

The definition of  $M_{k,\chi}$  implies

$$\|\mathbf{R}_{4k}(M_{k,k}(\lambda))\| \le \sum_{q=1}^{k+1} |C_q| \|\mathbf{R}_{4k}(S_k(\lambda/\ell_q)^{\ell_q})\|.$$
 (46)

Thus we upper bound  $\|\mathbf{R}_{4k}(S_k(\lambda/p)^p)\|$ . This bound follows similar logic to the bound for  $U(\lambda)$ , but the calculation is slightly more complicated because  $S_k$  is the product of many exponentials. Specifically,

<span id="page-9-1"></span>
$$S_k(\lambda/p) = \prod_{\ell=1}^{2m5^{k-1}} e^{-iH_{j_\ell}q_{k,\ell}\lambda/p},$$
(47)

where  $q_{k,\ell}$  is the ratio between  $\lambda/p$  and the duration of the  $\ell^{\text{th}}$  exponential in  $S_k$ . Lemma 9 gives

$$\|\mathbf{R}_{4k}(S_k(\lambda/p)^p)\| \le \frac{(2m5^{k-1}\max q_{k,\ell}h\lambda)^{4k+1}}{(4k+1)!}e^{2m5^{k-1}\max q_{k,\ell}h\lambda}.$$
(48)

Using the upper bound  $q_{k,\ell} \leq 2k/3^k$  from Appendix A of [20], we have

<span id="page-9-4"></span>
$$\|\mathbf{R}_{4k}(S_k(\lambda/p)^p)\| \le \frac{(\frac{4}{3}mk(5/3)^{k-1}h\lambda)^{4k+1}}{(4k+1)!}e^{\frac{4}{3}mk(5/3)^{k-1}h\lambda}.$$
(49)

This bound can be simplified using  $(4k+1)! \ge k^{4k+1}5!$  for  $k \ge 1$  (a consequence of (24)) and the hypothesis that  $\frac{4}{3}mk(5/3)^{k-1}h\lambda \le \log(2)$ , giving

$$\|\mathbf{R}_{4k}(S_k(\lambda/p)^p)\| \le \frac{2}{5!} \left(\frac{4}{3}m(5/3)^{k-1}h\lambda\right)^{4k+1}.$$
 (50)

Using this result and the assumption that  $|C_q| \leq 2$  in (46) gives

<span id="page-9-3"></span>
$$\|\mathbf{R}_{4k}(M_{k,k}(\lambda))\| \le \frac{8(k+1)}{5!} \left(\frac{4}{3}m(5/3)^{k-1}h\lambda\right)^{4k+1}.$$
 (51)

Combining (44), (45), and (51) gives

$$||U(\lambda) - M_{k,k}(\lambda)|| \le \left(1 + \frac{8(k+1)}{5!}\right) \left(\frac{4}{3}m(5/3)^{k-1}h\lambda\right)^{4k+1}$$

$$\le (2m(5/3)^{k-1}h\lambda)^{4k+1},$$
(52)

proving the lemma.  $\Box$ 

A useful consequence of performing  $M_{k,k}$  using a single subtraction step is that if a subtraction error occurs, the simulator performs the operation

<span id="page-10-0"></span>
$$E_k(\lambda) \colon |\psi\rangle \mapsto \frac{\sum_q |C_q| S_k(\lambda/\ell_q)^{\ell_q} |\psi\rangle}{\|\sum_q |C_q| S_k(\lambda/\ell_q)^{\ell_q} |\psi\rangle\|}.$$
 (53)

This error operation can be approximately corrected because, as Blanes et al. proved [19, Theorem 1],

<span id="page-10-2"></span><span id="page-10-1"></span>
$$E_k(-\lambda)E_k(\lambda) = \mathbb{1} + O(\lambda^{4k+2}). \tag{54}$$

Since the coefficients  $|C_q|$  are all positive, Theorem 3 shows that the approximate correction operation  $E_k(-\lambda)$  can be performed with success probability close to 1 provided  $\Delta$  is small. The following lemma states that the error incurred by approximately correcting subtraction errors is at most equal to our upper bound for the approximation error for  $M_{k,k}(\lambda)$ .

<span id="page-10-3"></span>**Lemma 10.** Let  $E_k(\lambda)$  act as in (53), where  $C_q$  and  $\ell_q$  are given in Definition 1. If  $2mk(5/3)^{k-1}h\lambda \leq 1/2$ , then

$$\max_{|\psi\rangle} \|(\mathbb{1} - E_k(-\lambda)E_k(\lambda))|\psi\rangle\| \le (2mk(5/3)^{k-1}h\lambda)^{4k+2}.$$
 (55)

*Proof.* By (53) and (54),

$$\max_{|\psi\rangle} \|(\mathbb{1} - E_k(-\lambda)E_k(\lambda))|\psi\rangle\| = \max_{|\psi\rangle} \|\mathbf{R}_{4k+1}(E_k(-\lambda)E_k(\lambda)|\psi\rangle)\|$$

$$\leq \frac{\|\mathbf{R}_{4k+1}\left(\sum_p \sum_q |C_p||C_q|S_k(-\lambda/p)^p S_k(\lambda/q)^q\right)\|}{\min_{|\phi\rangle} \|\sum_p |C_p|S_k(\lambda/\ell_p)^{\ell_p}|\phi\rangle\|^2}.$$
(56)

We then follow the same reasoning used in the proof of Lemma 9. By the triangle inequality, the norm of the remainder of a Taylor series is upper bounded by the sums of the norms of the individual terms in the remainder. This can be bounded by replacing the exponent of each exponential in  $S_k$  with its norm. We use similar reasoning to that used in (49) to find

$$\|\mathbf{R}_{4k+1} \left( S_k(-\lambda/p)^p S_k(\lambda/q)^q \right) \| \le \mathbf{R}_{4k+1} \left( e^{\frac{8}{3}mk(5/3)^{k-1}h\lambda} \right),$$
 (57)

so the numerator of (56) satisfies

$$\left\| \mathbf{R}_{4k+1} \left( \sum_{p} \sum_{q} |C_{p}| |C_{q}| S_{k} (-\lambda/p)^{p} S_{k} (\lambda/q)^{q} \right) \right\| \leq \sum_{p} \sum_{q} |C_{p}| |C_{q}| \mathbf{R}_{4k+1} \left( e^{\frac{8}{3}mk(5/3)^{k-1}h\lambda} \right)$$

$$\leq \|C\|_{1}^{2} \frac{\left( \frac{8}{3}mk(5/3)^{k-1}h\lambda \right)^{4k+2} e^{\frac{8}{3}mk(5/3)^{k-1}h\lambda}}{(4k+2)!}$$
(58)

where C is a vector with entries  $C_p$ , so  $||C||_1 = \sum_p |C_p|$ . Our assumptions imply  $\frac{8}{3}mk(5/3)^{k-1}h\lambda \leq 2/3 < \log(2)$ , so

$$\left\| \mathbf{R}_{4k+1} \left( \sum_{p} \sum_{q} |C_{p}| |C_{q}| S_{k} (-\lambda/p)^{p} S_{k} (\lambda/q)^{q} \right) \right\| \leq \|C\|_{1}^{2} \frac{2 \left( \frac{8}{3} m k (5/3)^{k-1} h \lambda \right)^{4k+2}}{(4k+2)!}$$

$$\leq \|C\|_{1}^{2} \frac{2 \left( \frac{2e}{3} m (5/3)^{k-1} h \lambda \right)^{4k+2}}{\sqrt{12\pi} e^{25/26}}, \tag{59}$$

where the last inequality results from using Stirling's approximation as given in (24). The denominator of (56) can be lower bounded as follows:

$$\min_{|\phi\rangle} \left\| \sum_{p} |C_{p}| S_{k}(\lambda/\ell_{p})^{\ell_{p}} |\phi\rangle \right\| = \min_{|\phi\rangle} \left\| \sum_{p} |C_{p}| (e^{-iHt} - (e^{-iHt} - S_{k}(\lambda/\ell_{p})^{\ell_{p}})) |\phi\rangle \right\| 
\geq \|C\|_{1} \left( 1 - \max_{p} \|e^{-iHt} - S_{k}(\lambda/\ell_{p})^{\ell_{p}}\| \right) 
= \|C\|_{1} (1 - \|e^{-iHt} - S_{k}(\lambda)\|).$$
(60)

Since  $2mk(5/3)^{k-1}h\lambda \le 1/2 < 3/(4\sqrt{2})$ , Theorem 3 of [20] implies that  $||e^{-iHt} - S_k(\lambda)|| \le 2(2mk(5/3)^{k-1}h\lambda)^{2k+1}$ . Using  $2mk(5/3)^{k-1}h\lambda \le 1/2$  and  $k \ge 1$  we have that

$$||e^{-iHt} - S_k(\lambda)|| \le \frac{1}{4},$$
 (61)

implying

$$\min_{|\phi\rangle} \left\| \sum_{p} |C_p| S_k(\lambda/\ell_p)^{\ell_p} |\phi\rangle \right\| \ge \frac{3}{4} \|C\|_1. \tag{62}$$

Combining this with our upper bound on the numerator gives

$$\max_{|\psi\rangle} \|(\mathbb{1} - E_k(-\lambda)E_k(\lambda))|\psi\rangle\| \le \frac{2(4/3)^2}{\sqrt{12\pi}e^{25/26}} \left(\frac{2e}{3}m(5/3)^{k-1}h\lambda\right)^{4k+2}$$

$$\le (2m(5/3)^{k-1}h\lambda)^{4k+2}$$
(63)

as claimed.  $\Box$ 

We simulate U(t) using r iterations of  $M_{k,k}(t/r)$  for some sufficiently large r. Our next step is to combine Lemma 8 and Lemma 10 to find upper bounds on r such that U(t) is approximated to within some fixed error. We take  $\delta = 1/2$ , i.e., we accept a maximum failure probability of 1/2 for each multi-product formula. We then sum the cumulative errors and use the Chernoff bound to show that, with high probability, the simulation error is at most  $\epsilon$ . These results are summarized in the following lemma.

<span id="page-11-1"></span>**Lemma 11.** Let  $M_{k,k}$  be a multi-product formula given by Definition 1 with  $|C_q| \le 2$  for all  $q \le k+1$ . Let  $\gamma$  be chosen as in Corollary 7 with  $\delta = 1/2$  and let the integer r satisfy

<span id="page-11-0"></span>
$$r \ge \frac{(2m(5/3)^{k-1}ht)^{1+1/4k}}{(\epsilon/5)^{1/4k}} \tag{64}$$

for  $\epsilon \leq mhtk^{-4k}$ . Then a quantum computer can approximately implement U(t) as  $M_{k,k}(t/r)^r$  with error at most  $\epsilon$  and with probability at least  $1 - e^{-r/13}$ , assuming that no addition errors occur during the simulation, while utilizing no more than 5r subtraction attempts and approximate inversions.

*Proof.* First we bound the probability of successfully performing the subtraction steps given a fixed maximum number of attempts. We simplify our analysis by assuming that the simulation uses exactly 3r subtractions, corresponding to the worst-case scenario in which 2r inversions are used. We want to find the probability that a randomly chosen sequence of subtractions contains at least r successes, correctly implementing the multi-product formula. The probability that a sequence is unsuccessful is exponentially small in r because for  $\delta = 1/2$ , the mean number of failures is  $\mu = 3r/2$ , which is substantially smaller than our tolerance of 2r failures. By the Chernoff bound, the probability of having more than 2r failures satisfies

$$\Pr(X > 2r) \le e^{-\mu((1+\alpha)\log(1+\alpha) - \alpha)} < e^{-r/13},\tag{65}$$

where  $1 + \alpha = 2r/\mu = 4/3$ .

If we attempt the subtraction steps in our protocol 3r times and fail 2r times, then 5r subtractions and approximate inversions must be performed, because every failure requires an approximate inversion. We bound the resulting error using Lemma 8, Lemma 10, and the subadditivity of errors. These lemmas apply because the requirement  $\frac{4}{3}mk(5/3)^{k-1}ht/r \leq \log(2)$  is implied by our choice of r and the assumption  $\epsilon \leq mhtk^{-4k}$ . By this argument, the simulation error satisfies

$$\|\tilde{M}_{k,k}(t/r)^r - U(t)\| \le 5r(2m(5/3)^{k-1}ht/r)^{4k+1}$$
(66)

with probability at least  $1 - e^{-r/13}$ , where  $\tilde{M}_{k,k}(t/r)$  denotes the operation performed by our non-deterministic algorithm for the multi-product formula  $M_{k,k}$ . The assumption  $\epsilon \leq mhtk^{-4k}$  and the value of r from (64) imply that  $\|\tilde{M}_{k,k}(t/r)^r - U(t)\| \leq \epsilon$  as required.

Lemma 11 assumes an error tolerance of at most  $mhtk^{-4k}$ , which may appear to be very small. However, our ultimate simulation scheme has  $k \in O(\sqrt{\log(mht/\epsilon)})$ , so in fact the error tolerance is modest.

Now we are ready to prove a key lemma that provides bounds on the number of exponentials used by the simulation in the realistic scenario where both addition and subtraction errors may occur. Our main result, Theorem 1, follows as a simple consequence.

<span id="page-12-0"></span>**Lemma 12.** Let  $M_{k,k}$  be a multi-product formula for  $H = \sum_{j=1}^m H_j$  as in Definition 1, with  $k \geq 1$ . Let  $\tilde{M}_{k,k}$  be the implementation of  $M_{k,k}$  described above. Let  $\epsilon$  be a desired error tolerance and let  $\beta$  be a desired upper bound on the failure probability of the algorithm. Then there is a simulation of  $U(t) = e^{-iHt}$  that has error at most  $\epsilon$  with probability at least  $1 - \beta$  using

<span id="page-12-1"></span>
$$N_{\text{exp}} \le 1000m5^{k-1}k^{9/4}e^{(1+\log(\eta)/2)k}r\tag{67}$$

exponentials of the form  $e^{-iH_jt}$ , where

1.  $\gamma = \frac{1}{k} \log \left[ \exp([1 + \log(\eta)/2 + \frac{1}{2k} \log(2(2k)^{5/2})]k) \right],$ 

2.  $\tilde{\epsilon} = \min(1, \epsilon, \beta, mhtk^{-4k}),$ 

3. 
$$r = \left[ \max \left\{ \frac{(4m(5/3)^{k-1}ht)^{1+1/4k}}{(\tilde{\epsilon}/5)^{1/4k}}, 13\log(2/\beta) \right\} \right].$$

Proof. We approximate U(t) as a product of r multi-product formulas, each implemented using the operation  $\tilde{M}_{k,k}$ . We can suppose that the sequence of r multi-product formulas is implemented using at most 5r subtraction and inversion steps according to Lemma 11. As k unitary operations are combined in each step, we must implement a total of 5rk unitary operations. Definition 1 implies that each of these unitaries is composed of at most  $e^{\gamma(k+1)}$  Suzuki integrators  $U_q$ . Each  $U_q$  is a product of  $2m5^{k-1}$  exponentials of elements from  $\{H_j\}$ . Thus, if the algorithm succeeds after performing this maximum number of subtractions and inversions, we have

$$N_{\text{exp}} \le 10m5^{k-1}ke^{\gamma(k+1)}r$$

$$\le 10m5^{k-1}k(2^{11/4}e^2k^{5/4}e^{(1+\log(\eta)/2)k}+1)r$$

$$< 1000m5^{k-1}k^{9/4}e^{(1+\log(\eta)/2)k}r$$
(68)

where we have used  $\gamma \leq 2$  and  $e^{\gamma k} \leq 2(2^{7/4}k^{5/4}e^{k(1+\log(\eta)/2)})$ . Equation (67) then follows by substituting the value of r assumed by the lemma, which guarantees that the simulation error is less than  $\epsilon$  when the simulation is successful because it exceeds the value of r from Lemma 11. We choose r to be larger because it simplifies our results and guarantees that the probability of an addition error is at most  $\tilde{\epsilon}/2$ .

Lemma 11 requires  $C_q \leq 2$ , which we have not explicitly assumed. Substituting the above value of  $\gamma$  into the upper bound for  $\Sigma_{-}$  in (34) shows that  $\sum_{q=1}^{k} |C_q| \leq 1$ , so  $|C_q| \leq 1$  for all  $q = 1, \ldots, k$ . Our multi-product formula satisfies  $\sum_{q} C_q = 1$ , so our choice of  $\gamma$  ensures  $C_{k+1} \leq 2$ . Thus  $C_q \leq 2$  for all q.

Lemma 11 implies that the probability of the simulation failing due to too many subtraction errors is at most  $e^{-r/13}$ . However, it does not address the possibility of the algorithm failing due to addition errors. There are at most 5r addition steps, so by Theorem 3 and the union bound, the probability of an addition error is at most

<span id="page-12-3"></span><span id="page-12-2"></span>
$$5rP_{+} \le \frac{5\Delta^{2}kr}{4}.\tag{69}$$

By the definition of  $\Delta$  in Theorem 3,

$$\Delta = \left\| \max_{q,q'} \mathbf{R}_{2k} \left( S_k(t/k_q r)^{k_q} - S_k(t/k_{q'} r)^{k_{q'}} \right) \right\|. \tag{70}$$

Using Lemma 9 (similarly as in (49)), the triangle inequality, and  $\frac{4}{3}mk(5/3)^{k-1}ht/r \leq \log(2)$ , we have

$$\Delta \le 4 \frac{\left(\frac{4}{3}mk(5/3)^{k-1}ht/r\right)^{2k+1}}{(2k+1)!}.\tag{71}$$

Substituting the assumed value of r into (71) gives

$$\Delta \le \frac{20k^{2k+1}}{(2k+1)!3^{2k+1}} \left(\frac{\tilde{\epsilon}}{4m(5/3)^{k-1}ht}\right)^{\frac{1}{2} + \frac{1}{4k}}.$$
(72)

Substituting this bound into (69) and using (24), we find that the total probability of an addition error is at most

$$\frac{20k^{4k+3}\tilde{\epsilon}}{((2k+1)!)^23^{4k+2}} \left(\frac{\tilde{\epsilon}}{4mk(5/3)^{k-1}ht}\right)^{1/4k} \le \frac{20k\tilde{\epsilon}}{6\pi(6/e)^{4k+2}e^{-2/13}} \left(\frac{\tilde{\epsilon}}{4mk(5/3)^{k-1}ht}\right)^{1/4k}.$$
 (73)

<span id="page-13-0"></span>

Since  $\tilde{\epsilon} \leq mhtk^{-4k}$ , this implies

$$P_{+} \le \frac{20\tilde{\epsilon}}{6\pi(6/e)^{4k+2}e^{-2/13}} \left(\frac{1}{4k(5/3)^{k-1}}\right)^{1/4k} < \frac{\tilde{\epsilon}}{130} < \frac{\tilde{\epsilon}}{2}.$$
 (74)

Here the second inequality follows from the first by substituting k = 1, since the middle expression is a monotonically decreasing function of k.

The total probability of success  $P_s$  satisfies

$$P_s \ge 1 - \frac{\tilde{\epsilon}}{2} - e^{-r/13}.\tag{75}$$

Using  $r \geq 13 \log(2/\beta)$  and  $\tilde{\epsilon} \leq \beta$ , we find  $P_s \geq 1 - \beta$  as claimed.

As in [11], there is a tradeoff between the exponential improvement in the accuracy of the formula and the exponential growth of  $M_{k,k}$  with k. To see this, note that apart from terms that are bounded above by a constant function of k,  $N_{\text{exp}}$  is the product of two terms:

$$N_{\text{exp}} \in O\left(\left[m^2 k^{9/4} e^{(1+\log(\eta)/2 + \log(25/3))k}\right] \left[mht/\tilde{\epsilon}\right]^{1/4k}\right)$$
 (76)

$$\in O\left(\left[m^2k^{9/4}e^{2.54k}\right]\left[\frac{mht}{\min(\epsilon,\beta)}\right]^{1/4k}\right).$$
(77)

Here we have not included the  $O(\log(1/\beta))$  term from r because  $\log(1/\beta) \in O(1/\beta)^{1/4k}$ . For comparison, the results of [11] and [20] have the following complexities:

$$N_{\text{exp}} \in O\left(\left[m^2 e^{3.22k}\right] \left[mht/\epsilon\right]^{1/2k}\right),\tag{78}$$

$$N_{\text{exp}} \in O\left(\left[m^2 k e^{2.13k}\right] \left[mht/\epsilon\right]^{1/2k}\right),\tag{79}$$

respectively. The tradeoff between accuracy and complexity as a function of k is more favorable in our setting than in either of these approaches. Finally, we give a detailed analysis of the tradeoff.

*Proof of Theorem 1.* Neglecting polynomially large contributions in (76), we see that the dominant part of (76) is

<span id="page-13-1"></span>
$$e^{(1+\log(\eta)/2+\log(25/3))k+\frac{1}{4k}\log(mht/\tilde{\epsilon})}$$
 (80)

It is natural to choose k to minimize (80). The minimum is achieved by taking  $k = k_{\text{opt}}$ , where

$$k_{\text{opt}} = \left[ \frac{1}{2} \sqrt{\frac{\log(mht/\tilde{\epsilon})}{1 + \log(\eta)/2 + \log(25/3)}} \right] \approx 0.3142 \sqrt{\log(mht/\tilde{\epsilon})}.$$
 (81)

Using this k, we find that

<span id="page-13-2"></span>
$$N_{\text{exp}} \in O\left(k_{\text{opt}}^{9/4} m^2 h t e^{1.6\sqrt{\log(mht/\tilde{\epsilon})}}\right).$$
 (82)

We have  $\tilde{\epsilon} = \min(1, \epsilon, \beta, mhtk^{-4k})$ , so  $\tilde{\epsilon}$  depends implicitly on k. However, we now show that this term can be neglected in the limit of large  $mht/\tilde{\epsilon}$ . In this limit, we have

$$\frac{k_{\text{opt}}^{4k_{\text{opt}}}}{mht} \in O\left(\frac{\log(mht/\tilde{\epsilon})^{0.16\sqrt{\log(mht/\tilde{\epsilon})}}}{mht}\right) \subset o(1/\tilde{\epsilon}). \tag{83}$$

The above follows since  $\lim_{x\to\infty} \log(x)^{c\sqrt{\log(x)}}/x = 0$  for any c > 0. Correspondingly,  $mhtk_{\text{opt}}^{-4k_{\text{opt}}} \in \omega(\tilde{\epsilon})$ . We therefore conclude that this term can be neglected asymptotically and that  $\tilde{\epsilon} \in \Omega(\epsilon)$ , so we can replace  $\tilde{\epsilon}$  with  $\epsilon$  asymptotically. The result then follows by substituting  $k_{\text{opt}}$  into (82) and dropping all poly-logarithmic factors.

The parameters  $\epsilon$  and  $\beta$  can be decreased to improve the simulation fidelity and success probability, respectively. The cost of such an improvement is relatively low, although it is not poly-logarithmic in  $1/\epsilon$  and  $1/\beta$ . If the initial state of a simulation can be cheaply prepared and the result of the computation can be easily checked, it may be preferable to use large values of  $\epsilon$  and  $\beta$  and repeat the simulation an appropriate number of times. Then the Chernoff bound implies that a logarithmic number of iterations is sufficient to achieve success with high probability. However, this may not be possible if the simulation is used as a subroutine in a larger algorithm (e.g., as in [6]).

### <span id="page-14-0"></span>V. CONCLUSIONS

We have presented a new approach to quantum simulation that implements Hamiltonian dynamics using linear combinations, rather than products, of unitary operators. The resulting simulation gives better scaling with the simulation error  $\epsilon$  than any previously known algorithm and scales more favorably with all parameters than simulation methods based on product formulas. Aside from the quantitative improvement to simulation accuracy, this work provides a new way to address the errors that occur in quantum algorithms. Specifically, our work shows that approximation errors can be reduced by coherently averaging the results of different approximations. It is common to perform such averages in classical numerical analysis, and we hope that the techniques presented here may have applications beyond quantum simulation.

It remains an open problem to further improve the performance of quantum simulation as a function of the error tolerance  $\epsilon$ . In particular, we would like to determine whether there is a simulation of n-qubit Hamiltonians with complexity poly $(n, \log \frac{1}{\epsilon})$ . Classical simulation algorithms based on multi-product formulas achieve scaling polynomial in  $\log \frac{1}{\epsilon}$ , but they are necessarily inefficient as a function of the system size. Our algorithms fail to provide such favorable scaling in  $\frac{1}{\epsilon}$  due to the sign problem discussed in Section III. A possible resolution to this problem could be attained by finding multi-product formulas with only positive coefficients and backward timesteps. Such formulas are not forbidden by Sheng's Theorem [24] since that result only applies to multi-product formulas that are restricted to use forward timesteps [18]. New approximation-building methods might use backward timesteps to give multi-product formulas that are easier to implement with our techniques. Conversely, a proof that Hamiltonian simulation with poly $(n, \log \frac{1}{\epsilon})$  elementary operations is impossible would also show that Lie–Trotter–Suzuki and multi-product formulas with positive coefficients cannot be constructed with polynomially many exponentials, answering an open question in numerical analysis.

Finally, we have focused on the case of time-independent Hamiltonian evolution. One can consider multi-product formulas that are adapted to handle time-dependent evolution, as discussed in [27]. It is nontrivial to use such formulas to generalize our results to the time-dependent case because of difficulties that arise when the Hamiltonian is not a sufficiently smooth function of time. Further investigation of these issues could lead to developments in numerical analysis as well as quantum computing.

### Acknowledgments

This work was supported in part by MITACS, NSERC, the Ontario Ministry of Research and Innovation, QuantumWorks, and the US ARO/DTO.

# <span id="page-14-1"></span>Appendix A: Optimality of the linear combination procedure

The goal of this appendix is to show that no protocol for implementing linear combinations of unitary operations in a large family of such protocols can have failure probability less than

$$\frac{4\kappa}{(\kappa+1)^2},\tag{A1}$$

where  $\kappa$  is defined in Theorem 3. Specifically, we consider protocols of the form shown in Figure 3. Our result shows that the protocol of Theorem 3 is optimal among such all protocols in the limit of small  $\Delta$  (i.e., when the unitary operations being combined are all similar).

**Theorem 13.** Any protocol for implementing  $V = \sum_{q=0}^{k} C_q U_q$  using a circuit of the form of Figure 3 must fail with probability at least  $4\kappa/(\kappa+1)^2$ .

*Proof.* For convenience, we take k to be an integer power of 2. We can generalize the subsequent analysis to address the case where k+1 is not a power of 2 by replacing k+1 by  $k'+1=2^{\lceil \log_2(k+1) \rceil}$  and taking  $C_p=0$  for p>k.

<span id="page-15-0"></span>![](_page_15_Picture_1.jpeg)

FIG. 3: A general circuit for implementing a linear combination of k+1 unitary operators using unitary operations A and B. We assume for simplicity that k+1 is an integer power of 2. This circuit corresponds to preparing the ancilla states in an arbitrary state (specified by A) and measuring them in an arbitrary basis (specified by B).

Observe that the circuit in Figure 3 acts as follows:

$$|0^{\log_2 k}\rangle|\psi\rangle \mapsto \sum_{m=0}^k A_{m,0}|m\rangle|\psi\rangle$$

$$\mapsto \sum_m A_{m,0}|m\rangle U_m|\psi\rangle$$

$$\mapsto \sum_{n,m} B_{n,m} A_{m,0}|n\rangle U_m|\psi\rangle. \tag{A2}$$

Furthermore, we can modify B to include a permutation such that desired transformation occurs when the first register is measured to be zero. (Orthogonality prevents us from having more than one successful outcome, as we show below.) The implementation is successful if there exists a constant K > 0 such that

<span id="page-15-1"></span>
$$B_{0,m}A_{m,0} = KC_m \tag{A3}$$

for all m.

Our goal is to maximize the success probability, which is equivalent to maximizing K over all choices of the unitary operations A and B satisfying (A3). We can drop the implicit normalization of the matrix elements of B and A by defining coefficients  $b_{0,m}$  and  $a_{m,0}$  such that

$$\frac{b_{0,m}}{\sqrt{\sum_{j}|b_{0,j}|^2}} := B_{0,m} \tag{A4}$$

$$\frac{a_{m,0}}{\sqrt{\sum_{j}|a_{j,0}|^2}} := A_{m,0}. \tag{A5}$$

Using these variables, we have

$$|KC_m| = \frac{|b_{0,m}a_{m,0}|}{\sqrt{(\sum_j |a_{j,0}|^2)(\sum_j |b_{0,j}|^2)}} \le \frac{|b_{0,m}a_{m,0}|}{\sum_j |a_{j,0}b_{0,j}|} = \frac{|C_m|}{\sum_j |C_j|},\tag{A6}$$

where the bound follows from the Cauchy-Schwarz inequality. This bound is tight because it can be saturated by taking  $a_{m,0} = b_{0,m} = \sqrt{C_m}$ . The probability of successfully implementing the multi-product formula is

$$1 - P_{-} = \left\| \sum_{j} K C_{j} U_{j} |\psi\rangle \right\|^{2} \le \left( \frac{\sum_{j} C_{j}}{\sum_{j} |C_{j}|} \right)^{2} = \left( \frac{\Sigma_{+} - \Sigma_{-}}{\Sigma_{+} + \Sigma_{-}} \right)^{2}, \tag{A7}$$

where  $\Sigma_{+}$  and  $\Sigma_{-}$  are defined in Lemma 6. We have  $\kappa := \Sigma_{+}/\Sigma_{-}$ , so

$$1 - P_{-} \le \left(\frac{\kappa - 1}{\kappa + 1}\right)^{2},\tag{A8}$$

which implies that the failure probability satisfies  $P_{-} \geq 4\kappa/(\kappa+1)^2$  as claimed.

It remains to see why it suffices to consider a single successful measurement outcome. In principle, we could imagine that many different measurement outcomes lead to a successful implementation of V. Assume that there exists a measurement outcome  $v \neq 0^{\log_2 k}$  such that the protocol also gives the same multi-product formula on outcome v. If both outcomes are successful then, up to a constant multiplicative factor, the coefficients of each  $U_q$  must be the same. This occurs if there exists a constant  $\Gamma \neq 0$  such that for all q,

$$B_{0,q}A_{q,0} = \Gamma B_{v,q}A_{q,0},\tag{A9}$$

i.e., if  $B_{0,q} = \Gamma B_{v,q}$  (note that  $A_{q,0}$  must be nonzero provided  $C_q \neq 0$ ). This is impossible because B is unitary and hence its columns are orthonormal. Consequently, we cannot obtain the same multi-product formula from different measurement outcomes.

The above proof implicitly specifies an optimal protocol for implementing linear combinations of unitaries. However, we do not use this protocol in Theorem 3 because it is difficult to perform a correction if the implementation fails. When the method of Lemma 2 fails to implement a difference of nearby unitaries, the desired correction operation is a sum of nearby unitaries, so it can be implemented nearly deterministically. The correction operation may not have such a form if we use the protocol implicit in the above proof.

One simple generalization of the form of the protocol shown in Figure 3 is to enlarge the ancilla register and allow each unitary in the linear combination to be performed conditioned on a higher-dimensional subspace of the ancilla states. It can be shown that a certain class of protocols of this form also do not improve the success probability. Whether protocols of another form could achieve a higher probability of success remains an open question.

- <span id="page-16-0"></span> D. Aharonov, W. van Dam, J. Kempe, Z. Landau, S. Lloyd, and O. Regev, Adiabatic quantum computation is equivalent to standard quantum computation, SIAM Journal on Computing 37, 166 (2007), preliminary version in FOCS 2004, arXiv:quant-ph/0405098.
- <span id="page-16-1"></span>[2] A. M. Childs, Universal computation by quantum walk, Physical Review Letters 102, 180501 (2009), arXiv:0806.1972.
- <span id="page-16-2"></span>[3] E. Farhi, J. Goldstone, S. Gutmann, and M. Sipser, Quantum computation by adiabatic evolution, arXiv:quant-ph/0001106.
- <span id="page-16-5"></span>[4] A. M. Childs, R. Cleve, E. Deotto, E. Farhi, S. Gutmann, and D. A. Spielman, Exponential algorithmic speedup by quantum walk, in Proceedings of the 35th ACM Symposium on Theory of Computing (2003), pp. 59–68, arXiv:quant-ph/0209131.
- [5] E. Farhi, J. Goldstone, and S. Gutmann, A quantum algorithm for the Hamiltonian NAND tree, Theory of Computing 4, 169 (2008), arXiv:quant-ph/0702144.
- <span id="page-16-17"></span>[6] A. W. Harrow, A. Hassidim, and S. Lloyd, *Quantum algorithm for linear systems of equations*, Physical Review Letters 103, 150502 (2009), arXiv:0811.3171.
- <span id="page-16-3"></span>[7] D. W. Berry, Quantum algorithms for solving linear differential equations (2010), arXiv:1010.2745.
- <span id="page-16-4"></span>[8] S. Lloyd, Universal quantum simulators, Science 273, 1073 (1996).
- <span id="page-16-6"></span>[9] D. Aharonov and A. Ta-Shma, Adiabatic quantum state generation and statistical zero knowledge, in Proceedings of the 35th ACM Symposium on Theory of Computing (2003), pp. 20–29, arXiv:quant-ph/0301023.
- <span id="page-16-7"></span>[10] A. M. Childs, Quantum information processing in continuous time, Ph.D. thesis, Massachusetts Institute of Technology (2004).
- <span id="page-16-15"></span>[11] D. W. Berry, G. Ahokas, R. Cleve, and B. C. Sanders, Efficient quantum algorithms for simulating sparse Hamiltonians, Communications in Mathematical Physics 270, 359 (2007), arXiv:quant-ph/0508139.
- <span id="page-16-16"></span>[12] A. Papageorgiou and C. Zhang, On the efficiency of quantum algorithms for Hamiltonian simulation, to appear in Quantum Information Processing (2012), arXiv:1005.1318.
- <span id="page-16-8"></span>[13] A. M. Childs and R. Kothari, Simulating sparse Hamiltonians with star decompositions, in Theory of Quantum Computation, Communication, and Cryptography (Springer, 2011), vol. 6519 of Lecture Notes in Computer Science, pp. 94–103, arXiv:1003.3683.
- <span id="page-16-9"></span>[14] N. Wiebe, D. W. Berry, P. Høyer, and B. C. Sanders, Simulating quantum dynamics on a quantum computer, Journal of Physics A 44, 445308 (2011), arXiv:1011.3489.
- <span id="page-16-10"></span>[15] D. Poulin, A. Qarry, R. Somma, and F. Verstraete, Quantum simulation of time-dependent Hamiltonians and the convenient illusion of Hilbert space, Physical Review Letters 106, 170501 (2011), arXiv:1102.1360.
- <span id="page-16-11"></span>[16] A. M. Childs, On the relationship between continuous- and discrete-time quantum walk, Communications in Mathematical Physics 294, 581 (2009), arXiv:0810.0312.
- <span id="page-16-12"></span>[17] D. W. Berry and A. M. Childs, *Black-box Hamiltonian simulation and unitary implementation*, Quantum Information and Computation 12, 29 (2012), arXiv:0910.4157.
- <span id="page-16-13"></span>[18] M. Suzuki, General theory of fractal path integrals with applications to many-body theories and statistical physics, Journal of Mathematical Physics 32, 400 (1991).
- <span id="page-16-14"></span>[19] S. Blanes, F. Casas, and J. Ros, *Extrapolation of symplectic integrators*, Celestial Mechanics and Dynamical Astronomy **75**, 149 (1999).

- <span id="page-17-0"></span>[20] N. Wiebe, D. W. Berry, P. Høyer, and B. C. Sanders, Higher order decompositions of ordered operator exponentials, Journal of Physics A 43, 065203 (2010), [arXiv:0812.0562.](http://arxiv.org/abs/arXiv:0812.0562)
- <span id="page-17-1"></span>[21] R. Cleve, D. Gottesman, M. Mosca, R. D. Somma, and D. Yonge-Mallo, Efficient discrete-time simulations of continuoustime quantum query algorithms, in Proceedings of the 41st ACM Symposium on Theory of Computing (2009), pp. 409–416, [arXiv:0811.4428.](http://arxiv.org/abs/arXiv:0811.4428)
- <span id="page-17-2"></span>[22] S. Chin, Multi-product splitting and Runge-Kutta-Nystr¨om integrators, Celestial Mechanics and Dynamical Astronomy 106, 391 (2010).
- <span id="page-17-3"></span>[23] L. F. Richardson, The approximate arithmetical solution by finite differences of physical problems including differential equations, with an application to the stresses in a masonry dam, Philosophical Transactions of the Royal Society of London Series A 210, 307 (1911).
- <span id="page-17-4"></span>[24] Q. Sheng, Solving linear partial differential equations by exponential splitting, IMA Journal of Numerical Analysis 9, 199 (1989).
- <span id="page-17-5"></span>[25] M. E. A. El-Mikkawy, Explicit inverse of a generalized Vandermonde matrix, Applied Mathematics and Computation 146, 643 (2003).
- <span id="page-17-6"></span>[26] M. Abramowitz and I. Stegun, Handbook of mathematical functions with formulas, graphs, and mathematical tables, vol. 55 of Applied Mathematics Series (U.S. Government Printing Office, 1964).
- <span id="page-17-7"></span>[27] S. A. Chin and J. Geiser, Multi-product operator splitting as a general method of solving autonomous and nonautonomous equations, IMA Journal of Numerical Analysis 31, 1552 (2011).
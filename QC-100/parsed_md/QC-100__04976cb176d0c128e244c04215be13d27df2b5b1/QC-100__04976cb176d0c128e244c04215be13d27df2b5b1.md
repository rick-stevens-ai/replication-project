# Error mitigation for short-depth quantum circuits

Kristan Temme, Sergey Bravyi and Jay M. Gambetta *IBM T.J. Watson Research Center, Yorktown Heights NY 10598* (Dated: November 7, 2017)

Two schemes are presented that mitigate the effect of errors and decoherence in short-depth quantum circuits. The size of the circuits for which these techniques can be applied is limited by the rate at which the errors in the computation are introduced. Near-term applications of early quantum devices, such as quantum simulations, rely on accurate estimates of expectation values to become relevant. Decoherence and gate errors lead to wrong estimates of the expectation values of observables used to evaluate the noisy circuit. The two schemes we discuss are deliberately simple and don't require additional qubit resources, so to be as practically relevant in current experiments as possible. The first method, extrapolation to the zero noise limit, subsequently cancels powers of the noise perturbations by an application of Richardson's deferred approach to the limit. The second method cancels errors by resampling randomized circuits according to a quasi-probability distribution.

From the time quantum computation generated wide spread interest, the strongest objection to its viability was the sensitivity to errors and noise. In an early paper, William Unruh [1] found that the coupling to the environment sets an ultimate time and size limit for any quantum computation. This initially curbed the hopes that the full advantage of quantum computing could be harnessed, since it set limits on the scalability of any algorithm. This problem was, at least in theory, remedied with the advent of quantum error correction [2–4]. It was proven that if both the decoherence and the imprecision of gates could be reduced below a finite threshold value, then quantum computation could be performed indefinitely [5, 6]. Although it is the ultimate goal to reach this threshold in an experiment that is scalable to larger sizes, the overhead that is needed to implement a fully fault-tolerant gate set with current codes [7] seems prohibitively large [8, 9]. In turn, it is expected that in the near term the progress in quantum experiments will lead to devices with dynamics, which are beyond what can be simulated with a conventional computer. This leads to the question: what computational tasks could be accomplished with only limited, or no error correction?

The suggestions of near-term applications in such quantum devices mostly center around quantum simulations with short-depth circuit [10–12] and approximate optimization algorithms [13]. Furthermore, certain problems in material simulation may be tackled by hybrid quantum-classical algorithms [14]. In most such applications, the task can be abstracted to applying a short-depth quantum circuits to some simple initial state and then estimating the expectation value of some observable after the circuit has been applied. This estimation must be accurate enough to achieve a simulation precision comparable or exceeding that of classical algorithms. Yet, although the quantum system evolves coherently for the most part of the short-depth circuit, the effects of decoherence already become apparent as an error in the estimate of the observable. For the simulation to be of value, the effect of this error needs to be mitigated.

In this paper we introduce two techniques for *quantum* error mitigation that increase the quality of any such short-depth quantum simulations. We find that the accuracy of the expectation value can be increased significantly in the

presence of noise. We are looking for error mitigation techniques that are as simple as possible and don't require additional quantum resources. Both techniques require that some noise parameter taken together with system size and circuit depth can be considered a small number. The first scheme does not make any assumption about the noise model other than it being weak and constant in time. In comparison, the second scheme can tolerate stronger noise; however, it requires detailed knowledge of the noise model.

Extrapolation to the zero noise limit: It is our goal to estimate the expectation value of some quantum observable A with respect to an evolved state  $\rho_{\lambda}(T)$  after time T that is subject to noise characterized by the parameter  $\lambda$  in the limit where  $\lambda \to 0$ . To achieve this, we apply Richardson's deferred approach to the limit to cancel increasingly higher orders of  $\lambda$  [15].

Although gates are typically used to describe quantum circuits, for our analysis it is more convenient to consider the time-dependent Hamiltonian dynamics implementing the circuit. The time-dependent multi-qubit Hamiltonian is denoted by K(t). It can be expanded into N - qubit Pauli operators  $P_{\alpha} \in \langle \mathbb{1}, X_j, Y_j, Z_j \rangle_{j=1...N}$ , where  $X_j, Y_j, Z_j$  acts as a single-qubit Pauli matrix on site j and trivially elsewhere. We allow for time-dependent coupling coefficients  $J_{\alpha}(t) \in \mathbb{R}$ . The circuit is encoded as  $K(t) = \sum_{\alpha} J_{\alpha}(t) P_{\alpha}$ . The total evolution of the open system with initial state  $\rho_0$  will be described by an equation of the following form:

$$\frac{\partial}{\partial t}\rho(t) = -i[K(t), \rho(t)] + \lambda \mathcal{L}(\rho(t)) \tag{1}$$

for time  $t \in [0,T]$ . We do not specify the exact form of the generator  $\mathcal{L}(\rho)$  but only require that it is invariant under time rescaling and independent from the parameters  $J_{\alpha}(t)$  in K(t). The noise term  $\mathcal{L}(\rho)$  could be given as a Lindblad operator, or it could correspond to a Hamiltonian that couples to a bath to model non-Markovian dynamics. We ask that there is a parameter  $\lambda \ll 1$  that indicates a weak action of the noise and that we can bound  $\|\mathcal{L}_{I,t_1} \circ \mathcal{L}_{I,t_2} \circ \ldots \circ \mathcal{L}_{I,t_n}(\rho)\|_1 \leq l_n$ , where at most  $l_n = \mathcal{O}(N^n)$ . The map  $\mathcal{L}_{I,t}$  is short-hand notation for the transformation of  $\mathcal{L}$  into the interaction frame generated

by K(t).

The expectation value of the observable A is obtained from the final state  $\rho_{\lambda}(T)$  as  $E_K(\lambda) = \operatorname{tr} (A\rho_{\lambda}(T))$ . The function  $E_K(\lambda)$  can be expressed as a series in  $\lambda$  where the contribution with  $\lambda^0$  corresponds to the noise-free evolution. This can be seen by transforming the evolution into the interaction frame w.r.t K(t) and expanding the Born series, c.f. supp. mat. sec I. Starting from the noise-free expectation value  $E^* = \operatorname{tr} (A\rho_0(T))$ , the expansion is given by

$$E_K(\lambda) = E^* + \sum_{k=1}^n a_k \lambda^k + R_{n+1}(\lambda, \mathcal{L}, T).$$
 (2)

The  $a_k$  are model-specific constants typically growing like  $a_k \sim N^k T^k$ . Here  $R_{n+1}(\lambda,\mathcal{L},T)$  is the remainder of the expansion and can be bounded by  $|R_{n+1}(\lambda,\mathcal{L},T)| \leq \|A\|l_{n+1}(\lambda T)^{n+1}/(n+1)!$  by standard arguments. Since we assumed an extensive scaling of  $l_n$ , such an expansion is only meaningful whenever  $NT\lambda$  is small. We are of course interested in  $\lim_{\lambda \to 0} E_K(\lambda) = E^*$ ; however, we are faced with a small but finite parameter  $\lambda$ . Since we only have access to  $E_K(\lambda)$ , our estimate of  $E^*$  will be off by  $\mathcal{O}(\lambda)$ .

This estimate can be improved by Richardson's deferred approach to the limit [15, 16]. To explain the idea, let us assume we can run the quantum circuit at different noise rates  $\lambda_j$ , with  $j=0,\ldots,n$  and obtain experimental estimates  $\hat{E}_K(\lambda_j)=E_K(\lambda_j)+\delta_j$ . Here the  $\lambda_j=c_j\lambda$  are appropriately rescaled values of the experimental noise rate  $\lambda$ . The estimate deviates from the actual expectation value due to experimental inaccuracies and finite sampling errors by an error  $\delta_j$ . The estimate of  $E^*$  can be significantly improved by considering the approximation  $\hat{E}_K^n(\lambda)$ , which is written as the linear combination

<span id="page-1-0"></span>
$$\hat{E}_K^n(\lambda) = \sum_{j=0}^n \gamma_j \hat{E}_K(c_j \lambda). \tag{3}$$

Here we require the coefficients  $\gamma_j$  to satisfy the linear system of equations [16].

<span id="page-1-1"></span>
$$\sum_{l=0}^{n} \gamma_j = 1 \quad \text{and} \quad \sum_{j=0}^{n} \gamma_j \ c_j^k = 0 \quad \text{for } k = 1 \dots n. \quad (4)$$

The linear combination Eq. (3) will be an approximation to  $E^*$  up to an error of order  $\mathcal{O}(\lambda^{n+1})$ .

To obtain estimates at different noise rates  $\lambda_j$ , we use a rescaling trick. We run the same circuit n+1 times with rescaled parameters in K(t). We follow the protocol:

- 1. For i = 0, ..., n
  - (a) choose a rescaling coefficient  $c_j > 1$  ( $c_0 = 1$ ) and evolve  $\rho_0$  with rescaled Hamiltonian  $K^j(t) = \sum_{\alpha} J^j_{\alpha}(t) P_{\alpha}$ , where

$$J_{\alpha}^{j}(t)=c_{j}^{-1}J_{\alpha}\left(c_{j}^{-1}t\right), \tag{5}$$
 for time  $T_{j}=c_{j}T.$ 

- (b) Estimate observable A to obtain  $\hat{E}_K(c_j\lambda)$ .
- 2. Solve equations (4) and compute  $\hat{E}_{K}^{n}(\lambda)$  as in Eq. (3).

A rescaling of the equations shows that the state  $\rho_{\lambda}^{j}(T_{j})$ , which evolves under  $\dot{\rho}_{\lambda}^{j}=-i[K^{j}(t),\rho^{j}]+\lambda\mathcal{L}(\rho^{j})$  for time  $T_{j}$ , satisfies  $\rho_{\lambda}^{j}(T_{j})=\rho_{c_{j}\lambda}(T)$ , c.f. supp. mat. sec. II. Hence the estimates  $\hat{E}_{K}(c_{j}\lambda)=\operatorname{tr}\left(A\rho_{\lambda}^{j}(T_{j})\right)+\delta_{j}$  can be obtained from the n+1 runs rescaled according to the protocol.

If the protocol is performed for n+1 steps, the error between the exact expectation value  $E^*$  and the estimator  $\hat{E}_K^n(\lambda)$  can be bounded by

$$|E^* - \hat{E}_K^n(\lambda)| \le \Gamma_n \left(\delta^* + ||A|| \frac{l_{n+1}(\lambda T)^{n+1}}{(n+1)!}\right).$$
 (6)

Here  $\Gamma_n = \sum_{j=0}^n |\gamma_j| c_j^{n+1}$  and  $\delta^* = \max_j |\delta_j|$  is the largest experimental error.

This follows from repeated application of the triangle inequality, c.f. supp. mat. sec. III. The equations (4) can be solved, and one finds that the coefficients  $\gamma_j = \prod_{m \neq j} c_m (c_j - c_m)^{-1},$  so that the constant  $\Gamma_n$  can be evaluated. In the literature [16], several choices for progression of  $c_j$  are common. The two most frequent series are exponential decrease (Bulirsch - Stoer) and harmonic decay. In our experiments we are actually increasing the noise rate starting from the optimal value, wheres it is common in the numerical literature to improve the small parameter. The result is, of course, the same.

*Examples*: To demonstrate this method we will consider three numerical examples. In all the examples the time evolution is given by a Hamiltonian K(t) that encodes a control problem. For a single drift step we evolve with a Hamiltonian  $K_R(t)=U_N(\theta)K_0U_N^\dagger(\theta)$ , where the single qubit product unitary  $U_N(\theta)\in SU(2)^{\otimes N}$  is chosen Haarrandom, and the drift Hamiltonian  $K_0 = \sum_{i,j} J_{i,j} X_i Z_j$  is chosen with respect to a random graph and Gaussian distributed couplings  $J_{i,j}$ . The evolution is subject to three different noise models: first Fig 1(a), we evolve in the presence of depolarizing noise described by the sum of single qubit generators  $\mathcal{L}_i = -\lambda(2^{-1}\operatorname{tr}_i(\rho) - \rho)$  acting on all N qubits. Second, Fig 1(b), we consider dephasing and amplitude damping noise on every qubit, where we have chosen a ratio of  $\lambda_1/\lambda_2 = 1.5$  with a generator  $\mathcal{L}_i =$  $\lambda_1 \left( \sigma_i^- \rho \sigma_i^+ - \frac{1}{2} \{ \sigma_i^+ \sigma_i^-, \rho \} \right) + \lambda_2 \left( Z_i \rho Z_i - \rho \right) \text{ and } \sigma_i^{\pm} =$  $2^{-1}(X_i \pm iY_i)$ . Third, Fig 1(c), we consider a highly non-Markovian setting, where each of the N qubits i is coupled to its own single-qubit bath  $b_i$  via the Hamiltonian  $V_i$  $1/2 X_i \otimes X_{b_i} + 1/2 Z_{b_i}$  and the bath is prepared in the initial state  $\rho_B = (2\cosh(\beta/2))^{-N} \exp(-\beta \sum_{b_i} \sigma_{b_i}^z)$ . Then, after the evolution of each noisy circuit T = td we measure a randomly chosen multi-qubit Pauli operator  $P_{\alpha}$ .

The graphs in Fig 1 show that with modest effort very high precisions can be obtained. In the low noise range  $\epsilon\sim 10^{-3}$ 

![](_page_2_Figure_1.jpeg)

<span id="page-2-0"></span>FIG. 1. (color online) The plots show a random Hamiltonian evolution for N=4 system qubits and d=6 drift steps, each for time t=2. For all systems plot the error  $\Delta E=|E^*-\hat{E}_K^n(\lambda)|$  for n=0,1,2,3. Here  $\lambda^1,n=0$  corresponds to the uncorrected error. The noise parameter  $\lambda=-1/2\log(1-\epsilon)$  is chosen so that all plots have the same perturbation measured in the depolarizing strength  $\epsilon=10^{-3}\dots 10^{-2}$ . The plot shows the mitigation of (a) Depolarizing noise (b) Amplitude damping / dephasing noise and (c) non-Markovian noise, for  $\{c_j\}$  chosen as random partition of in the interval [1,4].

the relative error can be reduced to  $\Delta E \sim 10^{-6}-10^{-11}$ . The precision is then essentially determined by the sampling error  $\delta^*$ , which we have neglected in the plots.

Probabilistic error cancellation: Here we discuss a noise reduction scheme for quantum circuits subject to a Markovian noise. First let us state our assumptions on the noise model. A noisy N-qubit device will be described by a basis set of noisy operations  $\Omega = \{\mathcal{O}_1, \dots, \mathcal{O}_m\}$  that can be implemented on this device. Each operation  $\mathcal{O}_{\alpha}$  is a tracepreserving completely positive (TPCP) map on N qubits that acts non-trivially only on a small subset of qubits, say at most two. For example,  $\mathcal{O}_{\alpha}$  could be a noisy unitary gate applied to a specified pair of qubits or a noisy qubit initialization. We assume that noise in the system can be fully characterized such that the map  $\mathcal{O}_{\alpha}$  is known for each  $\alpha$ . A circuit of length L in the basis  $\Omega$  is a sequence of L operations from  $\Omega$ . Let  $\Omega_L$  be a set of all length-L circuits in the basis  $\Omega$ . A circuit  $\alpha = (\alpha_1, \dots, \alpha_L)$  implements a map  $\mathcal{O}_{\alpha} = \mathcal{O}_{\alpha_L} \cdots \mathcal{O}_{\alpha_2} \mathcal{O}_{\alpha_1}$ . The expectation value of an observable A on the final state produced by a noisy circuit  $\alpha$  is

$$E(\boldsymbol{\alpha}) = \text{Tr}[A \mathcal{O}_{\boldsymbol{\alpha}}(|0\rangle\langle 0|^{\otimes n})].$$

For simplicity, we ignore errors in the initial state preparation and in the final measurement. Such errors can be accounted for by adding dummy noisy operations before each measurement and after each qubit initialization. Furthermore, we shall assume that A is diagonal in the Z-basis and  $\|A\| \leq 1$ .

Below we show that under certain conditions the task of simulating an ideal quantum circuit can be reduced to estimating the expectation value  $E(\alpha)$  for a suitable random ensemble of noisy quantum circuits  $\alpha$ . Moreover, the ideal and the noisy circuits act on the same number of qubits and have the same depth.

Let  $\Gamma = \{\mathcal{U}_1, \dots, \mathcal{U}_k\}$  be a fixed basis set of ideal gates.

Each gate  $\mathcal{U}_{\beta}(\rho) = U_{\beta}\rho U_{\beta}^{\dagger}$  is described by a unitary TPCP map on N qubits that acts non-trivially on a small subset of qubits. An ideal length-L circuit in the basis  $\Gamma$  is a sequence of L gates from  $\Gamma$ . A circuit  $\boldsymbol{\beta} = (\beta_1, \ldots, \beta_L)$  implements a map  $\mathcal{U}_{\boldsymbol{\beta}} = \mathcal{U}_{\beta_L} \cdots \mathcal{U}_{\beta_2} \mathcal{U}_{\beta_1}$ . Define an ideal expectation value

$$E^*(\boldsymbol{\beta}) = \operatorname{Tr}[A \mathcal{U}_{\boldsymbol{\beta}}(|0\rangle\langle 0|^{\otimes n})].$$

We consider a simulation task where the goal is to estimate  $E^*(\beta)$  with a specified precision  $\delta$ .

The key idea of our scheme is to represent the ideal circuit as a quasi-probabilistic mixture of noisy ones. Let us say that a noisy basis  $\Omega$  simulates an ideal circuit  $\boldsymbol{\beta}$  with the overhead  $\gamma_{\boldsymbol{\beta}} \geq 1$  if there exists a probability distribution  $P_{\boldsymbol{\beta}}(\boldsymbol{\alpha})$  on the set of noisy circuits  $\boldsymbol{\alpha} \in \Omega_L$  such that

$$\mathcal{U}_{\beta} = \gamma_{\beta} \sum_{\alpha \in \Omega_L} P_{\beta}(\alpha) \sigma_{\beta}(\alpha) \mathcal{O}_{\alpha}$$
 (7)

for some coefficients  $\sigma_{\beta}(\alpha)=\pm 1$ . We also require that the distribution  $P_{\beta}(\alpha)$  is sufficiently simple so that one can efficiently sample  $\alpha$  from  $P_{\beta}(\alpha)$ . The coefficients  $\gamma_{\beta}, \sigma_{\beta}(\alpha)$  must be efficiently computable. We shall refer to Eq. (41) as a quasi-probability representation (QPR) of the ideal circuit  $\beta$ . Note that  $\gamma_{\beta} \geq 1$  because  $\mathcal{U}_{\beta}$  and  $\mathcal{O}_{\alpha}$  are trace-preserving. Quasi-probability distributions have been previously used to construct classical algorithms for simulation of quantum circuits [17, 18]. Our work can be viewed as an application of these methods to the problem of simulating ideal quantum circuits by noisy ones.

Substituting Eq. (41) into the definition of  $E^*(\beta)$  gives

$$E^*(\beta) = \gamma_{\beta} \sum_{\alpha \in \Omega_L} P_{\beta}(\alpha) \sigma_{\beta}(\alpha) E(\alpha). \tag{8}$$

Let  $\alpha \in \Omega_L$  be a random variable drawn from  $P_{\beta}(\alpha)$  and  $x \in \{0,1\}^n$  be the final readout of the noisy circuit  $\alpha$  obtained by measuring each qubit of the final state  $\mathcal{O}_{\alpha}(|0\rangle\langle 0|^{\otimes n})$  in the Z-basis. Note that  $\langle x|A|x\rangle$  is an unbiased estimator of  $E(\alpha)$  with the variance O(1). Thus from Eq. (42) one infers that  $\gamma_{\beta}\sigma_{\beta}(\alpha)\langle x|A|x\rangle$  is an unbiased estimator of the ideal expectation value  $E^*(\beta)$  with the variance  $O(\gamma_{\beta}^2)$ . We can now estimate  $E^*(\beta)$  with any desired precision  $\delta$  by the Monte Carlo method. Define

<span id="page-2-1"></span>
$$M = (\delta^{-1}\gamma_{\beta})^2 \tag{9}$$

and generate M samples  $\alpha^1,\ldots,\alpha^M\in\Omega_L$  drawn from  $P_{\beta}(\alpha)$ . By Hoeffding's inequality,  $E^*(\beta)$  is approximated within error  $O(\delta)$  w.h.p. by a random variable

<span id="page-2-2"></span>
$$\hat{E}(\boldsymbol{\beta}) = \frac{\gamma_{\boldsymbol{\beta}}}{M} \sum_{a=1}^{M} \sigma_{\boldsymbol{\beta}}(\boldsymbol{\alpha}^a) \langle x^a | A | x^a \rangle, \tag{10}$$

where  $x^a \in \{0,1\}^n$  is the final string of the noisy circuit  $\alpha^a$ . Computing the estimator  $\hat{E}(\beta)$  requires M runs of the noisy circuits, with each run producing a single readout string

x a . Estimating E<sup>∗</sup> (β) with a precision δ in the absence of noise by Monte Carlo method would require approximately δ −2 runs. Thus the quantity γ β determines the simulation overhead (see Eq. [\(9\)](#page-2-1)).

A systematic method of constructing QPRs with a small overhead is given in supp. mat. sec. IV. Here we illustrate the method using toy noise models usually studied in the quantum fault-tolerance theory: the depolarizing noise and the amplitude damping noise. For concreteness, we choose the ideal gate set Γ as the standard Clifford+T basis.

Let D<sup>k</sup> be the depolarizing noise on k = 1, 2 qubits that returns the maximally mixed state with probability and does nothing with probability 1 − . Define a noisy version of a kqubit unitary gate U as DkU. The noisy basis Ω is obtained by multiplying ideal gates on the left by arbitrary Pauli operators and adding the depolarizing noise. Thus Ω is a set of operations O<sup>α</sup> = DkPU, where U ∈ Γ is a k-qubit ideal gate and P ∈ {I, X , Y, Z}<sup>⊗</sup><sup>k</sup> is a Pauli TPCP map. The random ensemble of noisy circuits O<sup>α</sup> that simulates an ideal circuit U<sup>β</sup> is constructed in three steps: (1) Start from the ideal circuit, O<sup>α</sup> = Uβ. (2) Modify O<sup>α</sup> by adding a Pauli X, Y, Z after each single-qubit gate with probability p<sup>1</sup> = /(4 + 2). The gate is unchanged with probability 1−3p1. (3) Modify O<sup>α</sup> by adding a Pauli IX, IY, . . . , ZZ after each CNOT with probability p<sup>2</sup> = /(16+ 14). The CNOT is unchanged with probability 1 − 15p2. The resulting circuit is then implemented on a noisy device (which adds the depolarizing noise after each gate) and the final readout string x is recorded. By generating M samples of x one can estimate E<sup>∗</sup> (β) from Eq. [\(10\)](#page-2-2). The sign function σβ(α) is equal to (−1)<sup>r</sup> , where r is the number of Pauli operators added to the ideal circuit Uβ. As shown in supp. mat. sec. IV, the above defines a QPR of the ideal circuit U<sup>β</sup> with the overhead γ<sup>β</sup> ≈ 1 + (3L1/2 + 15L2/8), where L<sup>1</sup> is the number of single-qubit gates and L<sup>2</sup> is the number of CNOTs in the ideal circuit. The method has been tested numerically for random noisy Clifford+T circuits, see Fig. [2.](#page-3-3)

A more interesting example is the noise described by the amplitude-damping channel A that resets every qubit to its ground state with probability . A noisy version of a k-qubit unitary gate U is defined as A<sup>⊗</sup><sup>k</sup>U. In contrast to the previous example, noisy unitary gates A<sup>⊗</sup><sup>k</sup>U alone cannot simulate any ideal unitary gate since A is not a unital map. To overcome this, we extend the noisy basis Ω by adding noisy versions of single-qubit state preparations AP<sup>|</sup>ψ<sup>i</sup> , where P<sup>|</sup>ψ<sup>i</sup> maps any input state to |ψihψ|. Our scheme requires state preparations for single qubit states |ψi = |+i, |−i, |0i, |1i that can be performed at any time step (not only at the beginning). In supp. mat. sec. V we show how to construct a QPR of the ideal Clifford+T circuit U<sup>β</sup> with the overhead γ<sup>β</sup> ≈ 1 + (2L<sup>1</sup> + 4L2). The examples considered above suggest that well-characterized noisy circuits can simulate ideal ones with overhead γ ≈ (1 +c) <sup>L</sup>, where is the typical error rate and c is a small constant. The value of c can be determined by performing quantum process tomography [\[19\]](#page-4-13)

![](_page_3_Figure_5.jpeg)

<span id="page-3-3"></span>FIG. 2. Simulation precision δ(β) = |Eˆ(β) − E ∗ (β)| for 500 randomly generated ideal Clifford+T circuits on N = 6 qubits with depth d = 20. The gates are subject to single- and two-qubit depolarizing noise = 10<sup>−</sup><sup>2</sup> . The figure shows results for simulations without (a) and with (b) error cancellation. In both cases each ideal circuit was simulated by M = 4000 runs of the noisy circuit. For each circuit U<sup>β</sup> we defined the observable A as a projector Πout onto the subset of 2 N−1 basis vectors with the largest weight in the final state. The results are consistent with γ<sup>β</sup> ≈ 4.3 so that γβM<sup>−</sup>1/<sup>2</sup> ≈ 0.07.

and finding the QPR for each ideal gate. Using Eq. [\(9\)](#page-2-1), one can estimate the number of noisy circuit runs of length L as M ∼ exp (2cL). Assuming error rates in the range ∼ 10<sup>−</sup><sup>3</sup> , it may be possible to simulate ideal circuits with O(10<sup>3</sup> ) gates.

*Conclusions:* Both error mitigation schemes require no additional quantum hardware such as ancilla or code qubits and work directly with the physical qubits. The zero-noise extrapolation requires sufficient control of the time evolution to implement the rescaled dynamics and hinges on the assumption of a large time-scale separation between the dominant noise and the controlled dynamics. For the probabilistic error cancellation a full characterization of the noisy computational operations is necessary. To obtain this to a precision of ∼ 10<sup>−</sup><sup>3</sup> is challenging in practice. However, if one is willing to sacrifice optimality, a Pauli- or Clifford-twirling [\[20,](#page-4-14) [21\]](#page-4-15) can be applied that converts any noise channel into a simple mixture of Pauli errors or depolarizing noise, making the characterization task much more manageable. A very recent independent paper by Li and Benjamin [\[22\]](#page-4-16) discusses similar issues to those addressed here.

*Acknowledgements:* We thank Antonio Mezzacapo for insightful discussions, and we acknowledge support from the IBM Research Frontiers Institute

<span id="page-3-0"></span><sup>[1]</sup> W. G. Unruh, Physical Review A 51, 992 (1995).

<span id="page-3-1"></span><sup>[2]</sup> P. W. Shor, Physical review A 52, R2493 (1995).

<sup>[3]</sup> A. M. Steane, Physical Review Letters 77, 793 (1996).

<span id="page-3-2"></span><sup>[4]</sup> A. R. Calderbank and P. W. Shor, Physical Review A 54, 1098 (1996).

- <span id="page-4-0"></span>[5] D. Aharonov and M. Ben-Or, in *Proceedings of the twenty-ninth annual ACM symposium on Theory of computing* (ACM, 1997) pp. 176–188.
- <span id="page-4-1"></span>[6] A. Y. Kitaev, Russian Mathematical Surveys 52, 1191 (1997).
- <span id="page-4-2"></span>[7] A. G. Fowler, M. Mariantoni, J. M. Martinis, and A. N. Cleland, Physical Review A 86, 032324 (2012).
- <span id="page-4-3"></span>[8] N. C. Jones, R. Van Meter, A. G. Fowler, P. L. McMahon, J. Kim, T. D. Ladd, and Y. Yamamoto, Physical Review X 2, 031007 (2012).
- <span id="page-4-4"></span>[9] S. J. Devitt, A. M. Stephens, W. J. Munro, and K. Nemoto, Nature communications 4 (2013).
- <span id="page-4-5"></span>[10] A. Peruzzo, J. McClean, P. Shadbolt, M.-H. Yung, X.-Q. Zhou, P. J. Love, A. Aspuru-Guzik, and J. L. O?Brien, Nature communications 5 (2014).
- [11] J. R. McClean, J. Romero, R. Babbush, and A. Aspuru-Guzik, arXiv preprint [arXiv:1509.04279](http://arxiv.org/abs/1509.04279) (2015).
- <span id="page-4-6"></span>[12] D. Wecker, M. B. Hastings, and M. Troyer, Physical Review A 92, 042303 (2015).
- <span id="page-4-7"></span>[13] E. Farhi, J. Goldstone, and S. Gutmann, arXiv preprint [arXiv:1411.4028](http://arxiv.org/abs/1411.4028) (2014).
- <span id="page-4-8"></span>[14] B. Bauer, D. Wecker, A. J. Millis, M. B. Hastings, and M. Troyer, arXiv preprint [arXiv:1510.03859](http://arxiv.org/abs/1510.03859) (2015).
- <span id="page-4-9"></span>[15] L. F. Richardson and J. A. Gaunt, Philosophical Transactions of

- the Royal Society of London. Series A, containing papers of a mathematical or physical character 226, 299 (1927).
- <span id="page-4-10"></span>[16] A. Sidi, "Practical extrapolation methods: Theory and applications, volume 10 of cambridge monographs on applied and computational mathematics," (2003).
- <span id="page-4-11"></span>[17] H. Pashayan, J. J. Wallman, and S. D. Bartlett, Physical review letters 115, 070501 (2015).
- <span id="page-4-12"></span>[18] N. Delfosse, P. A. Guerin, J. Bian, and R. Raussendorf, Physical Review X 5, 021003 (2015).
- <span id="page-4-13"></span>[19] M. Mohseni, A. Rezakhani, and D. Lidar, Phys. Rev. A 77, 032322 (2008).
- <span id="page-4-14"></span>[20] M. Silva, E. Magesan, D. W. Kribs, and J. Emerson, Physical Review A 78, 012347 (2008).
- <span id="page-4-15"></span>[21] E. Magesan, J. M. Gambetta, and J. Emerson, Physical Review A 85, 042311 (2012).
- <span id="page-4-16"></span>[22] Y. Li and S. C. Benjamin, arXiv preprint [arXiv:1611.09301](http://arxiv.org/abs/1611.09301) (2016).
- <span id="page-4-17"></span>[23] G. Lindblad, Communications in Mathematical Physics 48, 119 (1976).
- <span id="page-4-18"></span>[24] H.-P. Breuer and F. Petruccione, *The theory of open quantum systems* (Oxford University Press on Demand, 2002).
- <span id="page-4-19"></span>[25] C. Schneider, Numerische Mathematik 24, 177 (1975).

#### SUPPLEMENTAL MATERIAL

# Reducing noise by Richardson extrapolation

In numerical analysis, Richardson extrapolation [\[15,](#page-4-9) [16\]](#page-4-10) is a sequence acceleration method, used to improve the rate of convergence of a sequence. We use the same technique to extrapolate to the zero-noise limit in short-depth quantum circuits in the presence of noise. We assume that the noise process is constant in time and does not depend on the rescaling of the system Hamiltonian parameters. We consider various noise models in continuous time.

It is our goal to estimate the expectation value of some observable A with respect to the evolved state ρλ(T). The actual computation is now encoded in the time-dependent Hamiltonian K(t), and the full evolution is given by the equation

$$\frac{\partial}{\partial t}\rho = -i[K(t), \rho] + \lambda \mathcal{L}(\rho). \tag{11}$$

Here we have that

$$K(t) = \sum_{\alpha} J_{\alpha}(t) P_{\alpha} \tag{12}$$

is some multi-qubit Pauli Hamiltonian with time-dependent coupling constant Jα(t) ∈ R and Pauli operators P<sup>α</sup> ∈ h1, X<sup>i</sup> , Y<sup>i</sup> , Zii<sup>i</sup> . Starting from some initial state ρ<sup>0</sup> the system is evolved for some time T. We consider different forms of noise L(ρ). As the simplest form of noise, we assume a time-independent Lindblad operator [\[23\]](#page-4-17) of the form

$$\mathcal{L}(\rho) = \sum_{\beta} L_{\beta} \rho L_{\beta}^{\dagger} - \frac{1}{2} \{ L_{\beta}^{\dagger} L_{\beta}, \rho \}. \tag{13}$$

However, we can also imagine other forms of errors, such as

$$\mathcal{L}(\rho) = -i[V, \rho],\tag{14}$$

where V is some Hamiltonian. This setting in useful when we want to consider more general, possibly non-Markovian noise models, or a noisy evolution derived from first principle [\[24\]](#page-4-18). One can make the assumption that the initial state is given by ρ<sup>0</sup> = ρS(0) ⊗ ρB(0) and give the most general form of an interaction Hamiltonian between system and bath, such as

$$V = \sum_{\alpha} S_{\alpha} \otimes B_{\alpha} + H_{B}. \tag{15}$$

Here we take the point of view that a small  $\lambda$  indicates a separation of time scales, and  $\rho_S(0) = |\psi_0\rangle\langle\psi_0|$  may be the initial state of the computation. We assume that  $\rho(0) = \rho_S(0) \otimes \rho_B$ , where the bath state is a steady state w.r.t the bath Hamiltonian  $[H_B, \rho_B] = 0$ . The observable we want to estimate  $A = A_S \otimes \mathbb{1}$  is then only supported on the system degrees of freedom.

We assume that  $\rho_{\lambda}(T)$  is the state we obtain after the noisy evolution for time T. From this state we can estimate the expectation value of the observable A by various methods. Typically we will sample the expectation value

$$E_K(\lambda) = \operatorname{tr}\left(A\rho_{\lambda}(T)\right) \tag{16}$$

so that an additional sampling error  $\delta$  is introduced, and we obtain from out measurement the statistic  $\hat{E}_K(\lambda) = E_K(\lambda) + \delta$ . The error can assumed to be asymptotically Gaussian  $\delta = \mathcal{O}\left(M^{-1/2}\sqrt{\operatorname{tr}\left(\rho_\lambda(T)(A-E_K(\lambda))^2\right)}\right)$  since one typically repeats the experiment  $M\gg 1$  times and the i.i.d hypothesis holds.

## I Series expansion in the noise parameter

We now show that the function  $E_K(\lambda)$  can be expressed as a series in  $\lambda$  where the contribution with  $\lambda^0$  corresponds to the noise-free evolution. We also provide a bound on the error term. To this end, we transform into the interaction picture of K(t). We define  $U_K(t) = \mathcal{T}\left\{\exp(-i\int_0^t K(t')dt')\right\}$ , where  $\mathcal{T}\{\cdot\}$  defines the time order expansion. We define the interaction picture through

$$\rho_I(t) = U_K(t)\rho(t)U_K^{\dagger}(t) \quad \text{and} \quad \mathcal{L}_{I,t}(\circ) = U_K(t)\mathcal{L}\left(U_K^{\dagger}(t) \circ U_K(t)\right)U_K^{\dagger}(t), \tag{17}$$

where now the generator  $\mathcal{L}_{I,t}$  has become time-dependent. The evolution equation in the interaction picture now reads

$$\partial_t \rho_I(t) = \lambda \mathcal{L}_{I,t} \left( \rho_I(t) \right). \tag{18}$$

Recall that every first-order differential equation can be reformulated as an integral equation

$$\rho_I(T) = \rho_I(0) + \lambda \int_0^T \mathcal{L}_{I,t} \left( \rho_I(t) \right) dt. \tag{19}$$

This equation can be recursively solved to increasing order in  $\lambda$  so that

$$\rho_{I}(T) = \rho_{I}(0) + \lambda \int_{0}^{T} \mathcal{L}_{I,t} (\rho_{I}(0)) dt + \lambda^{2} \int_{0}^{T} \int_{0}^{t} \mathcal{L}_{I,t} \circ \mathcal{L}_{I,t'} (\rho_{I}(0)) dt dt' + \lambda^{3} \int_{0}^{T} \int_{0}^{t} \int_{0}^{t'} \mathcal{L}_{I,t} \circ \mathcal{L}_{I,t'} \circ \mathcal{L}_{I,t''} (\rho_{I}(0)) dt dt' dt'' \dots$$
(20)

Recall that  $\rho_I(0)=\rho(0)$ . Furthermore, we can conjugate the full expression on both sides with the unitary  $U_K(T)$ . Let us for notational convenience define  $\rho_\lambda(T)$  as the resulting state after evolution with noise rate  $\lambda$ . We observe that  $U_K(T)^\dagger \rho(0) U_K(T) = \rho_0(T)$ , whereas  $U_K(T)^\dagger \rho_I(T) U_K(T) = \rho_\lambda(T)$ , so that we obtain the expression in the Schrödinger picture as

$$\rho_{\lambda}(T) = \rho_{0}(T) + \sum_{k=1}^{n} \lambda^{k} \int_{0}^{T} \int_{0}^{t_{1}} \dots \int_{0}^{t_{k-1}} U_{K}^{\dagger}(T) \mathcal{L}_{I,t_{1}} \circ \mathcal{L}_{I,t_{2}} \circ \dots \circ \mathcal{L}_{I,t_{k}} \left(\rho(0)\right) U_{K}(T) dt_{1} dt_{2} \dots dt_{k}$$

$$+ \lambda^{n+1} \int_{0}^{T} \int_{0}^{t_{1}} \dots \int_{0}^{t_{n}} U_{K}^{\dagger}(T) \mathcal{L}_{I,t_{1}} \circ \mathcal{L}_{I,t_{2}} \circ \dots \circ \mathcal{L}_{I,t_{n}+1} \left(\rho_{I}(t_{n+1})\right) U_{K}(T) dt_{1} dt_{2} \dots dt_{n+1}. \quad (21)$$

The expectation value  $E_K(\lambda) = \operatorname{tr}(A\rho_{\lambda}(T))$  for the observable A can immediately be expanded in a series with parameter  $\lambda$  of the form

<span id="page-5-0"></span>
$$E_K(\lambda) = \operatorname{tr}(A\rho_0(T)) + \sum_{k=1}^n a_k \lambda^k + R_{n+1}(\lambda, \mathcal{L}, T),$$
(22)

where the constants  $a_k$  and the remainder  $R_{n+1}(\lambda, \mathcal{L}, T)$  are obtained by pairing the integrals with the trace  $\operatorname{tr}(A \cdot)$  and  $\operatorname{tr}(A \rho_0(T)) = E^*$  corresponds to the noise-free evolution to which we seek to extrapolate. We read off that

$$a_k = \int_0^T \int_0^{t_1} \dots \int_0^{t_{k-1}} \operatorname{tr}\left(U_K(T)AU_K^{\dagger}(T)\mathcal{L}_{I,t_1} \circ \mathcal{L}_{I,t_2} \circ \dots \circ \mathcal{L}_{I,t_k}\left(\rho(0)\right)\right) dt_1 dt_2 \dots dt_k, \tag{23}$$

as well as

$$R_{n+1}(\lambda, \mathcal{L}, T) = \lambda^{n+1} \int_0^T \int_0^{t_1} \dots \int_0^{t_n} \operatorname{tr}\left(U_K(T)AU_K^{\dagger}(T)\mathcal{L}_{I, t_1} \circ \dots \circ \mathcal{L}_{I, t_{n+1}}\left(\rho_I(t_{n+1})\right)\right) dt_1 \dots dt_{n+1}. \tag{24}$$

We can bound  $|R_{n+1}(\lambda, \mathcal{L}, T)|$  by a simple application of Cauchy's mean value theorem and Hölder's inequality. We observe by first applying the midpoint Theorem that there exist  $\xi_1, \ldots, \xi_{n+1}$  so that

$$R_{n+1}(\lambda, \mathcal{L}, T) = \frac{\lambda^{n+1} T^{n+1}}{(n+1)!} \operatorname{tr} \left( U_K(T) A U_K^{\dagger}(T) \mathcal{L}_{I, \xi_1} \circ \dots \circ \mathcal{L}_{I, \xi_n+1} \left( \rho_I(\xi_{n+1}) \right) \right). \tag{25}$$

We can then of course immediately bound the inner product

$$|\operatorname{tr}\left(U_{K}(T)AU_{K}^{\dagger}(T)\mathcal{L}_{I,t_{1}}\circ\ldots\circ\mathcal{L}_{I,t_{n}+1}\left(\rho_{I}(t_{n+1})\right)\right)|\leq||A|||\mathcal{L}_{I,t\xi_{1}}\circ\ldots\circ\mathcal{L}_{I,\xi_{n}+1}\left(\rho_{I}(\xi_{n+1})\right)||_{1}$$
(26)

by a direct application of Hölder's inequality. Note that all Schatten norms are unitarily invariant, so when the map  $\mathcal{L}$  is bounded, we can apply the subsequent operator norm inequalities

$$\|\mathcal{L}_{I,t\xi_1} \circ \dots \circ \mathcal{L}_{I,\xi_n+1} \left(\rho_I(\xi_{n+1})\right)\|_1 \le \|\mathcal{L}\|_{1\to 1}^{n+1}.$$
 (27)

It is safe to assume that a Lindblad operator  $\mathcal L$  acting on a finite dimensional system, such as a collection of qubits, is bounded. However, we also consider the case of a first-principle noise model that can even be non-Markvoian. In this setting the operator  $\mathcal L(\rho) = -[V,\rho]$  is expected to couple to an arbitrary large bath and V may contain unbounded operators, such as bosonic operators. In such a setting an upper bound in terms of an operator norm of  $\mathcal L$  is a moot point. Yet, in this case we can transform the evolution into the Heisenberg picture  $\mathcal L^*$ , for the observable  $A(0) = A_S \otimes \mathbb 1$ , and look at the equations for A(t) instead. The almost identical analysis as performed above can be carried through, but this time we can obtain a bound on

$$|\operatorname{tr}\left(\rho_{I}(0)\mathcal{L}_{I,\xi_{n+1}}^{*}\circ\ldots\circ\mathcal{L}_{I,t\xi_{1}}^{*}(A(t))\right)| \leq ||A(t)|||\mathcal{L}_{I,t\xi_{1}}\circ\ldots\circ\mathcal{L}_{I,\xi_{n+1}}(\rho_{I}(0))||_{1}.$$
(28)

We obtain almost the same type of bound from Hölder's inequality since  $\|A(t)\| \le \|A\|$  for contractive evolutions, where the sole difference is now that  $\|\mathcal{L}_{I,t\xi_1} \circ \ldots \circ \mathcal{L}_{I,\xi_{n+1}} \left(\rho_I(0)\right)\|_1 \le l_{n+1}$  only depends on the initial state. Since we now consider the action of the operators in V on a well-behaved initial state  $\rho(0)$ , we can assume that  $l_{n+1}$  is a reasonable bound. In either case, we will now write for the bound on  $|R_{n+1}(\lambda, \mathcal{L}, T)|$  from now on:

$$|R_{n+1}(\lambda, \mathcal{L}, T)| \le ||A|| \ l_{n+1} \ \frac{\lambda^{n+1} T^{n+1}}{(n+1)!}.$$
 (29)

The coefficients  $a_k$  can be bounded in a similar fashion. Note that, if we assume that noise acts locally on each qubit, such as for instance, when the dissipator  $\mathcal{L}$  corresponds to single-qubit depolarizing noise, so that  $\mathcal{L}(\rho) = \sum_{i=1}^N (\frac{1}{2} \mathrm{tr}_{[i]}(\rho) - \rho)$ . We have that  $||\mathcal{L}||_{1\to 1} = \mathcal{O}(N)$  is extensive in the system size. A similar argument holds for the case when the individual qubits couple to a bath. From this we can deduce that for local noise we typically find  $l_k = \mathcal{O}(N^k)$  as mentioned in the main text, and that  $|a_k| \leq \mathcal{O}((NT)^k)$ .

It is also worthwhile to point out the following observation. For different types of error terms  $\mathcal{L}$  it may happen that not all powers of  $\lambda$  are present in the expansion. It is conceivable that some system bath interactions could lead to an expansion in only even powers of  $\lambda$ . If this occurs, the Richardson extrapolation method is particularly efficient, since a higher order of precision can be obtained with fewer values of  $\lambda_j$ .

#### II Experimental rescaling of the noise parameter

In order to apply Richardson extrapolation, we have to be able to evaluate  $E_K(\lambda)$  for different values of  $\lambda$ . In an actual experiment, we can't directly control the parameter  $\lambda$ : however, we may control the evolution K(t). To this end, we introduce a rescaling. We redefine

<span id="page-6-0"></span>
$$T \to T' = cT$$
 as well as  $J_{\alpha}(t) \to J'_{\alpha}(t) = c^{-1}J_{\alpha}(c^{-1}t)$  from which also  $\rho(t) \to \rho'(t) = \rho(c^{-1}t)$ . (30)

We claim that this rescaling maps  $\rho'_{\lambda}(T') = \rho_{c\lambda}(T)$  if the noise operator  $\mathcal L$  does not depend on the Hamiltonian couplings  $J_{\alpha}(t)$  and is constant in time. This rescaled density matrix then leads to a new evaluation  $E'_{K}(\lambda) \to E_{K}(c\lambda)$  of the expectation value. To see that the rescaling has the desired effect, we again make use of the integral representation of  $\rho_{\lambda}(T)$ , for which we can write now in the Schrödinger picture

$$\rho_{\lambda}(T) = \rho(0) - i \int_0^T [K(t), \rho(t)] dt + \lambda \int_0^T \mathcal{L}(\rho(t)) dt.$$
(31)

We can now choose a re-parametrization of the evolution  $c^{-1}J_{\alpha}(c^{-1}t)$  and an increased runtime cT, and write

$$\rho_{\lambda}'(T') = \rho(0) - i \int_0^{cT} [K'(t), \rho'(t)] dt + \lambda \int_0^{cT} \mathcal{L}(\rho'(t)) dt$$
(32)

with  $K'(t) = \sum_{\alpha} c^{-1} J_{\alpha}(c^{-1}t) P_{\alpha}$ . If we now substitute the integration variable according to t = ct', we have that dt = cdt', which leads to

<span id="page-7-0"></span>
$$\rho_{\lambda}'(T') = \rho(0) - i \int_{0}^{T} \sum_{\alpha} c^{-1} J_{\alpha}(t') [P_{\alpha}, \rho(t')] c dt' + \lambda \int_{0}^{T} \mathcal{L}(\rho'(t)) c dt'$$

$$= \rho(0) - i \int_{0}^{T} \sum_{\alpha} [K(t'), \rho(t')] dt' + \lambda c \int_{0}^{T} \mathcal{L}(\rho(t')) dt'$$

$$= \rho_{c\lambda}(T).$$
(33)

Hence, rescaling the evolution according to equation (30) leads to an effective rescaling of the dissipative rate  $\lambda$ . This can be done for any constant dissipator  $\mathcal{L}$  and allows the experimenter to evaluate  $E_K(\lambda)$  for different values of  $c\lambda$  so that we can apply the Richardson extrapolation procedure.

Note that for different experimental circumstances, other rescaling methods of the parameter  $\lambda$  may actually be easier to implement. For example, in an optical experiment that is plagued by photon loss, it may be suitable to consider different methods of directly changing the photon loss rate. The only requirement is that the modification of  $\lambda_j$  can be performed sufficiently accurately so the extrapolation can be performed.

#### III Error bounds on the noise-free estimator

Let us now show that the protocol leads to the desired error bound on the estimated expectation value as claimed in the main text. Recall that we first choose a set of n+1 rescaling parameters  $c_0=1< c_1<\ldots< c_n$ , to evolve with respect to the rescaled Hamiltonian  $K^j(t)$  for time  $T_j=c_jT$ . As discussed in the previous section, this evolution leads to a state  $\rho_\lambda^j(T_j)=\rho_{c_j\lambda}(T)$ , c.f. Eq. (33) as was discussed in section II. If we now measure the observable A on these states we obtain for  $j=0\ldots n+1$  the estimates  $\hat{E}_K(c_j\lambda)=E_K(c_j\lambda)+\delta_j$ . Recall the set of equations for  $\gamma_j$  defined in [25] and given in the main text, which requires for the  $\{c_j\}$  that

$$\sum_{l=0}^{n} \gamma_{j} = 1$$

$$\sum_{j=0}^{n} \gamma_{j} c_{j}^{k} = 0 \quad \text{for } k = 1 \dots n.$$
(34)

Now we observe that estimators  $\hat{E}_K(c_j\lambda)$  can be expressed as

$$\hat{E}_K(c_j\lambda) = E^* + \sum_{k=1}^n a_k c_j^k \lambda^k + R(c_j\lambda, \mathcal{L}, T) + \delta_j$$
(35)

due to the expansion (22) discussed in section I. Recall now the definition of our improved estimator  $\hat{E}_K^n(\lambda)$  as given in the

main text,  $\hat{E}_K^n(\lambda) = \sum_{j=0}^n \gamma_j \hat{E}_K(c_j \lambda)$ , for which then

$$\hat{E}_K^n(\lambda) = \sum_{j=0}^n \left( \gamma_j E^* + \sum_{k=1}^n a_k c_j^k \lambda^k + R(c_j \lambda, \mathcal{L}, T) + \delta_j \right)$$

$$= E^* \left( \sum_{j=0}^n \gamma_j \right) + \sum_{k=1}^n a_k \lambda^k \left( \sum_{j=0}^n \gamma_j c_j^k \right) + \left( \sum_{j=0}^n \gamma_j R(c_j \lambda, \mathcal{L}, T) + \delta_j \right). \tag{36}$$

Recall the equations for  $\gamma_j$  from which we can then infer after the application of the triangle inequality

$$|E^* - \hat{E}_K^n(\lambda)| \le \sum_{j=0}^n |\gamma_j| \left( |R(c_j\lambda, \mathcal{L}, T)| + |\delta_j| \right). \tag{37}$$

After the application of the bound  $|R(c_j\lambda, \mathcal{L}, T)| \le ||A|| \ l_{n+1} \ c_j^{n+1}\lambda^{n+1}T^{n+1}((n+1)!)^{-1}$  and the observation that  $c_j \ge 1$ , we can bound the difference with  $\Gamma_n = \sum_{j=0}^n |\gamma_j| c_j^{n+1}$  and obtain the final bound

$$|E^* - \hat{E}_K^n(\lambda)| \le \Gamma_n \left( \delta^* + ||A|| \frac{l_{n+1} \lambda^{n+1} T^{n+1}}{(n+1)!} \right), \tag{38}$$

with  $\delta^* = \max_i |\delta_i|$ .

In the Richardson extrapolation literature [16], two types of sequences  $c_j$  are considered frequently. In the Bulirsch - Stoer series the rescalings are chosen so that  $c_j=h^jc_0$  constitutes an exponential series, which is typically chosen at base h=1/2; but harmonic series have also been frequently applied, e.g. for parameters  $q>1, \eta\geq 0$  one can choose  $c_j=(j+\eta)^{-q}c_0$ . Note that in our experiments we are actually increasing the noise rate starting from the optimal value, whereas it is common in the numerical literature to improve the small parameter, so that  $c_{j+1}\leq c_j$ . The result here is of course the same, and just corresponds to a reordering of the labels when n is finite. For both of the aforementioned cases, a bound on  $\Gamma_n$  has been derived. One is mostly interested in the asymptotic behavior of  $\Gamma_n$  as  $n\to\infty$  in order to analyze the numerical stability of the method. In current experiments we only expect to go to third or forth order, making the stability analysis less relevant.

## Probabilistic error cancellation by resampling

The key idea of our scheme is to represent the ideal circuit as a quasi-probabilistic mixture of noisy ones. Central to this approach is the quasi probability representation (QPR) of the noise-free circuit  $\mathcal{U}_{\beta}$ . We note that quasi-probability distributions have been previously used to construct classical algorithms for simulation of quantum circuits [17, 18]. Our work can be viewed as an application of these methods to the problem of simulating ideal quantum circuits by noisy ones.

The general approach to constructing a QPR for a quantum circuit is the following: Suppose you are given a set of noisy operations  $\Omega = \{\mathcal{O}_1, \dots, \mathcal{O}_m\}$  that can be implemented on a noisy N-qubit device. We assume that we can perform gate tomography [19] to specify the gates with an accuracy that is comparable to the desired accuracy of the ideal circuit. These noisy operations are noisy versions of ideal quantum gates and are assumed to form a full basis of TPCP operations, i.e. an element  $\mathcal{O}_k \in \Omega$  is always of the form

$$\mathcal{O}_k(\rho) = \sum_i O_{i,k} \rho O_{i,k}^{\dagger} \quad \text{with} \quad \sum_i O_{i,k}^{\dagger} O_{i,k} = \mathbb{1}.$$
 (39)

A crucial condition is that the set of noisy operators  $\Omega$  constitutes a basis in the space of TPCP operations that is sufficiently large, so that any ideal, unitary gate  $\mathcal{U}(\rho) = U\rho U^{\dagger}$  can be expressed as a linear combination of noisy gates in  $\Omega$ . Hence, there have to be coefficients  $\eta_{\alpha} \in \mathbb{R}$ , and noisy operations in  $\mathcal{O}_{\alpha} \in \Omega$  so that we can write for any ideal gate in the circuit

$$\mathcal{U}(\rho) = \sum_{\alpha} \eta_{\alpha} \mathcal{O}_{\alpha}(\rho), \quad \forall \rho.$$
 (40)

This linear expansion of  $\mathcal{U}$  can then be cast into the form of a quasi-probability representation.

On real quantum devices we can only apply the noisy operations  $\Omega$ . We say that a circuit of length L in the basis  $\Omega$  is a sequence of L operations from  $\Omega$ . Such a circuit, c.f. Fig 3(b), indexed by  $\alpha = (\alpha_1, \dots, \alpha_L)$  implements a noisy map  $\mathcal{O}_{\alpha} = \mathcal{O}_{\alpha_L} \cdots \mathcal{O}_{\alpha_2} \mathcal{O}_{\alpha_1}$ .

The expectation value of an observable A on the final state produced by a noisy circuit  $\alpha$  is

$$E(\boldsymbol{\alpha}) = \operatorname{Tr} \left[ A \mathcal{O}_{\boldsymbol{\alpha}}(|0\rangle\langle 0|^{\otimes n}) \right].$$

For simplicity, we ignore errors in the initial state preparation and in the final measurement. Such errors can be accounted for by adding dummy noisy operations before each measurement and after each qubit initialization. Furthermore, we shall assume that A is diagonal in the Z-basis and  $||A|| \le 1$ .

The task of simulating an ideal quantum circuit  $\mathcal{U}_{\beta}$ , c.f. Fig. 3(a), of ideal gates  $\mathcal{U}_{\beta} = \mathcal{U}_{\beta_L} \dots \mathcal{U}_{\alpha_2} \mathcal{U}_{\alpha_1}$ , can be reduced to estimating the expectation values  $E(\alpha)$  for a suitable random ensemble of noisy quantum circuits  $\alpha$ . That is, we can obtain estimates for the ideal expectation values

$$E^*(\boldsymbol{\beta}) = \operatorname{Tr}[A \mathcal{U}_{\boldsymbol{\beta}}(|0\rangle\langle 0|^{\otimes n})],$$

after the application of the circuit  $\mathcal{U}_{\beta}$  by estimating noisy circuit outputs. Moreover, the ideal and the noisy circuits act on the same number of qubits and have the same length.

We say that the noisy basis  $\Omega$  simulates an ideal circuit  $\beta$  if there exists a probability distribution  $P_{\beta}(\alpha)$  on the set of noisy circuits  $\alpha \in \Omega_L$  such that

<span id="page-9-0"></span>
$$\mathcal{U}_{\beta} = \gamma_{\beta} \sum_{\alpha \in \Omega_L} P_{\beta}(\alpha) \sigma_{\beta}(\alpha) \mathcal{O}_{\alpha}$$
(41)

for some coefficients  $\sigma_{\beta}(\alpha) = \pm 1$ . We require that the distribution  $P_{\beta}(\alpha)$  is sufficiently simple so that one can efficiently sample  $\alpha$  from  $P_{\beta}(\alpha)$ . The coefficients  $\gamma_{\beta}$ ,  $\sigma_{\beta}(\alpha)$  must be efficiently computable.

![](_page_9_Figure_10.jpeg)

<span id="page-9-2"></span>FIG. 3. (color online) The figure (a) represents the ideal circuit we want to simulate. It is comprised of single- and two-qubit gates  $\{U_{12},\ldots,U_{5}\}$ . We assume that a complete set of noisy gates exist  $\Omega=\{\mathcal{O}_{12}^{\alpha_{12}},\ldots,\mathcal{O}_{5}^{\alpha_{5}}\}$ , which serve as an operator basis in which the action of the ideal set can be expanded. It is then sufficient to sample circuits, as given in figure (b), where the gates are drawn from the probability distribution  $P_{\beta}$  in Eq. (41).

We can see that the estimates of the noisy circuit are related to the ideal circuit probability by substituting Eq. (41) into the definition of  $E^*(\beta)$ . This gives

<span id="page-9-1"></span>
$$E^*(\beta) = \gamma_{\beta} \sum_{\alpha \in \Omega_L} P_{\beta}(\alpha) \sigma_{\beta}(\alpha) E(\alpha). \tag{42}$$

The construction of QPRs with optimal overhead of general operation-dependent noise is an interesting open problem. A preliminary analysis shows that a noisy basis  $\Omega$  that includes noisy versions of all single-qubit and two-qubit Clifford gates, T-gates, and noisy qubit initializations in the X,Y,Z basis can simulate any ideal gate  $\mathcal{U}_{\beta}$  from the Clifford+T gate set with the overhead  $\gamma_{\beta} \leq 1 + O(\epsilon)$ , provided that each noisy operation is  $\epsilon$ -close to its ideal analogue. Unfortunately, the constant coefficient in this upper bound is far too large to have any practical implications.

Furthermore, the full Clifford group on two-qubits contains 11520 gates. It may not be feasible to perform process tomography for each of those gates. We shall see that for certain noise models, such as the amplitude damping noise, QPRs can be constructed only if the noisy basis  $\Omega$  includes some qubit initialization maps. In particular, noisy circuits  $\alpha$  that appear in Eq. (41) may apply qubit initializations at intermediate time steps, even though the ideal circuit  $\beta$  initializes all the qubits at the very first step. All QPRs constructed below preserve the circuit depth. That is, if the ideal circuit  $\beta$  has depth d then all noisy circuits  $\alpha$  in Eq. (41) have depth at most d.

## IV Minimal overhead decomposition of noise free circuit

Let us discuss how to construct QPRs with a small overhead. For concreteness, we choose the ideal gate set  $\Gamma$  as the Clifford+T basis. It includes the identity gate I, the Hadamard gate H, phase-shift gates  $S = \operatorname{diag}[1,i]$  and  $T = \operatorname{diag}[1,e^{i\pi/4}]$ , and the CNOT. For technical reasons, we shall assume that each CNOT is followed by single-qubit gates (that could be identity gates). We shall consider toy noise models usually studied in the quantum fault-tolerance theory: the depolarizing noise and the amplitude damping noise.

First let us describe product QPRs that can be constructed independently for each gate in the ideal circuit. Consider a fixed ideal gate  $\mathcal{U}_{\beta} \in \Gamma$ . Let  $\mathcal{O}_1, \dots, \mathcal{O}_p \in \Omega$  be the list of all noisy operations whose support is contained in the support of  $\mathcal{U}_{\beta}$ . Consider the following linear program with 2p real variables  $\mu_1, \dots, \mu_p, \eta_1, \dots, \eta_p$ .

<span id="page-10-0"></span>
$$\mathbf{minimize} \quad \sum_{\alpha=1}^{p} \mu_{\alpha} \tag{43}$$

<span id="page-10-1"></span>subject to 
$$\begin{cases} \eta_{\alpha} \leq \mu_{\alpha} \\ -\eta_{\alpha} \leq \mu_{\alpha} \\ \mathcal{U}_{\beta} = \sum_{\alpha=1}^{p} \eta_{\alpha} \mathcal{O}_{\alpha}. \end{cases}$$
(44)

Suppose  $\{\mu_{\alpha}, \eta_{\alpha}\}$  is the optimal solution of the program. Note that  $\mu_{\alpha} = |\eta_{\alpha}|$  for all  $\alpha$  since otherwise the objective function can be decreased. Define  $\gamma_{\beta} = \sum_{\alpha=1}^{p} \mu_{p}$ ,  $P_{\beta}(\alpha) = \mu_{\alpha}/\gamma_{\beta}$ , and  $\sigma_{\beta}(\alpha) = \operatorname{sgn}(\eta_{\alpha})$ . Then

<span id="page-10-2"></span>
$$\mathcal{U}_{\beta} = \gamma_{\beta} \sum_{\alpha=1}^{p} P_{\beta}(\alpha) \sigma_{\beta}(\alpha) \mathcal{O}_{\alpha}, \tag{45}$$

which is a gate-wise version of the QPR Eq. (41). We shall say that a noisy basis  $\Omega$  simulates a gate  $\mathcal{U}_{\beta}$  with the overhead  $\gamma_{\beta}$  if the linear program Eqs. (43,44) has a feasible solution with value  $\gamma_{\beta}$ . A product QPR of the ideal circuit  $\beta$  is defined as a product of all gate-wise QPRs Eq. (45). It gives  $\gamma_{\beta} = \gamma_{\beta_1} \cdots \gamma_{\beta_L}$ ,  $P_{\beta}(\alpha) = P_{\beta_1}(\alpha_1) \cdots P_{\beta_L}(\alpha_L)$  and  $\sigma_{\beta}(\alpha) = \sigma_{\beta_1}(\alpha_1) \cdots \sigma_{\beta_L}(\alpha_L)$ . The assumption that all noisy operations  $\mathcal{O}_{\alpha}$  in Eq. (44) act non-trivially only within the support of  $\mathcal{U}_{\beta}$  allows one to restrict Eq. (44) to operations acting on at most two qubits. Such operations can be represented by real matrices of size  $16 \times 16$  by computing matrix elements of  $\mathcal{O}_{\alpha}$  and  $\mathcal{U}_{\beta}$  in the Pauli basis. Thus the program Eqs. (43,44) can be solved in time O(1). Since the ideal gate set has size  $O(n^2)$ , product QPRs can be computed in time  $O(n^2)$ . Furthermore, if two ideal gates have disjoint supports, then the gate-wise QPRs defined in Eq. (45) have disjoint supports. Thus product QPRs preserve the circuit depth.

#### V Depolarizing noise cancellation and numerical results

Let us illustrate the construction of product QPRs using the depolarizing noise as an example. Let  $\mathcal{D}_k$  be the  $\epsilon$ -depolarizing channel on k qubits that returns the maximally mixed state with probability  $\epsilon$  and does nothing with probability  $1-\epsilon$ . Define a noisy version of a k-qubit unitary gate  $\mathcal{U}$  as  $\mathcal{D}_k\mathcal{U}$ . Define a noisy basis  $\Omega$  by multiplying ideal gates on the left by arbitrary Pauli operators and adding the depolarizing noise. Thus  $\Omega$  is a set of operations  $\mathcal{O}_{\alpha} = \mathcal{D}_k\mathcal{P}\mathcal{U}$ , where  $\mathcal{U} \in \Gamma$  is a k-qubit ideal gate and  $\mathcal{P} \in \{\mathcal{I}, \mathcal{X}, \mathcal{Y}, \mathcal{Z}\}^{\otimes k}$  is a Pauli TPCP map. A Pauli map  $\mathcal{P}$  corresponding to a Pauli operator  $P \in \{I, X, Y, Z\}$  is defined by  $\mathcal{P}(\rho) = P\rho P$ . Here k = 1, 2. We claim that  $\Omega$  simulates ideal single-qubit gates  $\mathcal{U}_{\beta} \in \Gamma$  with the overhead  $\gamma_{\beta} = (1 + \epsilon/2)/(1 - \epsilon)$  and simulates CNOTs with the overhead  $\gamma_{\beta} = (1 + 7\epsilon/8)/(1 - \epsilon)$ .

Indeed, suppose  $\mathcal{U}_{\beta} \in \Gamma$  is a single-qubit gate. Let us look for a solution of Eq. (44) in the form  $\mathcal{O}_{\alpha} = \mathcal{D}_1 \mathcal{P} \mathcal{U}_{\beta}$ , where  $\mathcal{P} \in \{\mathcal{I}, \mathcal{X}, \mathcal{Y}, \mathcal{Z}\}$ . Then Eq. (44) is equivalent to

$$\mathcal{D}_1^{-1} = \eta_1 \mathcal{I} + \eta_2 \mathcal{X} + \eta_3 \mathcal{Y} + \eta_4 \mathcal{Z}.$$

One can easily check that the optimal solution minimizing  $\sum_{\alpha} |\eta_{\alpha}|$  is  $\eta_{1} = 1 + 3\epsilon/4(1 - \epsilon)$  and  $\eta_{\alpha} = -\epsilon/4(1 - \epsilon)$  for  $\alpha = 2, 3, 4$ . Therefore  $\gamma_{\beta} = \sum_{\alpha} |\eta_{\alpha}| = (1 + \epsilon/2)/(1 - \epsilon)$ . The CNOT is simulated in a similar fashion by representing  $\mathcal{D}_{2}^{-1}$  as a linear combination of two-qubit Pauli maps. The random ensemble of noisy circuits  $\mathcal{O}_{\alpha}$  that simulates an ideal circuit  $\mathcal{U}_{\beta}$  is constructed in three steps:

1. Start from the ideal circuit,  $\mathcal{O}_{\alpha} = \mathcal{U}_{\beta}$ .

- 2. Modify O<sup>α</sup> by adding a Pauli X, Y, Z after each single-qubit gate with probability p<sup>1</sup> = /(4+2). The gate is unchanged with probability 1 − 3p1.
- 3. Modify O<sup>α</sup> by adding a Pauli IX, IY, . . . , ZZ after each CNOT with probability p<sup>2</sup> = /(16 + 14). The CNOT is unchanged with probability 1 − 15p2.

The resulting circuit is then implemented on a noisy device (which adds the depolarizing noise after each gate) and the final readout string x is recorded. By generating M samples of x one can estimate E<sup>∗</sup> (β) using Eq. (10) of the main text. The sign function σβ(α) is equal to (−1)<sup>r</sup> , where r is the number of Pauli operators added to the ideal circuit U<sup>β</sup> to obtain Oα.

## *Numerical simulations*

The error cancellation method was tested numerically for small Clifford+T circuits subject to the depolarizing noise. We choose the ideal circuit U<sup>β</sup> as a composition of d alternating layers of gates, with each layer being either a tensor product of n single-qubit gates I, H, S, T (for odd layers) or a tensor product of n/2 CNOTs (for even layers). The resulting circuit U<sup>β</sup> has depth d. Simulations were performed for 500 random circuits U<sup>β</sup> as above with the initial state |+i <sup>⊗</sup>n. Each single-qubit gate was picked randomly from the set {I, H, S, T}. Control and target qubits for each CNOT were picked at random.

For each ideal circuit U<sup>β</sup> we choose the observable A as a projector onto the subset of 2 <sup>n</sup>−<sup>1</sup> basis states x ∈ {0, 1} <sup>n</sup> whose probability in the final state of U<sup>β</sup> is above the median value. In other words,

$$A = \sum_{x \in S} |x\rangle \langle x|, \qquad S = \arg\min_{\substack{S \subseteq \{0,1\}^n \\ |S| = 2^{n-1}}} \sum_{x \in S} \langle x|\mathcal{U}_{\beta}(|+\rangle \langle +|^{\otimes n})|x\rangle.$$

By construction, E<sup>∗</sup> (β) ≥ 1/2 for any circuit β. Furthermore, we observed that E<sup>∗</sup> (β) is well separated from 1/2 for most of the circuits see Fig. [4.](#page-11-0) Recall that we define a noisy version of a k-qubit unitary gate U as DkU, where

![](_page_11_Figure_9.jpeg)

<span id="page-11-0"></span>FIG. 4. Distribution of the ideal circuits according to their output probability E ∗ (β).

$$\mathcal{D}_k(\rho) = (1 - \epsilon)\rho + \frac{\epsilon I}{2^k} \text{Tr}(\rho)$$

is the depolarizing channel on k qubits. Noise was added after all gates including the identity gates. In this case the total simulation overhead γ<sup>β</sup> depends only on the number of qubits and the circuit depth, namely

$$\gamma_{\beta} = \left[\frac{1+\epsilon/2}{1-\epsilon}\right]^{nd/2} \cdot \left[\frac{1+7\epsilon/8}{1-\epsilon}\right]^{nd/4}.$$

Consider a fixed ideal circuit U<sup>β</sup> and let Pβ(α), O<sup>α</sup> be the random ensemble of noisy circuits obtained from U<sup>β</sup> by inserting random Pauli operators and adding noise as described in the main text. Instead of using the estimate Eq. (10) of the main text for the ideal output probability  $E^*(\beta)$  we opted for a slightly optimized estimate. It is defined by dividing the total budget of M runs into K groups such that the j-th group contains  $M_j$  runs

$$M = \sum_{j=1}^{K} M_j.$$

Define a random variable

<span id="page-12-0"></span>
$$\hat{E}(\boldsymbol{\beta}) \equiv \gamma_{\boldsymbol{\beta}} K^{-1} \sum_{j=1}^{K} \sigma_{\boldsymbol{\beta}}(\boldsymbol{\alpha}^{j}) \frac{1}{M_{j}} \sum_{a=1}^{M_{j}} \langle x_{j}^{a} | A | x_{j}^{a} \rangle, \tag{46}$$

where  $\alpha^1, \ldots, \alpha^K$  are independent samples drawn from the distribution  $P_{\beta}(\alpha)$  and  $x_j^a \in \{0,1\}^n$  are readout strings obtained by measuring each qubit of the final state  $\mathcal{O}_{\alpha^j}(\rho_{in})$  in the Z-basis. We prepare a fresh copy of the final state to generate each string  $x_j^a$ . Thus computing  $\hat{E}(\beta)$  requires M runs of the noisy circuits with each run producing a single readout string. One can easily check that  $\hat{E}(\beta)$  is an unbiased estimator of  $E^*(\beta)$  for any choice of  $\{M_j\}$ . Our goal is to choose  $\{M_j\}$  that minimize the variance of  $\hat{E}(\beta)$  for a fixed M. One can easily check that the optimal choice is

$$M_j \approx \frac{M\sigma_j}{\sum_{i=1}^K \sigma_i}$$

where  $\sigma_j^2 = E(\alpha^j) - E(\alpha^j)^2$ . In order to choose optimal values of  $M_j$ , one has to run each circuit  $\alpha^j$  at least a few times, which gives a rough estimate of  $E(\alpha^j)$  and thus  $\sigma_j$ . Numerical simulations were performed for the following parameters:

| number of qubits     | n=6                          |
|----------------------|------------------------------|
| circuit depth        | d=20                         |
| error rate           | $\epsilon = 0.01$            |
| total number of runs | M = 4,000                    |
| simulation overhead  | $\gamma_{\beta} \approx 4.3$ |

Our results are presented on the left panel of Figure 5. For each of  $\approx 500$  ideal circuits  $\boldsymbol{\beta}$  generated at random we computed a simulation precision  $\delta(\boldsymbol{\beta}) \equiv |\hat{E}(\boldsymbol{\beta}) - E^*(\boldsymbol{\beta})|$  where  $\hat{E}(\boldsymbol{\beta})$  is the estimate defined in Eq. (46). The plot on Figure 5, left, shows distribution of the ideal circuits  $\boldsymbol{\beta}$  according to their simulation precision  $\delta(\boldsymbol{\beta})$ . The median value of  $\delta(\boldsymbol{\beta})$  is approximately 0.05. This is consistent with the estimate

$$\delta(\beta) \approx \frac{\gamma_{\beta}}{\sqrt{M}} = \frac{4.3}{\sqrt{4000}} \approx 0.07.$$

We also computed a simulation precision  $\delta_0(\beta)$  that one would obtain by running the circuit  $\beta$  directly on a noisy device without error cancellation, see the right panel of Figure 5. It is defined as  $\delta_0(\beta) \equiv |E(\beta) - E^*(\beta)|$ . For each circuit the output probability  $E(\beta)$  was estimated using M=4,000 circuit runs. Thus the simulations presented on the left and the right panels of Figure 5 have access to exactly the same resources. The median value of  $\delta_0(\beta)$  is approximately 0.15. We conclude that error cancellation significantly improves the simulation precision.

## VI Quasi-probability representation for amplitude-damping noise

A more interesting example is the noise described by the amplitude-damping channel  $\mathcal{A}(\rho)=A_0\rho A_0^\dagger+A_1\rho A_1^\dagger$ , where

$$A_0 = \left[ \begin{array}{cc} 1 & 0 \\ 0 & (1-\epsilon)^{1/2} \end{array} \right] \quad \text{and} \quad A_1 = \epsilon^{1/2} \left[ \begin{array}{cc} 0 & 1 \\ 0 & 0 \end{array} \right].$$

A noisy version of a k-qubit unitary gate  $\mathcal{U}$  is defined as  $\mathcal{A}^{\otimes k}\mathcal{U}$ . In contrast to the previous example, noisy unitary gates  $\mathcal{A}^{\otimes k}\mathcal{U}$  alone cannot simulate any ideal unitary gate. Indeed, assume the contrary. Suppose  $\mathcal{U}_{\beta}$  is a single-qubit gate that has a QPR Eq. (45) with  $\mathcal{O}_{\alpha} = \mathcal{A}\mathcal{V}_{\alpha}$  for some unitary maps  $\mathcal{V}_{\alpha}$ . Rewrite Eq. (45) as

$$\mathcal{A}^{-1} = \gamma_{\beta} \sum_{\alpha=1}^{p} P_{\beta}(\alpha) \sigma_{\beta}(\alpha) \mathcal{V}_{\alpha} \mathcal{U}_{\beta}^{-1}.$$

![](_page_13_Figure_1.jpeg)

![](_page_13_Figure_2.jpeg)

<span id="page-13-0"></span>FIG. 5. Simulation precision for  $\approx 500$  randomly generated ideal Clifford+T circuits on n=6 qubits with depth d=20. The left and the right panels show results for simulations with and without error cancellation. In both cases each ideal circuit was simulated by M=4000runs of the noisy circuit.

Since the maps  $V_{\alpha}U_{\beta}^{-1}$  are unital, we infer that  $A^{-1}$  and A are unital which is false. Thus Eq. (45) has no solutions.

To overcome this problem we shall extend the noisy basis by adding state preparations. Also we shall employ non-product QPRs. Given a single-qubit state  $|\psi\rangle$ , define a state preparation map

$$\mathcal{P}_{|\psi\rangle}(\rho) = \text{Tr}(\rho) \cdot |\psi\rangle\langle\psi|. \tag{47}$$

Let  $S(\rho) = S\rho S^{-1}$  be the S-gate considered as a TPCP map. Define a noisy basis  $\Omega$  that includes noisy state preparations  $\mathcal{AP}_{|\psi\rangle}$  with  $|\psi\rangle = |+\rangle, |-\rangle, |0\rangle, |1\rangle$ , noisy single-qubit gates  $\mathcal{AU}_{\beta}$ ,  $\mathcal{AS}^{\pm 1}\mathcal{U}_{\beta}$  for each ideal single-qubit gate  $\mathcal{U}_{\beta} \in \Gamma$ , and noisy two-qubit gates

$$\mathcal{A}_c \mathcal{A}_t \mathcal{S}_c^y \mathcal{S}_t^z \mathcal{U}_{\text{cnot}}, \quad y, z \in \{0, \pm 1\}$$

where c, t are the control and the target qubits of a CNOT gate  $\mathcal{U}_{cnot} \in \Gamma$ . Here the subscripts indicate qubits acted upon by each map. We claim that this noisy basis  $\Omega$  simulates any ideal Clifford+T circuit  $\beta$  with the overhead

<span id="page-13-1"></span>
$$\gamma_{\beta} \le \gamma^{L_1 + 2L_2}, \quad \gamma \equiv \frac{1 + \epsilon}{1 - \epsilon},$$
(48)

where  $L_k$  is the number of k-qubit gates in  $\beta$ . The corresponding QPR Eq. (41) preserves the circuit depth, although it does not have a simple product form as above.

Indeed, consider a single-qubit gate  $\mathcal{U}_{\beta} \in \Gamma$ . Let us look for a solution of Eq. (44) with p=4 and

$$\mathcal{O}_1 = \mathcal{A}\mathcal{U}_\beta, \ \mathcal{O}_2 = \mathcal{A}\mathcal{S}\mathcal{U}_\beta, \ \mathcal{O}_3 = \mathcal{A}\mathcal{S}^{-1}\mathcal{U}_\beta, \ \mathcal{O}_4 = \mathcal{P}_{|0\rangle}.$$

Note that  $\mathcal{P}_{|0\rangle} \in \Omega$  since  $\mathcal{AP}_{|0\rangle} = \mathcal{P}_{|0\rangle}$ . Furthermore, since  $\mathcal{P}_{|0\rangle} = \mathcal{AP}_{|0\rangle}\mathcal{U}_{\beta}$ , one can rewrite Eq. (44) as

<span id="page-13-2"></span>
$$\mathcal{A}^{-1} = \eta_1 \mathcal{I} + \eta_2 \mathcal{S} + \eta_3 \mathcal{S}^{-1} + \eta_4 \mathcal{P}_{|0\rangle}. \tag{49}$$

One can easily check that the optimal solution minimizing  $\sum_{\alpha} |\eta_{\alpha}|$  is

$$\eta_1 = \frac{1}{\sqrt{1-\epsilon}}, \ \eta_2 = \eta_3 = \frac{1-\sqrt{1-\epsilon}}{2(1-\epsilon)}, \ \eta_4 = -\frac{\epsilon}{1-\epsilon}.$$

Therefore,  $\Omega$  simulates  $\mathcal{U}_{\beta}$  with the overhead  $\sum_{\alpha} |\eta_{\alpha}| = \gamma$ , where  $\gamma$  is defined in Eq. (48). Next consider the CNOT gate  $\mathcal{U}_{\mathrm{cnot}} \in \Gamma$ . Consider a decomposition of  $\mathcal{A}_c^{-1} \mathcal{A}_t^{-1}$  obtained by applying Eq. (49) twice. Multiplying this decomposition on the right by  $\mathcal{U}_{\text{cnot}}$  and on the left by  $\mathcal{A}_c \mathcal{A}_t$  one obtains

<span id="page-13-3"></span>
$$\mathcal{U}_{\text{cnot}} = \sum_{\alpha} \eta_{\alpha} \mathcal{O}'_{\alpha} \mathcal{O}_{\alpha}, \quad \sum_{\alpha} |\eta_{\alpha}| = \gamma^{2}$$
(50)

where  $\mathcal{O}_{\alpha} = \mathcal{A}_c \mathcal{A}_t \mathcal{S}_c^y \mathcal{S}_t^z \mathcal{U}_{\mathrm{cnot}} \in \Omega$  is a valid noisy operation and  $\mathcal{O}'_{\alpha}$  is either identity or a state preparation map  $\mathcal{P}_{|0\rangle}$  applied to the control and/or target qubits. Here we noted that  $\mathcal{A}\mathcal{P}_{|0\rangle} = \mathcal{P}_{|0\rangle}\mathcal{A}$ . Although  $\mathcal{O}'_{\alpha}\mathcal{O}_{\alpha}$  might not be a valid noisy operation from  $\Omega$ , we may merge  $\mathcal{O}'_{\alpha}$  with the next gate applied after the CNOT. Indeed, by assumption, each CNOT in the ideal circuit is followed by some single-qubit gates  $\mathcal{U}_c$  and  $\mathcal{U}_t$  applied to the control and the target qubits. The gates I, S, T can be absorbed into  $\mathcal{P}_{|0\rangle}$  since they act trivially on the state  $|0\rangle$ . The only non-trivial case is when  $\mathcal{P}_{|0\rangle}$  is merged with the Hadamard gate. In this case the latter is replaced by the state preparation  $\mathcal{P}_{|+\rangle}$ .

Since  $\mathcal{P}_{|+\rangle}$  can now appear in the ideal circuit, we must be able to use noisy operations from  $\Omega$  to simulate  $\mathcal{P}_{|+\rangle}$ . Let us look for a solution of Eq. (44) with  $\mathcal{U}_{\beta} \equiv \mathcal{P}_{|+\rangle}$  in the form

<span id="page-14-0"></span>
$$\mathcal{P}_{|+\rangle} = \eta_1 \mathcal{A} \mathcal{P}_{|+\rangle} + \eta_2 \mathcal{A} \mathcal{P}_{|-\rangle} + \eta_3 \mathcal{A} \mathcal{P}_{|1\rangle}. \tag{51}$$

Note that the righthand side of Eq. (51) contains only noisy operations from  $\Omega$ . One can rewrite Eq. (51) as

$$|+\rangle\langle +| = \eta_1 \mathcal{A}(|+\rangle\langle +|) + \eta_2 \mathcal{A}(|-\rangle\langle -|) + \eta_3 \mathcal{A}(|1\rangle\langle 1).$$

The optimal solution minimizing  $\sum_{\alpha} |\eta_{\alpha}|$  is

$$\eta_{1,2} = \pm \frac{1}{2} \left( \frac{1}{\sqrt{1-\epsilon}} \pm \frac{1-2\epsilon}{1-\epsilon} \right), \quad \eta_3 = \frac{\epsilon}{1-\epsilon}.$$

Therefore  $\Omega$  simulates the ideal state preparation  $\mathcal{P}_{|+\rangle}$  with the overhead  $\gamma' = \sum_{\alpha} |\eta_{\alpha}| \leq \gamma$ , where  $\gamma$  is defined in Eq. (48).

A QPR of the ideal circuit  $\beta$  with the overhead Eq. (48) is constructed in two steps. First, one applies the decomposition Eq. (50) to each CNOT of  $\beta$  and merges state preparation maps  $\mathcal{P}_{|0\rangle}$  that appear in  $\mathcal{O}'_{\alpha}$  (if any) with the single-qubit gates of  $\beta$  following the CNOT. Now all CNOT gates are replaced by noisy gates from  $\Omega$ . The rest of the circuit consists of single-qubit gates  $\mathcal{U}_{\beta} \in \Gamma$  and state preparations  $\mathcal{P}_{|+\rangle}$ . At the second step, each of these ideal operations is replaced by its QPR constructed above. Note that each CNOT contributes  $\gamma^2$  to the total overhead  $\gamma_{\beta}$ , see Eq. (50). Each single-qubit gate  $\mathcal{U}_{\beta} \in \Gamma$  or a state preparation  $\mathcal{P}_{|+\rangle}$  contributes at most  $\gamma$  to the total overhead. This proves Eq. (48).
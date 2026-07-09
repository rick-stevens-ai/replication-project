# **Sparse non-Markovian Noise Modeling of Transmon-Based Multi-Qubit Operations**

Yasuo Od[a](https://orcid.org/0000-0002-4243-8532) , <sup>1</sup> Kevin Schultz [,](https://orcid.org/0000-0002-2664-6227) <sup>2</sup> Leigh Norris,<sup>2</sup> Omar Shehab [,](https://orcid.org/0000-0002-1689-6046) <sup>3</sup> and Gregory Quiroz [1](https://orcid.org/0000-0003-4329-1445),2[,\\*](#page-0-0) 1 *William H. Miller III Department of Physics & Astronomy, [Johns Hopkins University,](https://ror.org/00za53h95) Baltimore, Maryland 21218, USA [Johns Hopkins Applied Physics Laboratory,](https://ror.org/029pp9z10) Laurel, Maryland 20723, USA* 3 *IBM Quantum, [IBM Thomas J Watson Research Center,](https://ror.org/0265w5591) Yorktown Heights, New York, USA*

![](_page_0_Picture_3.jpeg)

(Received 20 December 2024; revised 2 January 2026; accepted 17 March 2026; published 12 May 2026)

The influence of noise on quantum dynamics is one of the main factors preventing current quantum processors from performing accurate quantum computations. Sufficient noise characterization and modeling can provide key insights into the effect of noise on quantum algorithms and inform the design of targeted error protection protocols. However, constructing effective noise models that are sparse in model parameters, yet predictive can be challenging. In this work, we present an approach for effective noise modeling of multi-qubit operations on transmon-based devices. Through a comprehensive characterization of seven devices offered by the IBM Quantum Platform, we show that the model can capture and predict a wide range of single- and two-qubit behaviors, including non-Markovian effects resulting from spatiotemporally correlated noise sources. The model's predictive power is further highlighted through multi-qubit dynamical decoupling demonstrations and an implementation of the variational quantum eigensolver. As a training proxy for the hardware, we show that the model can predict expectation values within a relative error of 0.5%; this is a sevenfold improvement over default hardware noise models. Through these demonstrations, we highlight key error sources in superconducting qubits and illustrate the utility of reduced noise models for predicting hardware dynamics.

#### DOI: [10.1103/lx8x-z29x](http://dx.doi.org/10.1103/lx8x-z29x)

# **I. INTRODUCTION**

Superconducting qubits have emerged as one of the most promising quantum technologies for realizing practical quantum computing. Many types of superconducting qubit devices have been developed, and the field is rapidly evolving [\[1,](#page-33-0)[2\]](#page-33-1). Among the assortment of superconducting qubits, the transmon is specifically designed to minimize sensitivity to charge noise [\[3\]](#page-33-2) and has been at the core of recent breakthroughs [\[4](#page-33-3)[–9\]](#page-33-4). With the advent of enhanced control capabilities in cloud-based quantum computing such as IBM's Quantum Platform (IBMQP) [\[10\]](#page-33-5), transmon-based devices have become a mainstream architecture employed to test state-of-the-art quantum algorithms.

Despite advancements in scale and quality, noise in superconducting qubit architectures poses a crucial

*Published by the American Physical Society under the terms of the [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/) license. Further distribution of this work must maintain attribution to the author(s) and the published article's title, journal citation, and DOI.*

challenge. In order to manage noise in quantum applications, a wide range of techniques have been devised to suppress [\[11–](#page-33-6)[14\]](#page-33-7), avoid [\[15–](#page-33-8)[19\]](#page-34-0), correct [\[20](#page-34-1)[,21\]](#page-34-2), and mitigate [\[22–](#page-34-3)[29\]](#page-34-4) errors. The benefits of many of these approaches have been showcased on superconducting hardware via demonstrations of dynamical decoupling (DD) [\[30](#page-34-5)[–34\]](#page-34-6), decoherence-free subspaces [\[35–](#page-34-7)[37\]](#page-34-8), quantum error correcting codes [\[9,](#page-33-4)[38–](#page-34-9)[43\]](#page-34-10), and various quantum error mitigation protocols [\[44–](#page-34-11)[47\]](#page-34-12).

Many error management (EM) protocols rely on knowledge of the underlying noise processes. Such information can be leveraged for the purposes of ensuring that specific assumptions are satisfied (e.g., Markovianity). It can also be crucial in assessing the inherent robustness and susceptibility of an EM protocol—and more generally, any quantum algorithm—to hardware-relevant noise sources. These can be key steps in properly devising targeted EM protocols and noise robust quantum algorithms.

The most common approaches to modeling noisy quantum dynamics rely on the quantum channel formalism, quantum master equations (MEs), or the stochastic Hamiltonian formalism. The first approach involves applying a composition of quantum error maps before or after an ideal gate operation. The channel representation aims

<span id="page-0-0"></span><sup>\*</sup>Contact author: gregory.quiroz@jhuapl.edu

to sacrifice modeling of intra-gate dynamics for simplicity [\[48\]](#page-34-13). Furthermore, there is typically an assumption of Markovianity (i.e., memoryless environment) which in part results in neglecting potential inter-gate correlations. In contrast, MEs are based on physically motivated differential equations that arise from the theory of open quantum systems [\[48–](#page-34-13)[50\]](#page-34-14). They allow for more accurate descriptions of Markovian and non-Markovian system-environment interactions acting during gate operations, at the expense of added model and computational complexity.

The stochastic Hamiltonian formalism relies on modeling system-environment interactions via a semiclassical Hamiltonian [\[51–](#page-34-15)[55\]](#page-35-0). System operators couple to stochastic, time-dependent, variables as opposed to additional quantum degrees of freedom. This mean-field approach enables modeling of noisy quantum dynamics resulting from spatiotemporally correlated error processes by averaging time evolved quantum states over random realizations of the noise. The advantage of the stochastic Hamiltonian approach lies in the trade-off between Hilbert space size and parametric complexity, which has proven particularly useful when non-Markovian noise is present [\[56](#page-35-1)[,57\]](#page-35-2).

Each strategy has been investigated as a means for modeling noise in superconducting qubits. Models based on compositions of Markovian quantum channels have had variable success [\[58](#page-35-3)[–61\]](#page-35-4). Sparse Pauli-Lindblad models, in particular [\[62](#page-35-5)[,63\]](#page-35-6), have recently proven advantageous in informing error mitigation strategies used to demonstrate a variational algorithm implementation with more than 100 qubits [\[5\]](#page-33-9). This, however, comes at the cost of noise tailoring via Pauli twirling [\[64–](#page-35-7)[67\]](#page-35-8), which can incur progressively larger sampling overheads as system size increases.

ME-based techniques have achieved substantially more success in modeling superconducting qubit devices. Although the presence of Markovian environmental noise sources is prominently observed in superconducting qubits [\[2\]](#page-33-1), recent studies have highlighted significant contributions from non-Markovian sources as well. For example, Post-Markovian [\[68](#page-35-9)[,69\]](#page-35-10) and Redfield [\[70,](#page-35-11)[71\]](#page-35-12) based MEs have shown to agree well with single- and two-qubit demonstrations. In addition, extensions of the Lindblad master equation (LME) [\[48,](#page-34-13)[72,](#page-35-13)[73\]](#page-35-14) that include non-Markovian contributions via stochastic unraveling [\[74\]](#page-35-15) or the addition of quantum degrees of freedom [\[75](#page-35-16)[,76\]](#page-35-17) have also shown promise in the study of multi-qubit dynamics. However, computational overheads such as obtaining solutions to multi-qubit dynamical equations, model training costs, and tomographical measurements must be balanced to ensure scalability.

The stochastic Hamiltonian formalism has also shown success in modeling non-Markovian dynamics in superconducting qubits. It has shown utility in capturing dephasing processes due to, for example, randomly fluctuating magnetic fields [\[2\]](#page-33-1). The formalism has been employed in studies of spatiotemporally correlated noise in single [\[77,](#page-35-18)[78\]](#page-35-19) and two-qubit [\[79\]](#page-35-20), as well as qudit [\[80\]](#page-35-21), systems. Extensions to larger quantum systems poses challenges, specifically when attempting to perform complete characterization of the Hamiltonian. For this reason, the stochastic Hamiltonian formalism is most applicable for effective modeling where sparse characterization is sufficient.

In this study, we develop a self-consistent hybrid noise model that integrates the channel formalism, MEs, and the stochastic Hamiltonian formalism into a *single predictive framework* for superconducting qubit hardware. Each of these techniques originate from distinct areas of modeling and characterization, and although standard in isolation, they are typically not combined. We demonstrate that a unification of these techniques can enable simultaneous and efficient characterization of noise processes that span fundamentally different physical origins and timescales.

This unified construction allows us to capture, within one model, both fast Markovian decoherence and slow, temporally correlated non-Markovian effects. Importantly, our method aims to balance sparsity in model parameters, and thus the required number of characterization experiments, with predictive power. Through extensive comparisons to experimental data, we demonstrate that this model not only predicts a wide range of hardware dynamics but also serves as an accurate proxy simulator that can be employed for training and benchmarking of variational quantum algorithms [\[81\]](#page-35-22). As such, the novelty lies not in a new microscopic error model, but in a unified, microscopically grounded, and experimentally validated framework that connects multiple noise mechanisms and yields a coherent predictive methodology.

Specifically, the model is based on compositions of faulty single- and two-qubit gate operations. Each gate is constructed using the LME with extended degrees of freedoms to account for non-Markovian spatiotemporally correlated noise sources. Classical degrees of freedom are specifically included to capture temporal features of qubit dephasing and control noise during gate operations. Quantum degrees of freedom enable modeling of spatial correlations due to two-level system (TLS) interactions and quantum crosstalk [\[82\]](#page-35-23). The model is parameterized by ten parameters per qubit and three parameters per qubit pair, that can be learned through a small number of characterization experiments.

With an eye towards balancing informational completeness with protocol efficiency, we focus on simplicity in the design of the characterization protocols. Thus, we do not depend upon tomographical methods that are traditionally resource intensive, such as gate-set tomography [\[83](#page-35-24)[,84\]](#page-35-25) or process tensor methods [\[85](#page-35-26)[,86\]](#page-35-27) to provide a detailed analysis of the effective noise channels. Instead, we consider a suite of canonical noise amplification circuits to learn model parameters for both Markovian and non-Markovian noise sources (see Refs. [76,87] for a similar approach). Key to our characterization procedure is quantum noise spectroscopy (QNS) [56,79,88–94]. QNS draws on the filter function formalism (FFF) [95–99] and carefully tailored control sequences to probe the spectral properties of system-environment interactions via measurement of the system's evolution.

It is through this suite of characterization experiments that we perform an extensive study of superconducting qubit devices offered by the IBMQP. Examining 39 qubits across seven devices, we comprehensively characterize Markovian and non-Markovian noise sources. Therein, we elucidate important details about correlated dephasing and control noise and the presence of TLSs on IBMQP devices.

The learned parameters are combined with the single and two-qubit models and shown to accurately predict a variety of quantum circuits. Randomized benchmarking (RB) [100] provides a benchmark to assess the model's ability to correctly predict single-qubit gate error rates captured by routine IBMQP calibrations. We go on to show that the model conveys strong agreement with state-dependent dynamics observed in multi-qubit DD sequences and a small-scale quantum algorithm. In particular, we train a variational quantum eigensolver (VQE) designed to find the ground state of molecular hydrogen H<sub>2</sub> and demonstrate that our noise model can serve as a surrogate to the hardware. It is shown that a relative error of 0.5% is achieved between hardware and the noise model, a sevenfold improvement over IBMQP's default hardware error models.

Together, our model characterization and validation studies provide strong evidence for the viability of the proposed model. Moreover, they highlight key noise sources for the current generation of superconducting qubits and establishes a simple yet flexible framework for noise modeling that may be extended or adapted to other cloud-based hardware platforms. This work illustrates the potential utility of reduced noise models that draw on aspects of both MEs and channel representations to describe complex quantum dynamics in superconducting qubit systems. Crucially, this approach does *not* require low-level hardware access, thus uniquely demonstrating that comprehensive and predictive error modeling can be achieved even in highly opaque cloud-based systems.

The structure of this paper is as follows. In Sec. II we introduce the noise model, with emphasis in modeling via the LME. In Sec. III we describe the characterization protocol and the relevant notation. More specifically, in Sec. III B we present a detailed description of the experiments used to characterize the device. Here, we also provide the analytical expressions obtained from solving the LME for each noise amplification circuit described in Sec. II. Section IV presents experimental results obtained

from running the characterization experiments on the IBMQP, as well as model fits and validation through simulation. In Sec. V we apply our noise model on nontrivial applications in order to test its predictability. Section VI describes strategies for extending the noise model to multiqubit circuits and scaling the characterization protocol. We conclude in Sec. VII with a summary of the protocol and results, as well as thoughts on limitations and future work.

#### <span id="page-2-2"></span><span id="page-2-0"></span>II. NOISE MODEL

We begin by defining the noise model utilized throughout this study. It includes both Markovian and non-Markovian noise sources that we effectively capture by the LME

$$\dot{\rho}(t) = -i[H(t), \rho] + \sum_{k} \gamma_{k} \left( L_{k} \rho L_{k}^{\dagger} - \frac{1}{2} \{ L_{k}^{\dagger} L_{k}, \rho \} \right). \tag{1}$$

The Hamiltonian H(t) describes the unitary contributions and will house specific contributions that generate non-Markovian noise. H(t) acts on the Hilbert space  $\mathcal{H} = \mathcal{H}_D \otimes \mathcal{H}_{Sp} \otimes \mathcal{H}_{TLS}$ , where the subspace  $\mathcal{H}_D$  defines the Hilbert space for the data qubits, i.e., the qubits that will be employed for a particular sequence of gate operations. Spectator qubits that impose unwanted external coupling on the data qubits are defined under  $\mathcal{H}_{Sp}$ . Lastly,  $\mathcal{H}_{TLS}$  denotes the inclusion of fluctuating TLSs that couple to the data qubits.

More explicitly, the Hamiltonian is formally given by

<span id="page-2-1"></span>
$$H(t) = H_C(t) + H_N(t) + H_{XT} + H_{TLS},$$
 (2)

where  $H_C(t)$  defines the control on the system and  $H_N(t)$ designates local noise contributions; both act on  $\mathcal{H}_{D}$ .  $H_C(t) = H_{C,1}(t) + H_{C,2}(t)$  is composed of two terms defining single and two-qubit control, respectively. Parasitic quantum crosstalk interactions between data and spectator qubits are captured by  $H_{XT}$  which acts on  $\mathcal{H}_D \otimes \mathcal{H}_{Sp}$ , with coupling between data qubits and TLSs being defined via  $H_{\text{TLS}}$ . The latter of which is defined within  $\mathcal{H}_{\text{D}} \otimes \mathcal{H}_{\text{TLS}}$ . Note that our model does not include local noise contributions for spectator qubits, nor coupling between spectators and TLSs. As we will show in Sec. IV, such additions to the model are not required to obtain strong agreement between model predictions and experimental results. Spectator qubits in particular are assumed to remain in the ground state throughout the evolution and thus are unaffected by the dissipative noise processes described below.

The latter part of our model includes jump operators  $L_k$  and decay rates  $\gamma_k$  that supply the dissipative effects. These terms are meant to capture Markovian effects of environmental noise sources that act upon the data qubits and are

not associated with spectator or TLS coupling. As such, the model does not include dissipative contributions for spectator qubits. As in the case of H(t), we do not observe a critical dependence on the inclusion of such terms and the predictability of our model.

We further distinguish between different types of noise based on their degree of correlation and modeling structure. We first define locally Markovian noise, corresponding to those processes which are uncorrelated and local for each qubit. An accurate description of locally Markovian noise effects does not require specific considerations of the degrees of freedom that give rise to noise.

Next, we define extended-Markovian noise to account for those processes which involve correlations, particularly spatial correlations, but whose effect on the system dynamics can be well modeled by a LME. This includes, for example, noise induced by TLSs or spectator qubits, which can be modeled via the LME by enlarging the qubit system to include the additional quantum degrees of freedom [75,76,82]. Thus, extended-Markovian noise requires careful consideration of the degrees of freedom that cause it, but its dynamical modeling is analogous to the locally Markovian case.

Lastly, we denote by *stochastic noise* those processes which can be described by time-dependent Hamiltonians with well-defined statistical properties. Stochastic noise can introduce time-correlations into the dynamics [95,98, 99], and proves to be a powerful tool for studying and modeling non-Markovian noise. In the following sections, we provide details about our model that fit within this framework. First, we focus on single-qubit operations, defining both Hamiltonian and dissipative operators. We then move to two-qubit noise and operations, in which we specify a noise model for cross-resonance (CR)-based operations.

#### A. Noiseless control

## 1. Single-qubit control

Arbitrary single-qubit operations can be parametrized using three Euler angles for which x- and z-rotations are sufficient [101]. Single-qubit microwave controlled x-rotations are represented by the n-qubit local control Hamiltonian

$$H_{C,1}(t) = \sum_{j=0}^{n-1} H_C^{(j)}(t), \tag{3}$$

where  $H_C^{(j)}(t) = \Omega_j(t)\sigma_x^{(j)}/2$  is the single-qubit control Hamiltonian at site j. Here,  $\sigma_{\mu}^{(j)}$ , with  $\mu = x, y, z$ , is a Pauli operator acting on the jth qubit, and  $\Omega_i(t)$  is the control amplitude. Note that the ideal total rotation at time t is given by the angle  $\Theta_j(t) = \int_0^t ds \Omega_j(s)$ . z-rotations are implemented virtually by performing instantaneous and noiseless phase shifts on the control [101]. The

action of a virtual Z-gate is modeled via the unitary  $U_{VZ}(\theta_0, \dots, \theta_{n-1}) = \exp(-i\sum_{j=0}^{n-1} \theta_j \sigma_z^{(j)}/2)$  for a set of rotation angles  $\{\theta_i\}_{i=0}^{n-1}$ .

### 2. Two-qubit control

In fixed-frequency transmon-based architectures, the CR gate is a microwave controlled operation that has shown promising potential as a two-qubit entangling gate [102–106]. Leveraging native qubit-qubit couplings, the CR gate generates entanglement by driving the control qubit at the frequency of the target qubit, without the need for qubit or coupling tunability.

The simplicity of the CR gate implementation makes it an appealing candidate for a go-to entangling gate in these architectures. However, during the implementation of a CR gate, unwanted errors arise. These errors are well known and documented [107,108], and several of them can be corrected by the implementation of echo pulses [107]. These echo pulses aim to cancel both local errors, and crosstalk between control-target and spectator qubits. This gate is known as the echo cross-resonance (ECR) gate [109], and its main two-qubit operation consists of a  $ZX_{\pi/2}$  rotation that can be modeled by the ideal CR Hamiltonian,

$$H_{C,2} = \frac{\pi}{4\tau_{CR}} \sigma_z^{(c)} \sigma_x^{(t)}.$$
 (4)

Here  $\tau_{CR}$  is the duration of the ECR gate, typically much larger than the single-qubit gate duration  $\delta t$ . Note that c and t refer to the control and target qubit, respectively.

## **B.** Locally Markovian model

## 1. Local dissipative noise

Next, we describe the sources of dissipation that are included in the LME as jump operators  $L_k$  with decay rates  $\gamma_k$ . These processes are locally Markovian and thus act only locally on each qubit. Here again the superscript (j) will denote the qubit index number.

<span id="page-3-0"></span>The first source of dissipative errors we consider is thermal relaxation in the form of generalized amplitude damping (GAD). GAD describes the effect of energy dissipation to an environment at a finite temperature  $T_{\text{env}}^{(j)}$ . Since  $\{T_{\text{env}}^{(j)}\}$  represent effective bath temperatures, they are assumed to be different for each qubit. We define  $0 \le q^{(j)} \le 1$  as the excited state probability at thermal equilibrium, and  $\gamma^{(j)} = 1/T_1^{(j)}$  as the relaxation rate. The  $T_1$  time is the characteristic decay time of the GAD process, where the relaxation probability  $1 - e^{-\tau/T_1^{(j)}}$  can be interpreted as the probability that a spontaneous emission occurs after a time  $\tau$ . Assuming that the equilibrium probabilities satisfy a Boltzmann distribution, we have

probabilities satisfy a Boltzmann distribution, we have 
$$1 - q^{(j)} = \left(1 + e^{-\hbar\omega_{01}^{(j)}/k_BT_{\rm env}^{(j)}}\right)^{-1}, \text{ where } \omega_{01}^{(j)} \text{ is the energy}$$

of the first excited state, typically near 5 GHz [1], and  $k_B$  is the Boltzmann constant. In addition, GAD has a simple description in terms of two jump operators:  $L_{\pm,j} = \sigma_{\pm}^{(j)} = \left(\sigma_x^{(j)} \pm i\sigma_y^{(j)}\right)/2$  with decay rates  $\gamma_{+,j} = q^{(j)}\gamma^{(j)}$  and  $\gamma_{-,k} = \left(1 - q^{(j)}\right)\gamma^{(j)}$ .

Next, we consider exchange couplings with the environment leading to dephasing noise, which appears as phase damping (PD). These are processes affecting the off-diagonal elements of the state density matrix. Analogously to the relaxation case, the characteristic decoherence time  $T_{\phi}$  can be related to the dephasing rate via  $\lambda^{(j)} = 1/T_{\phi}^{(j)}$  and decay probability  $1 - e^{-\tau/T_{\phi}^{(j)}}$ . In its Lindblad form, the action of PD is described with a single jump operator:  $L_{z,j} = \sigma_z^{(j)}/\sqrt{2}$ , with rate  $\gamma_{z,j} = \lambda^{(j)}$ .

Lastly, during the action of control operations, noise processes such as fluctuations in the control lines [110] can induce dissipation of information. To account for the presence of dissipation in control errors, we include a bit-flip noise contribution with rate  $v^{(j)}$  and probability  $1 - e^{-v^{(j)}\tau}$ . The Lindblad form of control dissipation is  $L_{x,j} = \sigma_x^{(j)}/\sqrt{2}$  with decay rate  $\gamma_{x,j} = v^{(j)}$ . Note that this form of error only acts during the implementation of x-rotations.

### 2. State preparation and measurement (SPAM)

We include SPAM errors in the error model as a bit-flip error in the quantum channel form acting before ideal state measurement operations. Previous work, e.g., Ref. [111], accounts for residual excited state population during state preparation by assuming that the initial state is the (unnormalized) thermal state  $\exp(-H/k_BT_{\rm env})$ , rather than the ground state  $|0\rangle\langle 0|$ , where H is the full system-bath Hamiltonian. However, since bit-flip errors constitute a gauge symmetry of our model, it is sufficient to group SPAM errors into a single error channel acting before measurement, hence simplifying the analytical derivations. This choice is standard practice in the literature, see, for example, Ref. [59]. Consequently, we choose to treat state preparation as an effectively ideal operation resulting in the  $|0\rangle\langle 0|$  state and assign all SPAM errors to measurement errors with rates  $s_i$ . In addition, although the error probability will in general be different for the measurement of ground versus excited states, we observe that in practice it is small enough that it can be treated symmetrically. When this condition is not sufficiently satisfied, however, the overall qubit performance is poor and thus we choose not to focus on these qubits in this work.

The effect of SPAM errors arising from measuring qubit j is given by

$$\mathcal{E}_{M}^{(j)}(\rho) = (1 - s_{j})\rho + s_{j}\sigma_{x}^{(j)}\rho\sigma_{x}^{(j)}, \tag{5}$$

where  $s_j$  is the probability of measurement errors on qubit j. Thus, the collective effect of data qubit measurement errors can be found by the application of maps  $\mathcal{E}_M^{(j)}(\cdot)$  for  $j = 0, \dots, n-1$ ,

$$\mathcal{E}_M(\rho) = \mathcal{E}_M^{(n-1)} \circ \cdots \circ \mathcal{E}_M^{(0)}(\rho). \tag{6}$$

To first order in the error parameters  $s_j \ll 1$ , this map can be approximated as  $\mathcal{E}_M(\rho) \approx \rho + \sum_{j=0}^{n-1} s_j \left( \sigma_x^{(j)} \rho \sigma_x^{(j)} - \rho \right)$ .

## C. Extended Markovian model

In addition to local noise, we allow the data qubits to couple nonlocally, both to other qubits and external degrees of freedom via ZZ interactions. First, we consider qubit-qubit crosstalk noise resulting from always-on interactions that yield residual couplings [32,112,113]. We denote by  $\mathcal C$  the set of qubits that couple to the data qubits. In general,  $\mathcal C$  will depend on the connectivity of the device, and for fixed-frequency coupling transmons, the most significant couplings will be induced by nearest-neighbor interactions.

Denoting by  $C(j) \subseteq C$  the set of qubits connected to the j th data qubit, the crosstalk Hamiltonian is thus given by

$$H_{\rm XT} = \sum_{j=0}^{n-1} \sigma_z^{(j)} \sum_{i \in C(j)} J_{ij} \sigma_z^{(i)},$$
 (7)

for coupling strengths  $J_{ij}$ . To avoid double counting, we assume nonzero coupling only for i < j, while  $J_{ij} = 0$  for i > j.

Analogously to crosstalk interactions, we can describe the TLS coupling via ZZ interactions, where each data qubit is coupled to  $n_{\text{TLS}}$  number of TLSs [75]. TLSs are defined on a computational basis  $\{|0\rangle_{\text{TLS}}, |1\rangle_{\text{TLS}}\}$  with Pauli operators  $\sigma_{\mu,\text{TLS}}^{(j,k)}$ , for  $\mu=x,y,z$ , qubit j and TLS k. Then, the Hamiltonian that describes the coupling between data qubits and TLSs is

$$H_{\text{TLS}} = \sum_{j=0}^{n-1} \sigma_z^{(j)} \sum_{k=1}^{n_{\text{TLS}}} \xi_{jk} \sigma_{z,\text{TLS}}^{(j,k)}, \tag{8}$$

where  $\xi_{jk}$  are the coupling strengths between qubit j and its kth TLS. At the beginning of each experiment, all TLSs are considered to be initialized in the thermal state  $p_0 |0\rangle \langle 0| + p_1 |1\rangle \langle 1|$ , where  $p_{0,1} = 1/\left(1 + e^{\mp\hbar\omega/k_BT_{\rm TLS}}\right)$  are temperature dependent populations. In this work, we assume the TLS is at infinite temperature, where the thermal state becomes the maximally mixed-state I/2. These are extended Markovian processes and thus can be studied within the LME by including the additional qubits and TLSs as part of Eq. (2). Note that both crosstalk and TLS interactions are included in single and two-qubit operations.

#### 1. Two-qubit gates and noise

We allow two-qubit errors in the Hamiltonian, but interestingly, we find that single-qubit incoherent errors are sufficient to obtain excellent agreement with the decays observed in the experiments. In other words, no two-qubit dissipative terms are found to be necessary to explain the experiment results observed. This remarkable fact significantly simplifies the modeling and characterization of the ECR gates and is a promising feature looking toward multi-qubit modeling and characterization.

Following Refs. [107,114], we model the effective ECR Hamiltonian as

$$H_{\text{CR}} = (1 + \epsilon_{zx})H_{C,2} + \frac{\beta^{(t)}}{2}I^{(c)}\sigma_z^{(t)} + \frac{\zeta}{2}I^{(c)}\sigma_x^{(t)} + \frac{J}{2}\sigma_z^{(c)}\sigma_z^{(t)}, \quad (9)$$

where  $I^{(c)}$  denotes the identity operation on the control qubit. The first term corresponds to the main ZX rotation of the ECR gate, allowing for an over-rotation fraction  $\epsilon_{zx}$  due to implementation errors. This Hamiltonian also includes local noise rotations on the target qubit: a relevant detuning term  $\beta^{(t)}$  and leftover single-qubit x-rotation  $\zeta$ . Lastly, qubit-qubit crosstalk is also present and accounted for in the last term with coupling strength J.

#### <span id="page-5-3"></span>D. Stochastic noise model

We represent both local control and dephasing noise in the stochastic Hamiltonian formalism by the following time-dependent noise Hamiltonian,

$$H_{N,1}(t) = \sum_{j=0}^{n-1} \epsilon_j(t) H_C^{(j)}(t) + \frac{\beta_j(t)}{2} \sigma_z^{(j)}.$$
 (10)

Here,  $\epsilon_j(t)$  and  $\beta_j(t)$  are time-dependent random variables that represent the stochastic control and dephasing noise. These variables are assumed to be Gaussian and widesense stationary, and thus they are completely determined by their mean  $\langle f \rangle = \overline{f}$  and two-point correlation function  $C_f(t) = \langle f(t)f(0) \rangle$ , for  $f = \epsilon_j, \beta_j$ . Here,  $\langle \cdot \rangle$  denotes the average over noise realizations. From  $C_f(t)$ , we can define the noise power spectral density (PSD)  $S_f(\omega) = \int_0^\tau C_f(t)e^{-i\omega t}dt$ , which captures the information of the noise fluctuations in the frequency domain. Note that the limiting case of detuning corresponds to nonzero mean and  $S_f(\omega) \equiv 0$ , while white noise is equivalent to  $\langle f \rangle \equiv 0$  and  $S_f(\omega) \neq 0$ .

In general, to evaluate the effect of stochastic noise on the system evolution in simulation, we first generate a number of different noise realizations, or trajectories. Then, the LME is solved for each realization, and lastly, the resulting density matrix is averaged over all generated trajectories. Intuitively, the evolution for each stochastic noise realization is treated as Markovian, and non-Markovianity arises from the averaging over many statistically correlated realizations.

#### E. Model solutions

To find a solution for Eq. (1), we take a canonical approach [48]. First, we expand the density matrix state on the *n*-qubit Pauli basis,  $\rho(t) = (1/2^n) \left( I + \vec{v}(t) \cdot \vec{\mathcal{O}} \right)$ , where  $\vec{v}(t)$  is the generalized Bloch vector, and  $\mathcal{O}_j \in \{I, \sigma_x, \sigma_y, \sigma_z\}^{\otimes n}$ , for  $j = 0, \dots, 2^{2n} - 1$ . In terms of the components of  $\vec{v}(t)$ , Eq. (1) becomes a system of coupled differential equations,

<span id="page-5-1"></span>
$$\dot{\vec{v}}(t) = \mathbf{G}(t) \cdot \vec{v}(t) + \vec{c}(t), \tag{11}$$

<span id="page-5-5"></span>where the vector  $\vec{c}(t)$  and the complex-valued coupling matrix  $\mathbf{G}(t)$  depend on the circuit and noise parameters. In this form, Eq. (11) can be solved using standard coupled differential equations methods. When studying circuit-based evolutions in the Markovian regime, it is possible to separate  $\mathbf{G}(t)$  into time-independent sections to be solved separately, and thus finding analytical solutions of Eq. (11) becomes feasible (see Appendix A). In this case, we can write the formal solution

<span id="page-5-2"></span>
$$\vec{v}(t+\tau) = e^{\mathbf{G}\tau} \cdot \vec{v}(t) + \left(e^{\mathbf{G}\tau} - 1\right) \cdot \mathbf{G}^{-1} \cdot \vec{c},\tag{12}$$

where  $\tau$  denotes the duration over which  $\mathbf{G} \equiv \mathbf{G}(t)$  remains constant. Note that, generally, under the condition of finite relaxation rates  $\gamma_j > 0$ ,  $\mathbf{G}(t)$  is diagonalizable and invertible.

<span id="page-5-4"></span>On the other hand, when time correlations are present through  $\{\beta_j(t), \epsilon_j(t)\}_j$ , finding general analytical solutions is challenging. Instead, the statistical properties of the stochastic noise processes can be used to generate realizations of noise trajectories. For each realization, assuming a discrete piecewise constant evolution of  $\epsilon(t)$ ,  $\beta(t)$ , Eq. (11) can be solved to find the final state  $\rho_k(\tau)$  for the kth noise realization. Lastly, the solution state is found by averaging over a sufficient number of noise realizations.

Gate-based experiments can be devised, where some sources of noise will contribute dominantly, while other types of noise will have limited effect. In the next section, we introduce a set of characterization experiments that aim to amplify and effectively isolate specific noise processes. In these cases, due to the relative simplicity of these circuits, we can solve Eq. (11) analytically, and use the resulting expression to learn the model parameters.

# <span id="page-5-0"></span>III. CHARACTERIZATION PROTOCOL

## <span id="page-5-6"></span>A. Overview

Figure 1 presents a graphical overview of the characterization protocol. After selecting the qubit or pair of

<span id="page-6-0"></span>![](_page_6_Figure_2.jpeg)

FIG. 1. Noise characterization protocol used to learn the model parameters. (a) The state is assumed to be perfectly initialized in the ground state  $|0\rangle$   $\langle 0|$ , and the characterization circuits  $C = \{M, T_1, T_2, P, Q, XT, CR\}$  are run on the device of interest. (b) The measurement data  $\{p_{\exp}^c(\tau)\}_{c\in C}$  is then used to fit the Markovian noise model parameters  $\mathcal{N} = \{s, \gamma, q, \lambda, \beta, \epsilon, \nu\}$ , based on analytical predictions obtained from solving the Lindblad master equation [Eq. (12)]. If deviations from the Markovian model are present in the data, the fixed total-time pulse sequences (Q) protocol is used to extract dephasing and control power spectral densities,  $S_{\beta}(\omega)$ ,  $S_{\epsilon}(\omega)$ , respectively, as well as the two-level system coupling  $\xi$  obtained from the Ramsey experiment, denoted by  $Q_{k=0}$ . Two-qubit crosstalk J can be obtained via analyzing the (XT) circuit results. (c) The model, either purely Markovian or extended with non-Markovian effects, is tested by predicting the randomized benchmarking decay rate.

qubits of interest, the characterization experiments are run; this includes the set of single-qubit experiments  $C_1 = \{M, T_1, T_2, P, Q\}$ , and two-qubit experiments  $C_2 =$ {XT, CR}, where each experiment may require the execution of multiple circuits. The experiments can be categorized by measurement (M), relaxation  $(T_1)$ , dephasing  $(T_2)$ , pulse (P), QNS (Q), crosstalk (XT), and cross resonance (CR), from where all the relevant parameters are learned. All noise amplification experiments are shown in Fig. 1(a), and described in detail in the next section. The association between model parameters and characterization experiments is summarized in Table I. In all cases, the qubits are assumed to be perfectly initialized in the ground state  $\rho(0) = |0\rangle\langle 0|$ . Each experiment results in estimates of the survival probabilities, denoted as  $\{p_{\text{exp}}^c(\tau_c)\}_{c\in C}$ , where  $C=C_1\cup C_2$  includes all characterization experiments performed. Note that the duration  $\tau_c$  of each experiment will in general vary between experiments.

Next, the experimental data are compared to the analytical predictions, shown later in this section, obtained from solving the LME with the extended Markovian noise model for each of the experiments; see Fig. 1(b). The procedure used to find the analytical predictions and its formalism was outlined in the previous section, and is developed in detail in Appendix A. The Markovian model predictions are denoted by  $\{p_{\text{pred}}^c(\tau_c, \mathcal{N})\}_{c \in C}$ , where  $\mathcal{N}$  defines the set of noise parameters. When performing these

computations, stochastic dephasing and control noise are assumed to be static and time-independent.

The fitting procedure finds optimal error parameters  $\mathcal{N}_{opt}$  that minimize the mean squared error (MSE) distance between vectors of length N, i.e.,  $D(\vec{x}, \vec{y}) =$  $(1/N)\sqrt{\sum_{i=1}^{N}(x_i-y_i)^2}$ , where N denotes the total number of data points obtained from experiments. Note that, since this metric is used to compare distances between survival probabilities, the MSE distance is always bounded between 0 and 1. The quality of the fit can then be formalized as the distance between data and experiment being smaller than a certain value  $\delta$ , that is,  $(1/|C|) \sum_{c \in C} D(p_{\text{exp}}^c(\tau_c), p_{\text{pred}}^c(\tau_c, \mathcal{N}_{\text{opt}})) < \delta$ . When a set of noise parameters satisfies this condition, we say it is  $\delta$ optimal, and  $0 < \delta < 1$  can be interpreted as a fractional error, with typical  $\delta$  values below 1%. Here, |C| denotes the number of experiment classes. Each class of experiments generally involves multiple circuits, with the exception of the single-circuit measurement experiment (M). The data points from each experiment are included within the vector of length N defined within the MSE

Note that we minimize the MSE jointly over all experiments simultaneously, as opposed to, for example, fitting the characterization experiments sequentially. In a sequential approach, the relaxation rate could be extracted from  $T_1$  experiments first, and then used as a fixed input to subsequent fits. This type of fit can lead to propagation of

<span id="page-7-1"></span>TABLE I. Mapping between model parameters and characterization experiments.

| Parameter name                | Parameter variable     | Characterization experiment |
|-------------------------------|------------------------|-----------------------------|
| Relaxation rate               | γ                      | $T_1$ experiment $[T_1]$    |
| Excited state probability     | q                      | $T_1$ experiment $[T_1]$    |
| Dephasing rate                | λ                      | Hahn echo $[T_2]$           |
| Detuning rate                 | $\boldsymbol{\beta}$   | Ramsey $[Q_{k=0}]$          |
| TLS coupling strength         | ξ                      | Ramsey $[Q_{k=0}]$          |
| Crosstalk coupling strength   | J                      | Crosstalk experiment [XT]   |
| Incoherent control error      | ν                      | FPW sequences [P]           |
| Measurement error probability | S                      | SPAM experiment [M]         |
| Coherent control error        | $\epsilon$             | FTTPS $[Q]$                 |
| Dephasing noise PSD           | $S_{\beta}(\omega)$    | FTTPS [Q]                   |
| Control noise PSD             | $S_{\epsilon}(\omega)$ | FTTPS $[Q]$                 |
| CR offset                     | ζ                      | CR experiment [CR]          |
| CR coherent control error     | $\epsilon_{zx}$        | CR experiment [CR]          |

fitting errors from experiments fit earlier into later ones, which would unevenly penalize parameters that appear only in later stages of a sequential pipeline. Although more sophisticated approaches, such as  $\chi^2$  or maximum likelihood estimation could in principle yield better performance, the joint MSE minimization proved sufficient in practice. When possible, we keep the number of circuits per experiment class uniform to avoid biasing the cost function toward experiment types with more data points.

Model selection is determined by the success of the fitting. This process begins by assuming the validity of the extended Markovian model, as nearly all IBMQP qubits are subject to quantum crosstalk. Additional degrees of freedom accounting for TLSs are determined in part by a Ramsey experiment, or equivalently, the first sequence within the fixed total-time pulse sequences (FTTPS) protocol. The model is tested against RB experiments run (ideally) immediately after the characterization data are obtained in order to minimize drift in the error model parameters. The optimal parameters  $\mathcal{N}_{\text{opt}}$  are used in simulation and evaluated against the experimental RB results. We employ a  $\delta_{RB}$ -optimal criterion analogous to the fitting procedure to validate the model. If the fit is satisfactory, we claim that the error present on the selected qubits is predominantly Markovian, with error parameters  $\mathcal{N}_{opt}$ ; see Fig. 1(c).

In general, discrepancies between predicted and experimental RB data may arise from multiple origins, such as time-dependent decay rates [115], initial systemenvironment correlations [116], effective non-Hermitian

Hamiltonians [117], or completely positive and trace non-increasing quantum operations [118]. In this work, we proceed self-consistently and assume that these discrepancies are likely to arise from the presence of time-correlated noise contributions, not included in the initial Markovian model. As such, these deviations are addressed by promoting the dephasing and control error processes from static to stochastic. QNS via the FTTPS protocol is then used to characterize the noise PSDs  $S_{\beta}(\omega)$  and  $S_{\epsilon}(\omega)$ . We find that the addition of stochastic noise is sufficient for reconciling the noise model with RB experiments.

## <span id="page-7-0"></span>**B.** Characterization experiments

In this section, we present the noise amplification experiments used to characterize the error model parameters. All qubits are initialized in the  $|0\rangle$  state and measured in the computational basis. Since all experiments are performed on the IBMQP, we write all circuits in terms of native IBMQP single-qubit gates:  $I, X, \sqrt{X}$  gates and arbitrary virtual z-rotations. Single-qubit gates are implemented over a duration  $\delta t$  that depends on the device (e.g.,  $\delta t = 0.035 \,\mu s$  for  $ibm\_algiers$ ). For each device, however,  $\delta t$  is equivalent for all single-qubit gates.

Below, we describe which sources of noise are expected to contribute most significantly for each type of circuit. We provide solutions to the LME for these circuits when local and extended Markovian noise processes are dominant. Details on the specific calculations can be found in Appendix A 4.

In the case of single-qubit experiments, the qubit index will be removed for clarity. For the measured qubit, the probability of finding the state in the ground state is computed in terms of the Bloch vector as  $p(\tau) =$  $\langle 0 | \mathcal{E}_M(\rho(\tau)) | 0 \rangle = \frac{1}{2} (1 + v_z(\tau)(1 - 2s))$ , where  $\rho(\tau)$  is the density matrix at the end of the circuit of duration  $\tau$ , obtained from solving Eq. (1). Consequently, it suffices to find expressions for the premeasurement Bloch vector component  $v_z(\tau)$ . For notational convenience, we will suppress the subscript z from the scalar quantity  $v_z(\tau)$ , and denote the z component of the Bloch vector for experiment  $c \in C$  as  $v^c(\tau)$ . With the exception of the SPAM circuit, the noiseless control time propagators of the characterization circuits perform identity operations, i.e.,  $U_c(\tau) = I$ . As a result, the expected ground state probabilities in the noiseless case are  $p(\tau) = 1$ .

## 1. $T_1$ experiments $(T_1)$

In a  $T_1$  experiment, the qubit is prepared in the excited state  $|1\rangle$  by implementing an X gate. It is then allowed to evolve freely for a period of time  $\tau$ . A measurement of the ground state population is performed after applying a second X gate to complete the circuit. This experiment captures thermal relaxation, i.e., the decay of the excited state to thermal equilibrium. The Bloch vector decays

exponentially with the relaxation decay rate  $\gamma$ , as obtained from solving the LME,

$$v^{T_1}(\tau) \approx 1 - 2q \left(1 - e^{-\gamma \tau}\right).$$
 (13)

Note that for a zero-temperature bath, q=1, and  $v^{T_1}(\tau\gg 1/\gamma)\to -1$ .

## 2. $T_2$ Hahn-echo (HE) experiments ( $T_2$ )

The  $T_2$  HE experiment is initialized by applying an  $\sqrt{X}$  gate and preparing the qubit in the equator state  $|-i\rangle = (|0\rangle - i|1\rangle)/\sqrt{2}$ . It is followed by a period of free evolution of duration  $\tau/2$ . Then an X (echo) gate is applied, with the objective of reversing the effect of constant detuning. The echo gate is succeeded by a second idle period of duration  $\tau/2$ . Lastly, a measurement of the ground state population is performed after applying a  $\sqrt{X}^{\dagger}$  gate. This experiment aims to measure the decay rate of coherence of the Bloch equator states. More specifically, Bloch vector decays as

$$v^{T_2}(\tau) \approx e^{-\tau(\frac{\gamma}{2} + \lambda)},$$
 (14)

which depends on both relaxation and phase decay rates  $\gamma$  and  $\lambda$ , respectively. To derive this expression, we have made the assumption that stochastic dephasing noise changes sufficiently slowly such that it can be decoupled with an echo pulse.

#### 3. Ramsey experiments

The Ramsey experiment, also known as  $T_2^*$  experiment, consists of preparing the qubit with a  $\sqrt{X}$  gate, letting it evolve freely for a time  $\tau$ , and applying  $\sqrt{X}^\dagger$  to complete the circuit. During the idle period, the qubit is susceptible to dephasing and relaxation. However, it will also exhibit susceptibility to detuning, spectator qubit crosstalk, and TLSs. By solving the LME and tracing out the TLS degree of freedom, we find that the Bloch vector evolves as

$$v^{R}(\tau) = e^{\left(\frac{\gamma}{2} + \lambda\right)\tau} \cos(\beta_{\text{eff}}\tau) \cos(\xi\tau), \tag{15}$$

where  $\beta_{\text{eff}} = \beta + \sum_{i \in C} J_i$  is the effective detuning.  $J_i$  is the crosstalk coupling strength for the ith nearest-neighbors coupled with the data qubit. A single TLS is assumed to be present, with coupling strength  $\xi$ . Here, we have taken dephasing noise to be static over the duration of the experiment, i.e.,  $\beta(t) = \beta$ . Note that when a TLS is present, the oscillations in these experiments will present two characteristic frequencies, rather than one. Ramsey experiments are shown in Fig. 1, labeled as  $Q_{k=0}$ .

## 4. SPAM (M)

Here, we characterize SPAM errors by preparing the qubit in a computational basis state and estimating the error

<span id="page-8-0"></span>probability. More specifically, we initialize the qubits in  $|1\rangle$  and examine the probability of obtaining  $|0\rangle$ . To leading order in the error parameters, the prediction for the SPAM circuit yields  $p^M(\delta t) = s$ .

## 5. $FTTPS(Q_k)$

The FTTPS are circuits used in QNS for estimating properties of correlated noise [57,98]. FTTPS consist of K distinct sequences (circuits) labeled by  $0 \le k < K$ . Each sequence contains N = 2 (K + 1) gates for a total sequence duration  $\tau = N\delta t$ . The kth FTTPS sequence is composed of identity and X gates, where the  $\ell$ th X gate is located at  $|(2\ell+1)K/2k|$  for  $0 \le \ell < 2k$ . Prior to each FTTPS sequence, the system is subject to a  $\sqrt{X}$  gate to prepare the qubit in the (x, y)-plane of the single-qubit Bloch sphere; thus, allowing it to be strongly sensitive to dephasing noise. Upon the completion of the sequence,  $\sqrt{X}^{\dagger}$  is applied to return the qubit to the ground state prior to measurement. The dynamics generated by FTTPS leads to narrow qubit filter functions (FFs) centered around  $\omega_k = 2\pi k/\tau$  (see Appendix B 2) that are well-suited for ONS.

<span id="page-8-3"></span>Intuitively, as shown in Fig. 1(a.Q), the X pulses are spaced out with a time difference  $\tau_k \approx \tau/2k$ . This expression is derived in the instantaneous pulse limit, and the approximation symbol is meant to account for deviations due to finite pulse-width (FPW). Note that the k=0 FTTPS is a fixed- $\tau$  Ramsey experiment. For 0 < k < K, the LME for the FTTPS experiments predicts Bloch vectors.

$$v_k^Q(\tau) \approx e^{-\tau \delta_k} \cos(2\pi k\epsilon),$$
 (16)

where the FTTPS decay rate is  $\delta_k = \gamma/2 + \lambda + (\gamma/2 - \lambda + 2\nu)k/2K$ . This form is derived in Appendix A 4. In finding these expressions, we have assumed that the over-rotation control noise is static, i.e.,  $\epsilon(t) = \epsilon$ .

## 6. FPW sequences (P)

<span id="page-8-2"></span>The finite-time duration  $\delta t$  of the native IBMQP gates results in deviations from ideal, instantaneous pulses. In order to characterize FPW errors, we define the FPW circuits by d repetitions of alternating pairs of X and -X pulses. These sequences are carefully chosen in order to cancel coherent control errors, while preserving FPW errors. In practice, each -X pulse is implemented by bookending an X gate with two Z gates, i.e., -X = ZXZ. Consequently, FPW sequences are implemented as  $(XZXZ)^d$ . The total duration of an FPW circuit of d repetitions is  $\tau = 2d \, \delta t$ .

The Bloch vector of the FPW experiment is obtained to be

<span id="page-8-1"></span>
$$v^P(\tau) \approx e^{-\tau \left(\frac{3}{4}\gamma + \frac{\lambda}{2} + \nu\right)} \cos\left(\frac{4}{3\pi}\beta_{\text{eff}}\tau\right),$$
 (17)

where  $\beta_{\rm eff}$  is the effective detuning computed from the Ramsey experiments. The factor of  $4/3\pi$  arises from the specifics of a Gaussian pulse shape, as shown explicitly in Appendix C. Note that, in addition to relaxation and PD, a dissipative process with decay rate  $\nu$  contributes to decay due to the presence of control.

## 7. Crosstalk experiments (XT)

The crosstalk noise amplification experiments involve simultaneously driving both qubits. As opposed to relying on the Joint Amplification of ZZ (JAZZ) protocol [119, 120], we employ joint  $T_2$  HE circuits. That is, qubits are prepared in the plane of the single-qubit Bloch sphere with  $\sqrt{X}$  gates, where they are most sensitive to Z rotations. Then, the qubits are allowed to evolve freely for a time  $\tau/2$  and subsequently subject to simultaneous X gates on both qubits. Both qubits are then allowed to evolve freely for an additional time of  $\tau/2$ . Lastly,  $\sqrt{X}^{\dagger}$  gates are applied before measurement.

To simplify the analysis of the experimental results, only one of the qubits is measured, denoted by qubit M, whereas the other qubit S is traced over. Due to crosstalk coupling, the dynamics of qubit M depend nontrivially on the characteristics of qubit S. By solving the two-qubit LME and tracing over qubit S, we find

$$v^{\rm XT}(\tau) \approx e^{-\alpha_M \tau} \left( \cos(\tau J_{\rm MS}) + \frac{\gamma_S}{2J_{\rm MS}} \sin(\tau J_{\rm MS}) \right)$$
 (18)

to first order in  $\gamma_S/J_{\rm MS}$ , and where  $\alpha_M = (\gamma_M + \gamma_S)/2 + \lambda_M$ . The decay rates  $\gamma_i$ ,  $\lambda_i$  are the relaxation and dephasing rates of qubit i = M, S, which can be learned by performing single-qubit characterization. Note that crosstalk between qubits M, S and their neighboring spectators, as well as local detunings, are decoupled by the echo pulses, thus amplifying the effect of crosstalk between qubits M and S. See Appendix A 4 for details on this calculation.

## 8. Cross-resonance (CR) experiments

The experiments used to characterize the ECR gates consist of repeated applications of ECR gates on a chosen pair of qubits. Instead of measuring the survival probability, the expectation values  $\langle Y_t \rangle$ ,  $\langle Z_t \rangle$  on the target qubit t are measured. Here, the expectation value of a target qubit operator  $O_t$  is defined by  $\langle O_t(\tau) \rangle = \text{Tr} \left[ \rho(\tau) O_t \right]$ , where  $\rho(\tau)$  is the circuit's final two-qubit state. For initial control qubit states  $q_c = 0, 1$ , corresponding to the states  $|0\rangle$ ,  $|1\rangle$ , the LME can be solved to leading order in the error parameters.

The resulting solutions can be expressed in terms of the Bloch vector components, or equivalently, the target qubit expectation values,

$$\langle Y_t(\tau) \rangle_{q_c=0,1} \approx \pm e^{-\delta_{\rm cr}\tau} \sin\left((\omega_{\rm cr} \mp \zeta) \tau\right), \langle Z_t(\tau) \rangle_{q_c=0,1} \approx e^{-\delta_{\rm cr}\tau} \cos\left((\omega_{\rm cr} \mp \zeta) \tau\right),$$
(19)

where  $\delta_{\rm cr} = 2\gamma/5 + \lambda/2 + \nu$  and  $\omega_{\rm cr} = \pi \left(1 + \epsilon_{zx}\right)/2\tau_{CR}$ . The experiment duration consists of multiples of the ECR gate duration, namely  $\tau = n\tau_{\rm CR}$ , for  $n = 0, 1, \ldots$  repetitions of ECR gates. The  $X_t$  expectation values are found to be proportional to  $\langle X_t \rangle_{q_c=0,1} \propto (\beta_t \pm J)\tau_{\rm CR}$  and are typically much smaller than  $\langle Y_t \rangle_{q_c}$ ,  $\langle Z_t \rangle_{q_c}$ . Here J is the crosstalk coupling between the control and target qubits. From fitting these functions to experimental data, the overrotation error  $\epsilon_{zx}$  and the offset  $\zeta$  can be obtained. The target qubit decay parameters  $\gamma, \lambda, \nu$  are obtained through single-qubit characterization.

## <span id="page-9-0"></span>IV. EXPERIMENT RESULTS

In this section, we showcase how the previous models and characterization protocols can be used to assess and predict a wide variety of experimental behavior on IBMQP devices. We begin by considering qubits that are dominated by Markovian noise and then extend the analysis to those that exhibit strong non-Markovian phenomena. Specifications for all devices studied can be found in Appendix K.

## <span id="page-9-2"></span>A. Locally Markovian noise on the IBMOP

<span id="page-9-1"></span>We begin by discussing qubits that exhibit dynamics consistent with the locally Markovian noise model. Figure 2 presents results obtained from running the  $(T_1)$ ,  $(T_2)$ , (Q), (P) characterization experiments on qubit 8 of  $ibm\_algiers$ . These experiments are sufficient to characterize all locally Markovian processes, namely amplitude damping, as well as Markovian dephasing and control noise. Panels (a)–(d) in Fig. 2 show the results of the characterization experiments.

A fitting procedure using Eqs. (13)–(17) is run to extract  $(\gamma, q, \lambda, \beta, \epsilon, \nu, s)$  from the characterization experiments. To validate the approximate solutions derived in the previous section, Markovian simulations are carried out by numerically solving the LME via Eq. (12) for each circuit element with the learned noise parameters. As can be seen in Fig. 2, the learned LME model conveys excellent agreement with experiment, thus successfully validating the noise model.

Next, we test the noise model's predictive capabilities by comparing it against experiments not used in the training process. In particular, we focus on RB experiments used to assess the single-qubit gate error rates, as the inherent randomization of RB distinguishes it from the characterization experiments. Moreover, as shown in Appendix F, RB possesses a robustness to coherent errors

<span id="page-10-0"></span>![](_page_10_Figure_2.jpeg)

FIG. 2. (a)–(d) Experimental implementation of the noise characterization protocol on qubit 8 of ibm\_algiers. The results of the characterization experiments are shown (purple circles). We perform a simultaneous fit of the experiments results to the Markovian model predictions given by Eqs. (13)–(17) (black lines), from where the noise parameters are obtained. Note that this set of experimental results agrees well with the Markovian model, including validation in Lindblad master equation simulation (green diamonds). State preparation and measurement results, not shown for clarity, yield s = 1.2%. Other error parameters obtained from the fit are  $\gamma = 0.0107(2)$  MHz, q =0.86(1),  $\beta = 0.208(1)$  MHz,  $\lambda = 0$  MHz,  $\epsilon = 0.121(4)\%$ ,  $\nu =$ 0.005(1) MHz. (e) Randomized benchmarking characterizations (with error bars) obtained from averaging over 10 gate realizations (dark-blue circles). The error parameters are used in combination with solutions to Eq. (1) to simulate the randomized benchmarking circuits (green diamonds). The experimental and simulated error-per-Clifford, obtained from the standard exponential fit (solid lines) of the randomized benchmarking decay curve  $p^{RB}(L) = (1 + (1 - 2s)e^{-rL})/2$ , agree within errorbars. In the randomized benchmarking fit, only the error-per-Clifford r is left as a free parameter. Hence, the randomized benchmarking error rate can be derived from the noise parameters without any a priori knowledge of randomized benchmarking results.

while still remaining susceptible to all incoherent errors. Interestingly, the Markovian model can provide intuition on how each noise process contributes to RB decay rates. To first order in  $\delta t$ , we find that the RB decay rate depends linearly on the dissipative parameters  $\gamma$ ,  $\lambda$ ,  $\nu$ , and quadratically on the coherent error parameters  $\epsilon$ ,  $\beta$ ; see Appendix F for simulation details.

We run experiments and numerical simulations for a set of 10 RB circuits averaged and fit to an exponential decay model to extract the error-per-Clifford (EPC) RB decay rate. As shown in Fig. 2(e), the model is able to predict the RB decay rate with great accuracy. We again emphasize that the noise model is not trained on the RB experimental result, hence showcasing the predictive power of the Markovian error model. To complement this analysis, in Appendix G we compare the experimentally obtained RB variances for 13 qubits on *ibm\_algiers* with those predicted by the model. From this data, we find a Pearson correlation coefficient of 0.7, suggesting strong correlation and a significant predictive power of the model.

## B. Extended Markovian noise on the IBMOP

Although the locally Markovian model can be used to characterize any of the IBMQP devices, model violations are often found when reconciling simulation with the characterization experiments. To accurately describe the phenomena observed, we examine the characterization of extended Markovian processes introduced in Sec. II. Here, we analyze two distinct effects: multifrequency oscillations induced by TLSs and crosstalk noise. These processes are non-Markovian effects when viewed locally, but are well modeled with a LME by extending the system Hilbert space to include TLS and spectator qubit degrees of freedom.

## <span id="page-10-1"></span>1. TLS in Ramsey experiments

It is well established that Ramsey experiments performed on superconducting qubits often present clear deviations from the Markovian model [121–123]. This is evidenced by oscillations that cannot be modeled as a single decaying and oscillating function of the form  $e^{-\alpha t}\cos(\beta t)$ , but instead present multiple oscillation frequencies. A common approach to modeling this phenomenon consists of coupling the qubit to fluctuating or static TLSs [121,122]. In this work, we treat the TLS as an effective qubit that couples to the main qubit via a static ZZ interaction. Thus, TLS excitations translate as dephasing on the main qubit. Note that alternative and more general approaches exist, such as considering additional couplings (e.g., ZX), varying the initial state of the TLS, or considering multiple TLSs; some of these approaches are discussed in Ref. [121]. Although the physical mechanism for TLS coupling is not entirely well understood—whether it is induced by defects, quasiparticles, etc. [122,124– 126—the TLS model is an attractive effective theory due to its mathematical simplicity and accurate description of experimental results.

Figure 3 presents experiments on four different qubits of  $ibm\_auckland$ , where multiple oscillation frequencies are present. Rather than a single oscillating function  $\cos(\beta t)$ , these experiments can be well described by two oscillation frequencies in accordance with Eq. (15), from where both detuning  $\beta$  and TLS coupling strength  $\xi$  can be obtained.

<span id="page-11-0"></span>![](_page_11_Figure_2.jpeg)

FIG. 3. Ramsey experiment (Q*k*<sup>=</sup>0) results for qubits (a) 5, (b) 8, (c) 0, (d) 9 of *ibm\_algiers*. Experiment results (purple circles) are shown, along with the fits based on Eq. [\(15\)](#page-8-2) (solid black lines). Markovian simulations (green diamonds) present excellent agreement with experiment. Detuning values β are obtained from single-qubit characterization: (a) 0.12(9), (b) 0.04(8), (c) 0.16(9), (d) 0.017(0) MHz. Two-level system coupling strength ξ values obtained from the fit of Eq. [\(15\):](#page-8-2) (a) 0.01(3), (b) 0.23(2), (c) 0.24(6), (d) 0.32(0) MHz. Note that for qubit 5 [see panel (a)], ξ is approximately tenfold smaller than β, making it closer to a Markovian evolution. Intuitively, this is seen in the close-to-uniform oscillation frequency.

The qubits shown in Fig. [3](#page-11-0) were selected because they present different ratios of β/ξ , leading to seemingly qualitatively different phenomena. However, these experiments can be well described within the same TLS model, outlined in detail in Sec. [II.](#page-2-0) The excellent agreement between experiment, theory, and simulation serves to validate the effectiveness of the simple yet strikingly predictive TLS model. Lastly, we note that the multifrequency TLS behavior can be found in the vast majority of the qubits studied. However, cases exist where the presence of TLSs may be less obvious. For example, when a single oscillation frequency is observed in Ramsey experiments, this can be the result of a TLS rather than detuning, as shown in Appendix [I.](#page-32-0)

# *2. Characterization of two-qubit crosstalk*

Figure [4](#page-11-1) shows the experimental results obtained from implementing the simultaneous HE protocol on *ibmq\_lima*. Here, Eq. [\(18\)](#page-9-1) is used to fit the crosstalk experiment results. Using the previously characterized singlequbit error parameters in the fit, the crosstalk coupling strength *J* is found, showing excellent agreement between the model fit and experiment. Note [from Eq. [\(18\)\]](#page-9-1) that the measured qubit's decay rate α*<sup>M</sup>* contains a contribution from the spectator qubit's relaxation rate γ*S*. This agrees with results derived in earlier work, see, for example, Refs. [\[71,](#page-35-12)[127,](#page-37-5)[128\]](#page-37-6).

<span id="page-11-1"></span>![](_page_11_Figure_7.jpeg)

FIG. 4. (a) Two-qubit crosstalk experiment (XT) results for all qubit pairs (*M*, *S*) of *ibmq\_lima*. (b) Experiment results of qubit *M* (circles) and fit based on Eq. [\(18\)](#page-9-1) (solid lines). (c) Diagram of crosstalk coupling strength values obtained from the fits shown in (b).

The noise model is able to accurately predict decay rates α*<sup>M</sup>* with information obtained from single-qubit experiments. This result indicates that, on top of coherent rotations, the presence of *ZZ* crosstalk causes an additional incoherent mixed dissipation between the qubits. Under the assumption that *J*MS γ*S*, the dynamics are well described by Eq. [\(18\).](#page-9-1) However, as noted in Ref. [\[127\]](#page-37-5), when *J*MS ∼ γ*S*, this incoherent evolution arises from the ensemble average of stochastic coherent errors on a pertrajectory basis, rather than from a white noise spectrum. This observation provides additional evidence of the detrimental effect that crosstalk has on applications relying on simultaneous qubit manipulation and preservation. This is particularly interesting when considering error suppression techniques such as DD, which can only cancel the coherent rotations but not the incoherent contributions [\[32,](#page-34-16)[71\]](#page-35-12).

## **C. Time-dependent correlated noise on the IBMQP**

In addition to spatially correlated errors such as crosstalk, clear evidence of strong time-correlated noise on IBMQP processors is observed. This type of noise is ubiquitous in solid-state devices, and is known in particular to be widely present in transmon-based qubits [\[77](#page-35-18)[–80,](#page-35-21)[129–](#page-37-7)[131\]](#page-37-8). As described in Sec. [II D,](#page-5-3) properties of time-correlated stochastic noise are captured by the mean and PSD *S*(ω) of the noise. The FFF is the core framework used to investigate the effect of time-correlated errors on system dynamics. The FFF quantifies the noisy dynamics by computing an overlap integral in frequency space between the noise PSD and the FFs *F*(ω, τ ), which capture the sensitivity of the system. Furthermore, the FFF can be used to reconstruct spectral properties of the noise via QNS; see Appendix [B 1](#page-26-0) for a detailed description of the FFF and QNS. In this section, we show that through selected characterization experiments, namely FTTPS and its variations, time-correlated non-Markovian dephasing and control noise can be detected and characterized on IBMQP systems.

## 1. Signatures of Markovian model violations via RB

In this work, we investigate qubits that are subject to dephasing that can be described within two distinct regimes. The first is the Markovian regime, an example of which is shown in Fig. 2. In this case, the observed RB decay rate agrees well with the expected value of  $\delta t(\gamma + \lambda + \nu)$  (see Appendix F for supporting numerical analysis). Here, the fitted noise model provides an accurate effective description of the qubit dynamics, and RB serves as a reliable validation of the fitting procedure.

We also investigate qubits subject to stochastic dephasing with short correlation times, specifically short enough that the HE pulse sequence does not fully refocus the noise. This regime is examined in detail below in Sec. IV C 2. Intuitively, if the dephasing field  $\beta(t)$  varies slowly compared to the experiment duration  $\tau$ , it can be treated as approximately constant, and a single X pulse applied at  $\tau/2$  is sufficient to refocus its effect. If, however,  $\beta(t)$  fluctuates on timescales shorter than  $\tau$ , a single HE pulse will not fully reverse the accumulated phase, and the residual noise correlations contribute to the HE decay.

As a result, the HE experiment decays faster than would be expected for purely white dephasing noise, and a simple exponential fit (motivated by a Markovian assumption) overestimates the incoherent dephasing rate. This behavior can be formalized using the FFF. In this picture, the fitted Markovian rate  $\lambda_{\rm fit}$  attempts to approximate the true whitenoise rate  $\lambda$  together with an additional contribution from the noise power spectral density  $S(\omega)$ , which enters with an approximately quadratic dependence on  $\tau$ . More explicitly, the fit yields a rate  $\lambda_{\rm fit}$  such that  $e^{-\lambda_{\rm fit}\tau}\approx e^{-(\lambda\tau+S(\pi/\tau)\delta\omega\tau^2)}$ . It is, therefore, clear that  $\lambda_{\rm fit}>\lambda$  cannot accurately reproduce the true decay unless  $S(\pi/\tau)\approx 0$  for all  $\tau\leq \tau_{\rm max}$ . Since in this work we consider  $\tau_{\rm max}\approx 200~\mu s$ , this would require  $S(\omega)\approx 0$  for frequencies above  $\sim 2~{\rm kHz}$ .

Consequently, enforcing a Markovian noise model on a qubit experiencing short-time-correlated dephasing leads to an effective white-noise dephasing rate that is artificially enhanced by residual stochastic contributions. Because RB sequences are more effective than HE at decoupling such correlated dephasing, the RB decay rate is primarily sensitive to the true white-noise component. This results in a predicted RB decay that is faster than what is observed experimentally. In this work, we, therefore, use this discrepancy—namely, an overestimation of the RB decay rate by the Markovian model—as a signature of correlated dephasing noise, which motivates the more detailed QNS analysis presented in the following section.

## <span id="page-12-0"></span>2. Correlated dephasing noise

We first focus on the characterization of correlated dephasing noise. We note an important distinction between two types of dephasing noise that are observed on hardware: white (uncorrelated) and colored (correlated). The former is Markovian, and is defined by a locally constant PSD, i.e.,  $S_{\beta}(\omega) = S_{\beta}^{(u)}$ . This corresponds to dephasing noise contributing to the  $1/T_2$  PD decay rate discussed in previous sections. Colored dephasing noise, on the other hand, is characterized by a PSD that varies with  $\omega$ , such that  $S_{\beta}^{(c)}(\omega \to \infty) \to 0$ , and commonly dominates at low frequencies. In practice, qubits generally experience a combination of both correlated and uncorrelated noise, which can be collectively notated by  $S_{\beta}(\omega) = S_{\beta}^{(c)}(\omega) +$  $S_{\beta}^{(u)}$ . This distinction between uncorrelated and correlated will become useful in the present analysis. Since characterization of uncorrelated dephasing noise was discussed in the previous section in the context of HE experiments, it suffices to characterize the correlated contributions.

In the presence of low-frequency correlated noise, a maximum cutoff frequency  $\omega_{\rm max}$  can be generally defined such that  $S_c(\omega < \omega_{\rm max}) \gg S_c(\omega > \omega_{\rm max})$ . The magnitude of this maximum frequency can be compared with the frequency resolution of a given circuit  $\delta\omega = 2\pi/\tau$ , set by the circuit duration  $\tau$ . As will be shown below, this comparison gives rise to three distinct regimes. In turn,  $\delta\omega$  is bounded by the qubit coherence time  $1/T_2 = 1/2T_1 + 1/T_\phi$ . This bound imposes a natural constraint on how finely the frequency features of the correlated dephasing PSD can be resolved. Namely, there exists a minimum frequency resolution  $\delta\omega > \delta\omega_{\rm min} = 2\pi/T_2$ .

First, when  $\omega_{\rm max}\gg\delta\omega_{\rm min}$ , it is possible to drive the qubit such that it becomes sensitive to a large number of frequencies in the range where correlated noise is strong. In this regime, the PSD can be characterized in detail, e.g., via standard QNS techniques [56,88] when  $S(\omega)$  changes sufficiently slow compared to  $\delta\omega$ . Despite the ease in characterization, qubits in this regime were not observed in the course of our investigations and will not be further discussed in this work.

On the other hand, when  $\omega_{\max} \gtrsim \delta \omega_{\min}$ , the PSD can be learned partially by assuming a functional form for  $S_c(\omega)$ . Model parameters can be extracted by fitting to specific experiments designed to sufficiently probe low-frequency dynamics. This approach enables super-resolution that is not afforded by standard QNS approaches. Lastly, if  $\omega_{\max} < \delta \omega_{\min}$ , qubit coherence is lost before enough information of long-time correlations can be collected, and the narrow spectral features of the PSD cannot be resolved. This slowly varying noise is commonly denoted as quasistatic or DC noise, where the PSD  $S_{\beta}^{(c)}(\omega) \propto \delta(\omega)$  is sharply concentrated around  $\omega=0$ . In addition, quasistatic noise can be thought of as fully correlated, the opposite limit to white noise.

<span id="page-13-1"></span>![](_page_13_Figure_2.jpeg)

FIG. 5. (a) Fixed total-time pulse sequences experiment results (circles) and predictions (solid line) obtained from the reconstructed power spectral density (inset) from qubit 4 of  $ibm\_hanoi$  and computed using Eq. (20). (b) Reconstructed power spectral densities from qubits 0 ( $\alpha=2$ ) and 2 ( $\alpha=0$ ) of  $ibmq\_belem$ , showcasing two qualitatively different spectra. Experimental results (solid markers) of Carr-Purcell-Meiboom-Gill experiments with varying dynamical decoupling pulses for (c) qubit 0 and (d) qubit 2 of  $ibmq\_belem$ . Solid lines represent the prediction for each experiment, obtained from using the corresponding power spectral densities shown in (b). (f) Histogram of decay powers A on  $ibm\_algiers$  for Ramsey and Hahn-echo.

When the noise correlations satisfy  $\omega_{\rm max} > \delta\omega_{\rm min}$ , FTTPS experiments can be used to characterize correlated dephasing spectra. Figure 5(a) shows experimental results of FTTPS circuits executed on qubit 4 of  $ibm\_hanoi$ , characterized by a  $T_1 \approx 70~\mu {\rm s}$  at the time of measurement and gate time  $\delta t \approx 0.035~\mu {\rm s}$ . For FTTPS, we set N=128, in order for the total evolution time  $\tau \approx 9~\mu {\rm s}$  to be small compared to  $T_1$ . In turn, this provides a sufficiently fine frequency resolution  $\delta\omega \approx 0.7~{\rm MHz}$ . This combination of parameters allows us to work in the  $\omega_{\rm max} \gtrsim \delta\omega_{\rm min}$  regime, where the noise PSD can be learned parametrically.

The inset of Fig. 5(a) presents the detected dephasing PSD obtained from QNS by fitting an autoregressive moving average (ARMA) model, following the method introduced in Ref. [57]. The expression that relates the survival probabilities with the PSD is given by

$$p_{\beta,k}(\tau) \approx \frac{1}{2} \left( 1 + e^{-\chi_{\beta,k}(\tau)} \right), \tag{20}$$

where the overlap integral is given by  $\chi_{\beta,k}(\tau) = \int_0^\infty S_\beta(\omega) F_{\beta,k}(\omega,\tau) d\omega$ . The definitions corresponding to the FTTPS FFs  $F_{\beta,k}(\omega,\tau) \approx \tau^2 \delta(\omega - 2\pi k/\tau)$  are given explicitly and shown numerically in Appendix B. To validate the noise reconstruction protocol, the spectrum is used to obtain predicted probabilities of FTTPS via numerical integration of the overlap integral. This is shown in the main panel as solid lines, displaying good agreement between the experimental and predicted FTTPS.

Through the ARMA fitting procedure, we identify an optimal number of model parameters based on the Akaike Information Criterion (AIC). The optimal model strongly overlaps with a Lorentzian-like spectrum,

<span id="page-13-2"></span>
$$S_L(\omega;\alpha) = \frac{S_0}{1 + (\omega/\omega_{\text{max}})^{\alpha}},$$
 (21)

where  $\alpha$  captures the color of the noise. This functional form for the correlated dephasing PSD proves to be applicable to a wide range of qubits observed on IBMQP. Furthermore, it is consistent with previous findings of  $1/f^{\alpha}$  dephasing detected on superconducting qubits [77,78,130,131].

By further inspecting FTTPS experimental results, we identify two examples that distinctly demonstrate the differences in ranges of correlation times. The resulting reconstructed PSDs of qubits 0 and 2 of  $ibmq\_belem$  are shown in Fig. 5(b). The spectra show qubit 0 dominated by low-frequency noise, with nonzero contributions above the frequency resolution threshold  $\delta\omega$  (see vertical dashed line), with noise color parameter  $\alpha=2$ . Qubit 2, on the other hand, presents Markovian dynamics with a constant PSD, consistent with  $\alpha=0$ .

Next, we explore the efficacy of the characterized spectra and Eq. (21) through DD experiments. Experiments inspired by  $T_2$  with varying duration and fixed number of DD pulses are selected, following the standard Carr-Purcell-Meiboom-Gill (CPMG) protocol [132,133]. CPMG and FTTPS probe different aspects of the same correlated noise dynamics. FTTPS vary the number of pulses for constant total time, thus changing the frequency location of maximum noise sensitivity  $\omega_k$ . The FF amplitudes are maintained and proportional to the circuit time squared, i.e.,  $F(\omega_k, \tau) \propto \tau^2$ . On the other hand, CPMG<sub>d</sub> experiments with fixed number of pulses d vary the inter-pulse delay times  $\tau/d$ , and consequently modify the FF amplitude without significantly changing the FF distribution in frequency. Analogous to the FTTPS, CPMG pushes the spectral weight of the FFs away from low frequencies, lowering the influence of low-frequency noise on the system evolution with increasing d.

<span id="page-13-0"></span>The results of the CPMG experiments for qubits 0 and 2 are shown in Figs. 5(c) and 5(d), respectively. The experiments show that after applying d=2 pulses to qubit 2, no additional improvement is achieved, indicating that all low

frequency has been decoupled. For qubit 0 [see Fig. 5(d)], on the other hand, significant improvement is observed as more DD pulses are added. This behavior is consistent with the presence of low-frequency dephasing noise in the  $\omega_{\rm max} > \delta \omega$  regime. See Appendix B for another example of a qubit with correlated dephasing noise in the  $\omega_{\rm max} \gg \delta \omega$  regime.

We compare the CPMG experiment results with predictions obtained from the reconstructed spectra. The predicted curves are obtained from assuming that the dominant sources of errors in the DD experiments with d>0 pulses are amplitude damping and dephasing noise. Thus, the survival probability is described by

$$p_{d>1}(\tau) \approx \frac{1}{2} \left( 1 + e^{-\chi_d(\tau) - \tau/2T_1} \right),$$
 (22)

with the decay parameter  $\chi_d(\tau) = \int_0^{\pi/\delta l} S(\omega) F_d(\omega, \tau) d\omega$  [see Appendix B 1]. The  $T_1$  time is obtained from separate  $T_1$  experiments, following the steps outlined in Sec. III B.

The CPMG<sub>d=0</sub> corresponds to Ramsey  $T_2^*$  experiments, and to find the predicted probabilities, we follow the Markovian noise derivation in Eq. (15). We augment the decay to include correlated dephasing noise and including detuning as well as TLS coupling, namely,

$$p_{d=0}(\tau) \approx \frac{1}{2} \left( 1 + e^{-\chi_R(\tau) - \tau/2T_1} \cos(\beta \tau) \cos(\xi \tau) \right), \quad (23)$$

where  $\chi_R(\tau)$  is the Ramsey overlap integral. Note that FTTPS,  $T_1$ , and CPMG experiments are run in a single batch of circuits to minimize the effect of drift in the noise. In all cases, excellent agreement is found between the CPMG<sub>d</sub> experiment results and the predictions, further reinforcing the validity of the correlated dephasing model with the chosen PSD model.

Although qubits exhibiting behavior consistent with the  $\omega_{max}\gtrsim\delta\omega_{min}$  regime are observed, they are not prominent. Based on our investigations, a majority of the IBMQP qubits suffering from correlated dephasing noise can be well described within the DC regime, namely  $\omega_{max}<\delta\omega_{min}$ . The trade-off between adequate frequency resolution and total circuit duration cannot be easily satisfied, thus limiting the utility of the FTTPS experiments. Noting the fact that in the quasistatic noise regime a single echo pulse suffices to decouple the noise, an alternative detection method can be devised through comparing decay rates of Ramsey and HE experiments.

In order to detect the presence of DC noise and quantify its strength, we fit the HE experiments to an *ad hoc* exponentially decaying function

$$p_{\text{HE}}(\tau) = \frac{1}{2} \left( 1 + \exp\left[ -A(\tau/\tau_{\text{max}})^a - \tau/T_2 \right] \right),$$
 (24)

where in the Ramsey case we also include the oscillating cosines as in Eq. (23). The fit parameters a, A, respectively,

capture the color of the noise and the normalized decay power sensed by the qubit in each experiment setting;  $\tau_{\text{max}} = 50 \,\mu\text{s}$  is the maximum experiment time, added for normalization. It is worth noting that the parameter *a* will vary from 1 to 2 for white noise and DC noise, respectively.

An example of a qubit coupled to dephasing noise in the DC regime is shown in Fig. 5(e) via qubit 7 of *ibm\_algiers*. Results are shown for both Ramsey and HE, where the improvement in decay rate after applying a single pulse is evident. This analysis can be further used to show that DC noise is pervasive in IBMQP systems. Figure 5(f) shows the decay power for 15 of the 27 qubits on the *ibm\_algiers* device for both Ramsey and HE. Overall, the Ramsey experiments have larger decay powers, indicating the presence and ubiquity of correlated dephasing noise.

It is worth noting that even though it is challenging to characterize DC noise in detail via QNS, its simplicity proves advantageous in gate modeling. When dephasing noise correlations are predominantly DC, the contributions can be accurately separated into uncorrelated and correlated components. These two contributions can be modeled independently in a straightforward way, avoiding the need to compute FFs and/or average over a large number of noise realizations in simulation. This property will be exploited in Sec. VI to simplify the modeling task in a gate-based approach for computation that provides improved scalability.

### <span id="page-14-1"></span>3. Correlated control noise

<span id="page-14-0"></span>In addition to correlated dephasing, strong indications of correlated control errors were observed on IBMQP devices. Below, we discuss the characterization of this noise source and provide a few representative examples to convey the typical features found on these devices. Through this discussion, we give justification for the inclusion of control noise in the device noise model presented in Eq. (10).

An approach to characterizing noise correlations in faulty control is through QNS. Previous work in this domain has focused on development of sophisticated control techniques based on functional expansions with the aim to thoroughly learn spectral features of control noise [91,94]. Here, we take an alternative, minimalistic approach centered around detection rather than detailed characterization. In order to detect correlations, we rely on FTTPS, which can be used to extract information about control noise under reasonable assumptions, namely that the noise is concentrated around low frequencies. As shown below, while originally designed to address dephasing noise, FTTPS can be tuned to either maximize or suppress sensitivity to low-frequency control noise.

Crucially, FTTPS are maximally sensitive to low-frequency control noise, meaning that most of the weight of their FFs is concentrated around  $\omega = 0$ . Intuitively,

coherent and low-frequency errors accumulate after each pulse, aggregating to a nonzero total over- or underrotation. Assuming control noise is dominant and ignoring for the moment other sources of noise, we can write the survival probability of the  $k^{th}$  FTTPS as

$$p_{\epsilon,k}(\tau) \approx \frac{1}{2} \left( 1 + e^{-\chi_{\epsilon,k}(\tau)} \cos(\bar{\epsilon}k) \right).$$
 (25)

The coherent contribution appears as  $\cos(\bar{\epsilon}k)$  oscillating periodically with the mean of the noise. Note that for weak noise  $\bar{\epsilon} \ll 1/K$ , this term becomes a deviation from identity that increases quadratically with k. In addition, the effect of the stochastic contribution can be quantified from the explicit computation of the control FFs of FTTPS. The control FF can be approximated as  $F_{\epsilon,k}(\omega,\tau) \approx 4k^2\delta(\omega)$ , where the delta function is defined by  $\int_0^{\delta\omega} \delta(\omega) d\omega = 1$  and  $\delta(\omega > \delta\omega) = 0$ . Stochastic noise enters in the survival probability as an exponential decay contribution  $e^{-\chi_{\epsilon,k}(\tau)}$ , where in the low-frequency noise regime  $\chi_{\epsilon,k}(\tau) = \int_0^\infty S_{\epsilon}(\omega) F_{\epsilon,k}(\omega,\tau) d\omega \approx \sigma k^2$ , with  $\sigma =$  $\pi^2 \delta \omega S_{\epsilon}(0)$  representing the standard deviation of the noise. Further details on these FF expressions can be found in Appendix B 3. Using this expression for  $\chi_{\epsilon,k}$  in Eq. (25), the parameter  $\sigma, \bar{\epsilon}$  can be obtained from comparison with experiments. Thus, this analysis shows that FTTPS can be used to detect the presence of low-frequency correlated control errors, as well as distinguish between coherent and stochastic contributions.

In Fig. 6(b), we show examples of FTTPS experiments applied to two qubits influenced predominantly by control noise on *ibmq lima*. Qubit 3 is mostly subject to coherent control errors, i.e.,  $\epsilon(t) \approx \bar{\epsilon}$  is constant. This characteristic is supported by the quadratic decay in the probability as a function of k. Qubit 2, in addition to oscillations, is subject to a decay, which is consistent with a correlated stochastic control noise description where  $\chi_{\epsilon,k}(\tau) > 0$ . As shown in solid lines, the decay and oscillations can be approximately reproduced in simulation by 1/f stochastic control noise. This serves to further justify the choice of low-frequency noise made in  $S_{\epsilon}(\omega)$ , used to derive the approximated expression for  $\chi_{\epsilon,k}$  discussed above. Note that the loss of fidelity with increasing k can be contrasted with the behavior previously observed due to low-frequency dephasing noise in Fig. 5(a), where the effect of the noise was more pronounced for small k. Apart from the qualitatively distinct phenomenon of resonances discussed in Appendix H, high-frequency dephasing noise was not observed, and thus these large-k features in FTTPS suggest that they are a signature of control noise.

To establish the connection between these FTTPS features and control noise with greater certainty, however, we need to evaluate the effect of control errors in isolation. This can be done, for example, by designing an alternative experiment where control noise effects are suppressed

<span id="page-15-1"></span><span id="page-15-0"></span>![](_page_15_Figure_7.jpeg)

FIG. 6. (a) Fixed total-time pulse sequences and robust-fixed total-time pulse sequences circuits, where the explicit distinction of alternating every even  $X_{\pi}$  pulse has been explicitly highlighted. (b) Fixed total-time pulse sequences and (c) robust-fixed total-time pulse sequences examples of qubits presenting mostly coherent (qubit 3) and strong stochastic (qubit 2) control errors in  $ibmq\_lima$ . Empty circles represent experimental results, and solid lines represent simulation of 1/f stochastic control noise with 100 Monte Carlo realizations. As shown, both the decay and oscillations can be approximately reproduced in simulation.

while the contributions of all other sources of errors are unchanged. Interestingly, this can be achieved with a simple modification through which the FTTPS are made insensitive to low-frequency control noise. To this end, we define the robust-FTTPS (R-FTTPS) by alternating the sign of every other X pulse in the standard FTTPS, i.e.,  $X \rightarrow -X$  [see Fig. 6(a)]. On the IBMQP, this is implemented by appending virtual Z gates on each side of all even pulses.

In the absence of control errors, this sign change is undetectable, since the Z gates commute with the native detuning and crosstalk errors, and X and -X pulses implement the same rotation on the Bloch sphere. However, when coherent or low-frequency control errors are present, even and odd pulses contribute approximately equal overrotation angles but with opposite signs. The collective over-rotation error contribution thus cancels after each pair of pulses, supplying the R-FTTPS with robustness to coherent and low-frequency control noise. In the language of the FFF, the effect of phase alternation is to shift the peak sensitivity of the qubit away from low frequencies, i.e.,  $F_{\epsilon,k}^R(\omega=0,\tau)\approx 0$ . Consequently, the R-FTTPS suppress low-frequency control errors on the survival probabilities, as seen by computing  $\chi_{\epsilon,k}^R(\tau)=\int_0^\infty S_\epsilon(\omega)F_{\epsilon,k}^R(\omega,\tau)d\omega\approx 0$  for predominantly low-frequency  $S_\epsilon(\omega)$ . We further elaborate on R-FTTPS in Appendix B 3 a.

The presence of correlated control errors can be established conclusively by comparing the experimental results of FTTPS and R-FTTPS. Figure 6(c) presents

experimental results of R-FTTPS on qubits 2 and 3 of *ibmq\_lima*. Notably, the features surmised to be associated with correlated control noise have been completely suppressed. This markedly distinct outcome from the standard FTTPS protocol agrees with expectations and further provides strong evidence for the presence of low-frequency correlated control errors on these qubits.

# *4. A word on the prevalence of single-qubit correlated noise on IBMQP devices*

The presence of correlated noise naturally gives rise to the following question: how prevalent are these noise sources on IBMQP devices? In order to provide insight into this question, we perform the characterization routines described in Sec. [III B](#page-7-0) on seven different devices. We summarize our findings in Table [II.](#page-16-0)

We categorize qubits as exhibiting Markovian noise only or including correlated noise processes as well. Our findings indicate that among the seven devices studied, approximately 64% of the qubits exhibited pure Markovian noise. Deviations from this behavior were observed, where approximately 26% and 10% experience correlated dephasing or control noise, respectively. Additional cases exist where both correlated noise processes are present. These qubits make up about 5% of the total. Importantly, we observed that the presence of correlated dephasing noise was stable in time across different qubits. That is, qubits undergoing correlated dephasing noise are likely to remain under the influence of this type of noise. This observation becomes important when selecting qubits for different applications and error management protocols. For instance, those that experience a significant amount of correlated noise are potentially promising candidates for DD suppression protocols.

<span id="page-16-0"></span>TABLE II. Summary of single-qubit characterizations performed over seven IBM's quantum platform devices. Qubits found to be well described by the Markovian model produce a fitting error of at most δ = 1% for the overall mean squared error between data and fit. Those above this threshold are determined to be subject to correlated dephasing, control noise, or both. Approximately 64% are found to exhibit purely Markovian behavior, while 26% and 10% experience correlated dephasing or control noise, respectively.

| Processor |      | Type of noise in qubits |                                |                              |
|-----------|------|-------------------------|--------------------------------|------------------------------|
| Name      | Type | Pure<br>Markovian       | Markovian +<br>Corr. dephasing | Markovian +<br>Corr. control |
| belem     | T    | 0,1,2,3                 | 4                              |                              |
| quito     | T    | 0,1,2,4                 | 3                              |                              |
| lima      | T    | 3,4                     |                                | 0,1,2                        |
| nairobi   | I    | 1,2,4,6                 | 0,3,5                          |                              |
| jakarta   | I    | 0,1,3                   | 2,4                            | 4                            |
| lagos     | I    | 1,2,3,5,6               | 0,4                            | 4                            |
| manila    | —    | 0,1,3                   | 2                              | 4                            |

## **D. Characterizing entangling two-qubit ECR gates**

Here, we turn our attention to entangling operations provided by the ECR gate. An example of the composite gate sequence is shown Fig. [7\(a\).](#page-16-1) We employ the noise model of Eq. [\(1\),](#page-2-2) leveraging single-qubit noise parameters in conjunction with additional fitting to the parameters of the effective ECR Hamiltonian [Eq. [\(9\)\]](#page-5-5). As we show below, this noise model is sufficient to account for errors observed during two-qubit operations on fixed coupler IBMQP devices.

Experimental results for repeated ECR gates between qubits 0 and 1 on *ibm\_lagos* can be seen in Fig. [7\(b\).](#page-16-1) Expectation value estimates for *Y* and *Z* are shown in the left and right panels, respectively, for control qubit states |0 and |1. Through the characterization protocols, we estimate a gate over-rotation of *zx* ≈ 0.14, while ζ ≈ 0.01 MHz. The duration of the CR gate is τCR = 0.576µs, which is approximately 16.5-fold larger than the single-qubit gate time.

Importantly, despite the complexity of the gate operation, the LME with single-qubit dephasing and amplitude damping proves to be sufficient for capturing the expectation value decay. As shown in Fig. [7\(b\),](#page-16-1) we find strong

<span id="page-16-1"></span>![](_page_16_Figure_12.jpeg)

FIG. 7. Comparison between experiment and the Lindblad master equation model for the echo cross-resonance gate. (a) Pulse schedule between qubits 0 (control) and 1 (target) of *ibm\_lagos* obtained from Qiskit Pulse. Here, τCR = 0.576µs is much larger than the single-qubit gate duration δ*t* = 0.035µs. (b) Experimental (empty circles) and simulated (solid lines) expectation values *Y* and *Z* for the target qubit obtained by *n* repeated applications of the pulse shown in (a). The control qubit is prepared in |0 (purple) and |1 (blue). Time on the *x* axis is computed as *n*τCR.

agreement between the experiments and the model up to *n* = 16 repetitions of the ECR gate. Although more experimental data may be needed in order to refine the model, we tested 7 pairs of qubits across four different devices, and found that this minimal ECR model was successful in fitting the CR characterization experiments. In addition, for qubits (*c*, *t*) = (0, 1) of *ibmq\_lagos*, the magnitude of *X* was non-negligible, and the model was not sufficient to fit *Y*,*Z*. We attribute these deviations to a large crosstalk strength of *J* ≈ 0.5 MHz, which is inconsistent with the approximations used in the present ECR gate characterization. For the other qubits, the maximum crosstalk strength found was *J* ≈ 0.09 MHz. Thus, we expect the model to fit the ECR experiments as long as crosstalk remains relatively small.

## <span id="page-17-0"></span>**V. APPLICATIONS**

Thus far, we have explored the efficacy of the single and two-qubit models, using the characterization experiments to convey model validation. Single-qubit RB experiments have been used to test the model and show agreement for predicted gate error rates when the qubit is subject to Markovian noise alone, or subject to additional non-Markovian noise sources. Here, we increase the complexity of model testing and examine two distinct multi-qubit scenarios. First, we examine multi-qubit DD and show that our model is capable of predicting state-dependent behavior in the ground state probability. Next, we consider an implementation of VQE in which the goal is to compute the dissociation curve of the H2 molecule.

# **A. Multi-qubit DD**

In this section, we study the impact of simultaneous driving in the presence of parasitic crosstalk. We consider a *main* qubit and investigate its dynamics in the presence of *spectator* qubits that interact with the main qubit via *ZZ* crosstalk. Following Refs. [\[70,](#page-35-11)[71\]](#page-35-12), we perform two types of simultaneous single-qubit experiments.

In Type 1 experiments, the main qubit is allowed to evolve freely. Meanwhile, the spectator qubits are subject to DD. In Type 2 experiments, the roles are reversed: the main qubit is subject to DD, whereas the spectators are allowed to evolve freely. Each experimental scenario utilizes the DD sequence XY4 = *Yf*τ*Xf*τ*Yf*τ*Xf*<sup>τ</sup> , where *X* and *Y* are π-rotations along the direction of the σ*<sup>x</sup>* and σ*<sup>y</sup>* Pauli operators, respectively. *f*<sup>τ</sup> denotes a period of free evolution, where the qubit is allowed to evolve according to its internal dynamics for time τ . To ensure each pulse has equivalent time, *Y* gates are compiled as *X* followed by a virtual *Z*<sup>π</sup> rotation. All qubits, main and spectators, are prepared in either |0, |1 or |+ via simultaneous application of the single-qubit rotation operator *U*. Upon completion of *n* repetitions of the DD sequence, the inverse state preparation unitary is applied to (ideally)

<span id="page-17-1"></span>![](_page_17_Figure_8.jpeg)

FIG. 8. (a) Multi-qubit dynamical decoupling experiment schematics. The main (spectators) qubit is driven by XY4, implementing the *Y* gate as *X* followed by a *Z*<sup>π</sup> rotation, whereas the spectators (main) are left to evolve freely. The state preparation gates used were to prepare the states along |ψ=|0, |1, |+ we use *U* = *I*, *X* , <sup>√</sup>*Y*, respectively. (b) Experiment (circles) and Lindblad master equation simulation (solid lines) results performed on *ibm\_cairo* using qubit 1 as the main qubit. Qubits 0,2 and 4 are taken to be spectators. Each curve is labeled as *MS*, |ψ, where *M*(*S*) represents the evolution of the main (spectator) qubit(s), and |ψ the initial states. F: free evolution; D: dynamical decoupling XY4.

return the qubits to the ground state prior to measurement. A schematic of the circuits is shown in Fig. [8\(a\).](#page-17-1) Note that the circuits shown in Fig. [8\(a\)](#page-17-1) contain the state preparation and measurement gates *U*, *U*†, and the whole circuit corresponds to identity operations on all qubits. As such, in the absence of noise, the survival probabilities would remain at *p*(τ ) = 1.

In Fig. [8\(b\),](#page-17-1) we show an implementation of Type 1 and 2 experiments on *ibm\_cairo*. The main qubit is designated by qubit 1, while spectators are qubits 0,2,4. Experimental data are collected up to a maximum time of *T* = 83.5µs = *n*τ*c*, or equivalently, *n* = 1176 repetitions of XY4. The inter-pulse delay is set to τ = 0, such that the total cycle time τ*<sup>c</sup>* = 4δ*t* is determined solely by the *X* pulse duration (δ*t* = 0.035µs). Measurement statistics are determined from 10 000 shots.

In comparing the experimental data with the LME model, we find excellent agreement. Simulations (solid lines) exhibit strong overlap with experimental data (open symbols). Most notably, the model captures statedependent oscillatory behavior observed in Type 1 experiments. As described in Sec. [III B,](#page-7-0) the presence of a TLS results in an additional oscillation frequency that accompanies ZZ crosstalk. Here, we observe this behavior for the main qubit, specifically for the equal superposition state. The extended LME model predicts these nontrivial dynamics over the range of time considered.

Similarly, our model agrees well with Type 2 experiments. Intuitively, DD applied to the main qubit should result in a suppression of the TLS interaction and thus, an elimination of the oscillation frequency. Both experimental results and simulations corroborate this expectation. In addition, experimental results indicate a slight state-dependent performance in the main qubit. This behavior is also well described by the trained model, further conveying its efficacy.

# B. VQE for H<sub>2</sub> molecule

In addition, we showcase the utility of our noise model in the prediction of hardware dynamics for a quantum algorithm. We focus on VQE [134], a hybrid classical-quantum algorithm for simulating properties of a Hamiltonian. VQE relies on a classical optimizer to minimize an energy functional across a set of parameterized quantum circuits, where the energy is estimated via execution of the quantum circuits on hardware. When focused on finding ground states, the algorithm identifies a circuit that generates an approximation of the molecule's ground state and provides an estimate of its ground state energy.

In this comparison, we study the dissociation curve of the H<sub>2</sub> molecule, using a previously implemented operator-to-circuit mapping [135]. In the ideal case, this two-qubit implementation has shown to produce results compatible with the ideal ground state energy. The circuit is shown in Fig. 9(a). It consists of five singlequbit gates (one of which is parameterized) and two CNOT gates. Based on the mapping of Ref. [135], the average energy  $\langle H(\theta, R) \rangle = \sum_{i} g_{i}(R) \langle O_{i}(\theta) \rangle$  for a given rotation angle  $\theta$  and bond length R can be calculated via a linear combination of expectation values of Pauli operators. As shown in Appendix A of Ref. [135], the expansion coefficients  $g_i(R)$  depend on the fixed bond length of the molecule, and are computed from the second quantization formulation using the Bravyi-Kitaev transformation [136]. The dependence on  $\theta$  enters via the state prepared by the VQE circuit  $|\psi(\theta)\rangle$ , shown in the middle z-rotation in Fig. 9(a), used to compute the expectation values  $\langle O_i(\theta) \rangle = \langle \psi(\theta) | O_i | \psi(\theta) \rangle$ , with  $O_i \in$  $\{\sigma_x^A \sigma_y^B, \sigma_y^A \sigma_y^B, \sigma_z^A \sigma_z^B, \sigma_z^A I^B, I^A \sigma_z^B\}$ . The optimization is carried out by varying the angle  $\theta$  to identify the minimum of  $\langle H(\theta, R) \rangle$ , from where we find the optimal  $\theta_{\text{opt}}$  using an ideal simulator.

We implement the above algorithm on  $ibm\_algiers$ , where A and B are given by qubits 12 and 15, respectively. Both qubits are first subject to the single and two-qubit characterization protocols described in Sec. III B. We find that qubit 15 possesses a strong contribution of correlated dephasing, while qubit 12 is predominantly characterized by Markovian processes. Experimental demonstrations are then performed to estimate the average energy using the optimal  $\theta$  parameters obtained for each R using 10 000

<span id="page-18-0"></span>![](_page_18_Figure_7.jpeg)

FIG. 9. (a) Circuit implementing the variational quantum eigensolver algorithm, from which the ground state energy  $\langle H(\theta,R) \rangle$  is computed. (b) Experiment results (dark blue) after finding optimal  $\theta_{\rm opt}$  offline in an ideal simulator (green), compared with IBM (pink) and our (light blue) simulations. The inset shows the relative error  $\Delta(R)$  between the experimentally obtained energies and the two noise models. At the optimal atomic distance, our model presents a relative error of 0.5%, showing a sevenfold improvement compared to the 3.5% relative error of the IBM model.

shots. The dissociation curve obtained from the quantum hardware is compared against the IBM device noise model and the learned LME model. The results of this comparison are shown in Fig. 9(b).

The IBM device noise model draws on characterization data imported from the backend properties. These data are updated periodically, typically once over the course of 24 h. In the simulations shown in Fig. 9, the characterizations were performed approximately 9 h prior to the experiments. The device noise model consists of single and two-qubit depolarizing errors followed by thermal relaxation errors. Readout errors for all measurements are also included. Assuming pure Markovian dynamics, the default device noise model does not fully capture prominent noise sources. As a result, we find that our noise model affords stronger agreement with the hardware.

We quantify the difference in performance between the models via the relative error in energy,

$$\Delta(R) = \left| \frac{E_{\text{sim}}(R) - E_{\text{exp}}(R)}{E_{\text{exp}}(R)} \right| \times 100\%.$$
 (26)

Shown in the inset of Fig. 9(b) is the relative error as a function of R for both noise models. The vertical dotted line denotes the optimal atomic distance  $R_{\text{opt}} =$ 

0.75 A. Here, the default IBM device noise model yields (*R*opt) ≈ 3.6%. In contrast, our noise model obtains a relative error of (*R*opt) ≈ 0.5%, a sevenfold improvement over the default model. This improved agreement speaks to the efficacy of our model and its potential applicability to larger quantum systems implementing more complex quantum circuits.

Lastly, we test the reliance of these results on the correlated dephasing noise contribution of our noise model. To this end, we substitute the correlated dephasing term in the Hamiltonian with a modified PD channel. The corresponding *T*<sup>φ</sup> is obtained from fitting the HE experiment with Eq. [\(14\),](#page-8-3) following the steps outlined in Sec. [IV A,](#page-9-2) from where we obtain *T*<sup>φ</sup> ≈ 29µs. This "Markovianized" version of our noise model resembles closely the IBM one, had it been characterized shortly before the VQE experiment was run, while including more realistic sources of noise. Using the "Markovianized" model, we calculate a relative error (*R*opt) ≈ 3.8%, consistent with the IBM model. Thus, the non-Markovian model outperforms the "Markovianized" model in the VQE application.

This result highlights the importance of including noise correlations for accurate predictions of complex quantum applications influenced by non-Markovian noise. The non-Markovian model rests on more physically motivated principles. Enforcing a Markovian fit often leads to model violations, where parameters such as *T*<sup>φ</sup> are obtained from a HE characterization experiment presenting clear deviations from exponential decays [e.g., see Fig. [5\(d\)\]](#page-13-1). Standard IBM calibrations appear to rely on assumptions of exponential decay for *all* qubits. This approach can yield unreliable predictions of model parameters when non-Markovian noise is present, and ultimately, improper modeling of quantum circuit dynamics. Consequently, when non-Markovian noise is present, the explicit modeling of correlations is paramount.

# **C. Proposals for informing error management protocols**

An accurate and physically grounded error model is a critical component of effective quantum error management across all layers of the quantum stack. In the domain of dynamical error suppression, detailed characterization of the underlying noise processes enables the design of control strategies that selectively target dominant decoherence mechanisms. For instance, knowledge of the noise PSD informs the construction of DD sequences optimized for suppressing specific frequency components, such as lowfrequency 1/*f* noise or narrowband fluctuations [\[91](#page-36-23)[,95\]](#page-36-2).

Similarly, realistic noise models are essential for the application of quantum optimal control techniques, such as GRAPE and CRAB, where pulse shaping can be tailored to minimize gate infidelity by exploiting regions of parameter space less sensitive to fluctuations [\[137](#page-37-15)[,138\]](#page-37-16). These approaches are particularly effective when error models account for non-Markovian dynamics or state-dependent dissipation, which can otherwise be overlooked in simplified models. That said, many of these techniques focus on specific subclasses of noise processes, while ignoring others, albeit often with well substantiated assumptions. Common examples of these assumptions are static Hamiltonians or ignoring dissipative processes. A more comprehensive model such as the one introduced in this work would allow for the development of more effective control strategies under hardware-informed noise models.

In error mitigation, accurate noise modeling directly impacts the fidelity of postprocessing strategies aimed at reducing the effects of noise in near-term devices. In techniques such as zero-noise extrapolation, the reliability of the extrapolated observables depends critically on how well the scaling of noise with circuit depth or control parameters is captured [\[23,](#page-34-17)[24,](#page-34-18)[45\]](#page-34-19). Physically motivated ansätze for extrapolation can significantly outperform naive polynomial fits, particularly in regimes where the noise exhibits saturation or nonlinearities. Probabilistic error cancelation relies on expressing the noisy operation as a linear combination of ideal gates and invertible noise processes [\[24,](#page-34-18)[25\]](#page-34-20). Error models that go beyond the Pauli channel approximation—capturing coherent or non-Pauli errors—can enable decompositions with lower sampling overhead or improved stability. Furthermore, detailed modeling of correlated or nonlocal errors can guide the development of hybrid mitigation strategies that incorporate device-specific noise structure, including crosstalk and leakage [\[139\]](#page-37-17).

In the regime of quantum error correction (QEC), accurate error models inform both the choice of codes and the design of decoding algorithms. For example, in systems with highly biased noise, tailored codes such as the XZZX surface code offer higher thresholds and lower overhead than conventional surface codes [\[140\]](#page-37-18). Similarly, when spatial or temporal correlations are present, decoding strategies can be adapted to incorporate these correlations, either analytically [\[141\]](#page-37-19), through machine learning approaches trained on realistic error distributions [\[142\]](#page-37-20), or windowing methods [\[143\]](#page-37-21). Ubiquitous noise mechanisms, such as coherent rotations or state leakage, can impact decoder performance and fault-tolerance thresholds as well if left unmodeled. Consequently, accurate noise characterization is indispensable not only for suppressing and mitigating errors in the near term, but also for achieving scalable fault-tolerant quantum computation in the long term.

# <span id="page-19-0"></span>**VI. EXTENSIONS TO MULTI-QUBIT CIRCUITS**

Here, we comment on the scalability of the characterization protocol and the model. In the former, we address the number of characterization experiments required as the system size increases. Model scalability is tackled by reducing the LME models to composite channel approximations that effectively capture stochastic and extended degrees of freedom when applicable.

## **A. Extending the noise model**

The LME models described above exhibit strong agreement with hardware in both single and two-qubit demonstrations. Despite this success, one cannot overlook the analytical and numerical challenges associated with solving the LME for multi-qubit systems beyond a few qubits. In order to address these challenges, we adopt a perturbative interaction-picture treatment of noisy gate dynamics, following the steps recently outlined in Ref. [\[144\]](#page-37-22). Here, the main strategy is to replace the need to solve the system of coupled differential equations with a sequence of matrix products. Although the dimension of these matrices grow exponentially in the number of qubits, this approach enables one to circumvent a costly eigenvalue problem; the trade-off being an approximate representation of the gate dynamics.

Let *L*(*t*) denote the possibly time-dependent Lindbladian describing the noise. In the interaction picture with respect to the ideal gate evolution, the noisy dynamics are governed by the master equation

$$\frac{d}{dt}\rho_{I}(t) = \mathcal{L}_{I}(t)[\rho_{I}(t)]$$

$$= -i[H_{I}(t), \rho_{I}(t)] + \sum_{j} \gamma_{j}(t) \left(L_{j,I}(t)\rho_{I}(t)L_{j,I}^{\dagger}(t)\right)$$

$$-\frac{1}{2} \left\{L_{j,I}^{\dagger}(t)L_{j,I}(t), \rho_{I}(t)\right\}, \qquad (27)$$

where *H*(*t*) is defined in Eq. [\(2\),](#page-2-1) and the interaction-picture density matrix, Hamiltonian, and jump operators evolve as

$$\rho_{I}(t) = U_{C}^{\dagger}(t)\rho(t)U_{C}(t), 
H_{I}(t) = U_{C}^{\dagger}(t)H(t)U_{C}(t) - H_{C}(t), 
L_{j,I}(t) = U_{C}^{\dagger}(t)L_{j}U_{C}(t),$$
(28)

with *UC*(*t*) being the unitary evolution generated by *HC*(*t*). This interaction-picture formalism captures how the gate reshapes the effective action of noise: even if *L*(*t*) is fixed in the lab frame, its transformed action can mix noise channels, break symmetries, or induce coherent rotations that are not captured in static approximations.

We use this framework to construct gate-dependent effective noise channels *<sup>k</sup>* for each gate *Gk* in a chosen gateset {*Gk*}, which is implemented with duration τ*<sup>k</sup>* via a Lindbladian *Lk*. Note that *Gk* may comprise multiple single- or two-qubit gates operated in parallel, and that the Lindbladian *L<sup>k</sup>* corresponds to the one introduced in Eq. [\(1\)](#page-2-2) for a *HC* generating a specific gate *Gk*. For each gate, we evaluate Eq. [\(27\)](#page-20-0) under a slowly varying realization of the parameters β(*t*) and (*t*). In practice, we may assume that the statistics of these parameters are quasistatic, and thus the cost of averaging becomes relatively low. The resulting evolution operator is then decomposed into the ideal and noisy parts

$$e^{\mathcal{L}_k \tau_k} = G_k \Lambda_k(\tau_k), \tag{29}$$

where the noise channel is computed by taking

$$\Lambda_k = \left\langle \mathcal{T} \exp \left[ \int_0^{\tau_k} \mathcal{L}_I(t) \, dt \right] \right\rangle_{\beta, \epsilon}, \tag{30}$$

with *T* denoting time ordering. In general, the operators *<sup>k</sup>* can be computed using perturbation theory via the Magnus expansion, as shown in Ref. [\[144\]](#page-37-22). In particular, this is computed explicitly in Appendix [A](#page-22-0) for single-qubit gates using our noise model, and was the approach followed to compute simulations throughout this work; thus, showcasing its effectiveness.

Lastly, the ideal evolution given by a specific circuit can be described by a sequence of operators {*Gk*}*k*∈*<sup>K</sup>* indexed by a set *K*, i.e., **G** = *<sup>k</sup>*∈*<sup>K</sup> Gk*. As such, the effect of the noise over a circuit can be modeled by a noisy implementation

<span id="page-20-1"></span>
$$\tilde{\mathbf{G}} = \left\langle \prod_{k \in K} G_k \Lambda_k \right\rangle_{\beta, \epsilon}, \tag{31}$$

<span id="page-20-0"></span>averaging the dynamical maps over many stochastic noise realizations. A convenient way of computing this product is to expand the exponential in terms of the Magnus terms. This approach avoids the need for a full matrix exponentiation at the cost of reducing the efficacy of the approximation [\[144\]](#page-37-22).

Note that Eq. [\(31\)](#page-20-1) assumes the noise is quasistatic. As was described in detail in Sec. [IV C 2,](#page-12-0) the majority of qubits exhibiting correlated dephasing noise consist of mostly quasistatic dephasing. Thus, this approach yields a gate-dependent noise model that accounts for both shorttime interaction effects and long-timescale fluctuations within a perturbative, but physically motivated framework. It also resolves the limitations of modeling noise as a gateindependent channel in the lab frame, particularly when high-fidelity gates are implemented via strong, but finite duration pulses that substantially modify the noise action.

## **B. Scaling of characterization protocol**

The scaling of the characterization protocol is tightly coupled to the required noise model. If we assume that all model parameters are needed then the model is determined by 10 single-qubit parameters and three parameters associated with qubit-qubit interactions. Thus, for a processor consisting of *Q* qubits, 10*Q* parameters are required to describe single-qubit dynamics. As such, an equivalent number of characterization circuits are required at a minimum. However, more may be desired to obtain more accurate estimates.

Parallelization can assist in reducing the number of circuits. This is common practice among existing IBMQP devices, where simultaneous characterization experiments are performed on next-nearest neighbor qubits to avoid unwanted crosstalk interactions. Note that parallelization in QNS is also possible using crosstalk robust characterization protocols such as those introduced in Ref. [\[32\]](#page-34-16). As a consequence, the inherent overhead in the number of qubits with regards to characterization time can be substantially reduced.

In the case of the two-qubit parameters, the number of required characterization experiments is highly dependent upon the device topology. For the heavy-hex topology, each unit cell contains 12 qubits with an average qubit degree of 2.4 [\[145\]](#page-37-23). The ringlike topology results in approximately 12 interactions per unit cell. For *L* unit cells, there are approximately 9*L* distinct interactions that must be characterized. The CR and crosstalk characterization protocols are sufficient to perform this characterization, where a lower bound of 9*L* circuits must be executed. Parallelization can again be utilized to further reduce the overhead, where non-nearest neighbor interactions are simultaneously characterized.

# <span id="page-21-0"></span>**VII. SUMMARY AND CONCLUSIONS**

In this work, we address the challenge of balancing model sparsity with predictive power. To this end, we propose a model for single and two-qubit gate operations on IBMQP fixed-frequency superconducting transmons. The model is a modified LME that includes both Markovian and non-Markovian contributions. The latter includes extending the model to include coupling between the system and classical or quantum environments. Using only a few additional degrees of freedom, the model is capable of capturing spatiotemporally correlated noise processes observed on hardware. The model is specified by at most 10 parameters per qubit and three parameters per qubit pair that can be learned via seven characterization experiments, each potentially comprised of multiple circuits depending on the desired accuracy.

Using deterministic characterization protocols, we study the noise profiles of seven devices within the *Falcon* and *Eagle* processor generations, for a total of 39 qubits. While we find that a significant subset of qubits are described by Markovian noise alone (64%), approximately 26% and 10% are subject to correlated dephasing or control noise, respectively. Quantum crosstalk and coupling to TLSs are also commonly observed.

Device characterizations provide key insights into dominant noise channels and are utilized to develop highly predictive error models for single- and two-qubit operations. The efficacy of the learned models is explored through characterization, error suppression, and quantum computing experiments. Single-qubit models are tested against RB demonstrations and shown to accurately predict gate error rates. Multi-qubit models are examined through simultaneous single-qubit DD and a VQE designed to find the ground state of molecular hydrogen. The former exhibits strong agreement with state-dependent fidelity decay observed in previous studies. The latter highlights the predictive power of our model particularly for qubits that display non-Markovian noise. We show that our model is capable of achieving relative errors that are sevenfold better than Qiskit's default error model.

Lastly, we present an approach for extending the noise model to multi-qubit circuits. This approach relies on effective Liouvillian theory and compositions of channels to model gate sequences with temporally correlated noise. Furthermore, we discuss how the model parameters can be learned via parallelization of the characterization protocol.

Although the noise model introduced here is targeted towards fixed-frequency transmons, the processes discussed are general and pervasive to all quantum devices. Thus, we expect this work to provide valuable insight into the development of different superconducting-based qubits as well as other architectures, most notably when subject to limited device access. In addition, accurate modeling is essential not only for quantum computing but also for all quantum applications. For instance, the scalability of this noise characterization model allows for efficient optimization of multi-qubit sensor arrays in real-time noise monitoring, enhancing the performance of quantum magnetometers and quantum-nondemolition-based photon detectors in dynamic environments.

Further examinations are required to determine if the model presented here continues to yield predictive power as the system size increases. This is true for both the LME approach, which suggests that at most two-qubit error operators are required to predict hardware behavior and the reduced model based on effective Liouvillian theory. Nevertheless, this work emphasizes the viability of effective non-Markovian noise models for describing complex multi-qubit dynamics on superconducting qubits in a variety of applications.

# **ACKNOWLEDGMENTS**

This work was supported in part by the U.S. Department of Energy (DOE), Office of Science, Office of Advanced Scientific Computing Research (ASCR), the Accelerated Research in Quantum Computing program under Award No. DE-SC0020316 and DE-SC0025509. This research used resources of the Oak Ridge Leadership Computing Facility, which is a DOE Office of Science User Facility supported under Contract No. DE-AC05-00OR22725.

### **DATA AVAILABILITY**

The data that support the findings of this article are openly available [146], embargo periods may apply.

# <span id="page-22-0"></span>APPENDIX A: SOLUTIONS TO THE LME IN THE MARKOVIAN REGIME

### 1. Single-qubits

In the Markovian limit, the dynamical evolution under the above mentioned processes can be studied directly using the LME. For simplicity, we suppress the qubit index j. We assume constant x-control with duration  $\delta t$  that executes a rotation  $\theta$ , i.e.,  $\Omega(t) = \theta/\delta t$ . Thus, the control Hamiltonian [Eq. (3)] during the implementation of a gate takes the time-independent form  $H_C = (\theta/2\delta t)\sigma_x$ . Furthermore, we assume the noise Hamiltonian [Eq. (10)] consists of detuning and coherent control errors, i.e.,  $\beta(t) = \beta$  and  $\epsilon(t) = \epsilon$ . Since SPAM errors act only at the end of the circuit, they are represented as a quantum map after the circuit's control sequence. Defining the noisy control rotation frequency  $\omega = (1 + \epsilon)\theta/\delta t$ , the LME becomes

$$\dot{\rho}(t) = \mathcal{L}(\rho, \mathcal{N}_1)$$

$$= -i\frac{\omega}{2} [\sigma_x, \rho] - i\frac{\beta}{2} [\sigma_z, \rho]$$

$$+ \frac{\lambda}{2} (\sigma_z \rho \sigma_z - \rho) + \frac{\nu_\theta}{2} (\sigma_x \rho \sigma_x - \rho)$$

$$+ \sum_{\pm} \gamma^{\pm} \left( \sigma^{\pm} \rho \sigma^{\mp} - \frac{1}{2} \{ \sigma^{\mp} \sigma^{\pm}, \rho \} \right), \quad (A1)$$

where  $\mathcal{L}$  is the Lindbladian superoperator, and  $\mathcal{N}_1$  the set of all single-qubit error parameters. Note that the bit-flip noise with rate  $\nu$  only acts when a gate is implemented, i.e.,  $\nu_{\theta} = 0$  if  $\theta = 0$ , and  $\nu_{\theta} = \nu$  otherwise.

In order to solve Eq. (A1), we follow the steps of Ref. [48]. Moving to the Bloch vector equation in Eq. (11), we find that  $\vec{c} = (0, 0, \gamma(2q - 1))$ , and the coupling matrix is

$$\mathbf{G} = \begin{pmatrix} -\left(\frac{\gamma}{2} + \lambda\right) & -\beta & 0\\ \beta & -\left(\frac{\gamma}{2} + \lambda + \nu\right) & -\omega\\ 0 & \omega & -(\gamma + \nu) \end{pmatrix}. \quad (A2)$$

In this form, Eq. (11) can be solved using standard coupled differential equations methods. This equation can be solved numerically for the identity gate and native X rotations, and subsequently stored for simulation. Moreover, in the weak noise regime, Eq. (12) can be written analytically (see next section).

An analytical solution of the LME can be a powerful way to provide insight into the effects of noise on the evolution of the system. However, computing the exponential  $U(\tau) = e^{G\tau}$  for a general **G** can be challenging. Furthermore, **G** may not be invertible. In this section, we provide analytical solutions to Eq. (12) in the two cases of interest: identity gates and X rotations.

## <span id="page-22-2"></span>2. Identity gates

In the case of identity operations, the LME can be solved exactly. Following the steps outlined in the previous section, we set  $\theta = \nu = 0$  since no control noise is present in the absence of qubit drive. Defining for notational convenience  $\alpha = \gamma/2 + \lambda$ , we write the LME solution in Bloch vector form

$$\vec{v}(t_0 + \tau) = \begin{pmatrix} e^{-\alpha\tau} \cos(\beta\tau) & -e^{-\alpha\tau} \sin(\beta\tau) & 0\\ e^{-\alpha\tau} \sin(\beta\tau) & e^{-\alpha\tau} \cos(\beta\tau) & 0\\ 0 & 0 & e^{-\gamma\tau} \end{pmatrix}$$

$$\cdot \vec{v}(t_0) + \frac{1 - e^{-\gamma\tau}}{\gamma} \vec{c}, \tag{A3}$$

which holds in general for a free evolution of duration  $\tau$ . In the practical case of weak noise and short gate time regime  $\gamma \tau \ll 1$ , it is possible to approximate the inhomogeneous term with  $(1-e^{-\gamma \tau})/\gamma \approx \tau$ .

#### 3. Perturbative solution for X control

<span id="page-22-1"></span>In this section, we provide a solution to the LME in the presence of X control in the weak noise regime. We follow the perturbative approach of the FFF [96]. For a nonzero rotation, such as those corresponding to X,  $\sqrt{X}$  gates, the generator G can be written as a perturbation from the noiseless generator  $G_0$ . Writing this explicitly as  $G = G_0 + g$ , we define

$$\mathbf{G_0} = \begin{pmatrix} 0 & 0 \\ 0 & 0 & -\omega \\ 0 & \omega & 0 \end{pmatrix}, \quad \mathbf{g} = \begin{pmatrix} -\alpha & -\beta & 0 \\ \beta & -\mu & 0 \\ 0 & 0 & -\eta \end{pmatrix},$$
(A4)

with  $\mu = \alpha + \nu$ ,  $\eta = \gamma + \nu$ . In the following we will assume  $||\mathbf{g}|| \ll ||\mathbf{G}_0||$ , which holds as long as the noise is sufficiently weak, where  $||\cdot||$  is the Schatten 1-norm. Distinguishing between  $\mathbf{g}$  and  $\mathbf{G}_0$  is further motivated by the fact that it is easy to compute the effect of an ideal rotation on the Bloch vector, i.e.,

$$U_0(\tau) = e^{\mathbf{G}_0 \tau} = \begin{pmatrix} 1 & 0 & 0 \\ 0 & \cos(\omega \tau) & -\sin(\omega \tau) \\ 0 & \sin(\omega \tau) & \cos(\omega \tau) \end{pmatrix}, \quad (A5)$$

which enables the perturbative approach.

First, we take the problem to the toggling frame, i.e., perform a change of basis with respect to  $\mathbf{G_0}$ , and we write  $U(\tau) = U_0(\tau)\tilde{U}(\tau)$ . Here,  $\tilde{U}(\tau)$  can be thought of as analogous to the noise propagator in the toggling frame, and is the solution to the differential equation  $(d/dt)\tilde{U}(t) = \tilde{\mathbf{g}}(t)\tilde{U}(t)$ , where  $\tilde{\mathbf{g}}(t) = U_0^{\dagger}(t)\mathbf{g}U_0(t)$ . Note that both  $U(\tau)$  and  $U_0(\tau)$  can be written as solutions to the same differential equation, with generators  $\mathbf{G}$  and  $\mathbf{G_0}$ , respectively. Using the first-order Magnus expansion [147], we can write  $\tilde{U}(\tau) \approx e^{\Phi(\tau)}$ , where

$$\Phi(\tau) = \int_0^{\tau} U_0^{\dagger}(t) \mathbf{g} U_0(t) dt \tag{A6}$$

is first order in the noise parameters.

Next, the inverse of **G** needs to be computed. In order to ensure that **G** is invertible we require that  $\alpha \neq 0$  and  $\omega \neq 0$ . The latter is satisfied for both  $\pi$  and  $\pi/2$  rotations of interest, as long as  $|\epsilon| \ll 1$ , whereas the former will hold as

long as  $T_1$ ,  $T_2$  are finite. Then, keeping the first two orders in the noise parameters,

$$\mathbf{G}^{-1} = \frac{-1}{\alpha \omega^2} \begin{pmatrix} \omega^2 & -\beta \eta & \beta \omega \\ \beta \eta & \alpha \eta & -\alpha \omega \\ \beta \omega & \alpha \omega & \alpha \mu + \beta^2 \end{pmatrix}. \tag{A7}$$

Lastly, a first-order approximation can be taken where  $\tilde{U}(\tau) \approx I + \Phi(\tau)$ , which yields  $e^{G\tau} \approx e^{G_0\tau}(I + \Phi(\tau))$ . With  $e^{G\tau}$  and  $G^{-1}$  calculated explicitly, we can find an analytical expression for Eq. (12). This is, by approximating  $e^{G\tau} \approx U_0(\tau) (I + \Phi(\tau))$ , we obtain

$$\vec{v}(t+\tau) = e^{\mathbf{G}\tau} \cdot \vec{v}(t) + \left(e^{\mathbf{G}\tau} - I\right) \cdot \mathbf{G}^{-1} \cdot \vec{c}$$

$$\approx \mathbf{L}(\tau) \cdot \vec{v}(t) + \vec{u}(\tau), \tag{A8}$$

where defining cosc(x) = (1 - cos(x))/x for notational convenience, we have

$$\vec{u}(\tau) = \gamma \tau (2q - 1) \begin{pmatrix} 0 \\ \cos c(\omega \tau) \\ -\sin c(\omega \tau) \end{pmatrix}$$
(A9)

and

$$\mathbf{L}(\tau) = \begin{pmatrix} e^{-\alpha\tau} & -\beta\tau \operatorname{sinc}(\omega\tau) & \beta\tau \operatorname{cosc}(\omega\tau) \\ \beta\tau \operatorname{sinc}(\omega\tau) & e^{-\frac{(\mu+\eta)\tau}{2}} \operatorname{cos}(\omega\tau) - \frac{(\mu-\eta)\tau}{2} \operatorname{sinc}(\omega\tau) & e^{-\frac{(\mu+\eta)\tau}{2}} \operatorname{sin}(\omega\tau) \\ \beta\tau \operatorname{cosc}(\omega\tau) & e^{-\frac{(\mu+\eta)\tau}{2}} \operatorname{sin}(\omega\tau) & e^{-\frac{(\mu+\eta)\tau}{2}} \operatorname{cos}(\omega\tau) + \frac{(\mu-\eta)\tau}{2} \operatorname{sinc}(\omega\tau) \end{pmatrix}. \tag{A10}$$

This analytical expression is useful to perform singlequbit simulations and examine the effect of noise when the qubit is being driven.

#### <span id="page-23-0"></span>4. Prediction of characterization circuits

The results from the above sections can be used to compute predictions for the characterization experiments. Here, we show how it can be used to compute the results shown in Eqs. (13)–(17). Denoting by  $\vec{v}(\tau)$  the Bloch vector state at the end of a given circuit, the effect of SPAM errors on the Bloch vector is to take

$$\vec{v}(\tau) = \begin{pmatrix} v_x(\tau) \\ v_y(\tau) \\ v_z(\tau) \end{pmatrix} \xrightarrow{\mathcal{E}_M(\cdot)} \begin{pmatrix} v_x(\tau) \\ v_y(\tau)(1 - 2s) \\ v_z(\tau)(1 - 2s) \end{pmatrix}. \tag{A11}$$

For the corresponding density matrix  $\rho(\tau) = (I + \vec{v}(\tau) \cdot \vec{\sigma})/2$ , the survival probability of the  $|0\rangle$  state is computed

in terms of the Bloch vector as

<span id="page-23-1"></span>
$$\langle 0 | \rho(\tau) | 0 \rangle = \frac{1}{2} \langle 0 | I + \vec{v}(\tau) \cdot \vec{\sigma} | 0 \rangle$$

$$= \frac{1}{2} \left( 1 + \sum_{j=x,y,z} v_j(\tau) \langle 0 | \sigma_j | 0 \rangle \right)$$

$$= \frac{1}{2} (1 + v_z(\tau)). \tag{A12}$$

Consequently, the Bloch vector component of interest is  $v_z(\tau)$ . Combining these two results, we can see that the survival probability becomes

$$\langle 0 | \rho(\tau) | 0 \rangle = \frac{1}{2} (1 + (1 - 2s)v_z(\tau)).$$
 (A13)

Throughout this section, we focus on calculating the z component of the Bloch vector at the end of the circuit

for the characterization experiments, of duration  $\tau$ . Moreover, we remove the subscript and denote  $v_z(\tau)$  by  $v(\tau)$ , for convenience of notation.

## a. (M) SPAM

The SPAM experiment consists of a single X gate of duration  $\delta t$ . Assuming weak noise, particularly  $s, \gamma \delta t \ll 1$ , it is straightforward to see that before the measurement

- (1) Coherent errors contribute quadratically, i.e.,  $v(\delta t) = -1 + O(\epsilon^2, (\beta \delta t)^2)$ .
- (2) Dissipative effects contribute linearly, i.e.,  $v(\delta t) = -1 + \delta t O(\gamma, \lambda, \nu)$ .

Then we apply the measurement error map  $\mathcal{E}_M$  with rate s. To first order in the noise parameters,

$$v(\delta t) = s + \delta t O(\gamma, \lambda, \nu). \tag{A14}$$

Finally, we make the experimentally verifiable assumption that the dissipative effects are weak compared to the duration of a single-qubit gate, i.e.,  $\delta t \ll 1/\gamma$ ,  $1/\lambda$ ,  $1/\nu$ . Thus, we obtain  $v(\delta t) \approx s$ .

## b. $(T_1)$ thermal relaxation

The  $T_1$  experiment result is easy to compute following a similar analysis. The experiment starts with a single X gate, which, as was discussed in the SPAM experiment case, only contributes error terms from dissipative effects, i.e.,  $v(\delta t) = -1 + \delta t \, O(\gamma, \lambda, \nu)$ . Since there are no more gates applied until the end of the experiment, and the state will be primarily along the  $|1\rangle$  direction, neither  $\lambda$  nor  $\nu$  will accumulate significantly. Consequently, we focus on the effect of GAD. Since the experiment consists of successive applications of I gates, we can use Eq. (A3), with  $t_0 = \delta t$  and  $\vec{v}(\delta t) \approx (0,0,-1)$ , where the approximation holds up to terms proportional to  $\gamma \, \delta t, \lambda \, \delta t, \nu \, \delta t \ll 1$ . Hence, the z component of the Bloch vector at time  $\tau \gg \delta t$  becomes

$$v(\tau) = -e^{-\gamma\tau} + (1 - e^{-\gamma\tau})(2q - 1)$$
  
= -1 + 2q(1 - e^{-\gamma\tau}), (A15)

up to a term  $\delta t O(\gamma, \lambda, \nu)$ . Note that a result of the above equation is that, after applying the final X measurement gate, the asymptotic probability of finding the state in the  $|0\rangle$  state is  $p(\tau \to \infty) = 1 - q + \delta t O(\gamma, \lambda, \nu)$ .

## c. (T<sub>2</sub>) Hahn-echo

The  $T_2$  experiment state can be computed in a similar fashion to that of  $T_1$ . Ignoring constant order effects that do not scale with  $\tau$ , we prepare the state on the plane with a  $\sqrt{X}$  gate, thus taking  $\vec{v}(0) = (0, 0, 1)$  to  $\vec{v}(\delta t) \approx (0, -1, 0)$ . Evolving with Eq. (A3) for a time  $\tau/2$ 

yields  $\vec{v}((\tau/2)^-) \approx e^{-\alpha\tau/2}(\sin(\beta\tau/2), -\cos(\beta\tau/2), \psi_1)$ , where we defined  $\psi_1 = e^{\alpha\tau/2}(1-e^{-\gamma\tau/2})(2q-1)$ . Next, an X gate is applied with the effect of changing signs of the y,z components, i.e.,  $\vec{v}((\tau/2)^+) \approx e^{-\alpha\tau/2}(\sin(\beta\tau/2),\cos(\beta\tau/2),-\psi_1)$ . The superscripts  $()^\pm$  indicate whether the vector is evaluated before or after the echo pulse. Following the echo, the qubit is left to evolve freely for a time  $\tau/2$ . Once again drawing on Eq. (A3), we find  $\vec{v}(\tau) \approx (0,e^{-\alpha\tau},\psi_2)$ , where the specifics of  $\psi_2$  are irrelevant for the final result. Once the final  $\sqrt{X}^\dagger$  is applied, the y and z components of the Bloch vector are exchanged, yielding

$$v(\tau) = e^{-\alpha \tau},\tag{A16}$$

up to terms proportional to  $\delta t O(\gamma, \lambda, \nu)$ .

## d. $(Q_{k=0})$ Ramsey experiments

The multifrequency oscillations observed in Ramsey experiments can be readily modeled by coupling the system qubits to a TLS initialized in the thermal state  $\rho_{\text{TLS}}^{\text{th}} = p_0 |0\rangle \langle 0| + p_1 |1\rangle \langle 1|$ , where  $p_{0,1} = 1/\left(1 + e^{\mp\hbar\omega/k_BT_{\text{TLS}}}\right)$  are the temperature dependent thermal state populations [50]. The single-qubit system is enlarged to a qubit+TLS system interacting via a ZZ coupling, which in the absence of control can be represented by the Hamiltonian

$$H = \frac{1}{2}(\beta Z_{Q}I_{\text{TLS}} + \xi Z_{Q}Z_{\text{TLS}}). \tag{A17}$$

Since this Hamiltonian is diagonal, and momentarily ignoring dissipative processes, the evolution is dominated by a diagonal unitary operator

$$U(t) = e^{-iHt}$$

$$= \operatorname{diag}(e^{-i\frac{t}{2}(\beta+\xi)}, e^{-i\frac{t}{2}(\beta-\xi)}, e^{i\frac{t}{2}(\beta+\xi)}, e^{i\frac{t}{2}(\beta-\xi)}).$$
(A18)

Upon executing the Ramsey protocol, the joint state is initialized in  $\rho_{Q,TLS}(0) = |0\rangle \langle 0|_Q \otimes \rho_{TLS}^{th}$ , followed by a  $\sqrt{X}$  gate on the qubit. Applying the operator  $U(\tau)$ , tracing over the TLS degrees of freedom, and applying the final gate  $\sqrt{X}^{\dagger}$ , we obtain a Bloch vector z component of  $v(\tau) = p_0 \cos((\beta + \xi)\tau) + p_1 \cos((\beta - \xi)\tau)$ , which shows the clear multifrequency dependence. In this work, we assume that the TLS is at infinite temperature, i.e.,  $T_{TLS} \to \infty$ , and thus  $p_0 = p_1 = 1/2$ , from where we can see that the Bloch vector simplifies to  $v(\tau) = \cos(\beta\tau)\cos(\xi\tau)$ . This is the expression used in Eq. (15).

Lastly, since the evolution is mostly free except state preparation and measurement operations, the exponential decay rate is given by  $\alpha$  as in the  $T_2$  experiment. This is confirmed numerically, as well as via solving the LME analytically. As before, all other errors, including

gate errors, will contribute factors of order  $\delta t$ , and are consequently omitted.

## e. (Q) FTTPS

FTTPS are a set of probe sequences used in QNS to access frequency dependent decay rates of a singlequbit system [57]. Following the protocol described in Appendix B 2, they can be used to learn the spectral properties of correlated dephasing noise. However, to obtain accurate characterization of correlated noise, it is essential to have a thorough understanding of the effects Markovian noise processes have on these experiments.

The k = 0 sequence is a Ramsey experiment, and it thus follows the discussion in the previous section. For k > 0, it is easy to first show the results of each type of noise independently. Each Markovian dissipative error contributes an exponential decay of the form  $e^{-\delta_k \tau}$  to the Bloch vector. The decays obtained from each source of dissipative noise acting individually are listed below:

- (1) Amplitude damping:  $\delta_k^{AD} = (\gamma/2)(1 + k/2K)$ , (2) PD:  $\delta_k^{PD} = \lambda (1 k/2K)$ , (3) Control noise:  $\delta_k^X = \nu(k/K)$ .

Note that  $\delta_k$  is independent of q in the AD case.

Additionally, it is straightforward to see that the effect of an under/over-rotation angle contributes a cosine to the Bloch vector. The Hamiltonian of a single gate is  $H_C =$  $(\pi/2\delta t)(1+\epsilon)\sigma_x$ , and the associated control propagator is found to be

$$U_C = \exp(-iH_C\delta t) = Xe^{-i\frac{\pi}{2}\epsilon\sigma_x}.$$
 (A19)

Since the kth FTTPS has 2k number of X gates, and we assume that no other noise is acting, the total propagator can be computed as  $U_k = (U_c)^{2k} = X^{2k}e^{-i\pi k\epsilon\sigma_x} =$  $e^{-i\pi k\epsilon \sigma_x}$ . Thus, the survival probability of the  $|0\rangle$  state is  $p_k(\tau) = |\langle 0|U_k|0\rangle|^2 = (1 + \cos(2\pi\epsilon k))/2$ . Combining these results, we can see that the analytical prediction of the Bloch vector becomes

$$v_k^{\mathcal{Q}}(\tau) = e^{-\tau \delta_k} \begin{cases} \cos(2\beta \tau), & \text{if } k = 0\\ \cos(2\pi k \epsilon), & \text{if } k > 0 \end{cases}, \tag{A20}$$

where FTTPS decay rate is  $\delta_k = \gamma/2 + \lambda + (\gamma/2 - \lambda + \gamma/2)$  $2\nu)k/2K$ . However, the simultaneous action of all noise processes may not combine trivially. To test the validity of Eq. (A20), we compare it to numerical simulation. In Fig. 10, we present the results of performing LME simulations with various combinations of Markovian noise parameters  $(\beta, \epsilon, \lambda, \gamma, q = 1, \nu)$ . The specific values of the noise parameters are shown in Table III. In these simulations, all noise parameters except one were set by default to the "weak" values shown on the left column of Table III. Then, for each curve of Fig. 10, one parameter at a time

<span id="page-25-1"></span>![](_page_25_Figure_15.jpeg)

FIG. 10. Comparison between fixed total-time sequences simulations (dots) and analytical prediction (solid lines) obtained from Eq. (A20). Each curve corresponds to a different set of noise parameters. The Markovian noise parameters q = 1 and  $\beta, \epsilon, \lambda, \gamma, \nu$  were obtained from Table III by selecting one process to be strong while maintaining the others as weak. The fixed total-time pulse sequences were chosen with K = 64. In all cases, we find excellent agreement between theory and simulation. Dashed lines represent the ideal probabilities, obtained in the noiseless scenario.

was set to the values corresponding to "strong" noise, shown on the right column of Table III. In all cases, we find excellent agreement between Eq. (A20) and the numerical results. This provides strong support for the use of Eq. (A20) to compute predictions when Markovian noise is dominant.

## f. (P) FPW

<span id="page-25-3"></span>Here, we examine the lowest order noise contribution to the FPW experiments under the square pulse approximation. The ideal FPW experiment is built with d repetitions of the unitary building block G = XZXZ, i.e., the circuit unitary is  $U_{FPW}(\tau = 2d\delta t) = G^d$ . The x control Hamiltonian and propagator follow from Eq. (A19), while the noise Hamiltonian  $H_N = (\beta/2)\sigma_z$  accounts for detuning. The effect of the noise on the ideal X operator can be understood intuitively in the Hamiltonian formulation. We transform  $H_N$  to the interaction picture with respect to  $H_C$ :

<span id="page-25-0"></span>
$$\tilde{H}_N(t) = U_C^{\dagger}(t)H_N U_C(t) 
= \frac{\beta}{2} \left( \sigma_z \cos\left(\theta \frac{t}{\delta t}\right) + \sigma_y \sin\left(\theta \frac{t}{\delta t}\right) \right).$$
(A21)

<span id="page-25-2"></span>TABLE III. Noise parameters used in FTTPS and RB simulation.

| Parameter     | Weak | Strong |  |
|---------------|------|--------|--|
| $\beta$ (MHz) | 0.06 | 0.6    |  |
| € (%)         | 0.1  | 2      |  |
| γ (MHz)       | 0.03 | 0.3    |  |
| λ (MHz)       | 0.03 | 0.6    |  |
| ν (MHz)       | 0.03 | 0.15   |  |

As a result, the rotated frame noise propagator is

$$\tilde{U}(\tau) = \mathcal{T}_{+} e^{-i \int_{0}^{\tau} dt \tilde{H}_{N}(t)} \\
\stackrel{(1)}{\approx} e^{-i \frac{\beta}{2} \int_{0}^{\tau} dt (\sigma_{z} \cos(\theta \frac{t}{\delta t}) + \sigma_{y} \sin(\theta \frac{t}{\delta t}))}, \tag{A22}$$

where  $T_+$  is the time ordering operator and in (1) we have approximated the time-ordered dynamics by the first-order Magnus expansion. More specifically, for a single X gate, where  $\tau = \delta t$ , we obtain

$$\tilde{U}(\delta t) \approx e^{-i\frac{\beta \delta t}{2\theta} \left(\sigma_z \sin \theta + \sigma_y (1 - \cos \theta)\right)}$$

$$\approx e^{-i\frac{\beta \delta t}{\pi} \sigma_y}, \tag{A23}$$

where we used the weak noise conditions  $\epsilon \ll 1$  and  $\beta \delta t \ll 1$  in approximating  $\sin \theta \approx -\pi \epsilon$ ,  $1 - \cos \theta \approx 2 - (\pi \epsilon)^2/2$ , and  $\beta/\theta \approx \beta/\pi$  to first order.

In the lab frame, the noisy X gate can be written in terms of the control and toggling frame propagators as

$$X' = U_C(\delta t)\tilde{U}(\delta t)$$

$$\approx Xe^{-i\frac{\pi\epsilon}{2}\sigma_x}e^{-i\frac{\beta\delta t}{\pi}\sigma_y}.$$
(A24)

Consequently, the noisy implementation of the building block *G* becomes

$$G' = X'ZX'Z$$

$$\approx Xe^{-i\frac{\pi\epsilon}{2}\sigma_{x}}e^{-i\frac{\beta\delta t}{\pi}\sigma_{y}}ZXe^{-i\frac{\pi\epsilon}{2}\sigma_{x}}e^{-i\frac{\beta\delta t}{\pi}\sigma_{y}}Z$$

$$= e^{-i\frac{\pi\epsilon}{2}\sigma_{x}}Xe^{-i\frac{\beta\delta t}{\pi}\sigma_{y}}XZe^{-i\frac{\pi\epsilon}{2}\sigma_{x}}ZZe^{-i\frac{\beta\delta t}{\pi}\sigma_{y}}Z$$

$$= e^{-i\frac{\pi\epsilon}{2}\sigma_{x}}e^{i\frac{\beta\delta t}{\pi}\sigma_{y}}e^{i\frac{\pi\epsilon}{2}\sigma_{x}}e^{i\frac{\beta\delta t}{\pi}\sigma_{y}}$$

$$\approx e^{i\frac{\beta\delta t}{\pi}\sigma_{y}}e^{i\frac{\beta\delta t}{\pi}\sigma_{y}}$$

$$\approx e^{2i\frac{\beta\delta t}{\pi}\sigma_{y}}.$$
(A25)

where we used that X and Z anticommute, as well as  $e^{-i\frac{\pi\epsilon}{2}\sigma_X}$  and  $e^{-i\frac{\beta\delta t}{\pi}\sigma_y}$  commute to first order; operator equalities hold up to a global phase. Additionally, we used  $\sigma_j e^{-i\phi\sigma_k}\sigma_j = e^{-i\phi\sigma_j\sigma_k\sigma_j} = e^{i\phi\sigma_k}$  for  $k\neq j$ . This result indicates that the interleaved Z gates cancel the X overrotation errors given by  $\epsilon$ , but maintain the first-order detuning errors, thus causing FPW errors.

Finally, the full intended operation consists of d repetitions of the G' operator, yielding

$$(G')^d \approx e^{i2d\frac{\beta\delta t}{\pi}\sigma_y}.$$
 (A26)

The survival probability for  $\tau = 2d\delta t$  can then be computed as

$$p(\tau) = \left| \langle 0 | (G')^d | 0 \rangle \right|^2$$

$$\approx \cos \left( \frac{2\beta}{\pi} \tau \right)^2, \tag{A27}$$

from where the functional form of Eq. (17) becomes clear. However, the numerical factor of the oscillation frequency of  $2\beta/\pi$  depends on the specific shape of the pulse. Interestingly, the difference between the square pulse and the Gaussian pulse is a factor of 2/3, as discussed in Sec. III B. Lastly, the decay rate can be found by successive implementation of Eq. (A10), and is given by  $(\mu + \eta)/2 = 3/4\gamma + \lambda/2 + \nu$ .

### g. (XT) crosstalk

The (XT) circuits can be computed similarly to the Ramsey experiments earlier in this section. In fact, the calculation is analogous, by renaming qubit Q to A and promoting the TLS-to-qubit B. The latter involves considering a detuning  $\beta_B$  for qubit B, as well as dissipative error contributions. Thus, the crosstalk Hamiltonian becomes,

$$H_{\rm XT} = \frac{\beta_A}{2} \sigma_z^A + \frac{\beta_B}{2} \sigma_z^B + \frac{J}{2} \sigma_z^A \sigma_z^B. \tag{A28}$$

Like in the TLS case,  $H_{\rm XT}$  is diagonal, and so is the time propagator it induces. More specifically,  $U_{\rm XT}(t)=e^{-iH_{\rm XT}t}$ , where the diagonal entries correspond to  $e^{-i\frac{t}{2}(\beta_A+\beta_B+J)}$ ,  $e^{-i\frac{t}{2}(\beta_A-\beta_B-J)}$ ,  $e^{-i\frac{t}{2}(-\beta_A+\beta_B-J)}$ ,  $e^{-i\frac{t}{2}(-\beta_A-\beta_B+J)}$ . Both qubits are initialized with  $\sqrt{X}$  gates, allowed to evolve freely for a time  $\tau/2$  after which an X gate is applied to both qubits. Then, the qubits evolve freely once again, before two final  $\sqrt{X}$  gates are applied prior to measurement in the computational basis. The resulting z component of the Bloch sphere after tracing out qubit B is given by

$$v^{XT}(\tau) = e^{-\left(\frac{\gamma_A + \gamma_B}{2} + \lambda_A\right)\tau} \left(\cos(J\tau) + \frac{\gamma_B}{2J}\sin(J\tau)\right)$$
(A29)

to lowest order in the dissipative noise parameters.

# <span id="page-26-1"></span>APPENDIX B: QNS

Time-correlated noise is commonly observed in superconducting qubits [32,68,79,86,148,149]. Its presence is commonly detected via superexponential decay in  $T_2$  experiments and more precisely characterized via QNS [89,98]. In the case of the IBMQP devices, we find a substantial number of devices where qubits exhibit time-correlated dephasing and control noise. Below, we discuss the FFF, a mathematical framework used to investigate the effect of correlated noise, and QNS based on FTTPS. We briefly summarize FTTPS-based QNS in the presence of dephasing and multiplicative control noise.

#### <span id="page-26-0"></span>1. Filter function formalism

The FFF takes a frequency domain perspective on the effect of spatiocorrelated noise on a quantum system. Here, we provide an overview for the FFF focusing on a single qubit governed by the noise Hamiltonian  $H_{N,1}(t)$ 

[Eq. (10)] and control Hamiltonian  $H_C(t)$  given by Eq. (3), where  $\Theta(t) = \int_0^t \Omega(s) ds$ . In the toggling frame, the density matrix is transformed by  $\tilde{\rho}(t) = U_C(t)\rho(t)U_C^{\dagger}(t)$ , and the noise Hamiltonian becomes

$$\begin{split} \tilde{H}_N(t) &= U_C(t)H_N(t)U_C^{\dagger}(t) \\ &= \left[\cos\Theta(t)\sigma_z + \sin\Theta(t)\sigma_y\right]\beta(t) + \Omega(t)\epsilon(t)\frac{\sigma_x}{2}. \end{split}$$

The time propagator of the noise dynamics in the toggling frame is given by

$$\tilde{U}_{N}(t) = \mathcal{T}_{+} \exp\left(\int_{0}^{t} ds \tilde{H}_{N}(s)\right)$$

$$\approx \exp\left(-i\vec{a}(\tau) \cdot \vec{\sigma}\right), \tag{B1}$$

where the approximation is a result of employing the Magnus expansion, truncating the dynamics to first order, and introducing the so-called error vector  $\vec{a}(t) = \int_0^t ds \left[\frac{1}{2}\Omega(s)\epsilon(s), \sin\Theta(s)\beta(s), \cos\Theta(s)\beta(s)\right]$  [96, 150]. The full dynamics are generated by  $U(t) = U_C(t)\tilde{U}_N(t)$ .

In anticipation of the dynamics generated during an FTTPS circuit, we will focus on the noise-averaged survival probability  $p(\tau) = \langle \langle -y|U(\tau)|-y\rangle \rangle_{\epsilon,\beta}$ , where  $|-y\rangle = 1/\sqrt{2}(|0\rangle - i\,|1\rangle)$  and  $\tau$  is the total time of one sequence within the FTTPS protocol. Accounting for the fact that the sequences generate identity evolution, the probability can be simplified further as

$$p(\tau) = \langle \cos^2 a(\tau) + (a_y^2(\tau)/a(\tau)) \sin^2 a(\tau) \rangle_{\epsilon,\beta}$$

$$= \frac{1}{2} \left( 1 + \left\langle \frac{a_y^2(\tau) + \left[ a_x^2(\tau) + a_z^2(\tau) \right] \cos(2a^2(\tau))}{a^2(\tau)} \right\rangle_{\epsilon,\beta} \right)$$

$$\stackrel{(1)}{=} \frac{1}{2} \left( 1 + e^{-\chi(\tau)} \cos \zeta(\tau) \right), \tag{B2}$$

where  $a(\tau) = |\vec{a}(\tau)|$  and the  $\langle \cdot \rangle_{\epsilon,\beta}$  represents the average over noise realizations. The expression in (1) results from assuming the pulses are instantaneous and thus,  $a_y(\tau) = 0$ . The dynamics are characterized by a decay factor  $\chi(\tau) \equiv \langle a^2(\tau) \rangle_{\epsilon,\beta}$  and rotation angle  $\zeta(\tau) \equiv 2 \langle a(\tau) \rangle_{\epsilon,\beta}$ .

Commonly, these expressions are transformed to the frequency domain, as this can provide greater intuition that draws on classical signal processing concepts. Expressing the error vector components in the frequency domain, we obtain

$$\langle a_x^2(\tau) \rangle_{\epsilon,\beta} = \frac{1}{\pi} \int_0^\infty F_{\epsilon}(\omega, \tau) S_{\epsilon}(\omega) d\omega,$$

$$\langle a_z^2(\tau) \rangle_{\epsilon,\beta} = \frac{1}{\pi} \int_0^\infty F_{\beta}(\omega, \tau) S_{\beta}(\omega) d\omega,$$
(B3)

where the control and dephasing FFs are defined by

$$F_{\epsilon}(\omega, \tau) = \frac{1}{4} \left| \int_{0}^{\tau} \Omega(t) e^{i\omega t} \right|^{2},$$

$$F_{\beta}(\omega, \tau) = \left| \int_{0}^{\tau} \cos \Theta(t) e^{i\omega t} \right|^{2}.$$
(B4)

The PSDs are defined in Sec. II D.

## <span id="page-27-0"></span>2. Dephasing QNS with FTTPS

In order to extract information about a device's dephasing noise PSD, we leverage the FTTPS. The advantage of using FTTPS for QNS lies in the large spectral concentration of their FFs [57]. This feature results in a favorable condition number in the FF matrix and thus, reduces the chance of encountering an ill-posed inversion problem in the spectrum reconstruction procedure. Here, we will study FTTPS in the absence of control noise.

Starting from Eq. (B2) and eliminating the contribution from control noise,  $\zeta(\tau) = 2\bar{\beta}\tau$  while

<span id="page-27-3"></span>
$$\chi(\tau) = \frac{1}{\pi} \int_0^\infty S_{\beta}(\omega) F_{\beta}(\omega, \tau) d\omega.$$
 (B5)

In the large  $\tau$  limit, the FF of the kth FTTPS  $F_{\beta,k}(\omega,\tau)$  is well approximated by

$$F_{\beta,k}(\omega,\tau) \approx \tau^2 \delta(\omega - 2\pi k/\tau),$$
 (B6)

where  $\omega_k = 2\pi k/\tau$  [see Fig. 11(a)]. The total FTTPS circuit duration is  $\tau = 2K\delta t$ . Using Eq. (B5), it is straightforward to estimate the PSD by computing  $\chi(\tau) \approx \tau S(\omega_k)$ , where to approximate the integral we used explicitly the discretized frequency step  $\delta\omega = 2\pi/\tau$ . Note that estimates of  $\chi$  are obtained from experimentally determined  $p_{\nu,k}(\tau)$ .

<span id="page-27-2"></span><span id="page-27-1"></span>![](_page_27_Figure_22.jpeg)

FIG. 11. Fixed total-time pulse sequences filter functions: (a) dephasing and (b) control. (c) Robust-fixed total-time pulse sequences control filter functions.  $K = 64, \delta t = 0.035 \,\mu s$ . Note that the fixed total-time pulse sequences control filter functions have large support in low frequencies, whereas the robust-fixed total-time pulse sequences control filter functions do not.

## <span id="page-28-1"></span>3. FTTPS in the presence of stochastic control noise

Another type of correlated noise was observed via FTTPS: correlated control noise. Imperfect control can manifest via fluctuating fields in the control lines, and can be stochastic or coherent. In the case of stochastic noise, a common approach is to treat the noise fluctuations as white, uncorrelated noise. In the case of X control, white noise can be well represented by a bit-flip channel (see Appendix D). In the general case, stochastic fluctuations of the control fields can be correlated in time, requiring a more sophisticated modeling approach. In this appendix, we focus on evaluating the effect of stochastic control noise, specifically on the FTTPS.

Consider the survival probability in Eq. (B2) under the influence of strong control noise, such that the dephasing noise can be neglected. The probability oscillates with an angle  $\zeta(\tau) = \bar{\epsilon}\Theta(\tau)$ , while the decay is dictated by  $\chi(\tau) = \left\langle a_x^2(\tau) \right\rangle_{\epsilon,\beta}$ . Under the square pulse approximation and assuming the pulses are located at times  $t = \tau_n \approx (\tau/2k)(n-1/2)$ , the mean of the accumulated angular error is  $\zeta_k = \pi k \bar{\epsilon}$ . The control FFs (ctrl-FFs) are defined as

$$F_{\epsilon,k}(\omega) = \left| \frac{\pi}{2} \sum_{n=1}^{2k} e^{-i\omega\tau_k} \right|^2 \approx \left( \frac{\pi}{2} \frac{\sin(\omega\tau/2)}{\sin(\omega\tau k/4)} \right)^2, \quad (B7)$$

where the approximation comes from assuming the instantaneous pulse limit. Roughly approximating the ctrl-FFs by  $F_{\epsilon,k}(\omega)=4k^2\delta(\omega)$  [see Fig. 11(b)], we obtain an expression for the second moment  $\chi_{\epsilon,k}(\tau)\approx\sigma k^2$  (defined in Sec. IV C 3), with  $\sigma=\pi^2\delta\omega S_{\epsilon}(0)$ . Thus, for predominantly low-frequency noise,  $S_{\epsilon}(0)$  captures the relevant noise strength.

## a. R-FTTPS

To obtain further confirmation of the presence of correlated control noise, we define the Robust-FTTPS (R-FTTPS) sequences, by alternating the sign of every other X pulse in the standard FTTPS, i.e.,  $X \to -X$ . In practice, this is implemented by appending virtual Z gates on each side of even pulses. In the absence of control errors, this sign change is undetectable. However, in their presence, the sign change implies  $e^{-\frac{i}{2}\Theta(t)\sigma_X} \to e^{+\frac{i}{2}\Theta(t)\sigma_X}$ . Alternating signs will suppress the coherent and low-frequency contributions of the noise, as can be seen by computing the R-FTTPS accumulated phase:  $\zeta_k^R = \pi \bar{\epsilon} \sum_{n=1}^{2k} (-1)^n = 0$ . The second moment is now characterized by the R-FTTPS ctrl-FFs

$$F_{\epsilon,k}^{R}(\omega) = \left| \frac{\pi}{2} \sum_{n=1}^{2k} (-1)^n e^{-i\omega\tau_n} \right|^2 \approx \left( \frac{\pi}{2} \frac{\sin(\omega\tau/2)}{\cos(\omega\tau k/4)} \right)^2$$
(B8)

[see Fig. 11(c)].

# <span id="page-28-0"></span>APPENDIX C: GAUSSIAN VS SQUARE PULSES IN FPW EXPERIMENTS

Remarkably, we find in practice that most experimental phenomena observed can be well described within the constant pulse approximation. This model robustness to pulse-shape greatly simplifies the task of simulating driven dynamics. The LME solution can be used whenever  $X, \sqrt{X}$  appear in a circuit of interest without the need of any Trotterization. One notable exception to this convenient simplification can be found in the FPW experiments. Since FPW experiments aim to amplify gate errors, it is perhaps not surprising that the results are largely influenced by pulse-shaping effects. In this appendix, we analyze the differences between Gaussian and constant pulses in FPW experiments.

The result of FPW experiments under Markovian noise can be parametrized with a decay rate a and oscillation frequency b as  $f(t;a,b) = e^{-at}\cos(bt)$ . In the constant pulse case, it can be shown analytically that  $a_{\rm const} = \frac{3}{4}\gamma + (\lambda + \nu)/2$ ,  $b_{\rm const} = (2/\pi)\beta$ . On the other hand, when the qubit is driven with a Gaussian pulse, it is challenging to find fully analytical expressions for the survival probability of the FPW experiments in the presence of noise.

A Gaussian pulse is characterized by  $\Omega(t) = Ae^{-(t-\delta t/2)^2/2\sigma^2} + B$  for  $t \in [0, \delta t)$ , where the *B* parameter is chosen such that the pulse starts and ends at zero, i.e.,  $\Omega(0) = \Omega(\delta t) = 0$ . A ubiquitous choice for the width of the Gaussian is  $\sigma = \delta t/4$  [114,151], while *A* is chosen to produce the desired rotation angle  $\int_0^{\delta t} \Omega(t) dt = \theta$ . Under these conditions, we simulate the dynamics using a discretization of N = 160 steps, consistent with IBM pulse characteristics. The simulation is performed by numerically solving the LME [Eq. (11)], with *X* rotation

<span id="page-28-2"></span>![](_page_28_Figure_15.jpeg)

FIG. 12. Noisy simulation of finite pulse-width circuits for constant (blue) and Gaussian pulses (orange). (a) Simulation for  $\beta = 0.5$  MHz (crosses) and fit (solid lines) using  $f(t; a = a_{\text{const}}, b) = e^{-at} \cos(bt)$ . The decay rates are set to  $\gamma = 0.05$  MHz,  $\lambda = \nu = 0.01$  MHz. (b) Oscillation frequency parameter b as a function of detuning  $\beta$ , obtained from fitting  $f(t; a = a_{\text{const}}, b)$  to simulations. This shows that for a constant pulse,  $v^P(t)$  oscillates with a frequency  $2\beta/\pi$ , whereas for a Gaussian pulse it oscillates with  $4\beta/3\pi$ .

angles given by  $\theta_n = \Omega(n\delta t)\delta t/N$ , for  $n=0,\ldots,N-1$ . In Fig. 12, we show numerically that fitting f(t;a,b) to the simulation results of FPW experiments under Gaussian pulses yields the same decay rate as in the constant pulse case, i.e.,  $a_{\rm Gauss} = a_{\rm const}$ , and an oscillation frequency  $b_{\rm Gauss} = (4/3\pi)\beta = \frac{2}{3}b_{\rm const}$ . This can be interpreted as Gaussian pulses providing suppression with a factor of 2/3 against detuning processes. Since the experiments are implemented with Gaussian pulses, in order to account for this suppression, we modify the analytical fit expression with a factor of 2/3, i.e.,  $v(t) = e^{-\tau\left(\frac{3}{4}\gamma + \frac{\lambda + \nu}{2}\right)}\cos((4/3\pi)\beta\tau)$ , as presented in Eq. (17).

# <span id="page-29-0"></span>APPENDIX D: RELATING STOCHASTIC NOISE WITH ERROR CHANNELS

In this appendix, we show how some common error channels, namely PD and depolarization, can be related to stochastic noise processes with simple statistical properties.

# 1. Dephasing noise and PD

Here, we establish a Hamiltonian description of the PD quantum channel. We start with the time-dependent dephasing Hamiltonian given in Eq. (10) with  $\epsilon(t) \equiv 0$ . The noise-averaged state of the system after time  $\tau$  is

$$\mathcal{E}(\rho) = \langle U(\tau)\rho U^{\dagger}(T)\rangle_{\beta}$$

$$= \left\langle \begin{pmatrix} 1 & 0 \\ 0 & e^{-i\int_{0}^{\tau}\beta(t)dt} \end{pmatrix} \begin{pmatrix} \rho_{00} & \rho_{01} \\ \rho_{10} & \rho_{11} \end{pmatrix} \begin{pmatrix} 1 & 0 \\ 0 & e^{i\int_{0}^{\tau}\beta(t)dt} \end{pmatrix} \right\rangle_{\beta}$$

$$= \left\langle \begin{pmatrix} \rho_{00} & \rho_{01}e^{i\int_{0}^{\tau}\beta(t)dt} \\ \rho_{10}e^{-i\int_{0}^{\tau}\beta(t)dt} & \rho_{11} \end{pmatrix} \right\rangle_{\beta}$$

$$\approx \begin{pmatrix} \rho_{00} & \rho_{01}e^{i\bar{\beta}\tau - \chi(\tau)} \\ \rho_{01}e^{-i\bar{\beta}\tau - \chi(\tau)} & \rho_{11} \end{pmatrix}, \quad (D1)$$

where  $\chi$  is given by Eq. (B5). The decaying component of the off-diagonal elements become dependent on the control in general. However, if the noise is white, i.e.,  $S(\omega) = S_0$ , it is straightforward to show (by following the steps in Appendix B1) that  $\chi(\tau) = S_0 \tau$ . This indicates that the superoperator formalism is equivalent to the time-dependent Hamiltonian description when the noise is white.

More concretely, the PD superoperator  $\mathcal{E}_{PD}(\rho)$  can be written in terms of the Krauss operators  $E_0 = \sqrt{1-p}I$ ,  $E_1 = \sqrt{p}Z$  with damping rate p. The effect on a general state  $\rho$  is

$$\mathcal{E}_{PD}(\rho) = E_0 \rho E_0 + E_1 \rho E_1$$
$$= \left(1 - \frac{p}{2}\right) \rho + \frac{p}{2} Z \rho Z$$

$$= \left(1 - \frac{p}{2}\right) \begin{pmatrix} \rho_{00} & \rho_{01} \\ \rho_{10} & \rho_{11} \end{pmatrix} + \frac{p}{2} \begin{pmatrix} \rho_{00} & -\rho_{01} \\ -\rho_{10} & \rho_{11} \end{pmatrix}$$

$$= \begin{pmatrix} \rho_{00} & \rho_{01}(1-p) \\ \rho_{10}(1-p) & \rho_{11} \end{pmatrix} \tag{D2}$$

and can be interpreted as acting on the state  $\rho$  with a Z operator with a given probability p. Adding a detuning noise  $\bar{\beta}\sigma_z$  with propagator  $U_{\beta}(t)=e^{-i\bar{\beta}t\sigma_z/2}$  leads to a density matrix

$$U_{\beta}(t)\mathcal{E}_{PD}(\rho)U_{\beta}^{\dagger}(t) = \begin{pmatrix} \rho_{00} & \rho_{01}e^{-i\bar{\beta}t}(1-p) \\ \rho_{10}e^{i\bar{\beta}t}(1-p) & \rho_{11} \end{pmatrix}, \quad (D3)$$

from where the identification of the detuning parameter with the mean of  $\beta(t)$  becomes evident. Lastly, by identifying  $p = 1 - e^{-S_0\tau}$  it becomes clear that the PD channel can be interpreted as the white noise limit of a time-dependent dephasing Hamiltonian, where the dephasing time can be defined as  $T_2 = 1/S_0$ .

### 2. Isotropic uncorrelated noise and depolarization

The control noise case discussed in Sec. IV C 3 is entirely analogous to the dephasing case. Rather, to showcase the versatility of the stochastic Hamiltonian description, we turn to depolarizing noise. In the superoperator formalism, the Kraus operators for depolarizing noise are  $E = \{\sqrt{1-3p/4}I, \sqrt{p}X/2, \sqrt{p}Y/2, \sqrt{p}Z/2\}$ , which can be interpreted as  $\rho$  is left alone with probability of 1-p, and the operators X, Y, Z being applied with probability p/3. The effect of depolarization on a general state can be written as

$$\mathcal{E}_{D}(\rho) = p \frac{I}{2} + (1 - p)\rho$$

$$= \begin{pmatrix} \rho_{00}(1 - p) + p/2 & \rho_{01}(1 - p) \\ \rho_{10}(1 - p) & \rho_{11}(1 - p) + p/2 \end{pmatrix}.$$
(D4)

Next, we propose a general time-dependent Hamiltonian, and find the conditions that the parameters need to satisfy in order for the stochastic Hamiltonian to reproduce the effects of depolarizing noise. We write a Hamiltonian  $H_N(t) = \vec{\eta}(t) \cdot \vec{\sigma}$ , where we consider  $\vec{\eta}(t)$  a Gaussian and stationary random variable with zero mean. The time evolution propagator is

$$U(\tau) = e^{-i\int_0^{\tau} \vec{\eta}(t)dt \cdot \vec{\sigma}} = e^{-i\vec{\theta}_{\eta} \cdot \vec{\sigma}}$$
  
=  $I\cos\theta_{\eta} - i(\hat{n}_{\eta} \cdot \vec{\sigma})\sin\theta_{\eta}$ , (D5)

where we defined  $\vec{\theta}_{\eta} = \int_0^{\tau} \vec{\eta}(t) dt = \theta_{\eta} \hat{n}_{\eta}$ , with  $\hat{n}_{\eta}^i = \vec{\theta}_{\eta}^i / \theta_{\eta}$  a unit vector. The state becomes

$$\mathcal{E}(\rho) = \langle U(\tau)\rho U^{\dagger}(\tau)\rangle_{\eta}$$

$$= \rho \left\langle \cos^{2}\theta_{\eta}\right\rangle_{\eta} - i[\left\langle \cos\theta_{\eta}\sin\theta_{\eta}\hat{n}_{\eta}\right\rangle_{\eta} \cdot \vec{\sigma}, \rho]$$

$$+ \left\langle (\hat{n}_{\eta} \cdot \vec{\sigma})\rho(\hat{n}_{\eta} \cdot \vec{\sigma})\sin^{2}\theta_{\eta}\right\rangle_{\eta}. \tag{D6}$$

In the weak noise approximation, the first two terms simplify greatly. Dropping the subscript  $\eta$  from the noise averaging, these terms can be expressed as

$$\langle \cos^2 \theta_{\eta} \rangle \approx \left\langle \left( 1 - \frac{1}{2} \theta_{\eta}^2 \right)^2 \right\rangle = 1 - \langle \theta_{\eta}^2 \rangle, \quad (D7)$$

$$\langle \cos \theta_{\eta} \sin \theta_{\eta} \hat{n}_{\eta} \rangle \approx \left\langle \left( 1 - \frac{1}{2} \theta_{\eta}^2 \right) \theta_{\eta} \frac{\vec{\theta}_{\eta}}{\theta_{\eta}} \right\rangle = \left\langle \vec{\theta}_{\eta} \right\rangle = 0. \quad (D8)$$

Next, we make two additional assumptions regarding the statistical properties of the noise parameters: (1) we assume that the noise is uncorrelated along different axes and (2) the noise is isotropic, i.e.,

$$\left\langle \vec{\theta}_{\eta}^{i} \vec{\theta}_{\eta}^{j} \right\rangle = \left\langle \vec{\theta}_{\eta}^{i} \vec{\theta}_{\eta}^{i} \right\rangle \delta_{ij}, \tag{D9}$$

$$\left\langle \vec{\theta}_{\eta}^{i} \vec{\theta}_{\eta}^{i} \right\rangle = \frac{\left\langle \theta_{\eta}^{2} \right\rangle}{3},$$
 (D10)

respectively. With these simplifying assumptions, the last term in Eq. (D6) becomes

$$\langle (\hat{n}_{\eta} \cdot \vec{\sigma}) \rho (\hat{n}_{\eta} \cdot \vec{\sigma}) \sin^2 \theta_{\eta} \rangle \approx \sum_{i,j} \langle \hat{n}_{\eta}^i \hat{n}_{\eta}^j \theta_{\eta}^2 \rangle \sigma_i \rho \sigma_j.$$

This can be further simplified as

$$\sum_{i,j} \langle \hat{n}_{\eta}^{i} \hat{n}_{\eta}^{j} \theta_{\eta}^{2} \rangle \sigma_{i} \rho \sigma_{j} = \sum_{i,j} \left\langle \frac{\vec{\theta}_{\eta}^{i} \vec{\theta}_{\eta}^{j}}{\theta_{\eta}^{2}} \theta_{\eta}^{2} \right\rangle \sigma_{i} \rho \sigma_{j}$$

$$= \sum_{i,j} \left\langle \vec{\theta}_{\eta}^{i} \vec{\theta}_{\eta}^{i} \right\rangle \sigma_{i} \rho \sigma_{j}$$

$$= \sum_{i} \left\langle \vec{\theta}_{\eta}^{i} \vec{\theta}_{\eta}^{i} \right\rangle \sigma_{i} \rho \sigma_{i} = \frac{\left\langle \theta_{\eta}^{2} \right\rangle}{3} \sum_{i} \sigma_{i} \rho \sigma_{i}$$

$$= \frac{\left\langle \theta_{\eta}^{2} \right\rangle}{3} (2I - \rho) . \tag{D11}$$

Thus.

$$\mathcal{E}(\rho) = \rho \left( 1 - \langle \theta_{\eta}^2 \rangle \right) + \frac{\langle \theta_{\eta}^2 \rangle}{3} (2I - \rho)$$
$$= \frac{2}{3} \langle \theta_{\eta}^2 \rangle I + \left( 1 - \frac{4}{3} \langle \theta_{\eta}^2 \rangle \right) \rho. \tag{D12}$$

<span id="page-30-1"></span>![](_page_30_Figure_15.jpeg)

<span id="page-30-0"></span>FIG. 13. Experimental results (circles) obtained from running an increasing number of dynamical decoupling pulses on qubit 6 of  $ibmq\_guadalupe$ . Improved performance with the number of dynamical decoupling pulses is observed. The experiment results are fit to a function  $\chi_d(\tau) = A/d + B$ , where the parameters A, B are common to all dynamical decoupling experiments. The results of these fits are presented as solid lines, where we obtain A = 0.0063(2) and  $B \approx 0$  (within error bars).

From here, the depolarizing error can be recovered by setting

$$p = \frac{4}{3} \langle \theta_{\eta}^2 \rangle = \frac{4}{3} \sum_{i} \int_0^{\tau} \int_0^{\tau} dt dt' \langle \eta_i(t) \eta_i(t') \rangle. \quad (D13)$$

Analogously to the dephasing case, a constant p implies that noise must be uncorrelated and isotropic in the Hamiltonian description. In this case, if  $\langle \gamma_i(t)\gamma_i(t')\rangle = C_\eta \delta(t-t')$ , we get  $p = 4C_\eta \tau/3$ .

# APPENDIX E: EVIDENCE OF CORRELATED DEPHASING THROUGH DD

In Sec. IV, we explore the detection and modeling of correlated dephasing noise. By adding a number of DD pulses on T2 experiments, dephasing can be detected by comparing the relative performance. Figure 13 shows experimental results obtained from running an increasing number of DD pulses on qubit 6 of  $ibmq\_guadalupe$ , as function of total evolution time  $\tau$ .

It is clear that the performance improves with the number of DD pulses. Based on the theory of DD, if this improvement is due to increased filtering of dephasing noise, the decay rate should decrease as 1/d, where d is the number of DD pulses. We fit the function  $p_D(\tau) = (1 + e^{-\chi_d(\tau)})/2$ , where  $\chi_d(\tau) \approx \int S(\omega) \operatorname{sinc}((\omega - \omega_d)\tau)^2 d\omega$  is the overlap function. Note that the number of DD pulses shifts the center of the frequency response, given by  $\omega_d = d \, 2\pi/\tau$ . Therefore, we can fit the experimental results to a function  $\chi_d(\tau) = A/d + B$ , where the parameters A, B are common to all DD experiments. The results of these fits are presented as solid lines with excellent agreement, obtaining further confirmation of the presence of correlated dephasing noise.

# <span id="page-31-0"></span>**APPENDIX F: PARAMETRIZING THE MARKOVIAN RB DECAY RATE**

We perform numerical studies to examine the impact of Markovian errors on the RB decay rate *r*RB. In the absence of SPAM errors, the RB experimental result can be modeled as *p*RB(*L*) = (1 + *e*<sup>−</sup>*r*RB*L*)/2, where *L* is the number of Cliffords in a given RB sequences. We perform simulation of multiple combinations of the Markovian parameters and find that, to first order, the decay rate can be approximated as

$$r_{\rm RB} \approx \delta t(\gamma + \lambda + \nu) + \left(\frac{\pi \epsilon}{2}\right)^2$$
. (F1)

Thus, the impact of dissipative Markovian errors on the decay rate increases linear as a function of the time elapsed in the sequence. Coherent errors, on the other hand, enter quadratically. Note that these results are consistent with the literature; see, for example, Ref. [\[152\]](#page-37-30). Figure [14](#page-31-3) presents examples of simulations performed with Markovian parameters near values obtained from real devices. The noise parameters were chosen to be "weak" by default, while varying one parameter set as "strong" (see left and right columns of Table [III,](#page-25-2) respectively). The exponential decays (solid lines) are analytically computed by combining Eq. [\(F1\)](#page-31-4) and *p*RB(*L*).

# <span id="page-31-1"></span>**APPENDIX G: RB STANDARD DEVIATIONS**

To complement the analysis in Sec. [IV A,](#page-9-2) we compare the variances obtained from the RB experiments on 13 different qubits of *ibm\_algiers* (qubits 0, 2, 3, 4, 5, 6, 8, 9, 10, 14, 17, 22 and 24), where the Markovian model with low-frequency dephasing noise was found to provide a good description of the qubit's dynamics. For each of these qubits, we follow the steps outlined in Sec. [III A](#page-5-6) to fit the noise parameters and simulate the RB experiments. Then, for each RB Clifford length *L* = 2*<sup>i</sup>* for *i* ∈ [3, 10], we compute the standard deviations σexp, σsim for the experiment and simulations, respectively. The results are shown

<span id="page-31-3"></span>![](_page_31_Figure_8.jpeg)

FIG. 14. Randomized benchmarking simulations (circles) with Markovian parameters chosen as shown in Table [III.](#page-25-2) Good agreement is found with the analytical predictions (solid lines) obtained from Eq. [\(F1\).](#page-31-4)

<span id="page-31-5"></span>![](_page_31_Figure_10.jpeg)

<span id="page-31-4"></span>FIG. 15. Comparison between experimental and simulated randomized benchmarking standard deviations (blue circles). The line of perfect correlation σexp = σsim is shown in green for comparison.

collectively in Fig. [15](#page-31-5) in a scatter plot to visualize the degree of correlation. The Pearson correlation coefficient was computed between the two datasets and was found to be 0.70. This strong correlation provides evidence that the model is able to capture the RB statistics to a larger extent than just the mean alone. Deviations from the perfect correlation (shown as the solid line in Fig. [15\)](#page-31-5) may be due to low statistics, as only 10 RB sequences per length were run, and model deviations. Although promising, this showcases that a more thorough analysis could shed additional light into the origin of these discrepancies. Due to the complexity of running additional experiments on the IBMQP, this is left for future work.

# <span id="page-31-2"></span>**APPENDIX H: RESONANCES IN FTTPS**

As discussed in Sec. [IV C 2,](#page-12-0) low-frequency dephasing noise is prominent in the superconducting qubit devices examined in this study. Despite the common spectral features of low-frequency noise accompanied by a white noise floor, exceptions do exist. In particular, we find a subset of qubits that exhibit resonance peaks at high frequency. An example of this phenomenon can be seen in Fig. [16,](#page-32-1) detected in an FTTPS experiment.

The large resonance at *k* = 30 can be mapped to a frequency value by drawing upon the FFF (see Appendix [B 1\)](#page-26-0). The *k*th FF *Fk*(ω) has a narrow frequency sensitivity peak centered at ω = 2π*k*/τ [see Fig. [11\(a\)\]](#page-27-2), where τ = 2*K*δ*t* is the FTTPS duration. Consequently, the resonance observed in Fig. [16](#page-32-1) corresponds to a frequency of ≈41 ± 1 MHz. This frequency value is consistent with that observed in other qubits, typically in the range of 25–70 MHz. A possible origin of this phenomenon is frequency collisions with neighboring qubits, since IBMQP Eagle generation devices have typical resonance frequency differences between nearest-neighbor qubits in the order of

<span id="page-32-1"></span>![](_page_32_Figure_2.jpeg)

FIG. 16. Fixed total-time pulse sequences experiment results (circles) and simulation (solid lines) on qubit 13 of *ibm\_algiers*. A resonance peak is observed at *k* = 30, consistent with a frequency of approximately 41 ± 1 MHz. Inset: Power spectral density obtained from the fixed total-time pulse sequences experiment, using the quantum noise spectroscopy protocol outlined in Appendix [B 2.](#page-27-0) This power spectral density is then used to generate the noise trajectories required for simulation. Excellent agreement is found between experiment and simulation, as quantified by the mean squared error defined in Sec. [III A.](#page-5-6)

10–100 MHz. A thorough study of the physical origin of this resonant phenomenon is left for future work.

Note that, as is the case with low-frequency noise, the PSD of this noise can be fit following the same procedure outlined in Appendix [B 2.](#page-27-0) The resulting PSD is shown in the inset. The PSD can be used alongside a stochastic noise simulation, showing excellent agreement with experiment.

# <span id="page-32-0"></span>**APPENDIX I: TLS AND CROSSTALK**

An interesting phenomenon was identified within the TLS model in the presence of crosstalk and local detuning. As introduced in Sec. [IV B 1,](#page-10-1) many qubits exhibit the TLS behavior in the Ramsey experiments; this is exemplified in four different qubits in Fig. [3.](#page-11-0) The multi-qubit model introduced in this paper has three relevant frequencies associated with the Ramsey experiment: the TLS-to-qubit and qubit-qubit crosstalk coupling strengths ξ and *J* , and the local single-qubit detuning frequency β. When all of these parameters are taken into account, the LME model yields

$$v(\tau) = e^{-\alpha\tau} \cos[(\beta + J)\tau] \cos(\xi\tau), \quad (I1)$$

where α = γ /2 + λ. Note that this Bloch vector corresponds to the single-qubit Ramsey experiments, where the spectator qubit remains in the |0 state and evolves freely.

Examples of these Ramsey experiments can be seen for two different qubits in Fig. [17](#page-32-2) (dark-blue circles; denoted as FE). Both of these qubits were selected due to their seemingly close-to-uniform oscillations, where the oscillations can be well described by a single relevant frequency. Looking at Eq. [\(I1\),](#page-32-3) we notice that this poses two alternatives: either ξ ≈ 0, or β = −*J* . In order to resolve this

<span id="page-32-2"></span>![](_page_32_Figure_11.jpeg)

FIG. 17. Ramsey experiments on qubits 0 and 3 of *ibm\_cairo*, where spectator qubits are left to evolve freely (dark-blue circles; FE) and decoupled via XY4 (light-blue triangles; DD). Note that XY4 is applied exclusively on spectator qubits. Solid lines correspond to multi-qubit Lindblad master equation simulations including two-level system and crosstalk couplings, where excellent agreement with the experiments is found.

uncertainty, we performed another experiment. Immediately after the single-qubit Ramsey experiment is run, the experiment is repeated with the XY4 decoupling sequence applied to all spectator qubits in order to suppress quantum crosstalk between the primary qubit and its spectators. The results of this experiment are shown as light blue triangles in Fig. [17](#page-32-2) (denoted as DD). The remaining oscillation suggests that the TLS is present. As such, the relevant equation that describes these experiments is Eq. [\(15\).](#page-8-2) From both experiments, ξ and β can be fit. Here, we find that one of the values is consistent with the single frequency oscillation obtained in the original Ramsey experiments. Consequently, we can positively state that, within our model, β ≈ −*J* , and that the frequency observed in the pure Ramsey experiment corresponds to the TLS coupling ξ .

The interpretation of these results is that the qubits's driving frequencies are calibrated to precisely cancel the

<span id="page-32-4"></span>![](_page_32_Figure_15.jpeg)

<span id="page-32-3"></span>FIG. 18. Results (dots) obtained from characterization experiments on qubit 117 of *ibm\_osaka*, which fits well a Markovian model. The same batch of experiments was run 20 times in the span of 1 hr, on February 10, 2024. Time on the horizontal axis is measured from the first experiment run, at 22:23h. Solid lines are obtained from cubic spline interpolations. Shaded regions represent uncertainties obtained from the fit.

combined effect of neighboring crosstalk. Thus, this result adds another layer of complexity to the modeling of dephasing noise, since the TLS frequencies are seen to oscillate on a timescale much shorter than detuning frequencies. A detailed study of the consequences of the presence of TLSs on stochastic dephasing noise is left for future work. However, we note that, in principle, it is a reasonable assumption to consider all qubits to have nonzero β, *J* , ξ .

# **APPENDIX J: MODEL STABILITY**

We investigate the stability of the model parameters over time. Figure [18](#page-32-4) presents experimental data obtained from fitting the results of the characterization experiments over a window of one hour. As shown, most parameters have a good degree of stability within this window. A thorough statistical analysis of the stability over many qubits and longer time windows is required to more adequately determine if these trends continue or if significant drift occurs. These time sensitive experiments likely require dedicated access to hardware that differs from the standard IBMQP access. For that reason, we leave this analysis for future work, but provide preliminary insight here.

<span id="page-33-11"></span>![](_page_33_Figure_5.jpeg)

FIG. 19. Device connectivity and coherence times properties. We show cumulative distribution functions of (a) *T*<sup>1</sup> and (b) *T*<sup>2</sup> times, collected by system size in number of qubits: (5a) *ibmq\_lima*, *ibmq\_belem*, (5b) *ibmq\_manila*, (7) *ibmq\_lagos*, (16) *ibm\_guadalupe*, (27) *ibm\_auckland*, *ibm\_cairo*, *ibm\_hanoi*, *ibm\_algiers*. (c) Device layouts for each system size.

## <span id="page-33-10"></span>**APPENDIX K: DEVICE PROPERTIES**

In this appendix, we present device topologies and cumulative distribution functions (CDFs) for IBMQP devices used throughout this work. See Fig. [19](#page-33-11) for device layouts and information regarding *T*<sup>1</sup> and *T*<sup>2</sup> times obtained from IBM's calibration data.

- <span id="page-33-0"></span>[1] M. Kjaergaard, M. E. Schwartz, J. Braumüller, P. Krantz, J. I.-J. Wang, S. Gustavsson, and W. D. Oliver, Supercon[ducting qubits: Current state of play,](https://doi.org/10.1146/annurev-conmatphys-031119-050605) Annu. Rev. Condens. Matter Phys. **11**, 369 (2020).
- <span id="page-33-1"></span>[2] P. Krantz, M. Kjaergaard, F. Yan, T. P. Orlando, S. Gustavsson, and W. D. Oliver, A quantum engineer's guide [to superconducting qubits,](https://doi.org/10.1063/1.5089550) Appl. Phys. Rev. **6**, 021318 (2019).
- <span id="page-33-2"></span>[3] J. Koch, T. M. Yu, J. Gambetta, A. A. Houck, D. I. Schuster, J. Majer, A. Blais, M. H. Devoret, S. M. Girvin, and R. J. Schoelkopf, Charge-insensitive qubit design derived [from the Cooper pair box,](https://doi.org/10.1103/PhysRevA.76.042319) Phys. Rev. A **76**, 042319 (2007).
- <span id="page-33-3"></span>[4] F. Arute *et al.*, Quantum supremacy using a programmable superconducting processor, Nature **574**[, 505 \(2019\).](https://doi.org/10.1038/s41586-019-1666-5)
- <span id="page-33-9"></span>[5] Y. Kim, A. Eddins, S. Anand, K. X. Wei, E. van den Berg, S. Rosenblatt, H. Nayfeh, Y. Wu, M. Zaletel, K. Temme, and A. Kandala, Evidence for the utility of quan[tum computing before fault tolerance,](https://doi.org/10.1038/s41586-023-06096-3) Nature **618**, 500 (2023).
- [6] C. Wang *et al.*, Towards practical quantum computers: Transmon qubit with a lifetime approaching 0.5 milliseconds, [npj Quantum Inf.](https://doi.org/10.1038/s41534-021-00510-2) **8**, 3 (2022).
- [7] R. Barends *et al.*, Superconducting quantum circuits at the [surface code threshold for fault tolerance,](https://doi.org/10.1038/nature13171) Nature **508**, 500 (2014).
- [8] P. Jurcevic *et al.*, Demonstration of quantum volume 64 on [a superconducting quantum computing system,](https://doi.org/10.1088/2058-9565/abe519) Quantum Sci. Technol. **6**, 025020 (2021).
- <span id="page-33-4"></span>[9] Z. Chen, K. J. Satzinger, J. Atalaya, A. N. Korotkov *et al.*, Exponential suppression of bit or phase errors with cyclic error correction, Nature **595**[, 383 \(2021\).](https://doi.org/10.1038/s41586-021-03588-y)
- <span id="page-33-5"></span>[10] T. Alexander, N. Kanazawa, D. J. Egger, L. Capelluto, C. J. Wood, A. Javadi-Abhari, and D. C McKay, Qiskit pulse: Programming quantum computers through the cloud with pulses, [Quantum Sci. Technol.](https://doi.org/10.1088/2058-9565/aba404) **5**, 044006 (2020).
- <span id="page-33-6"></span>[11] J. Werschnik and E. K. U. Gross, Quantum optimal control theory, [J. Phys. B: At., Mol. Opt. Phys.](https://doi.org/10.1088/0953-4075/40/18/R01) **40**, R175 (2007).
- [12] D. d'Alessandro, *Introduction to Quantum Control and Dynamics* (CRC, Boca Raton, 2021).
- [13] L. Viola, E. Knill, and S. Lloyd, Dynamical decoupling [of open quantum systems,](https://doi.org/10.1103/PhysRevLett.82.2417) Phys. Rev. Lett. **82**, 2417 (1999).
- <span id="page-33-7"></span>[14] *Quantum Error Correction*, edited by D. A. Lidar and T. A. Brun (Cambridge University, Cambridge, 2013).
- <span id="page-33-8"></span>[15] M. Grassl, Th. Beth, and T. Pellizzari, Codes for the quantum erasure channel, [Phys. Rev. A](https://doi.org/10.1103/PhysRevA.56.33) **56**, 33 (1997).
- [16] S. J. Devitt, W. J. Munro, and K. Nemoto, Quantum error [correction for beginners,](https://doi.org/10.1088/0034-4885/76/7/076001) Rep. Prog. Phys. **76**, 076001 (2013).

- [17] D. A. Lidar, I. L. Chuang, and K. B. Whaley, Decoherence-free subspaces for quantum computation, [Phys. Rev. Lett.](https://doi.org/10.1103/PhysRevLett.81.2594) **81**, 2594 (1998).
- [18] J. Kempe, D. Bacon, D. A. Lidar, and K. B. Whaley, Theory of decoherence-free fault-tolerant universal quantum computation, Phys. Rev. A **63**[, 042307 \(2001\).](https://doi.org/10.1103/PhysRevA.63.042307)
- <span id="page-34-0"></span>[19] D. A. Lidar, in *Advances in Chemical Physics* (John Wiley & Sons, Inc., Hoboken, 2014), pp. 295–354.
- <span id="page-34-1"></span>[20] D. Gottesman, Stabilizer codes and quantum error correction, [arXiv:quant-ph/9705052](https://arxiv.org/abs/quant-ph/9705052) [quant-ph].
- <span id="page-34-2"></span>[21] B. M. Terhal, Quantum error correction for quantum memories, [Rev. Mod. Phys.](https://doi.org/10.1103/RevModPhys.87.307) **87**, 307 (2015).
- <span id="page-34-3"></span>[22] Z. Cai, R. Babbush, S. C. Benjamin, S. Endo, W. J. Huggins, Y. Li, J. R. McClean, and T. E. O'Brien, [Quantum error mitigation,](https://doi.org/10.1103/RevModPhys.95.045005) Rev. Mod. Phys. **95**, 045005 (2023).
- <span id="page-34-17"></span>[23] Y. Li and S. C. Benjamin, Efficient variational quantum [simulator incorporating active error minimization,](https://doi.org/10.1103/PhysRevX.7.021050) Phys. Rev. X **7**, 021050 (2017).
- <span id="page-34-18"></span>[24] K. Temme, S. Bravyi, and J. M. Gambetta, Error mitiga[tion for short-depth quantum circuits,](https://doi.org/10.1103/PhysRevLett.119.180509) Phys. Rev. Lett. **119**, 180509 (2017).
- <span id="page-34-20"></span>[25] S. Endo, S. C. Benjamin, and Y. Li, Practical quantum [error mitigation for near-future applications,](https://doi.org/10.1103/PhysRevX.8.031027) Phys. Rev. X **8**, 031027 (2018).
- [26] F. B. Maciejewski, Z. Zimbor'as, and M. Oszmaniec, Mitigation of readout noise in near-term quantum devices by classical post-processing based on detector tomography, Quantum **4**[, 257 \(2020\).](https://doi.org/10.22331/q-2020-04-24-257)
- [27] B. Nachman, M. Urbanek, W. A. de Jong, and C. W. Bauer, [Unfolding quantum computer readout noise,](https://doi.org/10.1038/s41534-020-00309-7) npj Quantum Inf. **6**, 84 (2020).
- [28] P. D. Nation, H. Kang, N. Sundaresan, and J. M. Gambetta, Scalable mitigation of measurement errors on quantum computers, PRX Quantum **2**[, 040326 \(2021\).](https://doi.org/10.1103/PRXQuantum.2.040326)
- <span id="page-34-4"></span>[29] S. Bravyi, S. Sheldon, A. Kandala, D. C. Mckay, and J. M. Gambetta, Mitigating measurement errors in multiqubit experiments, Phys. Rev. A **103**[, 042605 \(2021\).](https://doi.org/10.1103/PhysRevA.103.042605)
- <span id="page-34-5"></span>[30] B. Pokharel, N. Anand, B. Fortman, and D. A. Lidar, Demonstration of fidelity improvement using dynamical [decoupling with superconducting qubits,](https://doi.org/10.1103/PhysRevLett.121.220502) Phys. Rev. Lett. **121**, 220502 (2018).
- [31] B. Pokharel and D. A. Lidar, Demonstration of algo[rithmic quantum speedup,](https://doi.org/10.1103/PhysRevLett.130.210602) Phys. Rev. Lett. **130**, 210602 (2023).
- <span id="page-34-16"></span>[32] Z. Zhou, R. Sitler, Y. Oda, K. Schultz, and G. Quiroz, [Quantum crosstalk robust quantum control,](https://doi.org/10.1103/PhysRevLett.131.210802) Phys. Rev. Lett. **131**, 210802 (2023).
- [33] B. Pokharel and D. A. Lidar, Better-than-classical grover [search via quantum error detection and suppression,](https://doi.org/10.1038/s41534-023-00794-6) npj Quantum Inf. **10**, 23 (2024).
- <span id="page-34-6"></span>[34] P. Singkanipa, V. Kasatkin, Z. Zhou, G. Quiroz, and D. A. Lidar, Demonstration of algorithmic quantum speedup [for an abelian hidden subgroup problem,](https://doi.org/10.1103/PhysRevX.15.021082) Phys. Rev. X **15**, 021082 (2025).
- <span id="page-34-7"></span>[35] A. Mena López and L.-A. Wu, Protectability of IBMQ [qubits by dynamical decoupling technique,](https://doi.org/10.3390/sym15010062) Symmetry **15**, 62 (2023).
- [36] G. Quiroz, B. Pokharel, J. Boen, L. Tewala, V. Tripathi, D. Williams, L.-A. Wu, P. Titum, K. Schultz, and D. Lidar, Dynamically generated decoherence-free subspaces and

- [subsystems on superconducting qubits,](https://doi.org/10.1088/1361-6633/ad6805) Rep. Prog. Phys. **87**, 097601 (2024).
- <span id="page-34-8"></span>[37] J.-X. Han, J. Zhang, G.-M. Xue, H. Yu, and G. Long, Pro[tecting logical qubits with dynamical decoupling,](https://doi.org/10.1103/lm8x-r48q) Phys. Rev. Appl. **24**, 024003 (2025).
- <span id="page-34-9"></span>[38] R. Harper and S. T. Flammia, Fault-tolerant logical gates [in the IBM quantum experience,](https://doi.org/10.1103/PhysRevLett.122.080504) Phys. Rev. Lett. **122**, 080504 (2019).
- [39] C. K. Andersen, A. Remm, S. Lazar, S. Krinner, N. Lacroix, G. J. Norris, M. Gabureac, C. Eichler, and A. Wallraff, Repeated quantum error detection in a surface code, Nat. Phys. **16**[, 875 \(2020\).](https://doi.org/10.1038/s41567-020-0920-y)
- [40] S. Krinner, N. Lacroix, A. Remm, A. Di Paolo, E. Genois, C. Leroux, C. Hellings, S. Lazar, F. Swiadek, J. Herrmann *et al.*, Realizing repeated quantum error correction in a distance-three surface code, Nature **605**[, 669 \(2022\).](https://doi.org/10.1038/s41586-022-04566-8)
- [41] K. C. Miao, M. McEwen, J. Atalaya, D. Kafri, L. P. Pryadko, A. Bengtsson, A. Opremcak, K. J. Satzinger, Z. Chen, P. V. Klimov *et al.*, Overcoming leakage in quantum error correction, Nat. Phys. **19**[, 1780 \(2023\).](https://doi.org/10.1038/s41567-023-02226-w)
- [42] V. V. Sivak, A. Eickbusch, B. Royer, S. Singh, I. Tsioutsios, S. Ganjam, A. Miano, B. L. Brock, A. Z. Ding, L. Frunzio *et al.*, Real-time quantum error correction beyond break-even, Nature **616**[, 50 \(2023\).](https://doi.org/10.1038/s41586-023-05782-6)
- <span id="page-34-10"></span>[43] Google Quantum AI, Suppressing quantum errors by scaling a surface code logical qubit, Nature **614**[, 676 \(2023\).](https://doi.org/10.1038/s41586-022-05434-1)
- <span id="page-34-11"></span>[44] E. F. Dumitrescu, A. J. McCaskey, G. Hagen, G. R. Jansen, T. D. Morris, T. Papenbrock, R. C. Pooser, D. J. Dean, and P. Lougovski, Cloud quantum computing of an atomic nucleus, Phys. Rev. Lett. **120**[, 210501 \(2018\).](https://doi.org/10.1103/PhysRevLett.120.210501)
- <span id="page-34-19"></span>[45] A. Kandala, K. Temme, A. D. Córcoles, A. Mezzacapo, J. M. Chow, and J. M. Gambetta, Error mitigation extends the computational reach of a noisy quantum processor, Nature **567**[, 491 \(2019\).](https://doi.org/10.1038/s41586-019-1040-7)
- [46] Y. Kim, C. J. Wood, T. J. Yoder, S. T. Merkel, J. M. Gambetta, K. Temme, and A. Kandala, Scalable error mitigation for noisy quantum circuits produces competitive expectation values, Nat. Phys. **19**[, 752 \(2023\).](https://doi.org/10.1038/s41567-022-01914-3)
- <span id="page-34-12"></span>[47] Y. Kim, A. Eddins, S. Anand, K. X. Wei, E. van den Berg, S. Rosenblatt, H. Nayfeh, Y. Wu, M. Zaletel, K. Temme *et al.*, Evidence for the utility of quantum computing before fault tolerance, Nature **618**[, 500 \(2023\).](https://doi.org/10.1038/s41586-023-06096-3)
- <span id="page-34-13"></span>[48] D. A. Lidar, Lecture notes on the theory of open quantum systems, [arXiv:1902.00967](https://arxiv.org/abs/1902.00967) [quant-ph].
- [49] F. Campaioli, J. H. Cole, and H. Hapuarachchi, Quantum master equations: Tips and tricks for quantum [optics, quantum computing and beyond,](https://doi.org/10.1103/PRXQuantum.5.020202) PRX Quantum **5**, 020202 (2024).
- <span id="page-34-14"></span>[50] H.-P. Breuer and F. Petruccione, *The Theory of Open Quantum Systems* (Oxford University, Oxford, 2007).
- <span id="page-34-15"></span>[51] D. Crow and R. Joynt, Classical simulation of quan[tum dephasing and depolarizing noise,](https://doi.org/10.1103/PhysRevA.89.042123) Phys. Rev. A **89**, 042123 (2014).
- [52] C. Benedetti, Decoherence, non-markovianity and quantum estimation in qubit systems subject to classical noise, PhD thesis, Università degli Studi di Milano, 2015, <https://hdl.handle.net/20.500.14242/83264>
- [53] M. A. C. Rossi, C. Foti, A. Cuccoli, J. Trapani, P. Verrucchi, and M. G. A. Paris, Effective description of the [short-time dynamics in open quantum systems,](https://doi.org/10.1103/PhysRevA.96.032116) Phys. Rev. A **96**, 032116 (2017).

- [54] S. M. H. Halataei, Classical simulation of arbitrary quantum noise, Phys. Rev. A **96**[, 042338 \(2017\).](https://doi.org/10.1103/PhysRevA.96.042338)
- <span id="page-35-0"></span>[55] L. Peng, N. Arai, and K. Yasuoka, A stochastic Hamiltonian formulation applied to dissipative particle dynamics, [Appl. Math. Comput.](https://doi.org/10.1016/j.amc.2022.127126) **426**, 127126 (2022).
- <span id="page-35-1"></span>[56] L. M. Norris, G. A. Paz-Silva, and L. Viola, Qubit noise spectroscopy for non-Gaussian dephasing environments, Phys. Rev. Lett. **116**[, 150503 \(2016\).](https://doi.org/10.1103/PhysRevLett.116.150503)
- <span id="page-35-2"></span>[57] A. Murphy, J. Epstein, G. Quiroz, K. Schultz, L. Tewala, K. McElroy, C. Trout, B. Tien-Street, J. A. Hoffmann, B. D. Clader, J. Long, D. P. Pappas, and T. M. Sweeney, Universal-dephasing-noise injection via Schrödinger-wave autoregressive moving-average models, Phys. Rev. Res. **4**[, 013081 \(2022\).](https://doi.org/10.1103/PhysRevResearch.4.013081)
- <span id="page-35-3"></span>[58] M. L. Dahlhauser and T. S. Humble, Modeling noisy quan[tum circuits using experimental characterization,](https://doi.org/10.1103/PhysRevA.103.042603) Phys. Rev. A **103**, 042603 (2021).
- <span id="page-35-29"></span>[59] K. Georgopoulos, C. Emary, and P. Zuliani, Modeling and simulating the noisy behavior of near-term quantum computers, Phys. Rev. A **104**[, 062432 \(2021\).](https://doi.org/10.1103/PhysRevA.104.062432)
- [60] L. I. Payne Torres, A. O. Schouten, and D. A. Mazziotti, Lifetime of strongly correlated states on near[term quantum Computers,](https://doi.org/10.1021/acs.jpca.4c02665) J. Phys. Chem. A **128**, 7269 (2024).
- <span id="page-35-4"></span>[61] T. Weber, K. Borras, K. Jansen, D. Krücker, and M. Riebisch, Construction and volumetric benchmarking of [quantum computing noise models,](https://doi.org/10.1088/1402-4896/ad406c) Phys. Scr. **99**, 065106 (2024).
- <span id="page-35-5"></span>[62] E. van den Berg, Z. K. Minev, A. Kandala, and K. Temme, Probabilistic error cancellation with sparse [Pauli–Lindblad models on noisy quantum processors,](https://doi.org/10.1038/s41567-023-02042-2) Nat. Phys. **19**, 1116 (2023).
- <span id="page-35-6"></span>[63] J. E. Jaloveckas, M. T. P. Nguyen, L. Palackal, J. M. Lorenz, and H. Ehm, Efficient learning of sparse Pauli Lindblad models for fully connected qubit topology, [arXiv:2311.11639](https://arxiv.org/abs/2311.11639) [quant-ph].
- <span id="page-35-7"></span>[64] C. H. Bennett, G. Brassard, S. Popescu, B. Schumacher, J. A. Smolin, and W. K. Wootters, Purification of noisy entanglement and faithful teleportation via noisy channels, [Phys. Rev. Lett.](https://doi.org/10.1103/PhysRevLett.76.722) **76**, 722 (1996).
- [65] E. Knill, Fault-tolerant postselected quantum computation: Threshold analysis, [arXiv:quant-ph/0404104](https://arxiv.org/abs/quant-ph/0404104) [quantph].
- [66] O. Kern, G. Alber, and D. L. Shepelyansky, Quantum error [correction of coherent errors by randomization,](https://doi.org/10.1140/epjd/e2004-00196-9) Eur. Phys. D **32**, 153 (2005).
- <span id="page-35-8"></span>[67] C. Dankert, R. Cleve, J. Emerson, and E. Livine, Exact and approximate unitary 2-designs and their application to fidelity estimation, Phys. Rev. A **80**[, 012304 \(2009\).](https://doi.org/10.1103/PhysRevA.80.012304)
- <span id="page-35-9"></span>[68] H. Zhang, B. Pokharel, E. M. Levenson-Falk, and D. Lidar, Predicting non-Markovian superconducting-qubit [dynamics from tomographic reconstruction,](https://doi.org/10.1103/PhysRevApplied.17.054018) Phys. Rev. Appl. **17**, 054018 (2022).
- <span id="page-35-10"></span>[69] T. Thorbeck, Z. Xiao, A. Kamal, and L. C. G. Govia, Readout-induced suppression and enhancement of [superconducting qubit lifetimes,](https://doi.org/10.1103/PhysRevLett.132.090602) Phys. Rev. Lett. **132**, 090602 (2024).
- <span id="page-35-11"></span>[70] V. Tripathi, H. Chen, E. Levenson-Falk, and D. A. Lidar, Modeling low- and high-frequency noise in transmon [qubits with resource-efficient measurement,](https://doi.org/10.1103/PRXQuantum.5.010320) PRX Quantum **5**, 010320 (2024).

- <span id="page-35-12"></span>[71] V. Tripathi, H. Chen, M. Khezri, K.-W. Yip, E. M. Levenson-Falk, and D. A. Lidar, Suppression of crosstalk in superconducting qubits using dynamical decoupling, [Phys. Rev. Appl.](https://doi.org/10.1103/PhysRevApplied.18.024068) **18**, 024068 (2022).
- <span id="page-35-13"></span>[72] D. Manzano, A short introduction to the Lindblad master equation, AIP Adv. **10**[, 025106 \(2020\).](https://doi.org/10.1063/1.5115323)
- <span id="page-35-14"></span>[73] K. Nakamura and J. Ankerhold, Gate operations for super[conducting qubits and non-Markovianity,](https://doi.org/10.1103/PhysRevResearch.6.033215) Phys. Rev. Res. **6**, 033215 (2024).
- <span id="page-35-15"></span>[74] G. Di Bartolomeo, M. Vischi, F. Cesa, R. Wixinger, M. Grossi, S. Donadi, and A. Bassi, Noisy gates for sim[ulating quantum computers,](https://doi.org/10.1103/PhysRevResearch.5.043210) Phys. Rev. Res. **5**, 043210 (2023).
- <span id="page-35-16"></span>[75] L. Shirizly, G. Misguich, and H. Landa, Dissipative dynamics of graph-state stabilizers with superconducting qubits, Phys. Rev. Lett. **132**[, 010601 \(2024\).](https://doi.org/10.1103/PhysRevLett.132.010601)
- <span id="page-35-17"></span>[76] G. O. Samach, A. Greene, J. Borregaard, M. Christandl, J. Barreto, D. K. Kim, C. M. McNally, A. Melville, B. M. Niedzielski, Y. Sung, D. Rosenberg, M. E. Schwartz, J. L. Yoder, T. P. Orlando, J. I.-J. Wang, S. Gustavsson, M. Kjaergaard, and W. D. Oliver, Lindblad tomography of a [superconducting quantum Processor,](https://doi.org/10.1103/PhysRevApplied.18.064056) Phys. Rev. Appl. **18**, 064056 (2022).
- <span id="page-35-18"></span>[77] J. Bylander, S. Gustavsson, F. Yan, F. Yoshihara, K. Harrabi, G. Fitch, D. G. Cory, Y. Nakamura, J.-S. Tsai, and W. D. Oliver, Noise spectroscopy through dynamical [decoupling with a superconducting flux qubit,](https://doi.org/10.1038/nphys1994) Nat. Phys. **7**, 565 (2011).
- <span id="page-35-19"></span>[78] D. A. Rower *et al.*, Evolution of 1/*f* flux noise in super[conducting qubits with magnetic fields,](https://doi.org/10.1103/PhysRevLett.130.220602) Phys. Rev. Lett. **130**, 220602 (2023).
- <span id="page-35-20"></span>[79] U. von Lüpke, F. Beaudoin, L. M. Norris, Y. Sung, R. Winik, J. Y. Qiu, M. Kjaergaard, D. Kim, J. Yoder, S. Gustavsson, L. Viola, and W. D. Oliver, Two-qubit spectroscopy of spatiotemporally correlated quantum noise in superconducting qubits, PRX Quantum **1**[, 010305 \(2020\).](https://doi.org/10.1103/PRXQuantum.1.010305)
- <span id="page-35-21"></span>[80] Y. Sung, A. Vepsäläinen, J. Braumüller, F. Yan, J. I.-J. Wang, M. Kjaergaard, R. Winik, P. Krantz, A. Bengtsson, A. J. Melville *et al.*, Multi-level quantum noise spectroscopy, [Nat. Commun.](https://doi.org/10.1038/s41467-021-21098-3) **12**, 967 (2021).
- <span id="page-35-22"></span>[81] M. Cerezo, A. Arrasmith, R. Babbush, S. C. Benjamin, S. Endo, K. Fujii, J. R. McClean, K. Mitarai, X. Yuan, L. Cincio *et al.*[, Variational quantum algorithms,](https://doi.org/10.1038/s42254-021-00348-9) Nat. Rev. Phys. **3**, 625 (2021).
- <span id="page-35-23"></span>[82] Z. Schwartzman-Nowik, L. Shirizly, and H. Landa, Modeling error correction with Lindblad dynamics and approximate channels, Phys. Rev. A **111**[, 022613 \(2025\).](https://doi.org/10.1103/PhysRevA.111.022613)
- <span id="page-35-24"></span>[83] D. Greenbaum, Introduction to quantum gate set tomography, [arXiv:1509.02921.](https://arxiv.org/abs/1509.02921)
- <span id="page-35-25"></span>[84] E. Nielsen, J. K. Gamble, K. Rudinger, T. Scholten, K. Young, and R. Blume-Kohout, Gate set tomography, Quantum **5**[, 557 \(2021\).](https://doi.org/10.22331/q-2021-10-05-557)
- <span id="page-35-26"></span>[85] G. A. L. White, F. A. Pollock, L. C. L. Hollenberg, K. Modi, and C. D. Hill, Non-Markovian quantum process tomography, PRX Quantum **3**[, 020344 \(2022\).](https://doi.org/10.1103/PRXQuantum.3.020344)
- <span id="page-35-27"></span>[86] G. A. L. White, C. D. Hill, F. A. Pollock, L. C. L. Hollenberg, and K. Modi, Demonstration of non-Markovian process characterisation and control on a quantum processor, [Nat. Commun.](https://doi.org/10.1038/s41467-020-20113-3) **11**, 6301 (2020).
- <span id="page-35-28"></span>[87] J. A. Gross, E. Genois, D. M. Debroy, Y. Zhang, W. Mruczkiewicz, Z.-P. Cian, and Z. Jiang, Characterizing

- [coherent errors using matrix-element amplification,](https://doi.org/10.1038/s41534-024-00917-7) npj Quantum Inf. **10**, 123 (2024).
- <span id="page-36-0"></span>[88] G. A. Alvare´z and D. Suter, Measuring the spectrum of [colored noise by dynamical decoupling,](https://doi.org/10.1103/PhysRevLett.107.230501) Phys. Rev. Lett. **107**, 230501 (2011).
- <span id="page-36-25"></span>[89] G. A. Paz-Silva, L. M. Norris, and L. Viola, Multiqubit [spectroscopy of Gaussian quantum noise,](https://doi.org/10.1103/PhysRevA.95.022121) Phys. Rev. A **95**, 022121 (2017).
- [90] Y. Romach, C. Müller, T. Unden, L. J. Rogers, T. Isoda, K. M. Itoh, M. Markham, A. Stacey, J. Meijer, S. Pezzagna, B. Naydenov, L. P. McGuinness, N. Bar-Gill, and F. Jelezko, Spectroscopy of surface-induced noise using [shallow spins in diamond,](https://doi.org/10.1103/PhysRevLett.114.017601) Phys. Rev. Lett. **114**, 017601 (2015).
- <span id="page-36-23"></span>[91] V. M. Frey, S. Mavadia, L. M. Norris, W. de Ferranti, D. Lucarelli, L. Viola, and M. J. Biercuk, Application of optimal band-limited control protocols to quantum noise sensing, [Nat. Commun.](https://doi.org/10.1038/s41467-017-02298-2) **8**, 2189 (2017).
- [92] K. W. Chan, W. Huang, C. H. Yang, J. C. C. Hwang, B. Hensen, T. Tanttu, F. E. Hudson, K. M. Itoh, A. Laucht, A. Morello, and A. S. Dzurak, Assessment of a silicon quantum dot spin qubit environment via noise spectroscopy, [Phys. Rev. Appl.](https://doi.org/10.1103/PhysRevApplied.10.044017) **10**, 044017 (2018).
- [93] G. A. Paz-Silva, L. M. Norris, F. Beaudoin, and L. Viola, Extending comb-based spectral estimation to multiaxis quantum noise, Phys. Rev. A **100**[, 042334 \(2019\).](https://doi.org/10.1103/PhysRevA.100.042334)
- <span id="page-36-1"></span>[94] V. Maloney, Y. Oda, G. Quiroz, B. D. Clader, and L. M. Norris, Qubit control noise spectroscopy with opti[mal suppression of dephasing,](https://doi.org/10.1103/PhysRevA.106.022425) Phys. Rev. A **106**, 022425 (2022).
- <span id="page-36-2"></span>[95] L. Cywinski, R. M. Lutchyn, C. P. Nave, and S. Das ´ Sarma, How to enhance dephasing time in superconducting qubits, Phys. Rev. B **77**[, 174509 \(2008\).](https://doi.org/10.1103/PhysRevB.77.174509)
- <span id="page-36-24"></span>[96] T. J. Green, J. Sastrawan, H. Uys, and M. J. Biercuk, Arbitrary quantum control of qubits in the presence of universal noise, New J. Phys. **15**[, 095004 \(2013\).](https://doi.org/10.1088/1367-2630/15/9/095004)
- [97] T. Green, H. Uys, and M. J. Biercuk, High-order noise fil[tering in nontrivial quantum logic gates,](https://doi.org/10.1103/PhysRevLett.109.020501) Phys. Rev. Lett. **109**, 020501 (2012).
- <span id="page-36-5"></span>[98] G. A. Paz-Silva and L. Viola, General transfer-function approach to noise filtering in open-loop quantum control, Phys. Rev. Lett. **113**[, 250501 \(2014\).](https://doi.org/10.1103/PhysRevLett.113.250501)
- <span id="page-36-3"></span>[99] A. G. Kofman and G. Kurizki, Universal dynamical control of quantum mechanical decay: Modulation of the [coupling to the continuum,](https://doi.org/10.1103/PhysRevLett.87.270405) Phys. Rev. Lett. **87**, 270405 (2001).
- <span id="page-36-4"></span>[100] E. Knill, D. Leibfried, R. Reichle, J. Britton, R. B. Blakestad, J. D. Jost, C. Langer, R. Ozeri, S. Seidelin, and D. J. Wineland, Randomized benchmarking of quantum gates, Phys. Rev. A **77**[, 012307 \(2008\).](https://doi.org/10.1103/PhysRevA.77.012307)
- <span id="page-36-6"></span>[101] D. C. McKay, C. J. Wood, S. Sheldon, J. M. Chow, and J. M. Gambetta, Efficient *Z* gates for quantum computing, Phys. Rev. A **96**[, 022330 \(2017\).](https://doi.org/10.1103/PhysRevA.96.022330)
- <span id="page-36-7"></span>[102] G. S. Paraoanu, Microwave-induced coupling of super[conducting qubits,](https://doi.org/10.1103/PhysRevB.74.140504) Phys. Rev. B **74**, 140504(R) (2006).
- [103] C. Rigetti and M. Devoret, Fully microwave-tunable universal gates in superconducting qubits with linear cou[plings and fixed transition frequencies,](https://doi.org/10.1103/PhysRevB.81.134507) Phys. Rev. B **81**, 134507 (2010).

- [104] E. Magesan and J. M. Gambetta, Effective Hamiltonian [models of the cross-resonance gate,](https://doi.org/10.1103/PhysRevA.101.052308) Phys. Rev. A **101**, 052308 (2020).
- [105] M. Malekakhlagh, E. Magesan, and D. C. McKay, Firstprinciples analysis of cross-resonance gate operation, Phys. Rev. A **102**[, 042605 \(2020\).](https://doi.org/10.1103/PhysRevA.102.042605)
- <span id="page-36-8"></span>[106] V. Tripathi, M. Khezri, and A. N. Korotkov, Operation and intrinsic error budget of a two-qubit cross-resonance gate, Phys. Rev. A **100**[, 012301 \(2019\).](https://doi.org/10.1103/PhysRevA.100.012301)
- <span id="page-36-9"></span>[107] S. Sheldon, E. Magesan, J. M. Chow, and J. M. Gambetta, Procedure for systematically tuning up cross-talk in the cross-resonance gate, Phys. Rev. A **93**[, 060302\(R\) \(2016\).](https://doi.org/10.1103/PhysRevA.93.060302)
- <span id="page-36-10"></span>[108] K. X. Wei, E. Magesan, I. Lauer, S. Srinivasan, D. F. Bogorin, S. Carnevale, G. A. Keefe, Y. Kim, D. Klaus, W. Landers, N. Sundaresan, C. Wang, E. J. Zhang, M. Steffen, O. E. Dial, D. C. McKay, and A. Kandala, Hamiltonian engineering with multicolor drives for fast entangling [gates and quantum crosstalk cancellation,](https://doi.org/10.1103/PhysRevLett.129.060501) Phys. Rev. Lett. **129**, 060501 (2022).
- <span id="page-36-11"></span>[109] N. Sundaresan, I. Lauer, E. Pritchett, E. Magesan, P. Jurcevic, and J. M. Gambetta, Reducing unitary and spectator errors in cross resonance with optimized rotary echoes, PRX Quantum **1**[, 020318 \(2020\).](https://doi.org/10.1103/PRXQuantum.1.020318)
- <span id="page-36-12"></span>[110] C. J. Wood and J. M. Gambetta, Quantification and char[acterization of leakage errors,](https://doi.org/10.1103/PhysRevA.97.032306) Phys. Rev. A **97**, 032306 (2018).
- <span id="page-36-13"></span>[111] M. Papic, A. Auer, and I. de Vega, Fast estima- ˇ tion of physical error contributions of quantum gates, [arXiv:2305.08916](https://arxiv.org/abs/2305.08916) [quant-ph].
- <span id="page-36-14"></span>[112] D. C. McKay, S. Sheldon, J. A. Smolin, J. M. Chow, and J. M. Gambetta, Three-qubit randomized benchmarking, Phys. Rev. Lett. **122**[, 200502 \(2019\).](https://doi.org/10.1103/PhysRevLett.122.200502)
- <span id="page-36-15"></span>[113] X. Li, T. Cai, H. Yan, Z. Wang, X. Pan, Y. Ma, W. Cai, J. Han, Z. Hua, X. Han, Y. Wu, H. Zhang, H. Wang, Y. Song, L. Duan, and L. Sun, Tunable coupler for realizing a controlled-phase gate with dynamically decoupled regime [in a superconducting circuit,](https://doi.org/10.1103/PhysRevApplied.14.024070) Phys. Rev. Appl. **14**, 024070 (2020).
- <span id="page-36-16"></span>[114] K. X. Wei, E. Pritchett, D. M. Zajac, D. C. McKay, and S. Merkel, Characterizing non-Markovian off-resonant errors in quantum gates, [Phys. Rev. Appl.](https://doi.org/10.1103/PhysRevApplied.21.024018) **21**, 024018 (2024).
- <span id="page-36-17"></span>[115] A. Brillant, P. Groszkowski, A. Seif, J. Koch, and A. A. Clerk, Randomized benchmarking with non-Markovian [noise and realistic finite-time gates,](https://doi.org/10.1103/tmfd-qc5q) Phys. Rev. Lett. **135**, 070601 (2025).
- <span id="page-36-18"></span>[116] G. A. Paz-Silva, M. J. W. Hall, and H. M. Wiseman, Dynamics of initially correlated open quantum systems: [Theory and applications,](https://doi.org/10.1103/physreva.100.042120) Phys. Rev. A **100**, 042120 (2019).
- <span id="page-36-19"></span>[117] Y. Ashida, Z. Gong, and M. Ueda, Non-Hermitian physics, Adv. Phys. **69**[, 249 \(2020\).](https://doi.org/10.1080/00018732.2021.1876991)
- <span id="page-36-20"></span>[118] O. Siltanen, T. Kuusela, and J. Piilo, Interferometric approach to open quantum systems and non-Markovian dynamics, Phys. Rev. A **103**[, 032223 \(2021\).](https://doi.org/10.1103/PhysRevA.103.032223)
- <span id="page-36-21"></span>[119] J. Ku, X. Xu, M. Brink, D. C. McKay, J. B. Hertzberg, M. H. Ansari, and B. L. T. Plourde, Suppression of unwanted *ZZ* [interactions in a hybrid two-qubit system,](https://doi.org/10.1103/PhysRevLett.125.200504) Phys. Rev. Lett. **125**, 200504 (2020).
- <span id="page-36-22"></span>[120] S. Shirai, Y. Okubo, K. Matsuura, A. Osada, Y. Nakamura, and A. Noguchi, All-microwave manipulation of

- superconducting qubits with a fixed-frequency transmon coupler, Phys. Rev. Lett. **130**[, 260601 \(2023\).](https://doi.org/10.1103/PhysRevLett.130.260601)
- <span id="page-37-0"></span>[121] A. Agarwal, L. P. Lindoy, D. Lall, F. Jamet, and I. Rungger, Modelling non-Markovian noise in driven superconducting qubits, [Quantum Sci. Technol.](https://doi.org/10.1088/2058-9565/ad3d7e) **9**, 035017 (2024).
- <span id="page-37-2"></span>[122] T. Thorbeck, A. Eddins, I. Lauer, D. T. McClure, and M. Carroll, Two-level-system dynamics in a superconducting [qubit due to background ionizing radiation,](https://doi.org/10.1103/PRXQuantum.4.020356) PRX Quantum **4**, 020356 (2023).
- <span id="page-37-1"></span>[123] J. J. Burnett, A. Bengtsson, M. Scigliuzzo, D. Niepce, M. Kudra, P. Delsing, and J. Bylander, Decoherence bench[marking of superconducting qubits,](https://doi.org/10.1038/s41534-019-0168-5) npj Quantum Inf. **5**, 54 (2019).
- <span id="page-37-3"></span>[124] D. Ristè, C. C. Bultink, M. J. Tiggelman, R. N. Schouten, K. W. Lehnert, and L. DiCarlo, Millisecond charge-parity fluctuations and induced decoherence in a superconducting transmon qubit, [Nat. Commun.](https://doi.org/10.1038/ncomms2936) **4**, 1913 (2013).
- [125] S. E. de Graaf, L. Faoro, L. B. Ioffe, S. Mahashabde, J. J. Burnett, T. Lindström, S. E. Kubatkin, A. V. Danilov, and A. Y. Tzalenchuk, Two-level systems in superconducting [quantum devices due to trapped quasiparticles,](https://doi.org/10.1126/sciadv.abc5055) Sci. Adv. **6**, eabc5055 (2020).
- <span id="page-37-4"></span>[126] S. E. de Graaf, S. Mahashabde, S. E. Kubatkin, A. Ya. Tzalenchuk, and A. V. Danilov, Quantifying dynamics and interactions of individual spurious low-energy fluctuators [in superconducting circuits,](https://doi.org/10.1103/PhysRevB.103.174103) Phys. Rev. B **103**, 174103 (2021).
- <span id="page-37-5"></span>[127] P. Jurcevic and L. C. G. Govia, Effective qubit dephas[ing induced by spectator-qubit relaxation,](https://doi.org/10.1088/2058-9565/ac8cad) Quantum Sci. Technol. **7**, 045033 (2022).
- <span id="page-37-6"></span>[128] A. McDonald and A. A. Clerk, Exact solutions of interact[ing dissipative systems via weak symmetries,](https://doi.org/10.1103/PhysRevLett.128.033602) Phys. Rev. Lett. **128**, 033602 (2022).
- <span id="page-37-7"></span>[129] E. Paladino, Y. M. Galperin, G. Falci, and B. L. Altshuler, 1/*f* noise: Implications for solid-state quantum information, [Rev. Mod. Phys.](https://doi.org/10.1103/RevModPhys.86.361) **86**, 361 (2014).
- <span id="page-37-9"></span>[130] F. Yan, S. Gustavsson, A. Kamal, J. Birenbaum, A. P. Sears, D. Hover, T. J. Gudmundsen, D. Rosenberg, G. Samach, S. Weber *et al.*, The flux qubit revisited to [enhance coherence and reproducibility,](https://doi.org/10.1038/ncomms12964) Nat. Commun. **7**, 12964 (2016).
- <span id="page-37-8"></span>[131] J. Burnett, L. Faoro, I. Wisby, V. L. Gurtovoi, A. V. Chernykh, G. M. Mikhailov, V. A. Tulin, R. Shaikhaidarov, V. Antonov, P. J. Meeson, A. Ya. Tzalenchuk, and T. Lindström, Evidence for interacting twolevel systems from the 1/f noise of a superconducting resonator, [Nat. Commun.](https://doi.org/10.1038/ncomms5119) **5**, 4119 (2014).
- <span id="page-37-10"></span>[132] H. Y. Carr and E. M. Purcell, Effects of diffusion on free precession in nuclear magnetic resonance experiments, Phys. Rev. **94**[, 630 \(1954\).](https://doi.org/10.1103/PhysRev.94.630)
- <span id="page-37-11"></span>[133] S. Meiboom and D. Gill, Modified spin-echo method for [measuring nuclear relaxation times,](https://doi.org/10.1063/1.1716296) Rev. Sci. Instrum. **29**, 688 (1958).
- <span id="page-37-12"></span>[134] J. Tilly, H. Chen, S. Cao, D. Picozzi, K. Setia, Y. Li, E. Grant, L. Wossnig, I. Rungger, G. H. Booth, and J. Tennyson, The variational quantum eigensolver: A [review of methods and best practices,](https://doi.org/10.1016/j.physrep.2022.08.003) Phys. Rep. **986**, 1 (2022).

- <span id="page-37-13"></span>[135] P. J. J. O'Malley *et al.*, Scalable quantum simulation of molecular energies, Phys. Rev. X **6**[, 031007 \(2016\).](https://doi.org/10.1103/PhysRevX.6.031007)
- <span id="page-37-14"></span>[136] A. Tranter, S. Sofia, J. Seeley, M. Kaicher, J. McClean, R. Babbush, P. V. Coveney, F. Mintert, F. Wilhelm, and P. J. Love, The Bravyi–Kitaev transformation: Properties and applications, [Int. J. Quantum Chem.](https://doi.org/10.1002/qua.24969) **115**, 1431 (2015).
- <span id="page-37-15"></span>[137] N. Khaneja, T. Reiss, C. Kehlet, T. Schulte-Herbrüggen, and S. J. Glaser, Optimal control of coupled spin dynamics: Design of NMR pulse sequences by gradient ascent algorithms, [J. Magn. Reson.](https://doi.org/10.1016/j.jmr.2004.11.004) **172**, 296 (2005).
- <span id="page-37-16"></span>[138] T. Caneva, M. Murphy, T. Calarco, R. Fazio, S. Montangero, V. Giovannetti, and G. E. Santoro, Optimal con[trol at the quantum speed limit,](https://doi.org/10.1103/PhysRevLett.103.240501) Phys. Rev. Lett. **103**, 240501 (2009).
- <span id="page-37-17"></span>[139] F. Arute *et al.*, Hartree-fock on a superconducting qubit quantum computer, Science **369**[, 1084 \(2020\).](https://doi.org/10.1126/science.abb9811)
- <span id="page-37-18"></span>[140] J. P. Bonilla Ataides, D. K. Tuckett, S. D. Bartlett, S. T. [Flammia, and B. J. Brown, The XZZX surface code,](https://doi.org/10.1038/s41467-021-22274-1) Nat. Commun. **12**, 2172 (2021).
- <span id="page-37-19"></span>[141] A. G. Fowler, M. Mariantoni, J. M. Martinis, and A. N. Cleland, Surface codes: Towards practical large-scale quantum computation, Phys. Rev. A **86**[, 032324 \(2012\).](https://doi.org/10.1103/PhysRevA.86.032324)
- <span id="page-37-20"></span>[142] F. Li, A.-Q. Li, Q.-D. Gan, and H.-Y. Ma, Recurrent neural network decoding of rotated surface codes based on distributed strategy, Chin. Phys. B **33**[, 040307 \(2024\).](https://doi.org/10.1088/1674-1056/ad2bef)
- <span id="page-37-21"></span>[143] D. Bhardwaj, E. Takou, Y. Lin, and K. R. Brown, Adaptive estimation of drifting noise in quantum error correction, [arXiv:2511.09491](https://arxiv.org/abs/2511.09491) [quant-ph].
- <span id="page-37-22"></span>[144] M. Malekakhlagh, A. Seif, D. Puzzuoli, L. C. Govia, and E. van den Berg, Efficient Lindblad synthesis for noise model construction, [npj Quantum Inf.](https://doi.org/10.1038/s41534-025-01139-1) **11**, 191 (2025).
- <span id="page-37-23"></span>[145] C. Chamberland, G. Zhu, T. J. Yoder, J. B. Hertzberg, and A. W. Cross, Topological and subsystem codes on low[degree graphs with flag qubits,](https://doi.org/10.1103/PhysRevX.10.011022) Phys. Rev. X **10**, 011022 (2020).
- <span id="page-37-24"></span>[146] Zenodo, <https://doi.org/10.5281/zenodo.19612185>
- <span id="page-37-25"></span>[147] P. C. Moan, J. A. Oteo, and J. Ros, On the existence of the [exponential solution of linear differential systems,](https://doi.org/10.1088/0305-4470/32/27/311) J. Phys. A: Math. Gen. **32**, 5133 (1999).
- <span id="page-37-26"></span>[148] B. Gulácsi and G. Burkard, Signatures of non-Marko[vianity of a superconducting qubit,](https://doi.org/10.1103/PhysRevB.107.174511) Phys. Rev. B **107**, 174511 (2023).
- <span id="page-37-27"></span>[149] S. Schlör, J. Lisenfeld, C. Müller, A. Bilmes, A. Schneider, D. P. Pappas, A. V. Ustinov, and M. Weides, Correlating decoherence in transmon qubits: Low frequency noise by single fluctuators, Phys. Rev. Lett. **123**[, 190502 \(2019\).](https://doi.org/10.1103/PhysRevLett.123.190502)
- <span id="page-37-28"></span>[150] L. M. Norris, D. Lucarelli, V. M. Frey, S. Mavadia, M. J. Biercuk, and L. Viola, Optimally band-limited spec[troscopy of control noise using a qubit sensor,](https://doi.org/10.1103/PhysRevA.98.032315) Phys. Rev. A **98**, 032315 (2018).
- <span id="page-37-29"></span>[151] F. Motzoi, J. M. Gambetta, P. Rebentrost, and F. K. Wilhelm, Simple pulses for elimination of leakage in weakly nonlinear qubits, Phys. Rev. Lett. **103**[, 110501 \(2009\).](https://doi.org/10.1103/PhysRevLett.103.110501)
- <span id="page-37-30"></span>[152] A. Hashim, R. K. Naik, A. Morvan, J.-L. Ville, B. Mitchell, J. M. Kreikebaum, M. Davis, E. Smith, C. Iancu, K. P. O'Brien, I. Hincks, J. J. Wallman, J. Emerson, and I. Siddiqi, Randomized compiling for scalable quantum computing on a noisy superconducting quantum processor, Phys. Rev. X **11**[, 041039 \(2021\).](https://doi.org/10.1103/PhysRevX.11.041039)
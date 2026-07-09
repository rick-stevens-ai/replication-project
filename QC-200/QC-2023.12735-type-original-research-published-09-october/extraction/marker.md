<!-- PROVENANCE NOTE
Marker not installed on host CherryRd at time of this replication (2026-07-06).
No cached Marker parse of Frontiers DOI 10.3389/frqst.2023.1273581 (SHA
e4360ed9d9b62ea0df0035253b8d6dfff4c184bd92dc48a7b4b6527fbbca3fdd) was found
in the central corpus.
This file is a FALLBACK extraction via `pdftotext -layout paper.pdf` (poppler).
Structural fidelity for tables/math/figures is reduced vs a real Marker parse,
but paragraph text, references, and the numerical claims used for
replication are preserved and were used verbatim in report/REPORT.md.
-->

                                                                                                                         TYPE Original Research
                                                                                                                         PUBLISHED 09 October 2023
                                                                                                                         DOI 10.3389/frqst.2023.1273581




                                               PANSATZ: pulse-based ansatz for
OPEN ACCESS                                    variational quantum algorithms
EDITED BY
Daniel Claudino,
Oak Ridge National Laboratory (DOE),           Dekel Meirom 1* and Steven H. Frankel 2*
United States                                  1
                                                 Faculty of Electrical Engineering, Technion—Israel Institute of Technology, Haifa, Israel, 2Faculty of
REVIEWED BY                                    Mechanical Engineering, Technion—Israel Institute of Technology, Haifa, Israel
Zixuan Hu,
Purdue University, United States
Abolfazl Bayat,
University of Electronic Science and
Technology of China, China                     Quantum computers promise a great computational advantage over classical
*CORRESPONDENCE                                computers, which might help solve various computational challenges such as the
Dekel Meirom,                                  simulation of complicated quantum systems, ﬁnding optimum in large
  dekelmeirom@gmail.com
                                               optimization problems, and solving large-scale linear algebra problems.
Steven H. Frankel,
  frankel@technion.ac.il                       Current available quantum devices have only a limited amount of qubits and a
                                               high level of noise, limiting the size of problems that can be solved accurately with
RECEIVED 06 August 2023
ACCEPTED 26 September 2023                     those devices. Variational quantum algorithms (VQAs) have emerged as a leading
PUBLISHED 09 October 2023                      strategy to address these limitations by optimizing cost function based on
CITATION                                       measurement results of shallow depth circuits. Recently, various pulse
Meirom D and Frankel SH (2023),                engineering methods were suggested in order to improve VQA results,
PANSATZ: pulse-based ansatz for
variational quantum algorithms.
                                               including optimizing pulse parameters instead of gate angles as part of the
Front. Quantum Sci. Technol. 2:1273581.        VQA optimization process. In this paper, we suggest a novel pulse-based
doi: 10.3389/frqst.2023.1273581                ansatz, which is parameterized mainly by pulses’ duration of pre-deﬁned pulse
COPYRIGHT                                      structures. This ansatz structure provides relatively low amounts of optimization
© 2023 Meirom and Frankel. This is an          parameters while maintaining high expressibility, allowing fast convergence. In
open-access article distributed under the
terms of the Creative Commons
                                               addition, the ansatz has structured adaptivity to the entanglement level required
Attribution License (CC BY). The use,          by the problem, allowing low noise and accurate results. We tested this ansatz
distribution or reproduction in other          against quantum chemistry problems. Speciﬁcally, ﬁnding the ground-state
forums is permitted, provided the original
author(s) and the copyright owner(s) are
                                               energy associated with the electron conﬁguration problem, using the
credited and that the original publication     variational quantum eigensolver (VQE) algorithm for several different
in this journal is cited, in accordance with   molecules. We manage to achieve chemical accuracy both in simulation for
accepted academic practice. No use,
distribution or reproduction is permitted
                                               several molecules and on one of IBM’s NISQ devices for the H2 molecule in
which does not comply with these terms.        the STO-3G basis, without the need for extensive error mitigation. Our results are
                                               compared to a common gate-based ansatz and show better accuracy and
                                               signiﬁcant latency reduction—up to 7× shorter ansatz schedules.

                                               KEYWORDS

                                               NISQ, VQA, VQE, pulse engineering, QOC, ansatz


                                               1 Introduction
                                                   Today’s quantum computers (QCs) are often described as noisy intermediate-scale
                                               quantum (NISQ) computers due to the relatively low numbers of qubits available (e.g., 10’s
                                               to 100’s) and the relatively high levels of noise associated with them (e.g., decoherence and
                                               gate ﬁdelity errors) (Preskill, 2018; Córcoles et al., 2019; Bharti et al., 2022). These limitations
                                               result in circuits with short width and shallow depth.
                                                   To make use of these NISQ machines, a class of hybrid quantum-classical algorithms are
                                               being developed that seek to leverage the relative strengths of quantum and classical
                                               computers. The most common example of such algorithms are variational quantum
                                               algorithms (VQAs) (Cerezo et al., 2021). VQAs use a QC to prepare a short-depth
                                               parameterized quantum circuit (PQC) representing a trial solution or ansatz to the
                                               problem at hand. Measurements of a ﬁnal quantum state are used to calculate a cost



Frontiers in Quantum Science and Technology                            01                                                                  frontiersin.org
Meirom and Frankel                                                                                                                 10.3389/frqst.2023.1273581




function, which is then minimized on a classical computer to
estimate the problem solution. Prominent examples of VQAs
include the variational quantum eigensolver (VQE) for quantum
chemistry and materials applications (Peruzzo et al., 2014; Kandala
et al., 2017), quantum approximate optimization algorithm (QAOA)
for combinatorial optimization problems (Farhi et al., 2014), and
variational quantum linear solver (VQLS) for linear algebra
problems (Bravo-Prieto et al., 2019).
     One of the main challenges associated with effective VQA
implementations is related to the design of a suitable PQC/ansatz
that balances expressibility and noise, while avoiding exponentially
vanishing gradients of the cost function, referred to as the barren
plateau (BP) problem. The two main categories of ansatz that have
been considered include problem-inspired ansatz (PIA) and
hardware-efﬁcient ansatz (HEA) (Kandala et al., 2017). PIA
structure is primarily determined by the details of the problem
being solved. HEA structure is determined by the properties of the
target hardware. HEAs are designed to reduce PQC depth while
maintaining a general and expressive ansatz. There have been a
number of attempts (Tilly et al., 2022) to improve the gate-based                  FIGURE 1
                                                                                   Demonstrating redundancy in the control pulses in non-native
ansatz approach including ADAPT-VQE (Grimsley et al., 2019) and
                                                                                   gate decomposition. (A) Qubit trajectory on the Bloch sphere which
Noise-Adaptive Search (QuantumNAS) (Wang et al., 2022).                            represents the logic of Rx (4π ) directly. (B) Qubit trajectory on the Bloch
                                                                                                                                                 √
     Recently, the idea of combining quantum optimal control                       sphere of a decomposition of a Rx (4π) gate into Rz(θ) and x gates.
                                                                                                                                                      √
                                                                                   (C) The logical decomposition of Rx (4π ) gate into Rz(θ) and x gates.
(QOC), a method by which optimal pulses can be designed to
                                                                                   The colors match the colors of the relevant trajectory in (B).
improve qubit coherence and gate ﬁdelity, with VQA has been
proposed (Magann et al., 2021). A few recent studies have sought to
implement this and related ideas, proposing to bypass the PQC at
the gate level for a pulse-based state-preparation (Meitei et al., 2021;        has to be run on the hardware, which is usually referred to as the
Asthana et al., 2022), ansatz generation (Choquette et al., 2021;               process of calibration. Today’s QCs are noisy and unstable, which
Liang et al., 2022a), machine learning tasks (Liang et al., 2022c) and          leads to the requirement of repeating calibrations frequently to
better gate compilation using QOC techniques tailored for VQAs                  maintain high-ﬁdelity of the gate operations.
(Earnest et al., 2021; Ibrahim et al., 2022; Leng et al., 2022; Niu and             The complexity of the calibration process and the need to do it
Todri-Sanial, 2022). These studies suggest either using gates in a way          very frequently limits the QC designers to only a small number of
that resembles ideas from the QOC theory or optimizing the pulses’              gates that will be mapped into control pulses. This set of gates should
amplitudes and the driving frequencies of the qubits during the                 be universal (to allow universal computing) and is called the native
VQA optimization, which are the parameters that are commonly                    gate set. Each quantum gate that is not included in the native gate set
used in gate calibrations also outside the context of VQAs. In this             must be ﬁrst decomposed into a sequence of native gates in a process
paper, we propose an ansatz at the pulse level with pulse duration as           termed transpilation. In most cases, such decompositions are not
the main optimization parameter, along with the phase of the pulses             unique, and ﬁnding the optimal one is challenging. The process
which is manipulated with the phase of the classical control                    usually introduces redundancy and added latency in the qubits
hardware. This new ansatz offers a way to reduce the incoherent                 manipulation compared to the case where the original gate was
noise of the circuit by dynamically matching the total schedule                 part of the native gate set and had its own mapping to control pulses.
duration to the complexity of preparing the optimal state of the                An example of this type of redundancy is shown in Figure 1.
given problem. We show that our proposed ansatz can converge fast                   The structure of the HEA tries to minimize the depth of the gates
to an accurate result, thanks to its low amount of training                     in their decomposed format in order to lower the noise of execution.
parameters and high expressibility, achieved by parameterizing                  Each HEA layer usually consists of an entangling layer, built from
also the two-qubit interaction pulses.                                          native two-qubit gates, followed by a parameterized single-qubit gate
                                                                                layer featuring rotation angles as parameters. In addition, there is
                                                                                another initial layer of parameterized single-qubit gates. Henceforth,
2 Materials and methods                                                         we will refer to an ansatz built from gates a GANSATZ and use the
                                                                                Real Amplitudes Ansatz, which is commonly used in VQE
2.1 Gate-based ansatz                                                           problems, as a baseline for comparison to our new approach.

   Most of today’s quantum computing logic is represented using
quantum gates. The implementation of such quantum gates on                      2.2 Our approach: pulse-based ansatz
quantum hardware is done using control pulses. In order to map
between the desired logic of a quantum gate and a sequence of                      The structure of our proposed pulse-based ansatz, which we will
control pulses, a series of experiments that select the correct pulses          henceforth refer to as PANSATZ, is similar to the GANSATZ



Frontiers in Quantum Science and Technology                                02                                                                      frontiersin.org
Meirom and Frankel                                                                                                                      10.3389/frqst.2023.1273581




   FIGURE 2
   PANSATZ structure. The PANSATZ is built out from repeated L layers, each consisting of parameterized two qubit pulses ordered in two alternating
   layers according to the device connectivity, followed by virtual Rz gates and single qubit pulses on all qubits. The initial layer consists of ﬁxed single qubit
   pulses which rotate the control qubits of the next layer to the XY plane. The two qubit pulses have ﬂat-top Gaussian shape, and are coloured in light red,
   acting on the two qubits adjacent to the line it is drawn on. The single qubit pulses have DRAG shape, and are coloured in red (which represents the
   Gaussian part of the pulse) and blue (which represents the DRAG derivative part of the pulse).




structure, where each gate is replaced with a parameterized pulse,                    different quantum hardware, the choice of the parameters to
including the two-qubit gates, which are also parameterized as part                   optimize should be hardware dependent. In this paper, we will
of the PANSATZ. This structure consists of consecutive layers,                        focus on speciﬁc well-studied hardware technology, based on
where each layer is built from two-qubit pulses followed by                           superconducting circuits. Recently, research on pulse level control
single-qubit pulses. The two-qubit pulses are ordered in an                           on other technologies started to emerge, like the natural atoms
alternating layout of non-overlapping groups to maximize the                          technology (de Keijzer et al., 2023).
number of qubit pairs manipulated at once and reduce the
overall duration of each layer (as illustrated in Figure 2). As
opposed to the GANSATZ, calibration is not performed and the                          2.3 Superconducting qubit implementation
pulses are not mapped into a logical unitary. Therefore, the logical
unitary of the pulse sequences in the ideal case is unknown, and it is                     This study is focused on ﬁxed-frequency superconducting
not trivial to trace the evolution of the qubits state after each pulse.              qubits, primarily because of their availability on devices accessible
Similar to other HEAs, the PANSATZ strives to prepare a quantum                       via IBM cloud access. The driving Hamiltonian of each qubit for this
state while minimizing the incoherent noise associated with the                       hardware can be expressed in the rotating frame using the rotating
preparation process [as VQAs have some resilience to coherent                         wave approximation (RWA) as Krantz et al. (2019):
errors (McClean et al., 2016; O’Malley et al., 2016), our focus is only                                 Hc (t)  A(t)ei((ωq −ωd (t))t+ϕ(t)) a^
                                                                                                                                                        (1)
on incoherent errors]. By trading off knowledge about the unitary                                                +e−i((ωq −ωd (t))t+ϕ(t)) a^† 
evolution in the noiseless case, the PANSATZ can have lower
incoherent noise and better expressibility (with the same number                      where A(t), ωd(t), ϕ(t) are the time-dependent amplitude, frequency,
of layers) compared to the GANSATZ, as each part of the unitary                       and phase of the driving microwave, ωq is the frequency of the qubit
evolution can be parameterized, including the two-qubit gates. Each                   and a^† , a^ are the bosonic creation and annihilation operators.
pulse has many degrees of freedom which can be parameterized.                         Previous studies have proposed to parameterize and optimize
While keeping more degrees of freedom as parameters improves the                      most of the possible driving Hamiltonian’s time-dependent
expressibility of the PANSATZ, it might also create over-                             variables (Meitei et al., 2021; Liang et al., 2022a). In our study, in
parameterization and introduce trainability issues. Therefore,                        order to avoid trainability issues and minimize the number of
ﬁxing some of the degrees of freedom as hyper-parameters and                          parameters, we propose to keep a ﬁxed shape (the envelope of
limiting the optimization process of the algorithm to only a few                      the waveform) to the pulses with only a few parameters to optimize,
parameters for each pulse is crucial for the trainability of the ansatz.              while the rest are calibrated as hyper-parameters at the start of the
As the structure and properties of the control pulses vary between                    algorithm based on the given hardware.



Frontiers in Quantum Science and Technology                                      03                                                                    frontiersin.org
Meirom and Frankel                                                                                                         10.3389/frqst.2023.1273581




    Decoherence and dephasing are major sources of incoherent                  taken in the optimization process of these pulses. The effective two-
noise for this qubit architecture. Hence, the duration of a quantum            level system Hamiltonian describing the CR pulse can be
schedule dramatically affects the amount of noise in the                       approximated as the time-independent Hamiltonian (Alexander
computation. Therefore, pulse duration was chosen as the main                  et al., 2020)
optimization parameter (as illustrated in Figure 2). This enables
                                                                                          HCR  ωIX IX + ωIY IY + ωIZ IZ
exploration of the Hilbert space with the shortest possible schedule                                                                              (2)
                                                                                                +ωZI ZI + ωZX ZX + ωZY ZY + ωZZ ZZ
duration. The pulse envelope shape, driving frequency ωd(t),
amplitude and parameters associated with the chosen envelope                   where the dominant terms are the entangling term ZX and the
shape, were chosen at the beginning of the algorithm as                        single-qubit terms ZI and IX (Sheldon et al., 2016; Ware et al., 2019;
described below and kept ﬁxed throughout the VQA                               Magesan and Gambetta, 2020). The ZX term is crucial for creating
computation. The phase ϕ(t) of the driving pulse is another                    entanglement and is usually the only desired term of the CR pulse
optimization parameter, which is manipulated using virtual Rz                  when designing a CNOT gate, while the ZI and IX are usually
gates, allowing the addition of only one parameter per qubit per               referred as unwanted terms and have the largest coefﬁcients. In the
ansatz layer, instead of an added parameter for each pulse envelope.           PANSATZ case, there is no target unitary for the CR pulse, only a
    In our implementation, we choose derivative removal by                     search for the mapping between the parameters of the pulse and the
adiabatic gate (DRAG) (Motzoi et al., 2009; Gambetta et al.,                   cost function, therefore these terms are not considered coherent
2011) as the shape of the single-qubit pulses to minimize leakage              errors. However, in our numerical experiments, we observed that a
into higher energy levels of the device. The σ and δ parameters of the         relatively small change in a CR pulse duration caused a large change
DRAG pulse were taken from the calibrated X gate of the device and             in the cost function, mainly as a result of these heavy weighted
kept ﬁxed. We also use ﬂat-top Gaussian functions as the shape of              single-qubit terms. These frequent large changes in the cost function
the cross-resonance (CR) (Chow et al., 2011) pulses to enable                  harm the ﬂow of the classical optimizer and lead to problems with
smooth waveforms with maximum amplitude for most of the                        the convergence of the algorithm. Therefore, we changed the CR
pulse duration. The σ and the rise-fall ratio of the ﬂat-top                   pulses into an echo format (Córcoles et al., 2013; Sheldon et al.,
Gaussian are taken from the CR part of the CNOT gate of the                    2016), which has a DRAG-shaped ﬂip pulse (which needs to be
device and kept ﬁxed. The frequencies of the pulses were chosen as             calibrated a priori) on the control qubit between the two halves of a
the resonance frequency of the qubit they are controlling and the              CR ﬂat-top pulse. Such an echo cancels these single-qubit terms
amplitude was chosen in a quick calibration process to ﬁnd the                 while keeping the entangling term. This makes each entangling pulse
maximum amplitude for short pulses which creates negligible                    longer than it needs to be in the optimal case, but helps with the
leakage. Negative duration was allowed in order to account for                 training process. This issue might be resolved by creating a tailor-
unconstrained optimizers, while negative time was translated into              made optimizer, but this is beyond the scope of this research.
negative amplitude and the absolute value of the duration. Between
the layer of the CR pulses and the single qubit DRAG pulses, a layer
of Rz gates was added in order to enable changing the relative phase           2.5 Robustness of solution over time
of each qubit, as the phase in the DRAG pulse is ﬁxed. In
superconducting qubits technology, such gates can be                               There are some applications where using the pulse schedule of
implemented as virtual gates with zero duration (McKay et al.,                 the optimal solution in future experiments is required. Gate-based
2017), therefore they are perfect gates that do not inject any noise to        ansatzes produce approximately the same quantum state for the
the system. We chose to keep the initial layer of single qubit pulses          same parameters vector when executed at some future time, as long
ﬁxed with pulses that rotate some of the qubits to the XY plane of the         as the native gates set is calibrated frequently. As opposed to that,
Bloch sphere. The qubits that were chosen are those which will act as          pulse-based ansatzes might produce different results if there is a big
control qubits in the ﬁrst entangling layer (which will be every other         gap between executions, even when using the same parameters
qubit if we assume linear nearest-neighbor connectivity). This was             vector. This inconsistency happens because of drifts in the
done in order to create as much entanglement as possible from this             quantum chip parameters, such as the qubits frequencies. Over a
layer, as the creation of entanglement is usually the most                     long period of time, such drifts may accumulate and create
computationally time consuming. Although the structure of the                  deviations in a repeated execution of an optimized pulse-based
PANSATZ is ﬁxed, by allowing some of the pulse duration                        ansatz. The structure of PANSATZ produces pulse schedules
parameters to be zero, some of the pulses and even entire layers               with short pulse sequences, making the optimized result less
can be kept out of the schedule (as opposed to the HEA, where the              sensitive to such drifts. We injected such drifts into some of the
CNOT gates are not parameterized), adjusting the structure of the              optimal pulse schedules we got from the simulations we have done
ansatz during the optimization process, beneﬁting from an adaptive             (described in the next section). The drifts we simulated were in the
approach similar to ADAPT-VQE (Grimsley et al., 2019).                         form of random changes to the qubits frequencies and qubit driving
                                                                               strengths of the simulated device. The new parameters were sampled
                                                                               from a Gaussian distribution with a mean of the original parameter
2.4 Two qubit pulse implementation                                             and a standard deviation of 10−4, resulting in deviations in the order
                                                                               of a few hundred KHz. We simulated the optimal schedule multiple
    The two qubit pulses are usually the most important, as they can           times with the new parameters and examined the deviations from
create entanglement between the qubits, but also the most time-                the optimal result. In most cases, the deviations were smaller than
consuming and error-prone. Therefore, additional care should be                the standard deviation created by the shot noise of our simulations.



Frontiers in Quantum Science and Technology                               04                                                           frontiersin.org
Meirom and Frankel                                                                                                                     10.3389/frqst.2023.1273581




   FIGURE 3
   Simulations results. The top insets of each ﬁgure are representations of the molecular geometry, not drawn to scale. The error bars on the simulation
   data are smaller than the size of the markers. The reference on the FCI for each point is highlighted as blue tick marks. (A) Simulation results of the VQE on
   H2 molecule. (B) Simulation results of the VQE on HeH+ molecule. (C) Simulation results of the VQE on LiH molecule. (D) Deviation of the simulation result
   from the FCI result of the VQE on H2 molecule. (E) Deviation of the simulation result from the FCI result of the VQE on HeH+ molecule. (F) Deviation
   of the simulation result from the FCI result of the VQE on LiH molecule. The transformation error is the error introduced by reducing the number of qubits
   needed to encode the molecule’s Hamiltonian and effectively reducing the active search space.




For larger problems, the pulse schedule will probably be longer, and                 qubits needed in order to encode the solution to the problem.
therefore the deviations will be larger. In order to address those                   The H2 and the HeH+ Hamiltonians were represented using
cases, running a few additional iterations of the optimization process               2 qubits, while the LiH Hamiltonian was represented using
might be required in order to ﬁnd the new optimal parameters                         4 qubits, which was achieved by reducing the active search
vector that suits the new device characteristics.                                    space of the spin orbitals, as explained in Kandala et al.
                                                                                     (2017). Such reduction introduces an error, especially in small
                                                                                     atomic distances, but reduces the number of required qubits to
3 Results                                                                            encode the Hamiltonian signiﬁcantly, which allows reaching
                                                                                     better results. We compared our results to the full
    In order to test our method we implemented the standard                          conﬁguration interaction (FCI) result with respect to the
VQE algorithm but with our PANSATZ as the ansatz to ﬁnd the                          minimal STO-3G basis calculated by diagonalizing the
ground state energy of different molecules. We ﬁrst implemented                      Hamiltonian. In both the simulation and on the actual IBM
the algorithm as a simulation, using the Qiskit-dynamics                             device hardware we used 10,000 shots for each circuit run to
package (Puzzuoli et al., 2022), which utilizes the JAX array                        measure the expectation value with a small variance. In the run on
library to enable accelerated GPU execution, to ﬁnd the                              ibm_lagos we used tensored readout error mitigation (Barron
minimum energy of the H2, HeH+ and LiH molecules. Next,                              and Wood, 2020; Geller and Sun, 2021). For these tasks, we used
we implemented the algorithm on one of IBM’s devices, ibm_                           PANSATZ with only 1 layer, consisting of ﬁxed single-qubit
lagos, to ﬁnd the minimum energy of H2. All of the molecular                         pulses, followed by parametrized two-qubit pulses and
Hamiltonians used in this work were computed in the STO-3G                           parametrized single-qubit pulses (as described in the previous
basis using Qiskit-nature package. These Hamiltonians                                section). This structure generates 5 parameters for the H2 and
were converted into spin Hamiltonians using parity                                   HeH+ molecules (while GANSATZ has 4 parameters) and
transformation, and encoded into qubits after utilizing                              11 parameters for the LiH molecule (while GANSATZ has
symmetries in the Hamiltonian, to reduce the amount of                               8 parameters). As initial pulse parameters, we chose duration



Frontiers in Quantum Science and Technology                                     05                                                                   frontiersin.org
Meirom and Frankel                                                                                                                   10.3389/frqst.2023.1273581




                                                                                        simulation. For comparison we also ran a GANSATZ simulation
                                                                                        with 1 layer using the IBM simulator. We used the same device
                                                                                        parameters and connectivity and inserted relaxation and decoherence
                                                                                        noises of T1 = T2 = 100[us], and simulated shot noise by sampling the
                                                                                        results with 10,000 shots. In the gate model simulator leakage cannot
                                                                                        be simulated, so we assumed that there was no leakage. The duration
                                                                                        parameter can be seen either as a continuous parameter, or as a discrete
                                                                                        parameter, with the smallest time unit of the classical control hardware
                                                                                        of the quantum processing unit as the discrete unit (about 0.222[ns] for
                                                                                        most of today’s IBM QCs). Therefore, we tested two different
                                                                                        optimizers in the simulation—simultaneous perturbation stochastic
                                                                                        approximation (SPSA), which is used for continuous parameters and
                                                                                        approximates the gradient of the parameter vector using only
                                                                                        2 measurements regardless of size (Spall, 1992), and steepest-ascent
                                                                                        hill climbing (Goldfeld et al., 1966; Selman and Gomes, 2006), which is
   FIGURE 4
   Duration of the PANSATZ schedules compared to Real                                   used for discrete parameters. Both optimizers had similar accuracy,
   Amplitudes HEA for H2, HeH+ and LiH molecules, based on numerical                    while the steepest-ascent hill climbing converged with much fewer
   simulations. The duration of the GANSATZ is constant because the
   ansatz has the same number of gates for each atomic distance,
                                                                                        iterations. As shown in Figure 3, using PANSATZ we reached chemical
   and the duration of each gate is ﬁxed.                                               accuracy (0.0016 Hartree) compared to the FCI result, up to a standard
                                                                                        deviation (calculated from the variance in the expectation value
                                                                                        calculation), across all atomic distances studied for the H2 and
for the single qubit pulses so the ﬁnal state will be approximately                     HeH+ molecules. Because of the small number of parameters, this
the Hartree-Fock (HF) state. All the two-qubit pulses were                              was achieved with only a few tens of iterations in the worst case.
initialized with zero duration (as there is no entanglement at                          Throughout the optimization process of the parameters, the duration
the HF state). For example, the HF state for the H2 molecule is the                     of the schedule slowly increased as entanglement was added to the
|01〉 state, so all the parameters were initialized with zero                            prepared state by including also CR pulses (with non-zero duration) in
duration except the single qubit pulse of the ﬁrst qubit. This                          the schedule. For cases where more entanglement was needed in order
pulse was initialized with the same duration as the pulse in the                        to reach chemical accuracy, the total duration of the schedule increased
ﬁxed layer (which is calibrated to create π2 rotation around the                        even further, until the optimizer converged to the correct result. For
X-axis), resulting in a π rotation to the ﬁrst qubit, yielding the HF                   example, the entanglement of the ground state of the Hamiltonian of
state. We achieved good agreement between the simulation                                the H2 molecule after the parity transformation is higher for large
results and the results from ibm_lagos device (after readout                            atomic distances. Therefore, as entanglement is usually the most time
error mitigation).                                                                      consuming to create in superconducting qubits, the optimizer
                                                                                        converged at a longer schedule duration when solving these
                                                                                        problems, as can be seen in Figure 4. Even the longest duration
3.1 Simulation                                                                          schedule achieved by using PANSATZ is less than half the duration
                                                                                        of the equivalent GANSATZ. For the LiH molecule, 1 layer is not
     We simulated ﬁxed-frequency transmon qubits by using the                           expressive enough for large atomic distances (although it is more
following device Hamiltonian                                                            expressive than 1 layer of GANSATZ). Therefore, the optimizer
                                                                                        converged with low entanglement state, which encountered
             N
                             δk † †
       H  ωk a^†k a^k −     a^ a^ a^k a^k  +  ga^†k a^l + a^†l a^k    (3)        minimal noise due to the short duration and had better results
             k1
                             2 k k               <kl>                                   than having longer CR pulses. Because of the low noise, good
                                                                                        results were achieved in small atomic distances, but the algorithm
where ω is the qubit frequency, δ is the qubit anharmonicity, g is the
                                                                                        solutions deviate from the FCI as the atomic distance increases.
neighboring qubit coupling strength and a^†k , a^k are the bosonic
                                                                                             Figure 3 shows excellent agreement between the PANSATZ
creation and annihilation operators. For the simulation, we used
                                                                                        predictions of the ground state energy in Hartree units versus
the values reported by IBM on ibm_manila for these parameters.
                                                                                        interatomic distance in angstroms to the FCI result.
In order to make the Hilbert space ﬁnite, we truncated the energy
levels of the transmons at 3 levels to be able to take into account
leakage to the |2〉 level. We also simulated relaxation and
decoherence noise using the following dissipators:
                                                                                        3.2 Real hardware
                                    
                           D0  Γ0 · σ +                           (4)                      We used ibm_lagos, one of the IBM Quantum Falcon
                                     †     †                                          processors, to ﬁnd the ground energy of the H2 molecule at
                      D1  Γ1 · a^k a^k − a^k a^k                (5)
                                                                                        various atomic distances. We used the open-pulse feature
where σ+ is the Pauli ladder operator (σx + iσy). We used Γ0, Γ1 which                  (Alexander et al., 2020) to create the algorithm ansatz at the
are proportional to T1 = T2 = 100[us]. At the end of each calculation of                pulse level, and the PANSATZ structure described above. We
qubit evolution, we sampled the ﬁnal qubit state with 10,000 shots in                   used the steepest-ascent hill climbing algorithm for the classical
order to introduce shot noise caused by ﬁnite sampling to the                           optimizer, as it converged with fewer iterations in our simulations.



Frontiers in Quantum Science and Technology                                        06                                                             frontiersin.org
Meirom and Frankel                                                                                                               10.3389/frqst.2023.1273581




                                                                                       FIGURE 6
                                                                                       Duration of the PANSATZ schedules results from ibm_lagos
                                                                                       compared to GANSATZ. The GANSATZ duration was taken as the
                                                                                       duration of 1 layer of Real Amplitudes HEA transpiled on the same
                                                                                       device.




   FIGURE 5
   VQE results for H2 molecule on ibm_lagos device. (A) The ﬁnal                       FIGURE 7
   ground energy found by the algorithm with and without readout error                 Convergence plot of the steepest-ascent hill climbing
   mitigation. The error bars on the data are smaller than the size of the             optimization algorithm for solving VQE for H2 molecule with
   markers. The reference on the FCI for each point is highlighted as                  0.7 angstrom atomic distance, run on ibm_lagos.
   blue tick marks. (B) Deviation of the result from the FCI result with and
   without readout error mitigation.


                                                                                    state close to the HF state, the PANSATZ reached the desired
                                                                                    solution within only a few iterations (example shown in
We also used uncorrelated readout error mitigation in our post                      Figure 7), giving hope for convergence within a reasonable
processing of the hardware measurement results, which is a scaleable                amount of iterations also in larger problems.
method that can be used also when solving larger VQA problems.
The results are shown at Figure 5. The results were obtained in a
single convergence process, while convergence was declared by                       4 Summary and discussion
either reaching chemical accuracy or reaching 30 iterations. The
readout error mitigated results show excellent agreement with the                       We developed a parameterized pulse-based ansatz, which we call
FCI results, including multiple points which reached chemical                       PANSATZ, to be used with VQAs. We chose pulse duration as the
accuracy. These results were achieved as a direct result of the                     main parameter, along with qubit driving phase which is manipulated
short duration of the PANSATZ schedule, as shown in Figure 6,                       only once for each layer. We tested PANSATZ in the context of VQE
which was adaptive to the amount of entanglement needed for each                    to ﬁnd ground state energies of small molecules on both simulation
atomic distance. The GANSATZ duration was taken as the duration                     and actual IBM hardware. We achieved state of the art results,
of 1 layer of Real Amplitudes HEA compiled on the same device. By                   reaching chemical accuracy with the raw expectation value results
using a relatively small amount of parameters, a discrete                           (mitigating only readout errors), which, to the best of our knowledge,
optimization algorithm, and initial parameters which create a                       is an achievement that has not been shown yet on superconducting



Frontiers in Quantum Science and Technology                                    07                                                              frontiersin.org
Meirom and Frankel                                                                                                                                             10.3389/frqst.2023.1273581




quantum hardware. Previous demonstrations of chemical accuracy on                                    Funding
superconducting quantum hardware (McCaskey et al., 2019; Jones
et al., 2022) used extensive post-processing error mitigation                                            The author(s) declare ﬁnancial support was received for the
techniques such as zero noise extrapolation (ZNE) (Li and                                            research, authorship, and/or publication of this article. The authors
Benjamin, 2017; Temme et al., 2017), probabilistic error                                             gratefully acknowledge the ﬁnancial support of the Israel Science
cancellation (PEC) (Temme et al., 2017) and puriﬁcation                                              Foundation (ISF) on grant number 3457/21.
(McCaskey et al., 2019), which might be used also with PANSATZ
to make the results even more resilient to noise and help solve larger
problems within the required accuracy. Adjustment of such                                            Acknowledgments
mitigation techniques to make them suitable for pulses [for
example, using pulse stretching instead of digital global folding in                                     We would like to thank Dr. Adi Makmal for the fruitful technical
ZNE (Schultz et al., 2022)] is left for further research. Our experiments                            discussions. We also gratefully acknowledge the use of IBM
show signiﬁcant latency reduction, resulting in improved accuracy of                                 Quantum services for this work and to advanced services
PANSATZ over typical gate-based ansatzes. The PANSATZ structure                                      provided by the IBM Quantum Researchers Program.
enables on-the-ﬂy adaptation of the schedule latency depending on
the entanglement level required to solve the given problem, potentially
enabling simulations of larger molecules accurately. Our PANSATZ                                     Conﬂict of interest
approach can be used with other VQAs as an improvement to the
HEA. The use of PANSATZ in quantum algorithms where problem-                                             The authors declare that the research was conducted in the
inspired ansatze are used, such as QAOA, remains to be considered.                                   absence of any commercial or ﬁnancial relationships that could be
Using a hybrid gate-based and pulse-based ansatz can be explored                                     construed as a potential conﬂict of interest.
similarly to Liang et al. (2022b). Expanding PANSAZT into other
hardware technologies is left for future research.
                                                                                                     Publisher’s note
Data availability statement                                                                              All claims expressed in this article are solely those of the authors
                                                                                                     and do not necessarily represent those of their afﬁliated
    The datasets presented in this study can be found in online                                      organizations, or those of the publisher, the editors and the
repositories. The names of the repository/repositories and accession                                 reviewers. Any product that may be evaluated in this article, or
number(s) can be found below: https://github.com/dekelmeirom/                                        claim that may be made by its manufacturer, is not guaranteed or
PANSATZ.                                                                                             endorsed by the publisher.



Author contributions                                                                                 Author disclaimer
   DM: Writing–original draft. SF: Supervision, Writing–review                                           The views expressed are those of the authors, and do not reﬂect
and editing.                                                                                         the ofﬁcial policy or position of IBM or the IBM Quantum team.


References
  Alexander, T., Kanazawa, N., Egger, D. J., Capelluto, L., Wood, C. J., Javadi-Abhari,                 Chow, J. M., Córcoles, A. D., Gambetta, J. M., Rigetti, C., Johnson, B. R., Smolin, J. A.,
A., et al. (2020). Qiskit pulse: programming quantum computers through the cloud with                et al. (2011). Simple all-microwave entangling gate for ﬁxed-frequency superconducting
pulses. Quantum Sci. Technol. 5, 044006. doi:10.1088/2058-9565/aba404                                qubits. Phys. Rev. Lett. 107, 080502. doi:10.1103/PhysRevLett.107.080502
  Asthana, A., Liu, C., Meitei, O. R., Economou, S. E., Barnes, E., and Mayhall, N. J.                 Córcoles, A. D., Gambetta, J. M., Chow, J. M., Smolin, J. A., Ware, M., Strand, J., et al.
(2022). Minimizing state preparation times in pulse-level variational molecular                      (2013). Process veriﬁcation of two-qubit quantum gates by randomized benchmarking.
simulations, 06818. arXiv preprint arXiv:2203. doi:10.48550/arXiv.2203.06818                         Phys. Rev. A 87, 030301. doi:10.1103/PhysRevA.87.030301
  Barron, G. S., and Wood, C. J. (2020). Measurement error mitigation for variational                  Córcoles, A. D., Kandala, A., Javadi-Abhari, A., McClure, D. T., Cross, A. W., Temme,
quantum algorithms. arXiv preprint arXiv:2010, 08520. doi:10.48550/arXiv.2010.08520                  K., et al. (2019). Challenges and opportunities of near-term quantum computing systems,
                                                                                                     02894. arXiv preprint arXiv:1910. doi:10.1109/JPROC.2019.2954005
  Bharti, K., Cervera-Lierta, A., Kyaw, T. H., Haug, T., Alperin-Lea, S., Anand, A., et al.
(2022). Noisy intermediate-scale quantum algorithms. Rev. Mod. Phys. 94, 015004.                       de Keijzer, R., Tse, O., and Kokkelmans, S. (2023). Pulse based variational quantum
doi:10.1103/RevModPhys.94.015004                                                                     optimal control for hybrid quantum computing. Quantum 7, 908. doi:10.22331/q-2023-
                                                                                                     01-26-908
  Bravo-Prieto, C., LaRose, R., Cerezo, M., Subasi, Y., Cincio, L., and Coles, P. J. (2019).
Variational quantum linear solver. arXiv preprint arXiv:1909, 05820. doi:10.48550/                     Earnest, N., Tornow, C., and Egger, D. J. (2021). Pulse-efﬁcient circuit transpilation
arXiv.1909.05820                                                                                     for quantum applications on cross-resonance-based hardware. Phys. Rev. Res. 3, 043088.
                                                                                                     doi:10.1103/PhysRevResearch.3.043088
  Cerezo, M., Arrasmith, A., Babbush, R., Benjamin, S. C., Endo, S., Fujii, K., et al.
(2021). Variational quantum algorithms. Nat. Rev. Phys. 3, 625–644. doi:10.1038/                       Farhi, E., Goldstone, J., and Gutmann, S. (2014). A quantum approximate
s42254-021-00348-9                                                                                   optimization algorithm. arXiv preprint arXiv:1411.4028. doi:10.48550/arXiv.1411.4028
  Choquette, A., Di Paolo, A., Barkoutsos, P. K., Sénéchal, D., Tavernelli, I., and Blais, A.          Gambetta, J. M., Motzoi, F., Merkel, S., and Wilhelm, F. K. (2011). Analytic control
(2021). Quantum-optimal-control-inspired ansatz for variational quantum algorithms.                  methods for high-ﬁdelity unitary operations in a weakly nonlinear oscillator. Phys. Rev.
Phys. Rev. Res. 3, 023092. doi:10.1103/PhysRevResearch.3.023092                                      A 83, 012308. doi:10.1103/PhysRevA.83.012308




Frontiers in Quantum Science and Technology                                                     08                                                                              frontiersin.org
Meirom and Frankel                                                                                                                                                10.3389/frqst.2023.1273581




  Geller, M. R., and Sun, M. (2021). Toward efﬁcient correction of multiqubit                            McKay, D. C., Wood, C. J., Sheldon, S., Chow, J. M., and Gambetta, J. M. (2017).
measurement errors: pair correlation method. Quantum Sci. Technol. 6, 025009.                          Efﬁcient z gates for quantum computing. Phys. Rev. A 96, 022330. doi:10.1103/
doi:10.1088/2058-9565/abd5c9                                                                           PhysRevA.96.022330
  Goldfeld, S. M., Quandt, R. E., and Trotter, H. F. (1966). Maximization by quadratic                   Meitei, O. R., Gard, B. T., Barron, G. S., Pappas, D. P., Economou, S. E., Barnes, E.,
hill-climbing. Econ. J. Econ. Soc. 34, 541–551. doi:10.2307/1909768                                    et al. (2021). Gate-free state preparation for fast variational quantum eigensolver
                                                                                                       simulations. npj Quantum Inf. 7, 155–211. doi:10.1038/s41534-021-00493-0
  Grimsley, H. R., Economou, S. E., Barnes, E., and Mayhall, N. J. (2019). An adaptive
variational algorithm for exact molecular simulations on a quantum computer. Nat.                        Motzoi, F., Gambetta, J. M., Rebentrost, P., and Wilhelm, F. K. (2009). Simple pulses
Commun. 10, 3007–3009. doi:10.1038/s41467-019-10988-2                                                  for elimination of leakage in weakly nonlinear qubits. Phys. Rev. Lett. 103, 110501.
                                                                                                       doi:10.1103/PhysRevLett.103.110501
  Ibrahim, M. M., Mohammadbagherpoor, H., Rios, C., Bronn, N. T., and Byrd, G. T.
(2022). Evaluation of parameterized quantum circuits with cross-resonance pulse-                         Niu, S., and Todri-Sanial, A. (2022). Effects of dynamical decoupling and pulse-level
driven entanglers. IEEE Trans. Quantum Eng. 3, 1–13. doi:10.1109/TQE.2022.3231124                      optimizations on ibm quantum computers. IEEE Trans. Quantum Eng. 3, 1–10. doi:10.
                                                                                                       1109/TQE.2022.3203153
  Jones, M. A., Vallury, H. J., Hill, C. D., and Hollenberg, L. C. (2022). Chemistry
beyond the Hartree–Fock energy via quantum computed moments. Sci. Rep. 12, 8985.                          O’Malley, P. J., Babbush, R., Kivlichan, I. D., Romero, J., McClean, J. R., Barends, R.,
doi:10.1038/s41598-022-12324-z                                                                         et al. (2016). Scalable quantum simulation of molecular energies. Phys. Rev. X 6, 031007.
                                                                                                       doi:10.1103/PhysRevX.6.031007
  Kandala, A., Mezzacapo, A., Temme, K., Takita, M., Brink, M., Chow, J. M., et al.
(2017). Hardware-efﬁcient variational quantum eigensolver for small molecules and                        Peruzzo, A., McClean, J., Shadbolt, P., Yung, M.-H., Zhou, X.-Q., Love, P. J., et al.
quantum magnets. Nature 549, 242–246. doi:10.1038/nature23879                                          (2014). A variational eigenvalue solver on a photonic quantum processor. Nat.
                                                                                                       Commun. 5, 4213–4217. doi:10.1038/ncomms5213
  Krantz, P., Kjaergaard, M., Yan, F., Orlando, T. P., Gustavsson, S., and Oliver, W. D.
(2019). A quantum engineer’s guide to superconducting qubits. Appl. Phys. Rev. 6,                        Preskill, J. (2018). Quantum computing in the nisq era and beyond. Quantum 2, 79.
021318. doi:10.1063/1.5089550                                                                          doi:10.22331/q-2018-08-06-79
  Leng, J., Peng, Y., Qiao, Y.-L., Lin, M., and Wu, X. (2022). Differentiable analog                     Puzzuoli, D., Lin, S. F., Malekakhlagh, M., Pritchett, E., Rosand, B., and Wood, C. J.
quantum computing for optimization and control, 15812. arXiv preprint arXiv:2210.                      (2022). Algorithms for perturbative analysis and simulation of quantum dynamics,
doi:10.48550/arXiv.2210.15812                                                                          11595. arXiv preprint arXiv:2210. doi:10.48550/arXiv.2210.11595
  Li, Y., and Benjamin, S. C. (2017). Efﬁcient variational quantum simulator                             Schultz, K., LaRose, R., Mari, A., Quiroz, G., Shammah, N., Clader, B. D., et al. (2022).
incorporating active error minimization. Phys. Rev. X 7, 021050. doi:10.1103/                          Impact of time-correlated noise on zero-noise extrapolation. Phys. Rev. A 106, 052406.
PhysRevX.7.021050                                                                                      doi:10.1103/PhysRevA.106.052406
  Liang, Z., Cheng, J., Ren, H., Wang, H., Hua, F., Ding, Y., et al. (2022a). Pan: pulse ansatz          Selman, B., and Gomes, C. P. (2006). Hill-climbing search. Encycl. cognitive Sci. 81, 82.
on nisq machines, 01215. arXiv preprint arXiv:2208. doi:10.48550/arXiv.2208.01215                      doi:10.1002/0470018860.s00015
  Liang, Z., Song, Z., Cheng, J., He, Z., Liu, J., Wang, H., et al. (2022b). Hybrid gate-pulse           Sheldon, S., Magesan, E., Chow, J. M., and Gambetta, J. M. (2016). Procedure for
model for variational quantum algorithms, 00661. arXiv preprint arXiv:2212. doi:10.                    systematically tuning up cross-talk in the cross-resonance gate. Phys. Rev. A 93, 060302.
48550/arXiv.2212.00661                                                                                 doi:10.1103/PhysRevA.93.060302
  Liang, Z., Wang, H., Cheng, J., Ding, Y., Ren, H., Gao, Z., et al. (2022c). “Variational               Spall, J. C. (1992). Multivariate stochastic approximation using a simultaneous
quantum pulse learning,” in 2022 IEEE International Conference on Quantum Computing                    perturbation gradient approximation. IEEE Trans. automatic control 37, 332–341.
and Engineering (QCE) (IEEE), 556–565. doi:10.1109/QCE53715.2022.00078                                 doi:10.1109/9.119632
  Magann, A. B., Arenz, C., Grace, M. D., Ho, T.-S., Kosut, R. L., McClean, J. R., et al.                Temme, K., Bravyi, S., and Gambetta, J. M. (2017). Error mitigation for short-depth
(2021). From pulses to circuits and back again: A quantum optimal control perspective                  quantum circuits. Phys. Rev. Lett. 119, 180509. doi:10.1103/PhysRevLett.119.180509
on variational quantum algorithms. PRX Quantum 2, 010101. doi:10.1103/
                                                                                                         Tilly, J., Chen, H., Cao, S., Picozzi, D., Setia, K., Li, Y., et al. (2022). The variational
PRXQuantum.2.010101
                                                                                                       quantum eigensolver: A review of methods and best practices. Phys. Rep. 986, 1–128.
  Magesan, E., and Gambetta, J. M. (2020). Effective Hamiltonian models of the cross-                  doi:10.1016/j.physrep.2022.08.003
resonance gate. Phys. Rev. A 101, 052308. doi:10.1103/PhysRevA.101.052308
                                                                                                         Wang, H., Ding, Y., Gu, J., Lin, Y., Pan, D. Z., Chong, F. T., et al. (2022). “Quantumnas:
  McCaskey, A. J., Parks, Z. P., Jakowski, J., Moore, S. V., Morris, T. D., Humble, T. S.,             noise-adaptive search for robust quantum circuits,” in 2022 IEEE International
et al. (2019). Quantum chemistry as a benchmark for near-term quantum computers.                       Symposium on High-Performance Computer Architecture (HPCA), Seoul, Korea,
npj Quantum Inf. 5, 99. doi:10.1038/s41534-019-0209-0                                                  Republic, 02-06 April 2022 (IEEE), 692–708. doi:10.1109/HPCA53966.2022.00057
  McClean, J. R., Romero, J., Babbush, R., and Aspuru-Guzik, A. (2016). The theory of                    Ware, M., Johnson, B. R., Gambetta, J. M., Ohki, T. A., Chow, J. M., and Plourde, B.
variational hybrid quantum-classical algorithms. New J. Phys. 18, 023023. doi:10.1088/                 (2019). Cross-resonance interactions between superconducting qubits with variable
1367-2630/18/2/023023                                                                                  detuning, 11480. arXiv preprint arXiv:1905. doi:10.48550/arXiv.1905.11480




Frontiers in Quantum Science and Technology                                                       09                                                                               frontiersin.org

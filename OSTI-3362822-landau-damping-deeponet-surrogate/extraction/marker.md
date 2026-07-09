![](_page_0_Picture_3.jpeg)

# **Surrogate Modeling of Landau Damping with Deep Operator Networks**

Simin Shekarpa[zaa](https://orcid.org/0009-0000-0502-5264), Chuanfei Dong[aa](https://orcid.org/0000-0002-8990-094X), and Ziyu Huan[gaa](https://orcid.org/0000-0002-8624-1264) Center for Space Physics and Department of Astronomy, Boston University, Boston, MA 02215, USA; [siminsh@bu.edu](mailto:siminsh@bu.edu), [dcfy@bu.edu](mailto:dcfy@bu.edu) *Received 2025 May 31; revised 2025 July 21; accepted 2025 July 22; published 2025 September 4*

## **Abstract**

Kinetic simulations excel at capturing microscale plasma physics phenomena with high accuracy, but their computational demands make them impractical for modeling large-scale space and astrophysical systems. In this context, we build a surrogate model, using Deep Operator Networks (DeepONets), based upon the Vlasov– Poisson simulation data to model the dynamical evolution of plasmas, focusing on the Landau damping process a fundamental kinetic phenomenon in space and astrophysical plasmas. The trained DeepONets are able to capture the evolution of electric field energy in both linear and nonlinear regimes under various conditions. Extensive validation highlights DeepONets' robust performance in reproducing complex plasma behaviors with high accuracy, paving the way for large-scale modeling of space and astrophysical plasmas.

*Unified Astronomy Thesaurus concepts:* Plasma [physics](http://astrothesaurus.org/uat/2089) (2089); Plasma [astrophysics](http://astrothesaurus.org/uat/1261) (1261); [Space](http://astrothesaurus.org/uat/1544) [plasmas](http://astrothesaurus.org/uat/1544) (1544)

## **1. Introduction**

In space and astrophysical plasmas, most physical processes are collisionless. Generally, simulating these collisionless processes demands kinetic approaches, such as the particle-incell (PIC) or Vlasov methods. However, these kinetic simulations are computationally demanding and therefore not well suited for efficiently addressing large-scale problems that involve collisionless physics. To manage this challenge with affordable computational costs, two main approaches have been developed for large-scale global simulations: the magnetohydrodynamics with embedded particle-in-cell (MHD-EPIC) model (L. K. S. Daldorff et al. [2014](#page-7-0); G. Tóth et al. [2016](#page-7-0); Y. Chen et al. [2017](#page-7-0); H. Zhou et al. [2020](#page-7-0)) and the multimoment multifluid model (L. Wang et al. [2015,](#page-7-0) [2018,](#page-7-0) [2020](#page-7-0); C. Dong et al. [2019;](#page-7-0) S. Jarmak et al. [2020](#page-7-0); E. Rulke et al. [2021](#page-7-0)). Recently, the MHD-EPIC model has evolved to include adaptively EPIC regions (X. Wang et al. [2022;](#page-7-0) Y. Chen et al. [2023](#page-7-0); D. Li et al. [2023](#page-7-0)), enabling flexibility to capture localized regions where kinetic effects are significant. On the other hand, substantial efforts have been dedicated to integrating kinetic effects into the multimoment multifluid model through machine learning techniques (C. Ma et al. [2020](#page-7-0); E. P. Alves & F. Fiuza [2022;](#page-7-0) W. Cheng et al. [2023](#page-7-0); J. Donaghy & K. Germaschewski [2023;](#page-7-0) Y. Qin et al. [2023](#page-7-0); Z. Huang et al. [2025](#page-7-0); E. R. Ingelsten et al. [2025](#page-7-0)).

The rapid evolution of neural network architectures has positioned machine learning as a promising approach for scientific discovery in partial differential equations (PDEs) and the development of surrogate models (C. Ma et al. [2020](#page-7-0); K. Parand et al. [2020](#page-7-0); B. Laperre et al. [2022;](#page-7-0) W. Cheng et al. [2023](#page-7-0); Z. Hajimohammadi et al. [2023](#page-7-0); A. S. Joglekar & A. G. R. Thomas [2023](#page-7-0); Y. Qin et al. [2023](#page-7-0); M. Razzaghi et al. [2023](#page-7-0); S. Wei et al. [2023;](#page-7-0) K. Shukla et al. [2025](#page-7-0)). Early efforts, such as those by C. Ma et al. ([2020](#page-7-0)), employed surrogate models for Hammett–Perkins closure (G. W. Hammett & F. W. Perkins [1990](#page-7-0)) using various architectures, including multilayer

Original content from this work may be used under the terms of the Creative Commons [Attribution](https://creativecommons.org/licenses/by/4.0/) 4.0 licence. Any further distribution of this work must maintain attribution to the author(s) and the title of the work, journal citation and DOI.

perceptrons, convolutional neural networks (CNNs), and discrete Fourier transform networks. M. Raissi et al. ([2019](#page-7-0)) introduced physics-informed neural networks (PINNs), which combine neural network approximation with physics-based constraints to learn solutions to differential equations directly from data. PINNs have demonstrated success in solving of ordinary and PDEs, including fractional equations (G. Pang et al. [2019](#page-7-0)), stochastic PDEs (D. Zhang et al. [2020](#page-7-0)), systems of differential equations (S. Shekarpaz et al. [2024](#page-7-0)), and inverse problems (X. Meng & G. Karniadakis [2020](#page-7-0)), without requiring explicit discretization. To further improve the robustness and accuracy of PINNs in solving high-dimensional nonlinear problems, S. Shekarpaz et al. ([2022](#page-7-0)) proposed a physicsinformed adversarial training framework. Adversarial training has been shown to be effective in achieving robustness against the specific perturbations used during training (M. Azizmalayeri & M. H. Rohban [2023](#page-7-0)). It is worth mentioning that Y. Qin et al. ([2023](#page-7-0)) utilized PINNs to construct a multimoment fluid model with an implicit fluid closure and applied it to study the Landau damping process focusing on the linear damping case.

Recently, operator learning—a deep learning framework that approximates linear and nonlinear differential operators by taking parametric functions (infinite-dimensional objects) as input and mapping them to complete solution fields—becomes a hot topic, among which, Fourier Neural Operator (Z. Li et al. [2020](#page-7-0)) and Deep Operator Networks (DeepONets; L. Lu et al. [2021](#page-7-0)) are probably the two most popular ones. In this study, we will use the latter. While traditional numerical methods often rely on discretization and operator splitting (e.g., K. Parand et al. [2019;](#page-7-0) S. Shekarpaz & H. Azari [2020](#page-7-0)), DeepONets utilize neural networks to directly approximate solutions of high-dimensional differential equations. This eliminates the need for explicit discretization or operator splitting, providing a scalable and efficient alternative to conventional numerical approaches. Notably, DeepONets enable accurate modeling of complex physical systems with strong generalization capabilities, which is an advantage over both traditional numerical solvers and other neural networkbased approaches such as PINNs and standard artificial neural networks. DeepONets have demonstrated promising performance across a wide range of applications, including weather

![](_page_1_Figure_2.jpeg)

**Figure 1.** The DeepONets architecture consists of two fully connected neural networks: the branch network, which encodes temperature values, T, and the trunk network, which encodes the coordinates (here the coordinates are time, t). The outputs of these networks are combined to approximate the electric field energy,  $\int |E_x|^2 dx$ . The final output is  $G_{\omega}(T)(t)$ , where  $\omega$  represents the model's learned weights and T is a vector as  $\{T_i\}_{i=1}^N$ .

forecasting (T. Kurth et al. 2023), multiphysics and multiscale modeling (S. Cai et al. 2021), disk-planet interactions in protoplanetary systems (S. Mao et al. 2023), and optimization (I. Sahin et al. 2024).

In this paper, we aim to build a surrogate model using DeepONets based upon the Vlasov–Poisson simulation data to model the dynamical evolution of plasmas, focusing on the Landau damping process—a fundamental kinetic phenomenon in space and astrophysical plasmas. The trained DeepONets are able to capture the evolution of electric field energy in both linear and nonlinear regimes under various conditions. It is noteworthy that Y. Qin et al. (2023) focused exclusively on linear Landau damping using PINNs, as the damping trend in this regime is monotonic and no electron phase-space holes are observed (see their Figure 3).

This paper is structured as follows: Section 2 introduces DeepONets. In Section 3, we describe the physical model and the data set generation. Section 4 focuses on demonstrating the accuracy and robustness of DeepONets by applying them for the Landau damping problem under two different scenarios. Section 5 gives the conclusion.

## 2. Methodology

DeepONets: The foundation of DeepONets is based on the universal approximation theorem (K. Hornik et al. 1989), which guarantees that neural networks can approximate any continuous function with arbitrary accuracy. DeepONets are designed to learn mappings between function spaces, making them useful in the context of PDEs.

As a reference, consider the parametric PDEs of the form

$$\mathcal{N}(T,\,\mathcal{E}) = 0,\tag{1}$$

where  $\mathcal{N}$  can be a linear or nonlinear differential operator, T denotes the parametric input, and  $\mathcal{E}$  is the corresponding functional output. DeepONets can be used to capture the relationship between T and  $\mathcal{E}$ , represented as

$$\mathcal{E} = G_{\omega}(T)(t) \approx \sum_{k=1}^{p} b_k(T(\eta_1), T(\eta_2), \dots, T(\eta_m)) \tau_k(t),$$

where t denotes the collocation points,  $\omega$  represents the network parameters, and  $b_k$  and  $\tau_k$  are the outputs of branch and trunk networks, as shown in Figure 1. The function

T evaluated at fixed sensors  $\{\eta_i\}_{i=1}^m$  will be used as the input of the branch network. For the Landau damping problem,  $G_{\omega}$  maps a set of temperature values, T, to the electric field energy,  $G_{\omega}(T)(t)$ , at different time steps, t.

For different kinds of problems, the branch and trunk networks can be residual network, CNN, recurrent neural network, or feed forward neural network. In high-dimensional problems, where t is a vector with d components, the dimension of t no longer matches the dimension of  $T(\eta_i)$  for i=1,2,...,m, and at least two subnetworks are necessary to handle  $[T(\eta_1),T(\eta_2),...,T(\eta_m)]^T$  and t separately. Furthermore, depending on the number and characteristics of input functions, one can incorporate multiple branch networks instead of one (L. Lu et al. 2021).

#### 3. Implementation

### 3.1. Physical Model for Data Generation

For collisionless electrostatic plasmas, their kinetic behavior can be well described by the Vlasov–Poisson equations. The Vlasov equation describes the evolution of the plasma distribution function in phase space:

$$\frac{\partial f_s}{\partial t} + \mathbf{v}_s \cdot \nabla_r f_s + \left(\frac{e_s}{m_s}\right) \mathbf{E} \cdot \nabla_v f_s = 0, \tag{2}$$

where  $f_s(x, \mathbf{v_s}, t)$  is the velocity distribution function and  $\frac{e_s}{m_s}$  is the charge-to-mass ratio of the species, s. Meanwhile, the Poisson equation governs the electrostatic potential generated by charge distributions in a plasma:

$$E_{x}(x,t) = -\nabla \phi, \tag{3}$$

$$\Delta \phi = -\frac{\rho}{\varepsilon_0},\tag{4}$$

where  $\phi(x, t)$  is the electrostatic potential and  $\varepsilon_0$  is the vacuum permittivity.  $\rho(x, t) = \sum_s e_s n_s$  is the charge density, where  $e_s$  is the charge and

$$n_s(x, t) = \int f_s(x, v_s, t) dv_s$$
 (5)

is number density of the particle species, s.

Solving the Vlasov–Poisson equations using traditional numerical methods is computationally expensive due to the high dimensionality and fine resolution required. Although multimoment fluid models offer a more efficient alternative, they fail to capture certain kinetic plasma behaviors. In contrast, machine learning–based surrogate models provide a promising compromise by significantly reducing computational cost while maintaining the accuracy necessary to model key kinetic phenomena, including nonlinear effects.

In the present work, we use DeepONets to predict the dynamical evolution of electric field energy and thus the rate of Landau damping:

$$\mathcal{E}(t) = \int |E_x(x, t)|^2 dx. \tag{6}$$

### 3.2. Data for Training and Testing

The reference solutions are obtained by using the open-source continuum Vlasov code Gkeyll (J. Juno et al. 2018). The simulation configuration is established with a fixed background of ions serving as a neutralizing background.

<span id="page-2-0"></span>![](_page_2_Figure_2.jpeg)

Figure 2. The dispersion relation, i.e., the real and imaginary frequencies vs. wavenumber, of the least damped mode in a uniform, electrostatic plasma with immobile ion background and temperature T=1. The blue dot identifies the wavenumber k=0.35 used for our single-mode case. The frequencies and wavenumbers are normalized over electron plasma frequency,  $\omega_{pe}$ , and electron Debye length,  $\lambda_e$ , respectively.

Initially, perturbations are applied to the electron density to initiate the dynamical evolution of the system. The number densities of ions and electrons are described as follows:

$$n_i(x) \equiv n_0, \tag{7}$$

$$n_e(x, t = 0) = n_0(1 + \sum_i A_i \cos(k_i x)),$$
 (8)

where  $n_0$  is the initial uniform number density of ions and electrons without perturbation.  $A_i$  and  $k_i$  are the amplitude and wavenumber of each perturbed mode, respectively. The dispersion relation of the least damped mode in a uniform, electrostatic plasma with immobile ion background and temperature T = 1 is shown in Figure 2, where the left and right panels depict the oscillatory (real) frequency,  $\omega_R$ , and damping rate ( $\gamma$ ; negative growth rate), respectively, versus the wavenumber, k. Normalized values are used for simplicity. As can be clearly seen, in the long wavelength limit  $(k \ll \lambda_e^{-1})$ , there is little damping. As the wavenumber grows past about  $k \sim 0.2 \lambda_e^{-1}$ , the damping rate increases rapidly, indicating that short-wavelength modes are damped more quickly. For our study, in the single-mode case, we use k = 0.35 (and a small perturbation A = 0.05), as marked by the blue dot in the right panel of Figure 2. This serves as a convenient baseline case where the damping is substantial but not too aggressive. For the five-mode case, several wavenumbers  $k_i$  are chosen around this baseline value to include modes with relatively comparable damping rates to allow meaningful competition between each other. The  $k_i$ values and the corresponding perturbation magnitudes,  $A_i$ , are described in Table 1.

## 4. Results and Discussion

In this section, we demonstrate the capability of DeepONets for two different cases. By using DeepONets, the inputs of the branch net are temperature values that are randomly chosen in the range [0.5, 1.5], and the inputs of the trunk net are equidistant points  $t^j = j\Delta t$  ( $j = 0, 1, \cdots, J$ ) with a step size of  $\Delta t$ . The output of the network is the electric field energy. During the training phase, the model is optimized by minimizing the loss function to determine the weights. In the testing phase, the trained model is applied to unseen data to assess its accuracy and generalization capability. The network

 Table 1

 Wavenumber and Perturbation Amplitude of Each Mode

| $\overline{n}$ | $k\lambda_e$ | $A_n$ |
|----------------|--------------|-------|
| 1              | 0.4          | 0.1   |
| 2              | 0.35         | 0.05  |
| 3              | 0.25         | 0.025 |
| 4              | 0.5          | 0.25  |
| 5              | 0.7          | 0.5   |

architecture and hyperparameters have been specified in Table 2, and the optimization algorithm employed is the Adaptive Moment Estimation (Adam) method, with an exponential learning rate decay starting at 0.001.

#### 4.1. Single-mode Case

We first consider the initial condition consisting of a single mode with k=0.35 and A=0.05, and the network is trained on  $t\in[0,20\omega_{\rm pe}^{-1}]$  with a step size of  $\Delta t=0.002\omega_{\rm pe}^{-1}$ .

Figure 3 compares the results obtained from DeepONets with the reference solutions generated by the Gkeyll Vlasov model for various previously unseen test samples. Figure 3 shows that DeepONets are capable of accurately capturing the dynamical evolution of the system, as the predicted solutions match with the reference solutions.

The accuracy of the algorithm is assessed using the relative  $L^2$  error norm, calculated as follows:

relative 
$$L^2$$
 error = 
$$\frac{\sqrt{\sum_{j=1}^{J} (\mathcal{E}(t^j) - G_{\omega}(T)(t^j))^2}}{\sqrt{\sum_{j=1}^{J} (\mathcal{E}(t^j))^2}}.$$
 (9)

Table 3 summarizes the error norm statistics for the single-mode case, including the mean, minimum, maximum, and standard deviation of the errors. The results indicate that DeepONets perform well, achieving a mean error norm of 0.0078 for training and 0.0083 for testing. Additionally, the small standard deviations (0.00215 for training and 0.00220 for testing) demonstrate the model's consistency in both phases. These results highlight DeepONets' stability, accuracy, and uniform performance across different data samples,

<span id="page-3-0"></span>![](_page_3_Figure_2.jpeg)

Figure 3. Single-mode case: comparison of DeepONets predictions with reference solutions obtained from the Gkeyll Vlasov model for a range of temperature values (T). The vertical axis shows the electric field energy,  $\int |E_x|^2 dx$ , on a logarithmic scale, and the horizontal axis represents time in  $\omega_{\rm pe}^{-1}$ .

 ${\bf Table~2}\\ {\bf DeepONets~Architectures~and~Hyperparameters~Used~for~Training~and~Testing}$ 

| Problems    | Number of<br>Training Samples | Number of<br>Test Samples | Depth | Width | Activation<br>Function | Optimizer | Iterations      |
|-------------|-------------------------------|---------------------------|-------|-------|------------------------|-----------|-----------------|
| Single mode | 200                           | 50                        | 6     | 200   | tanh                   | Adam      | 10 <sup>6</sup> |
| Five modes  | 400                           | 100                       | 6     | 200   | tanh                   | Adam      | $10^{6}$        |

Table 3 Statistics of Relative  $L^2$  Errors for the Single-mode Case

|                | Mean   | Min    | Max    | std. dev. |
|----------------|--------|--------|--------|-----------|
| Training error | 0.0078 | 0.0049 | 0.0248 | 0.00215   |
| Test error     | 0.0083 | 0.0054 | 0.0160 | 0.00220   |

which indicates that DeepONets produce reliable results with minimal fluctuation in errors.

The convergence of loss functions is depicted in Figure 4. The loss functions decrease continuously, indicating that the DeepONets surrogate model is learning effectively and converging to a solution that minimizes the error.

The loss function used is the mean square error, which is defined as follows:

$$MSE = \frac{1}{N} \sum_{i=1}^{N} \sum_{j=1}^{J} (\mathcal{E}_i(t^j) - G_\omega(T_i)(t^j))^2.$$
 (10)

N is the number of samples,  $G_{\omega}(T_i)(t^j)$  is the predicted value corresponding to  $T_i$  at  $t^j$ , and  $\mathcal{E}_i(t^j)$  is the true value. In the loss function,  $\omega$  is used because it represents the model's trainable parameters that are adjusted to minimize the error between the

![](_page_3_Figure_13.jpeg)

Figure 4. Single-mode case: training and test loss functions.

predicted and the true values. This allows the model to learn and improve its predictions during the training process.

#### 4.2. Five-mode Case

Now, let us consider the initial condition consists of five modes, with the corresponding values listed in Table 1. The network is trained using 400 samples over the interval  $[0,\,40\omega_{\rm pe}^{-1}]$  with a time step of  $\Delta t=0.002\omega_{\rm pe}^{-1}$ , and the test set consists of 100 samples.

<span id="page-4-0"></span>![](_page_4_Figure_2.jpeg)

Figure 5. Five-mode case: comparison between DeepONet predictions and reference Gkeyll Vlasov solutions for varying temperatures (*T*). The vertical axis shows the electric field energy,  $\int |E_x|^2 dx$ , on a logarithmic scale, and the horizontal axis represents time in  $\omega_{pe}^{-1}$ .

Figure 5 compares the DeepONets predictions with the corresponding reference solutions at different temperature values (T). As in the single-mode case, the test cases shown

were not included during the training phase, highlighting the model's generalization capability. Given the relatively large wave perturbation amplitudes,  $A_n$ , listed in Table 1 for certain

<span id="page-5-0"></span>![](_page_5_Figure_2.jpeg)

![](_page_5_Figure_3.jpeg)

Figure 6. Five-mode case: training (left) and test (right) losses as a function of epochs for different training sample sizes (see Table 4).

Table 4

Mean Relative  $L^2$  Error Norms for the Five-mode Case with Different Numbers of Training and Test Samples

| Number of<br>Training Samples | Number of<br>Test Samples | Training<br>Error | Test<br>Error |
|-------------------------------|---------------------------|-------------------|---------------|
| 50                            | 12                        | 0.0035            | 0.0312        |
| 200                           | 50                        | 0.0061            | 0.0093        |
| 400                           | 100                       | 0.0047            | 0.0049        |
| 800                           | 200                       | 0.0044            | 0.0043        |

modes, nonlinear Landau damping is expected to occur. In the nonlinear regime (e.g., see the top-left panel of Figure 5), large perturbations drive significant energy transfer from the wave to resonant particles moving slightly below the wave phase speed, accelerating them beyond it. These faster particles subsequently transfer energy back to the wave, leading to an oscillatory exchange of energy. Nonlinear Landau damping is characteristically accompanied by the formation of electron phase-space holes (see, e.g., Figure 4 in Z. Huang et al. 2025). The comparison again demonstrates that the DeepONets surrogate model accurately captures the complex plasma dynamics, with its predictions in close agreement with the reference solutions.

The mean relative  $L^2$  error norms of the predicted solutions for different numbers of training samples are presented in Table 4. As the number of training samples increases, the test errors decrease, and the model's predictive accuracy on previously unseen test data improves, indicating its robustness and reliability. The observed increase in training error norms may be attributed to the model's exposure to more complex patterns and greater data variability with larger training sets.

The convergence of the loss functions with different numbers of training samples, depicted in Figure 6, tends toward smaller values of 10<sup>-4</sup>. This demonstrates that the DeepONets surrogate model not only effectively learns from the training data but also improves its accuracy on test data as the size of the training data set increases, which again highlights the model's robustness and generalization capability.

The proposed method demonstrates remarkable efficiency, with a training time of  $1.93 \times 10^{-3}\,\mathrm{s}$  per epoch. In the best-performing run, predicting 100 test cases took only 0.00148 s using one NVIDIA L40S GPU with 32 GB of memory,

representing a significant speedup compared to the conventional numerical solver applied to the same test data set.

#### 5. Conclusion

The integration of machine learning techniques with plasma physics has demonstrated that data-driven approaches can effectively model and interpret complex plasma dynamics in the collisionless regime. Among these approaches, DeepONets are notable for by their ability to directly approximate solutions to high-dimensional differential equations without the need for explicit discretization.

This study explores the use of DeepONets to simulate the Landau damping process—a fundamental kinetic phenomenon in space and astrophysical plasmas—highlighting their advantages over traditional numerical methods. The trained DeepONets surrogate model accurately captures the evolution of electric field energy in both single-mode and five-mode scenarios, achieving accuracy comparable to fully kinetic first-principles simulations. Its ability to generalize across varying initial conditions and perturbations underscores its robustness and adaptability. Notably, the neural network is trained on a range of initial conditions, enabling it to predict the evolution of new, unseen inputs without retraining, as long as the governing physical laws remain consistent.

By learning solution operators, DeepONets provide a computationally efficient and accurate framework for simulating complex plasma dynamics. These findings demonstrate the potential of DeepONets for broader applications in plasma physics, especially for modeling nonlinear and kinetic phenomena. Future research may extend this approach to other plasma processes and explore its performance in terms of accuracy, computational efficiency, and generalizability.

#### Acknowledgments

This work was partially supported by NASA grant 80NSSC23K0908, DOE grant DE-SC0024639, and the Alfred P. Sloan Research Fellowship. The authors thank Liang Wang for insightful discussions and for providing the dispersion relation calculations. We would like to acknowledge high-performance computing support from the NASA High-End Computing Program through the NASA Advanced Supercomputing Division at Ames Research Center, from National Energy Research Scientific Computing Center, a DOE Office

of Science user facility, and from the Derecho system (doi: 10.5065/[qx9a-pg09](https://doi.org/10.5065/qx9a-pg09)) provided by the NSF National Center for Atmospheric Research (NCAR), sponsored by the National Science Foundation. For distribution of the model results used in this study, please contact the corresponding authors.

## **Author Contributions**

C.D. supervised the project and, together with S.S., designed the research. S.S. developed the machine learning architecture based on the DeepONet model and completed the data analyses. Z.H. generated the simulation data. S.S. and C.D. wrote the manuscript. All authors reviewed and approved the final version.

## **Appendix Error Analysis and Convergence Behavior in the Five-Mode Case**

In Figure 7, we examine how the number of training samples affects model performance in the five-mode case. Figure 7 displays the mean relative *L*<sup>2</sup> error norms and loss functions for both training and test samples, plotted against the number of training samples. After training for 400 samples, DeepONets achieved a prediction error of less than 0.0049. Figure 8 provides further insights into the distribution of prediction errors across all test data sets for the case with 800 training samples and 200 test samples.

![](_page_6_Figure_7.jpeg)

![](_page_6_Figure_8.jpeg)

**Figure 7.** Five-mode case: the left panel shows the error norms for training and testing as a function of the number of training samples. The right panel depicts the training and test losses vs. the number of training samples. The error norms and losses are calculated using Equations ([9](#page-2-0)) and ([10](#page-3-0)).

![](_page_6_Figure_10.jpeg)

![](_page_6_Figure_11.jpeg)

**Figure 8.** Five-mode case: histogram (left) and scatter plot (right) of the relative *L*<sup>2</sup> test errors for the case with 800 training samples and 200 test samples.

#### **ORCID iDs**

<span id="page-7-0"></span>Simin Shekarpaz https://orcid.org/0009-0000-0502-5264 Chuanfei Dong https://orcid.org/0000-0002-8990-094X Ziyu Huang https://orcid.org/0000-0002-8624-1264

#### References

```
Alves, E. P., & Fiuza, F. 2022, PhRvR, 4, 033192
Azizmalayeri, M., & Rohban, M. H. 2023, Machine Learning, 112, 3003
Cai, S., Wang, Z., Lu, L., Zaki, T. A., & Karniadakis, G. 2021, JCoPh, 436,
   110296
Chen, Y., Tóth, G., Cassak, P., et al. 2017, JGRA, 122, 10,318
Chen, Y., Tóth, G., Zhou, H., & Wang, X. 2023, CoPhC, 287, 108714
Cheng, W., Fu, H., Wang, L., et al. 2023, CoPhC, 282, 108538
Daldorff, L. K. S., Tóth, G., Gombosi, T. I., et al. 2014, JCoPh, 268, 236
Donaghy, J., & Germaschewski, K. 2023, JPIPh, 89, 895890105
Dong, C., Wang, L., Hakim, A., et al. 2019, GeoRL, 46, 11,584
Hajimohammadi, Z., Shekarpaz, S., & Parand, K. 2023, Engineering with
   Computers, 39, 2169
Hammett, G. W., & Perkins, F. W. 1990, PhRvL, 64, 3019
Hornik, K., Stinchcombe, M., & White, H. 1989, NN, 2, 359
Huang, Z., Dong, C., & Wang, L. 2025, PNAS, 122, e2419073122
Ingelsten, E. R., McGrae-Menge, M. C., Alves, E. P., & Pusztai, I. 2025,
   JPlPh, 91, E64
Jarmak, S., Leonard, E., Akins, A., et al. 2020, AcAau, 170, 6
Joglekar, A. S., & Thomas, A. G. R. 2023, MLS&T, 4, 035049
Juno, J., Hakim, A., TenBarge, J., Shi, E., & Dorland, W. 2018, JCoPh,
  353, 110
Kurth, T., Subramanian, S., Harrington, P., et al. 2023, in Proc. Platform for
```

Advanced Scientific Computing Conf. PASC '23 (New York: Association

Laperre, B., Amaya, J., Jamal, S., & Lapenta, G. 2022, PhPl, 29, 032706

Li, D., Chen, Y., Dong, C., Wang, L., & Toth, G. 2023, AIPA, 13, 015126

for Computing Machinery)

```
Li, Z., Kovachki, N., Azizzadenesheli, K., et al. 2020, arXiv:2010.08895
Lu, L., Jin, P., Pang, G., Zhang, Z., & Karniadakis, G. 2021, NatMI, 3, 218
Ma, C., Zhu, B., Xu, X.-Q., & Wang, W. 2020, PhPl, 27, 042502
Mao, S., Dong, R., Lu, L., et al. 2023, ApJL, 950, L12
Meng, X., & Karniadakis, G. 2020, JCoPh, 401, 109020
Pang, G., Lu, L., & Karniadakis, G. 2019, SJSC, 41, A2603
Parand, K., Razzaghi, M., Sahleh, R., & Jani, M. 2020, Engineering with
  Computers, 36, 789
Parand, K., Yari, H., Taheri, R., & Shekarpaz, S. 2019, SeMA Journal, 76,
  615
Qin, Y., Ma, J., Jiang, M., et al. 2023, PhRvR, 5, 033079
Raissi, M., Perdikaris, P., & Karniadakis, G. E. 2019, JCoPh, 378, 686
Razzaghi, M., Shekarpaz, S., & Rajabi, A. 2023, in Solving Ordinary
   Differential Equations by LS-SVM, ed. J. A. Rad, K. Parand, &
   S. Chakraverty (Singapore: Springer), 147
Rulke, E., Wang, L., & Dong, C. 2021, AGUFM, 2021, SM53C
Sahin, I., Moya, C., Mollaali, A., Lin, G., & Paniagua, G. 2024, IJHMT, 219,
   124813
Shekarpaz, S., & Azari, H. 2020, Numerical Methods for Partial Differential
   Equations, 36, 654
Shekarpaz, S., Azizmalayeri, M., & Rohban, M. H. 2022, arXiv:2207.06647
Shekarpaz, S., Zeng, F., & Karniadakis, G. 2024, CCoPh, 35, 1
Shukla, K., Zou, Z., Chan, C. H., et al. 2025, CMAME, 433, 117498
Tóth, G., Jia, X., Markidis, S., et al. 2016, JGRA, 121, 1273
Wang, L., Germaschewski, K., Hakim, A., et al. 2018, JGRA, 123, 2815
Wang, L., Hakim, A. H., Bhattacharjee, A., & Germaschewski, K. 2015, PhPl,
Wang, L., Hakim, A. H., Ng, J., Dong, C., & Germaschewski, K. 2020, JCoPh,
   415, 109510
Wang, X., Chen, Y., & Tóth, Y. 2022, JGRA, 127, e2021JA030091
Wei, S., Liu, Y., Fu, H., Dong, C., & Wang, L. 2023, in 2023 International
   Applied Computational Electromagnetics Society Symposium (ACES-
   China) (Piscataway, NJ: IEEE), 01
Zhang, D., Guo, L., & Karniadakis, G. 2020, SJSC, 42, A639
Zhou, H., Tóth, G., Jia, X., & Chen, Y. 2020, JGRA, 125, e28162
```
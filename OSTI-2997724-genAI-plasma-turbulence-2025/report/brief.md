# Brief

**Paper:** Clavier, Zarzoso, del-Castillo-Negrete & Frénod (2025), "A generative
artificial intelligence framework for long-time plasma turbulence simulations,"
*Phys. Plasmas* 32, 063905. DOI:10.1063/5.0255386. OSTI 2997724.

**What:** The paper introduces **GAIT** (Generative AI Turbulence), a surrogate model
that accelerates 2D plasma turbulence simulation. GAIT = a Convolutional Variational
Auto-Encoder (CVAE) that compresses 64×64 Hasegawa–Wakatani (HW) potential snapshots
into a 64-dim latent space + a Recurrent Neural Network (RNN) that rolls the latent
state forward in time. Decoding the RNN-generated latent trajectory yields new,
physically-faithful turbulence frames at a fraction of the cost of direct pseudo-spectral
integration (claimed ~400× faster). Fidelity is judged by Fourier/POD spectra, the
Okubo–Weiss flow topology, the turbulent autocorrelation time, and the effective
turbulent diffusivity from passive-particle transport.

**Why replicate:** Method is fully specified (HW params, CVAE Tables I–II, RNN Table III,
training recipe, quantitative claims for diffusivity and speedup). Data/code are "available
upon request" (NOT public), so we reproduce the *method* end-to-end: generate our own HW
turbulence ground truth, build the CVAE+RNN to spec, train on uicgpu A100, and test the
central claims — (a) latent surrogate reconstructs HW fields, (b) RNN rollout produces
statistically-stationary turbulence with matching spectra/autocorrelation, (c) large
speedup over direct integration.

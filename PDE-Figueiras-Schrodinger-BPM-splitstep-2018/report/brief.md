# Brief

**Paper:** Figueiras, Olivieri, Paredes, Michinel, *"An open source virtual laboratory for the Schrödinger equation"*, Eur. J. Phys. **39** (2018) 055802. DOI:10.1088/1361-6404/aac999 (CC-BY 3.0 Open Access, IOP).

**What/why:** The paper presents a Python split-step (beam-propagation-method, BPM) pseudospectral solver for the dimensionless linear and nonlinear time-dependent Schrödinger equation in 1D/2D, and demonstrates it on textbook and research phenomena (reflectionless Pöschl-Teller scattering, bright-soliton propagation/collision, vortex beams). We independently re-implemented the split-step Fourier scheme from scratch (numpy FFTs only, no third-party PDE solver) and verified its correctness against closed-form analytic solutions **first**, then reproduced the paper's headline physical phenomena and its stated first-order O(dt) accuracy. The Schrödinger/NLSE family was not previously covered in the PDE-100 set.

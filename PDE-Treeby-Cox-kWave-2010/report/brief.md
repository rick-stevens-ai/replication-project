# Brief

**Paper.** Treeby, B. E. & Cox, B. T. (2010) *k-Wave: MATLAB toolbox for the simulation and reconstruction of photoacoustic wave fields*, J. Biomed. Opt. **15**(2), 021314. DOI: 10.1117/1.3360308.

**What.** Independent, from-scratch numerical replication of the k-space pseudospectral time-domain (k-space PSTD) acoustic solver at the heart of k-Wave. The paper's three core numerical claims — (C1) the k-space correction κ = sinc(c₀ Δt |k|/2) eliminates temporal dispersion and yields unconditional stability for the homogeneous problem, (C2) accurate wave propagation vs analytic solutions, (C3) ~2 grid-points-per-wavelength (Nyquist) spectral accuracy — are each tested numerically with real errors measured against closed-form / high-resolution analytic references.

**Why.** k-Wave is one of the most widely used photoacoustic/ultrasound simulators (>1000 citations for this JBO paper) and its numerical selling point is spectral accuracy at Nyquist plus unconditional stability. These are non-trivial claims worth verifying without touching k-Wave's own MATLAB code.

**How.** From-scratch Python + NumPy implementation of the coupled first-order acoustic equations on a staggered spatial and temporal grid, with the FFT-based k-space spatial derivative including the paper's κ correction. Three experiments were run locally on CPU (no k-Wave code involved) and compared to (i) the exact d'Alembert half-split for 1D, (ii) a Hankel-quadrature analytic reference for smooth 2D initial conditions, (iii) a self-convergence sweep for the classical hard-edged 2D disk PSA.

**Result.** All three claims replicated with real numerical evidence. See `REPORT.md` §Results.

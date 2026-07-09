# Progress: Galerkin Approximations for the Stochastic Burgers Equation

## Paper
- **Title:** Galerkin Approximations for the Stochastic Burgers Equation
- **Authors:** Dirk Blömker, Arnulf Jentzen
- **Journal:** SIAM J. Numer. Anal. 51(1), 694-715, 2013
- **arXiv:** 1304.3288
- **Citations:** ~105

## Steps

### Step 1: Paper Analysis ✅
- Found paper on arXiv (1304.3288), downloaded PDF
- Extracted all mathematical details: domain, BCs, basis functions, eigenvalues, noise structure, nonlinearity, initial condition, parameters

### Step 2: Implementation ✅
- Implemented spectral Galerkin solver with exponential Euler time integration
- Two nonlinear term methods: pseudospectral (O(NM)) and analytic triple-product (O(N²))
- **Bug found and fixed:** analytic method was missing √2/2 normalization factor
- Verified pseudospectral vs analytic agree to machine precision (rel error ~10⁻¹⁵)
- Optimized solver with precomputed matrices (GalerkinSolver class)
- Benchmarked: N=4096 runs in ~60s per realization

### Step 3: Spatial Convergence Analysis ✅
- N_ref = 4096, N ∈ {16, 32, 64, 128, 256, 512, 1024, 2048}
- 10 independent realizations with shared Brownian motion
- Overall log-log slope: −0.618 (paper predicts ~−0.5)
- Pairwise rates 0.48–0.73 in the main range, concentrated around 0.5

### Step 4: Temporal Convergence ✅
- N = 128, Δt from 5e-4 to 1.56e-5
- 20 realizations, overall temporal slope: 0.893
- Consistent with exponential Euler (between order 0.5 and 1.0)

### Step 5: Visualizations ✅
- `figures/convergence_rates.png` — Replication of Figure 4.1 (log-log convergence)
- `figures/sample_paths.png` — Sample paths, evolution, space-time plot, coefficient decay
- `figures/N_comparison.png` — Solutions at different N with shared noise
- `figures/temporal_convergence.png` — Temporal convergence rates

### Step 6: Report ✅
- Full report in `report/REPORT.md`
- Honest scoring: 8.5/10
- Main result (spatial convergence ~N^{−1/2} in L∞) clearly replicated

## Final Score: 8.5/10

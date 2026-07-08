# Replication: Drift-Flux Indoor Particle Model
## Chen, Yu & Lai (2006) — Atmospheric Environment 40, pp 357-367

**DOI**: 10.1016/j.atmosenv.2005.09.044
**Priority**: TOP OF QUEUE
**Started**: 2026-05-15

---

## Paper Summary

A 3D Eulerian drift-flux model for particle distribution and deposition in ventilated indoor environments. The model solves the turbulent airflow (RNG k-ε) first to steady state, then solves transient particle transport with gravitational settling and wall deposition for 10 particle sizes (0.01–10 μm). Validated against PDA measurements in a scale chamber.

## Geometry

- Model room: 0.8m × 0.4m × 0.4m (L × W × H)
- Inlet: 0.04m × 0.04m, center at (x=0, y=0.2m, z=0.36m) — on front wall, near ceiling
- Outlet: 0.04m × 0.04m, center at (x=0.8m, y=0.2m, z=0.04m) — on back wall, near floor
- Symmetry plane at y=0.2m (center plane)

## Flow Conditions

| Parameter | Case 1 | Case 2 |
|-----------|--------|--------|
| Inlet velocity | 0.225 m/s | 0.45 m/s |
| Air change rate | 10 h⁻¹ | 20 h⁻¹ |
| Flow regime | Turbulent | Turbulent |

- Air: incompressible, isothermal
- ρ_air = 1.205 kg/m³, ν = 1.5e-5 m²/s (standard conditions)
- Re_inlet ≈ 600 (Case 1), 1200 (Case 2) based on inlet hydraulic diameter

## Governing Equations

### Airflow (steady-state)
- Continuity + RANS momentum with RNG k-ε model
- Coefficients from Speziale & Thangam (1992):
  - C_μ = 0.0845, C_ε1 = 1.42, C_ε2 = 1.68
  - σ_k = 0.7194, σ_ε = 0.7194
  - Additional strain-rate term η₀ = 4.38, β = 0.012
- Log-law wall functions

### Particle Transport (transient, Eq. 2)
```
∂C/∂t + ∇·[(u + vs)C] = ∇·[(D + εp)∇C] + SC
```
Where:
- C = particle mass (or number) concentration
- u = air velocity field (from steady-state solution)
- vs = settling velocity (gravitational, downward = -z direction)
- D = Brownian diffusion coefficient
- εp = particle eddy diffusivity ≈ νt (turbulent viscosity)
- SC = source term (zero in interior; inlet provides C⁺=1)

### Settling Velocity (Stokes)
```
vs = ρp × dp² × g × Cc / (18μ)
```
Where:
- ρp = 1400 kg/m³ (particle density)
- dp = particle diameter
- g = 9.81 m/s²
- Cc = Cunningham slip correction factor
- μ = dynamic viscosity of air (1.81e-5 Pa·s)

### Cunningham Slip Correction
```
Cc = 1 + (2λ/dp)[1.257 + 0.4 exp(-1.1dp/2λ)]
```
λ = 0.066 μm (mean free path of air)

### Brownian Diffusion
```
D = kT × Cc / (3πμdp)
```
k = 1.38e-23 J/K, T = 293 K

### Wall Deposition (Lai & Nazaroff 2000)
- Deposition flux: J_d = v_d × C_b
- v_d = deposition velocity from semi-empirical model
- C_b = concentration at first near-wall cell
- Input: friction velocity u* = sqrt(τ_w/ρ)
- Model accounts for Brownian diffusion, turbulent diffusion, and gravitational settling in the concentration boundary layer

## Particle Sizes

| dp (μm) | vs (m/s) | D (m²/s) | τp (s) | Cc |
|----------|----------|----------|--------|-----|
| 0.01 | 6.6e-8 | 5.3e-8 | 6.7e-9 | 22.6 |
| 0.05 | 5.0e-7 | 2.7e-9 | 1.5e-7 | 4.96 |
| 0.1 | 8.8e-7 | 6.8e-10 | 5.4e-7 | 2.85 |
| 0.5 | 1.1e-5 | 2.8e-11 | 1.3e-5 | 1.33 |
| 1.0 | 3.5e-5 | 6.8e-12 | 4.3e-5 | 1.16 |
| 2.0 | 1.2e-4 | 1.6e-12 | 1.5e-4 | 1.08 |
| 3.0 | 2.7e-4 | 7.3e-13 | 3.2e-4 | 1.05 |
| 5.0 | 7.6e-4 | 2.8e-13 | 9.0e-4 | 1.03 |
| 7.0 | 1.5e-3 | 1.4e-13 | 1.8e-3 | 1.02 |
| 10.0 | 3.1e-3 | 7.0e-14 | 3.6e-3 | 1.02 |

(Values approximate — will compute exactly in code)

## Numerical Method

- Grid: 40 × 20 × 20 (16,000 cells) — validated against 80×40×40
- Convection: 2nd-order upwind
- Diffusion: central differencing (2nd-order)
- Transient: 1st-order fully implicit (Euler)
- Pressure-velocity coupling: SIMPLER algorithm
- Steady-state flow solved first
- Transient particle transport: 1800s simulation time
- Initial condition: C⁺ = 0 everywhere; inlet C⁺ = 1

## Validation Targets

### Figure 4: Velocity profiles
- x-velocity (u) vs z at x=0.2, 0.4, 0.6m in center plane (y=0.2m)
- Case 1 only (0.225 m/s)

### Figure 5: Concentration contours
- 1 μm and 10 μm particles at t = 60, 180, 300, 1800s
- Center plane contour maps

### Figure 6: Coefficient of Variation
- CV(t) for dp = 1, 2, 5, 10 μm at both velocities
- CV = std(C)/mean(C) across all cells
- Mixing time = time when CV < 10% permanently
- Paper reports: 1μm mixing time ~429s, 2μm ~489s (low velocity)

### Figure 7: Concentration profiles
- Normalized concentration of 10μm particles vs z at x=0.2, 0.4, 0.6m
- Both velocities, at t=1800s (steady state)

## Implementation Plan

### Approach: Python/FEniCS (preferred over OpenFOAM for this problem)

OpenFOAM would work but requires a custom solver for the drift-flux transport equation with the Lai-Nazaroff deposition BC. FEniCS gives us more flexibility for:
- Custom weak form with settling velocity
- Robin-type BC for wall deposition
- Easy post-processing in Python

However, the RNG k-ε turbulence model in FEniCS requires significant implementation. 

### REVISED: Hybrid approach
1. **OpenFOAM for airflow**: simpleFoam with RNG k-ε → export velocity + νt fields
2. **Python for particle transport**: Read OpenFOAM fields, solve drift-flux equation with FiPy or custom FVM
3. **Python for post-processing**: All figures and validation

### Alternative: Pure Python with simplified turbulence
Since the room is small and the flow is a simple jet-driven recirculation, we could:
1. Solve steady RANS with a k-ε model in FEniCS
2. Solve particle transport in the same framework
3. Everything in one codebase

### FINAL DECISION: OpenFOAM + Python post-processing
- OpenFOAM has RNG k-ε built in, SIMPLER, and scalarTransport
- Use `scalarTransportFoam` or custom `driftFluxFoam` for particle transport
- Python scripts for post-processing and validation plots

## Stages

### Stage 1: Mesh & Airflow (OpenFOAM)
- [ ] blockMeshDict for room geometry
- [ ] simpleFoam steady-state with RNG k-ε
- [ ] Validate velocity field against Fig 4

### Stage 2: Particle Transport
- [ ] Implement drift-flux scalar transport with settling
- [ ] Implement Lai-Nazaroff wall deposition BC
- [ ] Run for 10 particle sizes, 1800s
- [ ] Validate concentration against Fig 7

### Stage 3: Analysis & Figures
- [ ] Reproduce Fig 3 (velocity field)
- [ ] Reproduce Fig 4 (velocity profiles)
- [ ] Reproduce Fig 5 (concentration evolution)
- [ ] Reproduce Fig 6 (CV vs time)
- [ ] Reproduce Fig 7 (concentration profiles)
- [ ] Mixing time analysis

### Stage 4: Report
- [ ] Full replication report with comparisons

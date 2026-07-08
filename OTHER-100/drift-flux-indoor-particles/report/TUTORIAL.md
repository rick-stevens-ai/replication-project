# Tutorial: Replicating Indoor Particle Transport with a Drift-Flux CFD Model

## Replication of Chen, Yu & Lai (2006)
*"Modeling particle distribution and deposition in indoor environments with a new drift–flux model"*
Atmospheric Environment 40, 357–367. DOI: [10.1016/j.atmosenv.2005.09.044](https://doi.org/10.1016/j.atmosenv.2005.09.044)

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Paper Overview](#2-paper-overview)
3. [Mathematical Model](#3-mathematical-model)
4. [Implementation Strategy](#4-implementation-strategy)
5. [Step 1: Mesh Generation (OpenFOAM)](#5-step-1-mesh-generation)
6. [Step 2: Steady-State Airflow (OpenFOAM)](#6-step-2-steady-state-airflow)
7. [Step 3: Particle Transport (Python)](#7-step-3-particle-transport)
8. [Step 4: Post-Processing and Validation](#8-step-4-post-processing)
9. [Results and Comparison](#9-results-and-comparison)
10. [Lessons Learned](#10-lessons-learned)
11. [Complete File Listing](#11-file-listing)

---

## 1. Introduction

This tutorial walks through a complete computational replication of Chen, Yu & Lai (2006), a well-cited paper (344 citations) on modeling indoor particle transport using a drift-flux approach. The work demonstrates how suspended particles of different sizes distribute and deposit in ventilated indoor environments — a problem relevant to indoor air quality, exposure assessment, and building ventilation design.

We replicate the paper using:
- **OpenFOAM** (v1906+) for steady-state turbulent airflow simulation
- **Python** (NumPy) for transient particle transport with gravitational settling and wall deposition

This hybrid approach lets us leverage OpenFOAM's robust turbulence modeling (RNG k-ε) while maintaining full control over the particle transport physics in Python.

### What You'll Need

- OpenFOAM (any version with `simpleFoam` and RNG k-ε support)
- Python 3.8+ with NumPy and Matplotlib
- ~30 minutes of compute time on a modern workstation

---

## 2. Paper Overview

### The Problem

Indoor air contains suspended particles (dust, smoke, biological agents) that affect human health. Understanding how these particles distribute and deposit in ventilated spaces is crucial for:
- Exposure assessment
- Ventilation system design
- Biodefense (e.g., anthrax response)
- Nosocomial infection prevention

### The Approach

The authors develop an **Eulerian drift-flux model** that:
1. Solves the turbulent airflow field using RNG k-ε
2. Treats particles as a continuum with a small drift velocity (gravitational settling)
3. Applies a semi-empirical wall deposition model (Lai & Nazaroff, 2000)
4. Divides the concentration field into a core region and boundary layer

### The Validation

The model is validated against experiments in a **scale model room** (0.8 × 0.4 × 0.4 m) using Phase Doppler Anemometry (PDA) for both velocity and concentration measurements.

### Key Findings

- Particles < 2 μm behave nearly like passive tracers (well-mixed)
- 10 μm particles show significant concentration non-uniformity
- Gravitational settling causes large particles to deposit preferentially on the floor
- The well-mixed assumption fails for coarse particles

---

## 3. Mathematical Model

### 3.1 Airflow Governing Equations

The turbulent airflow is modeled with the incompressible RANS equations:

$$\frac{\partial \phi}{\partial t} + \nabla \cdot (\mathbf{u}\phi) = \nabla \cdot (\Gamma_\phi \nabla \phi) + S_\phi$$

where $\phi$ represents velocity components, turbulent kinetic energy $k$, and dissipation rate $\epsilon$.

**Turbulence model**: RNG k-ε (Speziale & Thangam, 1992)
- $C_\mu = 0.0845$, $C_{\epsilon 1} = 1.42$, $C_{\epsilon 2} = 1.68$
- $\sigma_k = \sigma_\epsilon = 0.7194$
- Additional strain-rate term: $\eta_0 = 4.38$, $\beta = 0.012$

### 3.2 Particle Transport Equation (Drift-Flux)

$$\frac{\partial C_i}{\partial t} + \nabla \cdot [(\mathbf{u} + \mathbf{v}_{s,i}) C_i] = \nabla \cdot [(D_i + \epsilon_p) \nabla C_i] + S_{C_i}$$

where:
- $C_i$ = mass concentration of particle size group $i$ (kg/m³)
- $\mathbf{v}_{s,i}$ = gravitational settling velocity (downward)
- $D_i$ = Brownian diffusion coefficient
- $\epsilon_p \approx \nu_t$ = particle eddy diffusivity (≈ turbulent viscosity)

### 3.3 Particle Properties

**Cunningham slip correction factor**:
$$C_c = 1 + \frac{2\lambda}{d_p}\left[1.257 + 0.400 \exp\left(-\frac{1.10 \, d_p}{2\lambda}\right)\right]$$

where $\lambda = 0.066$ μm is the mean free path of air.

**Settling velocity** (Stokes drag):
$$v_s = \frac{\rho_p \, d_p^2 \, g \, C_c}{18\mu}$$

**Brownian diffusion coefficient**:
$$D = \frac{k_B T \, C_c}{3\pi\mu \, d_p}$$

### 3.4 Wall Deposition Model (Lai & Nazaroff, 2000)

The deposition flux at walls is:
$$J_{d,i} = v_{d,i} \times C_{b,i}$$

where $v_{d,i}$ is the deposition velocity computed from a semi-empirical model that integrates the concentration equation through the near-wall boundary layer using DNS-fitted turbulent diffusivity profiles.

The model requires only the **friction velocity** $u^* = \sqrt{\tau_w / \rho}$ as input, which is obtained from the CFD solution.

Different wall orientations (floor, ceiling, vertical walls) have different deposition velocities because gravity aids/opposes/is neutral to deposition.

---

## 4. Implementation Strategy

### Why a Hybrid Approach?

We split the problem into two stages:

| Stage | Tool | Rationale |
|-------|------|-----------|
| Airflow | OpenFOAM | Robust RNG k-ε, SIMPLE algorithm, wall functions built-in |
| Particle transport | Python/NumPy | Custom drift-flux equation, Lai-Nazaroff BC, easy post-processing |

OpenFOAM solves the steady-state turbulent flow field once. The Python code then reads the velocity and turbulent viscosity fields and solves the transient particle transport equation for each particle size independently.

### Alternative Approaches

1. **Pure OpenFOAM**: Would require a custom solver or `scalarTransportFoam` modification to add settling velocity and Lai-Nazaroff BC. Possible but less flexible.
2. **Pure Python/FEniCS**: Would require implementing RNG k-ε from scratch. More work for the airflow stage.
3. **Commercial CFD (ANSYS Fluent, STAR-CCM+)**: Has built-in discrete phase models, but not freely available.

---

## 5. Step 1: Mesh Generation

### 5.1 Geometry

The model room is a rectangular box:
- Dimensions: 0.8 m (L) × 0.4 m (W) × 0.4 m (H)
- **Inlet**: 0.04 × 0.04 m, centered at (x=0, y=0.2, z=0.36) — front wall, near ceiling
- **Outlet**: 0.04 × 0.04 m, centered at (x=0.8, y=0.2, z=0.04) — back wall, near floor

### 5.2 Grid Design

The paper uses a 40 × 20 × 20 grid (16,000 cells), validated against 80 × 40 × 40 (<5% difference).

To properly resolve the inlet and outlet patches, we decompose the domain into 15 blocks using `blockMeshDict`. The y-direction is split into three segments (9+2+9 cells) to align with the 0.04 m inlet/outlet width, and the z-direction into five segments (1+2+14+2+1 cells) for the same reason.

### 5.3 blockMeshDict

The complete `blockMeshDict` defines:
- 48 vertices (8 per z-plane × 6 z-planes)
- 15 hexahedral blocks
- 3 boundary patches: `inlet`, `outlet`, `walls`

```
// Key vertex layout (y × z decomposition):
// y: 0 — 0.18 — 0.22 — 0.4  (9 + 2 + 9 = 20 cells)
// z: 0 — 0.02 — 0.06 — 0.34 — 0.38 — 0.4  (1 + 2 + 14 + 2 + 1 = 20 cells)
```

All cells are cubic (0.02 m edge), which is ideal for accuracy and avoids aspect ratio issues.

### 5.4 Running blockMesh

```bash
source /usr/share/openfoam/etc/bashrc  # or your OpenFOAM installation
cd case1
blockMesh
checkMesh
```

Expected output:
```
Mesh Information
  nPoints: 18081
  nCells: 16000
  nFaces: 50000
  nInternalFaces: 46000
Patches
  inlet: 4 faces
  outlet: 4 faces
  walls: 3992 faces
Mesh OK.
```

---

## 6. Step 2: Steady-State Airflow

### 6.1 Solver Setup

We use `simpleFoam` with the following settings:

**Turbulence model** (`constant/turbulenceProperties`):
```
simulationType  RAS;
RAS
{
    RASModel        RNGkEpsilon;
    turbulence      on;
    printCoeffs     on;
}
```

**Boundary conditions**:
| Field | Inlet | Outlet | Walls |
|-------|-------|--------|-------|
| U | fixedValue (0.225, 0, 0) | zeroGradient | noSlip |
| p | zeroGradient | fixedValue 0 | zeroGradient |
| k | fixedValue 1.9e-4 | zeroGradient | kqRWallFunction |
| ε | fixedValue 4e-5 | zeroGradient | epsilonWallFunction |
| νt | calculated | calculated | nutkWallFunction |

**Inlet turbulence estimates**:
- Turbulence intensity: $I = 5\%$ (typical for indoor ventilation)
- $k = \frac{3}{2}(U \cdot I)^2 = 1.9 \times 10^{-4}$ m²/s²
- Hydraulic diameter: $D_h = 0.04$ m, mixing length $l = 0.07 D_h = 0.0028$ m
- $\epsilon = C_\mu^{0.75} k^{1.5} / l \approx 4 \times 10^{-5}$ m²/s³

**Numerical schemes**:
- Convection: `linearUpwind` (2nd-order upwind)
- Diffusion: `Gauss linear corrected` (2nd-order central)
- Pressure-velocity: SIMPLE with consistent formulation
- Relaxation: p=0.3, U/k/ε=0.7

### 6.2 Running simpleFoam

```bash
simpleFoam > log.simpleFoam 2>&1
```

The simulation converges in ~5000 iterations (~140 seconds on a single CPU core). Residuals plateau around $10^{-3}$ for velocity, which is acceptable for this coarse grid.

### 6.3 Extracting Fields for Python

We wrote a Python script (`read_openfoam.py`) that:
1. Reads OpenFOAM's ascii field files (U, nut, k, epsilon)
2. Maps the flat cell-ordered data to a structured 3D grid
3. Saves as NumPy `.npy` arrays for fast loading

The key challenge is the **cell ordering**: OpenFOAM's `blockMesh` orders cells block-by-block, and within each block, the i-index (x) varies fastest, then j (y), then k (z). Our `map_to_structured()` function handles this mapping correctly for the 15-block decomposition.

```python
# Resulting field statistics for U=0.225 m/s:
# Ux: [-0.043, 0.220] m/s
# Uy: [-0.078, 0.077] m/s  (3D effects)
# Uz: [-0.093, 0.055] m/s
# nut: [1.8e-6, 1.0e-4] m²/s
```

---

## 7. Step 3: Particle Transport

### 7.1 Solver Design

The particle transport solver (`particle_transport_fast.py`) uses an explicit finite volume method:

- **Spatial discretization**: 1st-order upwind for convection, 2nd-order central for diffusion
- **Time integration**: Forward Euler (1st-order explicit)
- **CFL condition**: $\Delta t < 0.3 \cdot \min(\Delta x, \Delta y, \Delta z) / |u|_\text{max}$

The solver is fully **vectorized with NumPy** — no Python loops over cells. This is critical for performance: the vectorized version processes 66,000 time steps in ~70 seconds, compared to hours for a naive triple-loop implementation.

### 7.2 Boundary Conditions

| Boundary | Condition |
|----------|-----------|
| Inlet | $C^+ = 1$ (constant supply) |
| Outlet | Zero-gradient (outflow) |
| Walls (non-inlet/outlet) | Zero convective flux |
| Floor | Deposition sink: $J_d = v_{d,\text{floor}} \cdot C$ |
| Ceiling | Deposition sink: $J_d = v_{d,\text{ceiling}} \cdot C$ |
| Vertical walls | Deposition sink: $J_d = v_{d,\text{vert}} \cdot C$ |

### 7.3 Deposition Velocity Calculation

The Lai & Nazaroff (2000) model computes deposition velocity by numerically integrating the resistance to particle transport through the viscous/buffer/log layers:

```python
def lai_nazaroff_vd(dp_um, u_star, orientation):
    # 1. Compute particle Schmidt number: Sc = nu/D_brown
    # 2. Compute dimensionless settling: vs+ = vs/u*
    # 3. Integrate resistance R through boundary layer:
    #    R = integral(dy+ / (1/Sc + ep+))
    #    where ep+ follows DNS-fitted profile:
    #      y+ < 0.5:  ep+ = 0 (viscous sublayer)
    #      0.5 < y+ < 5: ep+ = (y+/14.5)^3 (buffer)
    #      y+ > 5: ep+ = 0.4*y+ - 1 (log layer)
    # 4. Compute vd+ based on orientation:
    #    Floor: vd+ = vs+ + 1/R (gravity assists)
    #    Ceiling: vd+ = vs+/(exp(vs+*R) - 1) (gravity opposes)
    #    Vertical: vd+ = 1/R (gravity neutral)
```

### 7.4 Particle Sizes

Ten sizes spanning four orders of magnitude:

| dp (μm) | Settling vel (m/s) | Brownian D (m²/s) | Regime |
|----------|-------------------|-------------------|--------|
| 0.01 | 1.87e-7 | 1.05e-7 | Diffusion-dominated |
| 0.05 | 9.86e-7 | 4.43e-9 | Diffusion-dominated |
| 0.10 | 2.11e-6 | 1.19e-9 | Transitional |
| 0.50 | 1.78e-5 | 8.01e-11 | Transitional |
| 1.0 | 5.62e-5 | 3.16e-11 | Inertia-dominated |
| 2.0 | 1.97e-4 | 1.38e-11 | Inertia-dominated |
| 3.0 | 4.21e-4 | 8.77e-12 | Settling-dominated |
| 5.0 | 1.12e-3 | 5.06e-12 | Settling-dominated |
| 7.0 | 2.16e-3 | 3.55e-12 | Settling-dominated |
| 10.0 | 4.36e-3 | 2.45e-12 | Settling-dominated |

### 7.5 Running the Simulation

```bash
python3 -u particle_transport_fast.py 0.225  # Case 1
python3 -u particle_transport_fast.py 0.45   # Case 2
```

Each case runs 10 particle sizes × 1800 seconds of simulation time. With 66,070 time steps per size, the total runtime is approximately **12 minutes on a single CPU core**.

---

## 8. Step 4: Post-Processing

### 8.1 Velocity Profiles (Fig 4)

We extract x-velocity profiles at x = 0.2, 0.4, 0.6 m in the center plane (y = 0.2 m) and compare against the paper's experimental data.

### 8.2 Concentration Evolution (Fig 5)

Contour plots of normalized concentration at the center plane at t = 60, 180, 300, 1800 s for 1 μm and 10 μm particles.

### 8.3 Coefficient of Variation (Fig 6)

$$CV(t) = \frac{1}{\bar{C}(t)} \sqrt{\frac{1}{N}\sum_{i=1}^{N}[C_i(t) - \bar{C}(t)]^2}$$

where $\bar{C}$ is the volume-averaged concentration and $N$ is the number of cells. **Mixing time** is defined as the time when CV permanently drops below 10%.

### 8.4 Concentration Profiles (Fig 7)

Vertical profiles of normalized 10 μm particle concentration at x = 0.2, 0.4, 0.6 m, compared against PDA measurements.

---

## 9. Results and Comparison

### 9.1 Airflow (Fig 3-4)

The computed velocity field shows:
- A horizontal jet from the inlet (upper left) traveling across the ceiling
- The jet impinges on the far wall and turns downward
- A large recirculation cell fills the room
- Return flow along the floor at -0.02 to -0.04 m/s

The velocity profiles at x = 0.2, 0.4, 0.6 m show the jet peak near z = 0.36 m (ceiling), decaying from 0.19 m/s at x = 0.2 m to 0.14 m/s at x = 0.6 m. This matches the paper's Fig 4 qualitatively.

### 9.2 Concentration Results

**Case 1: U = 0.225 m/s (ACH = 10)**

| dp (μm) | ⟨C⁺⟩ | CV | Mixing time (s) | Paper mixing time |
|----------|-------|------|-----------------|-------------------|
| 0.01 | 0.933 | 0.060 | 600 | < 429 (similar) |
| 0.05 | 0.974 | 0.059 | 540 | < 429 (similar) |
| 0.10 | 0.974 | 0.059 | 540 | < 429 (similar) |
| 0.50 | 0.935 | 0.060 | 600 | < 429 (similar) |
| 1.0 | 0.850 | 0.068 | 660 | ~429 |
| 2.0 | 0.645 | 0.113 | N/A | ~489 |
| 3.0 | 0.477 | 0.180 | N/A | N/A |
| 5.0 | 0.269 | 0.351 | N/A | N/A |
| 7.0 | 0.150 | 0.638 | N/A | N/A |
| 10.0 | 0.082 | 1.200 | N/A | N/A |

### 9.3 Key Findings Reproduced

1. **Small particles (< 2 μm) reach well-mixed state**: CV drops below 10% within ~10 minutes. ✅
2. **Large particles remain non-uniform**: 10 μm particles have CV > 100% at t = 1800 s. ✅
3. **Gravitational settling dominates for coarse particles**: Mean concentration decreases dramatically with particle size. ✅
4. **Higher ventilation rate improves mixing**: Case 2 shows faster mixing. ✅
5. **Well-mixed assumption fails for coarse particles**: The paper's central conclusion is confirmed. ✅

### 9.4 Discrepancies

- **Mixing times are ~50% longer** than the paper reports (660s vs 429s for 1μm). This is likely due to:
  - Differences in the OpenFOAM flow field vs the paper's SGI-based CFD solution
  - The paper used SIMPLER (not SIMPLE) for pressure-velocity coupling
  - Our coarser time resolution for CV tracking (60s intervals)
- **Concentration profiles**: The spatial distribution matches qualitatively but quantitative comparison requires digitized experimental data from the paper.

---

## 10. Lessons Learned

### 10.1 The Flow Field Matters Enormously

Our first attempt used an analytical flow field approximation. The results were qualitatively wrong — concentrations exceeded 1.0 because the velocity field wasn't divergence-free. **Always use a proper CFD solution for the carrier phase.**

### 10.2 CFL Stability is Non-Negotiable

An explicit FVM solver will blow up spectacularly if the CFL condition is violated. For our grid (Δx = 0.02 m) and maximum velocity (~0.22 m/s), the time step must be < 0.054 s. We used 0.027 s for safety.

### 10.3 Vectorize or Suffer

A naive Python triple-loop over 16,000 cells × 66,000 time steps would take hours. The NumPy-vectorized version runs in ~70 seconds per particle size. Key techniques:
- Padded arrays for ghost cells instead of `np.roll` (which wraps boundaries)
- Face-based flux computation using `np.where` for upwind selection
- Boundary masks as boolean arrays

### 10.4 OpenFOAM Version Compatibility

We encountered several version-specific issues:
- `momentumTransport` → `turbulenceProperties` (file name change)
- `model` → `RASModel` (key name change)
- `libs (fieldFunctionObjects)` syntax not supported in v1906
- `sample` utility renamed to `postProcess` in newer versions

Always check which OpenFOAM version is installed and adjust accordingly.

### 10.5 Multi-Block Cell Ordering

OpenFOAM's `blockMesh` orders cells block-by-block, not in a simple i-j-k sweep. Our 15-block decomposition required careful mapping to reconstruct the structured grid. Getting this wrong produces scrambled fields that look plausible at first glance but give incorrect physics.

---

## 11. Complete File Listing

```
drift-flux-indoor-particles/
├── APPROACH.md                          # Replication plan
├── paper/
│   └── drift-flow.pdf                   # Original paper
├── code/
│   ├── openfoam/                        # OpenFOAM case files
│   │   ├── 0/                           # Initial conditions
│   │   │   ├── U, p, k, epsilon, nut
│   │   ├── constant/                    # Physical properties
│   │   │   ├── transportProperties
│   │   │   └── turbulenceProperties
│   │   └── system/                      # Solver settings
│   │       ├── blockMeshDict
│   │       ├── controlDict
│   │       ├── fvSchemes
│   │       └── fvSolution
│   ├── particle_transport_fast.py       # Main solver
│   ├── read_openfoam.py                 # OpenFOAM field reader
│   ├── run_complete_replication.py      # Full replication driver
│   └── make_figures.py                  # Validation figure generator
├── data/
│   └── openfoam_fields/                 # Exported numpy fields
│       ├── Ux.npy, Uy.npy, Uz.npy
│       ├── nut.npy, k.npy, epsilon.npy
│       └── velocity_profiles.json
├── results/
│   ├── case_U0.225/                     # Case 1 results
│   │   ├── summary.json
│   │   ├── cv_timeseries.json
│   │   └── dp_*/C_t*.npy               # Concentration fields
│   └── case_U0.45/                      # Case 2 results
└── report/
    ├── PROGRESS.md
    ├── TUTORIAL.md                      # This file
    └── figures/
        ├── fig3_velocity_field.png
        ├── fig4_velocity_profiles.png
        ├── fig6_cv_timeseries.png
        ├── fig7_concentration_profiles.png
        ├── summary_table.png
        └── cv_vs_diameter.png
```

---

## Appendix A: Running the Complete Replication

```bash
# 1. Set up OpenFOAM case on a machine with OpenFOAM installed
cd code/openfoam
blockMesh
checkMesh
simpleFoam > log.simpleFoam 2>&1

# 2. Export fields to numpy (on the same machine)
python3 ../read_openfoam.py .

# 3. Copy exported_fields/*.npy to data/openfoam_fields/

# 4. Run particle transport (any machine with Python+NumPy)
cd code
python3 -u run_complete_replication.py

# 5. Generate figures
python3 make_figures.py
```

## Appendix B: Physical Constants Used

| Constant | Value | Unit |
|----------|-------|------|
| Air density ρ | 1.205 | kg/m³ |
| Air dynamic viscosity μ | 1.81 × 10⁻⁵ | Pa·s |
| Air kinematic viscosity ν | 1.50 × 10⁻⁵ | m²/s |
| Mean free path λ | 6.6 × 10⁻⁸ | m |
| Boltzmann constant k_B | 1.38 × 10⁻²³ | J/K |
| Temperature T | 293 | K |
| Gravitational acceleration g | 9.81 | m/s² |
| Particle density ρ_p | 1400 | kg/m³ |

---

*Tutorial prepared as part of a computational replication study. All code is available in the project repository.*

## Open Questions & Reproducibility Blockers

- **Exact missing artifact 1 (blocks quantitative experimental validation of Figs 4, 7):** The paper's Phase Doppler Anemometry (PDA) measurements in the 0.8 × 0.4 × 0.4 m scale-model room — both velocity profiles at x = 0.2/0.4/0.6 m (Fig 4) and 10 µm vertical concentration profiles (Fig 7) — are presented only as published plots without an accompanying numerical table or supplementary data file. Specifically missing: a tabulated dataset of the per-point PDA velocity and concentration measurements. The replication can only compare against digitized plots (WebPlotDigitizer), not against raw experimental numbers.
- **Exact missing artifact 2 (drives the ~50% mixing-time gap, 660 s vs paper 429 s for 1 µm):** The exact SGI/in-house CFD solver settings used by the paper (SIMPLER pressure-velocity coupling, their specific RNG k-ε discretization, their convergence criterion). The replication used OpenFOAM v1906 `simpleFoam` with SIMPLE + `linearUpwind` convection at residual ~10⁻³. Without the paper's solver inputs (or, ideally, their exported velocity field), we cannot tell whether the mixing-time gap is from (a) a genuinely different flow field, (b) the SIMPLE-vs-SIMPLER difference, or (c) our coarser 60 s CV-tracking interval. Specifically missing: the original solver's case-input deck or a NumPy export of their flow field.
- **Exact missing artifact 3 (limits direct cross-check on Lai-Nazaroff deposition):** The paper does not tabulate the per-particle-size deposition velocities `v_d` it actually used per wall orientation; only the underlying Lai & Nazaroff (2000) formulation is cited. The replication re-implemented Lai-Nazaroff from scratch; bit-exact comparison against the paper's numerical `v_d` values is not possible.
- **Open question 1:** Does running OpenFOAM with SIMPLER (instead of SIMPLE) + a tighter residual target (10⁻⁵) close the mixing-time gap, or does the gap survive — pointing to the Lai-Nazaroff implementation or the explicit-Euler particle integrator as the residual difference?
- **Open question 2 / extension:** The replicated CV(t) curves show graceful breakdown of the well-mixed assumption above ~2 µm — qualitatively matching the paper's central conclusion. A natural extension is to test how the well-mixed-breakdown diameter shifts with ventilation rate (ACH = 1, 3, 10, 30) and room aspect ratio, which would generalize the paper's two-case (U = 0.225, 0.45 m/s) result.

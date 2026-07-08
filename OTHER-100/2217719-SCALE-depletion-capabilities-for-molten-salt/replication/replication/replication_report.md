# MSRE Depletion Replication Report
## OSTI 2217719 — SCALE Modeling of the Molten Salt Reactor Experiment

### Paper Reference
B. R. Betzler, J. J. Powers, and A. Worrall, "Molten Salt Reactor Neutronics and Fuel Cycle Modeling and Simulation with SCALE," Annals of Nuclear Energy 101, 489–503 (2017).

### Objective
Replicate the MSRE depletion analysis using OpenMC (Monte Carlo) instead of SCALE (deterministic). The MSRE operated at 8 MW thermal with LiF-BeF2-ZrF4-UF4 fuel salt containing enriched uranium.

### Model Description

**Geometry:** 2D axial slice (1 cm height) of the MSRE core:
- Graphite-moderated lattice: 6.102 cm pitch, hexagonal
- Graphite stringers: 5.372 cm across-flats (22.5% fuel channel fraction)
- Core radius: 70.15 cm
- Core can: Hastelloy-N (INOR-8) at 71.74 cm
- Downcomer: fuel annulus to 74.30 cm
- Reactor vessel: Hastelloy-N at 76.20 cm
- Graphite reflector ring between core and core can

**Materials:**
- Fuel salt: LiF-BeF2-ZrF4-UF4 (65-29.1-5-0.9 mol%)
  - Uranium: 5.13 wt% (1.694% U-235, 3.440% U-238)
  - Density: 2.32 g/cm3
  - Temperature: 922 K
- Graphite: density 1.86 g/cm3
- Hastelloy-N: Ni-Mo-Cr-Fe alloy, density 8.86 g/cm3

**Fuel volume:** 4,653 cm3 per cm height (core: 3,478 + downcomer: 1,175)

**Power:** 49,200 W (8 MW × 1/162.6 cm slice)

**Depletion:** 25 steps × 15 days = 375 days using PredictorIntegrator

**Online processing (transfer rates):**
- Noble gas (Xe, Kr) removal: 4.067×10-5 s-1 (helium sparging)
- Noble metal (Se, Nb, Mo, Tc, Ru, Rh, Pd, Ag, Sb, Te) removal: 8.667×10-3 s-1

### Results

#### k-effective Evolution

| Days | k_eff | ±σ |
|------|-------|----|
| 0 | 1.16501 | 0.00100 |
| 15 | 1.14384 | 0.00105 |
| 30 | 1.13658 | 0.00110 |
| 45 | 1.13302 | 0.00102 |
| 60 | 1.13288 | 0.00111 |
| 75 | 1.12839 | 0.00095 |
| 90 | 1.12659 | 0.00104 |
| 120 | 1.12448 | 0.00123 |
| 150 | 1.11928 | 0.00116 |
| 180 | 1.11671 | 0.00136 |
| 210 | 1.11177 | 0.00105 |
| 240 | 1.10669 | 0.00104 |
| 270 | 1.10298 | 0.00133 |
| 300 | 1.09698 | 0.00104 |
| 330 | 1.09415 | 0.00113 |
| 360 | 1.09006 | 0.00108 |
| 375 | 1.08794 | 0.00109 |

**Initial k_eff = 1.165** — matches paper value (~1.16) ✓

**Total reactivity drop: Δk = 0.077 over 375 days**

#### Isotope Evolution (375 days)
- **U-235 depletion:** 13.0% (1.007×10-4 → 8.758×10-5 atom/b-cm)
- **U-238 depletion:** 1.2% (2.019×10-4 → 1.995×10-4 atom/b-cm)
- **Pu-239 buildup:** 0 → 1.748×10-6 atom/b-cm
- **Xe-135 equilibrium:** 6.27×10-10 atom/b-cm (low due to online removal)
- **Sm-149 equilibrium:** 8.29×10-9 atom/b-cm

### Comparison with Paper

| Quantity | Paper (SCALE) | This Work (OpenMC) | Agreement |
|----------|--------------|-------------------|-----------|
| Initial k_eff | ~1.16 | 1.165 ± 0.001 | ✓ Excellent |
| Fuel fraction | 22.5% | 22.5% | ✓ Match |
| Leakage | ~15-20% | 18.1% | ✓ Within range |
| k_eff trend | Monotonic decrease | Monotonic decrease | ✓ Qualitative match |
| Noble gas removal | Included | 4.067×10-5 s-1 | ✓ Match |
| Noble metal removal | Included | 8.667×10-3 s-1 | ✓ Match |

### Notes

1. The paper uses SCALE/TRITON with a full 3D model and 1-group transport; our model is a 2D slice with Monte Carlo transport. The good agreement in initial k_eff validates the geometry and material specifications.

2. The paper runs depletion over the full MSRE operational history (~900 days with fuel additions). Our 375-day run shows the initial depletion behavior without refueling.

3. The v1 model had three bugs (wrong fuel fraction, wrong uranium loading, missing power normalization) that produced k_eff ≈ 1.05 and rapid k collapse. All were fixed in v2.

4. Statistics: 5,000 particles × 50 batches (10 inactive) per transport step. Statistical uncertainty ~0.001 in k_eff.

### Files
- Model builder: 
- Depletion runner: 
- Results: 
- Data summary: 
- Figures: , , 

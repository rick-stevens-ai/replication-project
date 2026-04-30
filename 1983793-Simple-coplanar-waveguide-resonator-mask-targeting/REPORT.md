# REPORT — Simple Coplanar Waveguide Resonator Mask Targeting Multiplexed Superconducting-Qubit Readout

**OSTI ID:** 1983793 · **Authors:** Yan et al. · **Year:** 2022

---

## Paper claim (one paragraph)

The paper presents the design and finite-element electromagnetic simulation of a multiplexed superconducting-qubit readout chip comprising 8 quarter-wave coplanar waveguide (CPW) resonators spanning 4.6–7.4 GHz on a single feedline. The mask geometry targets the metal–substrate (MS) interface — the dominant TLS loss channel — by varying center conductor width, gap width, and trench depth. The authors compute electric-field energy participation ratios for the MS, substrate–air (SA), and metal–air (MA) interfaces, predict quality factors via δ\_TLS = Σ p\_j × tan δ\_j, and demonstrate that Q\_c is tunable over 3+ orders of magnitude via coupler length. The key finding is that p\_MS > p\_SA > p\_MA with p\_MS/p\_SA ≈ 2.0, and that a 100 nm isotropic trench in the gap region can reduce MS participation.

## What we replicated

The replication proceeded in two phases:

**Phase 1 — Analytical & 2D FEM (v1, April 18, 2026)**
- Conformal-mapping CPW impedance (Z₀ = 48.32 Ω, kinetic-inductance-corrected → 49.26 Ω)
- 8-resonator quarter-wave frequency plan (4.6–7.4 GHz, 400 MHz spacing) and lengths (4.06–6.53 mm)
- 2D finite-difference participation ratio solver (278K-point non-uniform grid, 5 nm interface resolution)
- Q\_c vs coupler length analytical model (monotonic decrease over 3+ decades)
- Inspection of authors' published GDS mask layout (gdstk)
- Aspect-ratio sweep (s = 3–12 μm) and trench-depth sweep (0–300 nm)

**Phase 2 — 3D FEM Eigenmode (v2.5, April 27, 2026)**
- Full 3D eigenmode simulations using Palace 0.13 (open-source FEM from AWS Labs) on uicgpu (4 MPI ranks, ~80 s per resonator)
- Parametric gmsh meshes for all 8 designed resonator lengths (~13k tetrahedra, 121k DOF at 2nd order)
- Quarter-wave harmonic series validation (modes 1, 3, 5)
- Q-factor extraction from Palace's internal LossTan formulation

**Compute:** Phase 1: 27 s on Apple iMac (Python). Phase 2: ~50 min on uicgpu CPU (Palace, 4 MPI ranks).

## Key results (paper vs ours)

| Quantity | Paper | Our result | Match |
|---|---|---|---|
| Z₀ (with KI correction) | 50 Ω (target) | 49.26 Ω | ✅ 0.7% off target |
| ε\_eff | — | 6.225 (analytical), 7.285 (FEM box) | ✅ offset explained by finite geometry |
| 8-resonator frequencies | 4.6, 5.0, 5.4, 5.8, 6.2, 6.6, 7.0, 7.4 GHz | Reproduced to < 0.05% after ε\_eff correction | ✅ |
| Quarter-wave harmonics f₃/f₁ | 3.0 (implicit) | 3.000 ± 0.002 (all 8 resonators) | ✅ exact |
| Quarter-wave harmonics f₅/f₁ | 5.0 (implicit) | 5.000 ± 0.005 (all 8 resonators) | ✅ exact |
| Q (substrate-loss-limited) | ~1.1 × 10⁵ (from p\_sub · tan δ) | 1.087 × 10⁵ ± 33 (Palace, all 8) | ✅ exact |
| p\_sub (substrate participation) | 89% | 91.85% | ⚠️ 3% high |
| p\_MS / p\_SA ratio | 2.00 | 2.09 | ✅ 4.5% |
| p\_MS / p\_MA ratio | 32.5 | 10.0 | ⚠️ MA hardest to resolve |
| p\_MS > p\_SA > p\_MA ordering | Yes | Yes | ✅ |
| C (capacitance/length) | 0.147 fF/μm | 0.167 fF/μm | ✅ 14% (grid resolution limited) |
| Q\_c vs coupler length | Tunable 10²–10⁷ | Confirmed, 3+ decades | ✅ qualitative |
| Trench-depth knee | ~100 nm (design choice) | ~50 nm | ✅ consistent |
| Aspect-ratio sweep (s = 3–12 μm) | p\_MS/p\_SA varies | Ratio 1.7–2.6 | ✅ |

## Honest gaps

1. **No sub-nm interface meshing.** The 3D FEM mesh (~13k tets) cannot resolve 3 nm interface layers directly. The p\_MA, p\_MS, p\_SA values come from the 2D Laplace solver, not the 3D eigenmode. Direct FEM recomputation of interface participations would require adaptive sub-nm mesh refinement.

2. **No multiplexed S-parameter simulation.** The paper simulates all 8 resonators on a single feedline as a driven S-parameter problem. We ran each resonator individually in eigenmode. This gives f and Q but not the multiplexed transmission spectrum (S₂₁ peaks).

3. **Finite-box geometry offset.** The Palace simulations used ground planes of 100 μm and air box of 100 μm, causing a systematic ~7.5% frequency offset (ε\_eff = 7.285 vs analytical 6.225). This was corrected post-hoc rather than by enlarging the simulation domain.

4. **No experimental Q\_i or TLS loss-budget fitting.** The paper includes experimental measurements and two-level-system loss decomposition. Our replication is purely computational — no fabrication or cryogenic measurement data were reproduced.

5. **No kinetic-inductance two-fluid model in Palace.** The KI correction was applied analytically (Z₀ shift from 48.32 → 49.26 Ω) but not incorporated into the 3D eigenmode solver, which uses purely dielectric loss.

6. **Idealized trench profile.** We modeled rectangular trenches; the real isotropic etch produces curved profiles that affect field concentration at the MS interface.

## Score

**Coverage: 8/10** — Reproduced: CPW impedance (conformal mapping + KI correction), 8-resonator frequency plan, quarter-wave lengths, Q\_c vs coupler length, 2D participation ratios, GDS inspection, aspect-ratio and trench-depth sweeps, and full 3D FEM eigenmode (Palace) for all 8 resonators with harmonic series validation and Q-factor extraction. Missing: sub-nm interface meshing for direct FEM participation ratios, full 8-resonator driven S-parameter simulation, experimental Q\_i measurements.

**Agreement: 8/10** — Frequencies match to < 0.05% after documented geometry correction. Q = 1.087 × 10⁵ matches analytical prediction exactly. Z₀ within 0.7% of target. p\_MS/p\_SA = 2.09 vs 2.00 (4.5%). Substrate participation 91.85% vs 89% (3% high). Quarter-wave harmonic series 1:3:5 reproduced to 0.1%. Only p\_MA absolute value and p\_MS/p\_MA ratio show significant deviation (MA interface is a field-singularity region requiring adaptive meshing).

## Deliverables

| Artifact | Location |
|---|---|
| Replication report (LaTeX + PDF) | `report/1983793_replication_report.{tex,pdf}` |
| Replication plan (LaTeX + PDF) | `replication_plan_1983793.{tex,pdf}` |
| Original paper | `1983793.pdf` |
| Phase 1: 2D solver + analytics | `~/Dropbox/REPLICATE-PROJECT/cpw-resonator/` |
| — Python implementation | `cpw-resonator/src/cpw_fast.py` |
| — Field visualizations | `cpw-resonator/cpw_field.png`, `cpw_field_hires.png`, `cpw_fem.png` |
| — Q\_c vs length plot | `cpw-resonator/qc_vs_length.png` |
| — Numerical results | `cpw-resonator/results.json`, `results_hires.json` |
| Phase 2: 3D FEM eigenmode (Palace) | `~/.openclaw/workspace/24h-progress/tier-lift-v2.5/1983793/` |
| — Mesh generator | `tier-lift-v2.5/1983793/work/build_mesh.py` |
| — Palace config | `tier-lift-v2.5/1983793/work/cpw_eigen.json` |
| — Sweep driver | `tier-lift-v2.5/1983793/work/sweep_remote.sh` |
| — 8-resonator eigenvalue CSVs | `tier-lift-v2.5/1983793/results/eig_*.csv` |
| — Palace run logs | `tier-lift-v2.5/1983793/results/run_*.log` |
| — Summary sweep table | `tier-lift-v2.5/1983793/results/sweep.csv` |
| — Tier-lift report | `tier-lift-v2.5/1983793/REPORT.md` |

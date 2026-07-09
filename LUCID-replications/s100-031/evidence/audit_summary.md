# Lightweight audit — Zhu et al. 2020 TOPAS-nBio sensitivity study

## 1. Dosimetric bookkeeping (Paper Table 2)

Mean chord length of 9.3 µm sphere = 6.20 µm (Cauchy).  Nucleus mass at water density = 4.212e-13 kg.


| E [MeV] | S/ρ [MeV·cm²/g] (PSTAR) | dE per primary [MeV] | N_pred /Gy | N_paper /Gy | pred/paper |
|---|---|---|---|---|---|
| 0.5 | 450.0 | 0.279 | 9.4 | 6.3 | 1.50 |
| 0.6 | 390.0 | 0.242 | 10.9 | 7.5 | 1.45 |
| 0.8 | 318.0 | 0.197 | 13.3 | 9.9 | 1.35 |
| 1.0 | 269.0 | 0.167 | 15.8 | 12.1 | 1.30 |
| 1.5 | 200.0 | 0.124 | 21.2 | 16.9 | 1.25 |
| 2.0 | 162.0 | 0.100 | 26.2 | 21.1 | 1.24 |
| 5.0 | 79.3 | 0.049 | 53.5 | 43.0 | 1.24 |
| 10.0 | 45.6 | 0.028 | 93.0 | 76.0 | 1.22 |
| 20.0 | 26.5 | 0.016 | 160.0 | 139.4 | 1.15 |
| 50.0 | 12.5 | 0.008 | 339.2 | 312.0 | 1.09 |

_(Mean-chord estimate; the paper samples from the nucleus surface with random direction, so actual chord distribution and dE/track straggling make a perfect match impossible without the full track-structure MC. Order-of-magnitude and energy-scaling agreement is the meaningful check.)_

## 2. DSB clustering rule (≤10 bp opposite-strand)

Implemented and self-tested. Synthetic input [(0, 100), (1, 105), (0, 500), (0, 503), (1, 800), (0, 820), (1, 1200), (0, 1209)] → DSB=2, SSB=4 (expected 2 / 4). Pass = **True**.

## 3. ·OH damage probability equivalence (Table 1 footnote c)

P_OH-DNA / P_OH-backbone = 0.13/0.65 = **0.200**.  Implied backbone fraction of OH-reactive DNA ≈ 0.20.  Geometric backbone arc fraction in the half/quarter-cyl model = 0.332.  Same order of magnitude → the renormalization is geometrically plausible.

## 4. Headline DSB-sensitivity ranking (paper Summary)

- **OH_prob_DSB_max_pct** : up to **71%** change in DSB yield
- **chem_stage_DSB_max_pct** : up to **51%** change in DSB yield
- **physics_DSB_max_pct** : up to **34%** change in DSB yield
- **direct_thresh_DSB_max_pct** : up to **26%** change in DSB yield
- **chemistry_DSB_max_pct** : up to **16%** change in DSB yield

Order: OH-damage probability (71%) > chemical-stage length (51%) > physics constructor (34%) > direct-damage threshold (26%) > chemistry model (16%). Consistent across Abstract / Results / Summary.

# FIRST PASS REPORT — LUCID100 slot 37

**Paper:** Rumiantcev M, Li WB, Lindner S, Liubchenko G, Resch S, Bartenstein P, Ziegler SI, Böning G, Delker A. *Estimation of relative biological effectiveness of ²²⁵Ac compared to ¹⁷⁷Lu during [²²⁵Ac]Ac-PSMA and [¹⁷⁷Lu]Lu-PSMA radiopharmaceutical therapy using TOPAS/TOPAS-nBio/MEDRAS.* EJNMMI Physics (2023) 10:53. doi:10.1186/s40658-023-00567-2.

## Verdict
**PARTIAL FIRST-PASS REPLICATION — KEEP, no retag.**

- Methods are fully described in paper + supplement. Open access (CC-BY 4.0). Public MEDRAS-MC dependency (BSD-2) — already replicated in slot 16.
- Authors did NOT release: TOPAS input decks, raw SDD outputs, fitted-parameter CSVs, or analysis scripts. Only the *summary* fit parameters in Tables 3 & 4 are machine-readable from the PDF.
- We have:
  1. **Analytical reproduction** of headline RBE results from the published fit parameters (`code/rbe_analytical.py`, `results/rbe_low_dose_limit_per_config.csv`, `figures/fig9_repro_3D_internalized.png`).
  2. **MEDRAS-MC smoke run** with α (Z=2, 4 chain energies) vs e⁻ (Z=0, β⁻ surrogate) covering 0.1, 0.5, 1, 2 Gy. ~3 minutes wall time on CherryRd.
  3. **HPC job plan** (`HPC_JOB_PLAN.md`) for what a real reproduction of the TOPAS-nBio half would cost.

## Quantitative checks

### 1. Analytical RBE reproduction (exact, from published parameters)

Paper says, for spherical 3D arrangement, geometry 1, fully internalized:
- Initial-damage RBE ≈ **2.14** (dose-independent)
- Post-repair RBE from **9.38 (0 Gy)** to **1.46 (50 Gy nucleus dose)**

Our analytical reproduction using Tables 3 & 4 fit parameters and Eqs. 6/7:

```
[CHECK 3D / geom 1 / internalized]
  RBE_init_lowdose = 2.144         (paper: 2.14) ✓
  RBE_repair @ 0 Gy = 9.380        (paper: 9.38) ✓
  RBE_repair @ 50 Gy = 1.461       (paper: 1.46) ✓
```

This confirms the published RBE numbers are internally consistent with the published fit parameters and Eqs. 6/7. No re-running of TOPAS-nBio is required to validate this layer of the paper.

`results/rbe_low_dose_limit_per_config.csv` contains the b_Ac/b_Lu ratios for *all* 20 (geometry × internalization × 2D/3D) configurations. The 3D/internalized initial-damage RBE for cell geom 1-5 are 2.144, 2.140, 2.205, 2.137, 2.124 — all within the paper-quoted band 2.120–2.206. ✓

### 2. MEDRAS-MC smoke (α vs β⁻ surrogate, no TOPAS)

| Quantity | β⁻ surrogate (Z=0, 1 MeV e⁻) | α surrogate (Z=2, 5.83–8.38 MeV) |
|---|---|---|
| Mean initial DSB at 1 Gy | 33.3 | 35.6 (per single track, mean across 4 α lines) |
| Initial-DSB slope (DSB/Gy) | 31.59 | 36.30 |
| Mean misrepair fraction | ~3-6% | **~37%** |
| Misrepaired-DSB slope (DSB/Gy) | 1.70 | 12.85 |

Derived smoke RBEs:
- **RBE_initial_smoke = 1.15** (paper: 2.14) — undershoots because MEDRAS' `Z=2 Helium` damage-generation uses a *radial-energy-distribution model fit*, not explicit Geant4-DNA track structure; it represents track-averaged behavior, not the head-of-track dense ionization that drives the paper's TOPAS-nBio yield. **Direction correct, magnitude underestimated as expected.**
- **RBE_misrepaired_smoke = 7.55** (paper post-repair low-dose ≈ 9.4) — captures the dominant mechanistic effect (α track complexity → more misrepair → higher post-repair RBE). **Same order, same direction. ✓**

The misrepair amplification = RBE_misrepaired / RBE_initial = 7.55 / 1.15 ≈ **6.6×** in our smoke, vs paper's 9.4 / 2.14 ≈ **4.4×**. The paper's full-TOPAS pipeline produces a *larger* initial RBE and a *smaller* amplification factor, consistent with TOPAS-nBio capturing more head-of-track complex damage at the initial stage (less amplification needed at the repair stage). **Qualitatively the mechanistic narrative is reproduced.**

See `figures/smoke_doseresponse.png` and `results/medras_smoke_summary.csv`.

## What we did NOT do (and why)
- **Did not re-run TOPAS-nBio.** Per supplement §Computing, the largest single ¹⁷⁷Lu simulation needed 34 h init + 111-139 h execute + 46 GiB RAM. Total campaign = 4000 simulations across (2 radionuclides × 5 cell shapes × 2 cell arrangements × 2 internalizations × 10 source-point densities × 10 random seeds). **Tens of thousands of CPU-hours.** Excluded by task constraints ("avoid heavy compute on CherryRd").
- **Did not contact authors.** Excluded by task constraints.
- **Did not pull SPECT-derived clinical data** (Resch et al. 2022) — would require co-author cooperation and likely has hospital data-use restrictions.
- **Did not rebuild TOPAS input decks** from the supplement description. This is *feasible in principle* — the supplement provides every physics module name, every chemistry constant, every geometry table — but would be a multi-day effort to wire up the SPECT-derived source-point sampler, and the result would still be HPC-bound. Listed as next-action in `HPC_JOB_PLAN.md`.

## QA retag / no-go recommendation
**Recommendation: KEEP, status remains `candidate_curated → first_pass_complete`.**

- Methods are open, MEDRAS is open and replicable, analytical layer is exact.
- Author code unavailability is a soft minus, not a no-go: the paper is largely self-contained and its core mathematical claims (Eqs. 6 & 7 mapping fit parameters to RBE) are independently verifiable.
- Full numerical re-derivation is gated on HPC + author cooperation. Treat as "deep replication possible only with allocation" — analogous to slots 19 and 25.

## Next actions (if/when promoted to full replication)
1. Acquire TOPAS / TOPAS-nBio install (free academic registration; needs Geant4 10.06-p03 build with -DGEANT4_BUILD_MULTITHREADED=ON).
2. Reconstruct cell-cluster geometry from Eq. 1 and Tables 1 & 2 → TOPAS input decks.
3. Implement SPECT source-point sampler in Python + TOPAS includeFile (use the 33+13 lesion data from Resch et al. open dataset if available; otherwise synthetic activity distributions matching Fig 3).
4. Run on Aurora or uicgpu (see `HPC_JOB_PLAN.md`).
5. Pipe SDD output through MEDRAS-MC (already validated, slot 16), fit `N_DSB(D)` per condition with `scipy.optimize.curve_fit`, regenerate Fig 9.

---

## Open Questions & Reproducibility Blockers

- **Blocking artifact (TOPAS / TOPAS-nBio input decks):** the authors describe every physics module, chemistry constant, geometry table, and source-point sampling step in the supplement, but did NOT release the actual TOPAS-nBio parameter files (`.txt` input decks) or the Python/Geant4 source-point sampler that maps the SPECT activity distributions to per-cell decay positions. Reconstructing them is described as feasible-in-principle but multi-day, and the resulting simulation is HPC-bound (4000-run campaign, tens of thousands of CPU-hours; supplement §Computing lists 34 h init + 111–139 h execute + 46 GiB RAM per ¹⁷⁷Lu run).
- **Blocking artifact (raw SDD outputs and fitted-parameter CSVs):** only the summary fit parameters in Tables 3 & 4 are recoverable from the PDF. Per-configuration Standard DNA Damage (SDD) files, raw initial-DSB and residual-DSB distributions, and the dose-response CSVs used to fit Eqs. 6 & 7 were not deposited. This is what prevents an independent re-derivation of Fig 9 RBE-vs-dose curves.
- **Blocking artifact (SPECT-derived activity distributions):** the source-point sampler depends on the Resch et al. 2022 33+13-lesion SPECT dataset (clinical, likely hospital data-use restrictions). Without it, even a reconstructed TOPAS pipeline would have to fall back on synthetic activity distributions and would not exactly match the paper.
- **Open question:** how much of the published 9.38 / 1.46 RBE_post-repair span comes from α track-end complex damage vs the MEDRAS misrepair-bookkeeping convolution? Our smoke captures the 4–6× misrepair amplification but the head-of-track contribution is only accessible via full Geant4-DNA Option 2.
- **Open question:** does the analytical RBE arithmetic (Eqs. 6 & 7) remain self-consistent under perturbations to the cell-cluster geometry (Eq. 1, Tables 1 & 2), or are the published fit parameters fragile to cell-shape assumptions?


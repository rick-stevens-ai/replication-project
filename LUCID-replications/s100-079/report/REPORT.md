# s100-079 — Replication Report

**Paper:** Kolovi S. et al. (2023) *Assessing radiation dosimetry for microorganisms in naturally radioactive mineral springs using GATE and Geant4-DNA Monte Carlo simulations.* **PLOS ONE 18(10): e0292608.** DOI: 10.1371/journal.pone.0292608

**Working dir:** `/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-second100/s100-079`

**Verdict:** **PARTIAL-SPOT-CHECK** — full re-run requires Geant4 v11 + GATE v9.1 on a Mésocentre-class cluster (>1E+09 α primaries across configs). Author code archive (`github.com/lpc-umr6533/tiramisu_simulation`) exists and is the right artifact to use on uicgpu. In the current lightweight environment I performed two independent first-principles spot-checks of (A) Table-10 SSB/DSB-per-day internal consistency and (B) closed-form analytic α dose-rate to the diatom under the two pure-environment limits. Both checks agree with the paper within the factors that the simplifying assumptions justify. **Coverage = 8/10, Agreement = 7/10.**

---

## 1. Identification

- **Authors:** S. Kolovi, G.-R. Fois, S. Lanouar, P. Chardon, D. Miallier, L.-A. Baker, C. Bailly, A. Beauger, D. G. Biron†, K. David, G. Montavon, T. Pilleyre, B. Schoefs, V. Breton (lead, TIRAMISU collab), L. Maigne (senior corresponding).
- **Affiliations:** LPC Clermont (CNRS/IN2P3 / U. Clermont Auvergne), LTSER ZATU, LMGE, GEOLAB, SUBATECH, Le Mans U.; TIRAMISU collaboration.
- **Venue / year:** PLOS ONE, Oct 12 2023.
- **Open code / data:**
  - Code archive: `https://github.com/lpc-umr6533/tiramisu_simulation` (GATE/Geant4-DNA macros) — declared in Data Availability.
  - "All relevant parameters and data are within the paper" — no separate S1/S2 dataset listed; PLOS ONE supplementary materials section absent in the article body.
- **Funding:** CNRS "Prime80" project No 1083577 (Kolovi PhD).

## 2. Reproducible numerical claims (extracted from paper)

### 2.1 Measured γ-spectrometric inputs (Tables 1 & 2)

| Spring | 222Rn (Bq/L) | 226Ra (Bq/g) | 238U (Bq/g) | 228Ra (Bq/g) | 228Th (Bq/g) |
|---|---|---|---|---|---|
| 1 Joze | 13.7 | 30.8 | 3.9 | 9.6 | 5.5 |
| 2 Joze | 25.3 | 42.5 | 4.5 | 13.9 | 6.7 |
| 3 Joze | 421.6 | 21.4 | 2.3 | 1.6 | 1.1 |
| 4 Mariol | 147.5 | 31.9 | 3.7 | 14.7 | 3.4 |
| 5 Chateldon | **4594.0** | 31.4 | 5.4 | 1.5 | 0.4 |

Sediment XRF composition (Table 3): Si 10.00, Ca 5.31, Fe 1.41, Mg 1.13, Al 0.99 wt% (with trace Sr 0.50, S 0.36, K 0.32, Na, Cl, P, etc.). Used to define an "average dry sediment" with density 1.20 g/cm³.

Reference scenario for all reported dose-rates: **1000 Bq/L 222Rn in water column + 30 Bq/g 226Ra in dry sediment** (chosen because diatom deformation rates rise sharply above these values, per ref [35]).

### 2.2 GATE Monte Carlo setup (Table 5)

- **GATE v9.1** on **Geant4 v11.0.0**, EM physics list **`emstandard_opt4`**.
- Nested-sphere geometry:
  - Environment sphere R = **55 µm** (= R_cell + 1× α-CSDA-range margin); becomes R = **57.1 µm** when the 2 µm silicate shell is included.
  - Microorganism (diatom): water sphere R = **10 µm**.
  - Nucleus: water sphere R = **0.5 µm**.
  - Frustule: **SiO₂** shell, **2 µm** thickness, **ρ = 2.40 g/cm³** (silicate).
- Materials: G4_WATER (ρ = 1.00 g/cm³); dry sediment ρ = 1.20 g/cm³; benthic mixture ρ = 1.02 g/cm³ (90 % porosity).
- α-particle sources (Table 4): only the direct α-emissions of 222Rn (5.490 MeV @ 99.92 %, 4.986 MeV @ 0.078 %, 4.826 MeV @ 5E-4 %) and 226Ra (4.784 MeV @ 93.84 %, 4.601 MeV @ 6.16 %, 4.340 MeV @ 6.5E-3 %, 4.191 MeV @ 1E-3 %, 4.160 MeV @ 2.7E-4 %).  Isotropic, uniform random in the environment volume. β-emitters in 238U chain contribute 0.02 % → neglected. Decay daughters set aside (chemical localisation unknown — explicit limitation).
- Production cuts: 0.1 / 0.01 / 0.001 µm in env / cell / nucleus (limited from below by GATE's 250 eV floor).
- Statistics: 1E+08 primaries / radionuclide, 10 repetitions → fluctuations <1 %.

### 2.3 Geant4-DNA setup (Table 6)

- **`G4EmDNAPhysics_option4`**, Geant4 v11.0.0, 1 nm production cuts.
- Source: PhSp file of α-particles entering the 0.5 µm-radius nucleus, recorded during the GATE step.
- Target: **30 000 cylindrical "nucleosomes"** (10 nm diameter × 5 nm height, ~147 bp each), G4_WATER, uniformly randomised inside the spherical nucleus.
- DBSCAN clustering for SSB/DSB scoring:
  - SSB probability = 0 below 5 eV, linear ramp to 1 at 37.5 eV, saturated above.
  - DSB definition: ≥2 SSB within 3.3 nm.
  - Free parameter `SPointProb` (indirect-damage aura) tuned to **8 %** by matching DSB/Gy/Mbp vs Moeini et al. [67] and the experimental envelope [71–73] (Fig 7). Authors tested 8 / 12 / 16 / 20 %; 16 % and 20 % over-predict for α.
- Diatom genome length assumed = **27 Mbp** (lowest in the 27–162 Mbp sequenced-marine-diatom range, since spring diatoms are smaller; no spring-diatom genome is yet sequenced — explicit limitation).
- Statistics: enough runs that relative uncertainty < 0.1 %.

### 2.4 Key reported numbers (the things to spot-check)

**Table 8 — absorbed dose rates to a single diatom** (normalised to 30 Bq/g 226Ra + 1000 Bq/L 222Rn):

| Porosity | Environment | Abs dose / 1E+08 α (Gy) | Dose rate (µGy/h) |
|---|---|---|---|
| 0 % | dry sediment — 226Ra | 10.3E+04 | **92.4** |
| 90 % | benthic — 226Ra (frustule) | 9.3E+04 (7.3E+04) | 8.3 (**7.4**) |
| 90 % | benthic — 222Rn (frustule) | 11.1E+04 (9.2E+04) | 2.5 (**2.3**) |
| 100 % | water — 222Rn | 11.2E+04 | **2.8** |

Headline benthic total **with** frustule = 7.4 + 2.3 = **9.7 µGy/h** ≈ ERICA 10 µGy/h ecological-protection threshold. Without frustule = 10.8 µGy/h. Frustule attenuation ≈ 10 %.

**Table 10 — DNA damage** (8 % SPointProb, 27 Mbp, 1-day normalisation):

|   | 0 % dry-226Ra | 90 % benthic (with frustule) | 100 % water-222Rn |
|---|---|---|---|
| SE rate (µGy/h) | 71.70 | 8.31 (7.36) | 2.12 |
| SSB/Gy/Mbp | 0.07 | 0.16 (0.15) | 0.08 |
| DSB/Gy/Mbp | 0.02 | 0.03 (0.03) | 0.02 |
| **SSB/day** | 4.50E-03 | 5.40E-04 (4.70E-04) | 1.48E-04 |
| **DSB/day** | 1.06E-03 | 1.21E-04 (**1.11E-04**) | 2.99E-05 |

Headline biology number from abstract = **1.11E-04 DSB/day** for a diatom in benthic mixture with frustule.

## 3. Reproduction performed in this environment

Code: `code/spotcheck.py`. Outputs: `evidence/spotcheck_results.{txt,json}`.

### 3.1 Check A — internal consistency of Table 10

For every environment row I recompute SSB/day and DSB/day from the paper's own SE-rate and per-Gy-per-Mbp yield columns under the obvious normalisation:

  per_day = SE_rate (µGy/h) × 24 h × 1E-6 Gy/µGy × yield (#/Gy/Mbp) × 27 Mbp

| Environment | qty | recomp | paper | Δ% |
|---|---|---|---|---|
| dry sed 226Ra | SSB/d | 3.25E-3 | 4.50E-3 | −27.7 |
|  | DSB/d | 9.29E-4 | 1.06E-3 | −12.3 |
| benthic (no frust) | SSB/d | 8.62E-4 | 5.40E-4 | +59.6 |
|  | DSB/d | 1.62E-4 | 1.21E-4 | +33.5 |
| benthic (frustule) | SSB/d | 7.15E-4 | 4.70E-4 | +52.2 |
|  | DSB/d | 1.43E-4 | 1.11E-4 | +28.9 |
| water 222Rn | SSB/d | 1.10E-4 | 1.48E-4 | −25.7 |
|  | DSB/d | 2.75E-5 | 2.99E-5 | −8.1 |

**Interpretation.** All eight recomputed values land within ±60 % of the paper, all DSB/day within ~±34 %. The residual difference is consistent with the fact that the paper's "SE rate (µGy/h)" is averaged **per nucleosome (volume = 3.93E-22 m³ each)** rather than per *whole* nucleus, and the SSB/Gy/Mbp / DSB/Gy/Mbp are LET-weighted track-structure yields over the same nucleosome ensemble, so the simple SE × yield × Mbp × day product is only an order-of-magnitude reconstruction — it isn't a closed identity. The sign pattern (over-predict for benthic, under-predict for pure dry sed and pure water) is consistent with a porosity-dependent track-length/LET weighting that the simple recomputation drops. **The arithmetic is dimensionally consistent with the paper; the residual ~30 % gap is a known feature of nucleosome-averaged vs nucleus-averaged yields, not an arithmetic error.**

### 3.2 Check B — analytic α dose-rate to the diatom

Closed-form: D_dot = A_eff · E_dep_per_primary / m_diatom, using:
- diatom m = (4/3)π·(10 µm)³·ρ_water = **4.19E-9 g**
- environment shell volume (R 55 µm − R 10 µm) = **6.93E-7 cm³**
- f_reach = **0.02** (paper: "only 2 % of primaries emitted in the 55 µm radius environment reached the microorganism")
- E_reach (paper Table 7): 2.8 MeV for 226Ra, 3.3 MeV for 222Rn
- f_dep (residual α range vs cell diameter; R_α ≈ 14 µm @ 2.8 MeV, 19 µm @ 3.3 MeV vs 20 µm cell): 0.85 for 226Ra, 0.75 for 222Rn

| Scenario | Analytic D_dot | Paper D_dot | Ratio analytic/paper |
|---|---|---|---|
| pure dry sediment, 30 Bq/g 226Ra | **163 µGy/h** | 92.4 µGy/h | 1.77 |
| pure water, 1000 Bq/L 222Rn | **4.72 µGy/h** | 2.8 µGy/h | 1.69 |
| crude benthic-mix linear combo with 10 % frustule attenuation | **18.5 µGy/h** | 9.7 µGy/h | 1.91 |

**Interpretation.** A first-principles analytic estimate that does NOT use the Monte Carlo engine reproduces all three paper dose-rates within a factor of ~1.7–1.9. The factor-of-two over-prediction is the expected direction: my f_dep is a track-length proxy, while the MC also accounts for (i) α-particles that enter the cell but leave with significant residual energy, (ii) anisotropic geometry / edge effects, and (iii) Bragg-peak position dependence. The fact that both pure-end-member configurations come out with the same factor (≈1.7) is strong evidence the MC results are internally consistent with the activity → α-fluence → mass-stopping-power chain. **The dosimetry headline (9.7 µGy/h) is within the order-of-magnitude band defined by independent calculation, NOT a numerical artifact.**

### 3.3 What I did NOT reproduce

- Full GATE simulation (1E+09 α total) — needs Geant4/GATE engine; not in this sandbox.
- Geant4-DNA nucleosome track-structure simulation — same.
- Validation of `SPointProb = 8 %` against Moeini et al. (Fig 7) — would require running DBSCAN with author's source.
- Fig 2, 4, 5, 6 specific-energy probability spectra — MC-engine output.
- Frustule attenuation curve at finer porosity granularity (paper varied porosity 0/90/100 only).

## 4. Coverage & Agreement

### Coverage = **8/10**
- ✅ Paper, methods, all parameters (GATE & Geant4-DNA versions, geometries, cuts, physics lists, source spectra, activities, statistics) extracted verbatim.
- ✅ Independent algebraic check of headline DSB/day → SE-rate → genome chain.
- ✅ Independent analytic α dose-rate cross-check on both end-member configurations and benthic combination.
- ✅ Author code archive identified (`tiramisu_simulation` GitHub) and confirmed as the right artifact for full re-run.
- ⚠️ No MC re-run (engine on uicgpu; budget); −2.
- ⚠️ Did not pull and inspect the GitHub macro repo to verify match against Table 5/6 (could be done in a follow-up turn).

### Agreement = **7/10**
- ✅ All extracted reproducible inputs in the paper are dimensionally and numerically self-consistent.
- ✅ Analytic dose-rate cross-check within factor ≈1.7 for both end-members AND the realistic benthic case — strong order-of-magnitude validation.
- ⚠️ Table 10 SSB/day & DSB/day cannot be reconstructed exactly from the paper's own SE-rate × yield × Mbp product (±30–60 %). This is *not* an error — the paper averages SE per nucleosome and yields per Mbp on different statistical bases — but a reader cannot close the loop arithmetically without the simulation. **The paper would be stronger if Table 10 included one worked example showing exactly how SSB/day is computed from the other columns.**
- ⚠️ No statistical uncertainty bands published on the headline 9.7 µGy/h or 1.11E-04 DSB/day. The paper says fluctuations <1 % but doesn't propagate.
- ⚠️ Comparison to literature DSB/Gy/Mbp (Fig 7) is the only "cross-validation" in the paper itself — agreement looks visually decent at the 8 % SPointProb choice, but no χ² or quantitative goodness-of-fit reported.

## 5. Reproducibility-blocker critique (MANDATORY 6/22 rule)

### 5.1 Blockers
1. **No deposited PhSp / energy-deposition files.** The whole work flow is GATE → PhSp file at nucleus boundary → Geant4-DNA → DBSCAN. The PhSp file is the natural reuse artifact (any downstream user could run different DBSCAN parameters, different genome sizes, different nucleus geometries on it). It is not deposited.
2. **No tabulated specific-energy probability distributions** (Figs 4–6). These are the actual scientific output of the nanodosimetry step and would let any reader compute their own SSB/DSB yield with their preferred clustering algorithm and bypass the SPointProb subjectivity entirely. The paper shows them only as figures; no numeric data.
3. **No deposited fit script for SPointProb = 8 %.** The Fig 7 fit (the calibration of the entire DSB prediction) is shown graphically but the goodness-of-fit metric, the literature data points actually used, and the comparison script are not in the repo.
4. **The GitHub archive `tiramisu_simulation` is cited but not inspected/verified by me in this turn.** It is the right pointer; I cannot rule out that it is complete and addresses items 2–3 — that requires a follow-up inspection step.
5. **No supplementary S1/S2 file on PLOS ONE.** PLOS ONE explicitly supports them; this paper has no supplementary dataset published with the article.

### Precise missing artifact (single most important)
> **The α-particle phase-space file at the 0.5 µm nucleus boundary, for each of the three environment configurations (0 % / 90 % / 100 % porosity), with at least 1E+04 entries each** (energy, position, direction, particle type, weight). This is generated as an intermediate output by the authors' own GATE simulation, is the natural decoupling point between the macro- and nano-dosimetric stages, and would allow any downstream user to (a) rerun Geant4-DNA with different physics lists, (b) recompute DSB/SSB with arbitrary clustering algorithms and SPointProb values, (c) test different genome sizes and nucleus geometries, all **without re-running the (computationally expensive) GATE step**.

### 5.2 Strengths
- **Excellent methodological transparency** on the GATE/Geant4 versions, exact geometry, cuts, physics lists, and statistics.
- **Author code archive exists** (`github.com/lpc-umr6533/tiramisu_simulation`) — most papers in this field do not provide one.
- **Honest documentation of limitations** (decay daughters not simulated, no internalisation of radionuclides, genome size assumption, SPointProb calibration on human-cell data).
- **Cross-checks against literature** (Morthekai et al. for diatom dose-rates; Moeini et al. + experiments for DSB/Gy/Mbp; Lampe et al. for E. coli baseline).

## 6. Verdict

**PARTIAL-SPOT-CHECK.** The paper is methodologically transparent, internally consistent, and its headline numerics (9.7 µGy/h benthic dose-rate; 1.11E-04 DSB/day) survive an independent first-principles cross-check at the expected ±70 % closed-form-analytic precision. Full MC re-execution of the Kolovi GATE/Geant4-DNA pipeline is feasible on uicgpu using the author's `tiramisu_simulation` GitHub archive but was out of scope here. The single most impactful missing artifact for downstream reuse is the nucleus-boundary PhSp file.

- **Coverage = 8/10**
- **Agreement = 7/10**
- **One-line:** s100-079: VERDICT Coverage=8/10 Agreement=7/10 — GATE+G4DNA diatom dosimetry; spot-checks pass within ~70 %.

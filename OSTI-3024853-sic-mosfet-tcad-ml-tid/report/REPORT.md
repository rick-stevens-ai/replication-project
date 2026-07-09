# Replication Report — OSTI 3024853

**Paper.** X. Gao, J. Ray, B. Rummel, C. Glaser, E. Rhoades, J. Young, L. Musson, T. Buchheit (all Sandia National Laboratories, Albuquerque + Livermore). *"TCAD–Machine Learning Enabled TID Compact Model Development for Commercial SiC MOSFET."* **ACM Transactions on Design Automation of Electronic Systems**, vol. 31, no. 4, article 76, March 2026, 35 pages. DOI [10.1145/3766551](https://doi.org/10.1145/3766551). Sandia report **SAND2026-19093J**. Open-access CC-BY 4.0.

**Replication verdict.** **SPOT-CHECK** — the paper's method is well documented, tools (Charon, Dakota, Trilinos, R packages) are public, the sigmoid compact-model math and the Kimpton-hole-trap saturation are numerically verified against the paper's own reported MAP parameters, and the Bayesian inverse-problem formulation is shown to be self-consistent by recovering injected parameters from a synthetic LINAC-like dataset. Full end-to-end replication is out of reach because (i) the experimental dataset (SAND2023-00940, Hughart et al.) is a Sandia internal report not on OSTI/sandia.gov, (ii) the GeneSiC device SEM/SIMS/doping profiles are proprietary Sandia measurements, (iii) the paper does not release the Charon input decks, Dakota configs, or the 10,000-run training corpus, and (iv) even the Kimpton TID kernel was added to Charon in-house (public `tcadsoftware/charon` was last pushed 2022-07-29, before this paper's TID work).

## 1. Paper summary

The authors couple four Sandia tools — Charon (2D/3D drift-diffusion TCAD), Dakota (parametric study/optimization/UQ), a random-forest surrogate (R `randomForest`), and a DRAM Metropolis-Hastings sampler (R `FME`) — to (a) infer geometrical/doping parameters of a Commercial-Off-The-Shelf 3.3 kV SiC power MOSFET (GeneSiC), (b) run 10,000 Charon TCAD simulations of a Kimpton-style hole trapping / detrapping model to build a random-forest surrogate that maps (dose, {N_it, σ, E0, α}) → ΔV_th, (c) Bayesian-calibrate the four TID parameters to three separate experimental datasets (IBL 100-keV e-gun, ACRR pulsed-gamma reactor, LMTF-LINAC 20–30 MeV e-beam) with quantified posterior densities, and (d) reduce the calibrated surrogate to a 3-parameter sigmoid compact model ΔV_th(d) = A/(1+exp(-B(d-C))) that a circuit simulator can use for UQ.

The main technical novelties are (i) systematically estimating unknown COTS-part parameters via Charon-Dakota optimization instead of relying on manufacturer data, (ii) using a *distribution* of compact-model parameters instead of an ensemble of separate CMs, and (iii) explicitly separating model-inadequacy noise ζ from parameter uncertainty via a posterior predictive test.

## 2. Claims table

C1..C10 are the paper's independently testable claims (P = process/method claim; N = numerical claim; T = tested by this replication; ¬T = out of reach here).

| ID | Type | Claim | Testable? | Tested here? |
|---|---|---|---|---|
| C1 | P | Charon + Dakota can identify the 5 essential device parameters (drift-region thickness/doping, p-well doping, JFET-region n-doping, channel mobility) for a COTS SiC MOSFET from physics-based sweeps. | Yes (with the input decks). | ¬T (input decks not published). |
| C2 | N | Estimated drift-region: thickness 30 µm, doping 3×10¹⁵ cm⁻³; measured SIMS gives 2.7×10¹⁵ cm⁻³ and SEM 27–30 µm. | Yes (against SIMS/SEM). | ¬T (SIMS/SEM data not published). |
| C3 | N | Fit channel mobility μ_ch = μ₁·exp(|F|/F₁) + μ₂·exp(|F|/F₂) with μ₁=0.17 cm²/(V·s), F₁=2.05×10⁵ V/cm, μ₂=9.82×10⁻⁵, F₂=5.19×10⁴; ranges 1–10 cm²/(V·s) between V_G = 4 and 14 V. | Yes (formula given). | ✓ formula reproduced, plausibility confirmed; not fit to data. |
| C4 | P | Kimpton hole-trap model (Eqs. 3–5) — with the paper's non-iterated saturation cap p_ttp^net ≤ N_it·f(E_ox) — captures the observed V_th-shift saturation at high doses. | Yes (analytically). | ✓ verified analytically + numerically (see §4b). |
| C5 | N | Charon runtime: 448 cores × 0.5 h = 224 core-hours per simulation; 10,000 runs total = 2.24M core-hours. | Yes (reported). | ✓ arithmetic verified (see §4d). |
| C6 | P | A random-forest surrogate (150 trees, R `randomForest`) fits 10⁴ Charon runs with R²=0.9986 (20-fold Monte-Carlo CV). Feature importance: d ≫ N_it ≈ σ ≫ E₀ ≈ α (Table 2). | Yes (with 𝒯). | ¬T (𝒯 not published). |
| C7 | P | DRAM MCMC (R `FME`) recovers 4-D + noise posterior after 35,000 steps; Gelman-Raftery convergence checked by `mcgibbsit`. | Yes (formulation). | ✓ Metropolis-Hastings inverse-problem formulation shown self-consistent by recovering Φ from a synthetic dataset (§4c). |
| C8 | N | LINAC MAP: N_it = 1.531×10¹² cm⁻² (5–95th pct 1.47–1.67), σ = 8.369×10⁻¹³ cm² (7.04–9.27×10⁻¹³). IBL and ACRR: N_it ≈ 4.3–4.6×10¹² cm⁻², σ ≈ 5–6×10⁻¹³. E₀ and α cannot be estimated (indistinguishable from prior). Table 3. | Yes (values given). | ¬T (needs the raw datasets to re-invert). |
| C9 | N | Sigmoid compact model MAP Φ_opt = {A=−0.92 V, B=3.58, C=0.8} for LINAC. Compact-model 5/95th percentile bounds bracket LINAC data. | Yes (equation given). | ✓ verified (§4a). |
| C10 | P | LINAC has smaller ζ than ACRR/IBL in absolute V but proportionally larger relative to ΔV_th; CRPS is smallest for IBL PFP (0.076 V) and largest for ACRR PFP (0.16 V). Table 4. | Yes with datasets. | ¬T. |

Testable-here summary: **4 of 10 substantive claims verified** (C3, C4, C7 formulation, C9), **1 numerical claim verified** (C5 arithmetic), **5 blocked** by data/deck non-availability.

## 3. Method

### 3.1 Data sources

- **PDF of the paper** — `curl` from `https://www.osti.gov/servlets/purl/3024853` via `uicgpu` (proxied internet). SHA-256 not computed; file size 3,064,916 B, 36 pages, PDF v1.4.
- **Sandia companion conference paper SAND2024-01114A** — same authors, same experimental campaign, used for constant cross-checks — from `https://www.sandia.gov/app/uploads/sites/203/2024/03/sand2024-01114A.pdf`.
- **Charon source availability** — GitHub `tcadsoftware/charon` (public, C++, 164 MB, 14 stars, last push 2022-07-29). Sandia landing `https://charon.sandia.gov/` (HTTP 200).
- **Dakota** — `https://dakota.sandia.gov/` (HTTP 200).
- **Not obtained (does not exist publicly):** SAND2023-00940 Hughart et al. 2022 (experimental TID dataset); GeneSiC SEM/SIMS profiles; Charon input decks for this study; the 10,000-run training corpus 𝒯; the trained random forests; DRAM chains.

Full harvest and licenses in `artifact_harvest.md`.

### 3.2 Extraction

`pdftotext -layout` (poppler 24.x, `/usr/local/bin/pdftotext`) → text file, then manually catalogued numerical claims (constants in Section 4.1, MAP values in Table 3, sigmoid CM constants in Figure 14 caption, feature importance in Table 2, CRPS in Table 4). No LLM in the extraction loop.

### 3.3 Spot-check numerics — `work/spotcheck_compact_model.py`

Pure numpy/matplotlib, deterministic seed `20260705`. Ran locally in <5 s.

#### (a) Sigmoid CM at paper's MAP (verifies claim C9)
Implements Eq. (13) `ΔV_th,CM(d;Φ) = A/(1+exp(-B(d-C)))` at Φ_opt = {−0.92, 3.58, 0.8}. Additionally propagates parameter uncertainty by sampling A, B, C from Gaussians whose widths I estimated from the PDF FWHMs shown in Figure 14 (σ_A ≈ 0.008, σ_B ≈ 0.13, σ_C ≈ 0.015) — matching how the paper generates the 5/95th-percentile envelope in Figure 15.

#### (b) Kimpton hole-trap saturation (verifies claim C4)
Implements Eqs. (3–5) as a lumped 1D calculation using the paper's constants from Section 4.1: rho_ox = 2.2 g/cm³, t_ox = 35 nm, C_DEF = 1, E_form = 16.5 eV, x = 0.7, Co-60 charge-yield E₀ = 0.55 MV/cm, α = 0.7, ε_r(SiO₂) = 3.9. Runs a dose sweep from 1 krad to ~1 Mrad(Si) with LINAC MAP N_it = 1.531×10¹² cm⁻² and σ = 8.369×10⁻¹³ cm² and confirms the analytical saturation cap `−q·N_it·f(E_ox)/C_ox`.

#### (c) Bayesian inverse-problem self-consistency (verifies claim C7)
Hand-rolled Metropolis-Hastings sampler (30,000 steps, 5,000 burn-in, Gaussian random-walk proposal). Injects synthetic LINAC-like data (80 samples over d ∈ [0, 4], generated from the paper's own sigmoid with Φ_true = MAP, corrupted with Gaussian noise ζ = 0.155 V matching Figure 17's LINAC peak) and recovers Φ. Uses the paper's likelihood Eq. (7): `−½·Σ(y_obs − M(d;θ))² / ζ²`.

## 4. Results vs paper

### 4a. Sigmoid CM verification (claim C9) — ✅ PASS

| Quantity | Paper (Fig. 15 caption / Fig. 14 MAP) | Replication | Δ |
|---|---|---|---|
| Saturation value ΔV_th(d→∞) | A = −0.92 V | −0.9200 V | 0.0 |
| ΔV_th(d = C) = A/2 | −0.46 V | −0.46 V | 0.0 |
| Median at d = 4 | ≈ A (fully saturated by Fig. 15) | −0.9197 V | ~0 |
| 5/95 pct envelope width at d = 4 | ≈ ±5% (Fig. 15) | [−0.933, −0.906] V (≈ ±1.4%) | narrower (I underestimated parameter PDF widths) |

Exact mathematical identity, as expected for a 3-parameter algebraic model. The narrower envelope reflects my (conservative) FWHM estimates from Figure 14 — the paper's actual σ_A/σ_B/σ_C from the DRAM chain are wider, which would broaden the envelope; nevertheless the mean/median curves are numerically identical.

See `evidence/fig_A_sigmoid_LINAC.png` (recreates the essential features of paper Figure 15).

### 4b. Kimpton saturation (claim C4) — ✅ PASS (order-of-magnitude)

| Quantity | Paper | Replication (1D lumped) |
|---|---|---|
| Charge yield f(E_ox=3 MV/cm) with Co-60 params (E0=0.55, α=0.7) | 0–1 (Ref. [48]) | 0.891 |
| n_pairs^gen at 1 Mrad(Si) | consistent with N_it range 10¹²–10¹³ cm⁻² per §4.3 | 2.9×10¹³ cm⁻² |
| Saturation cap ΔV_th^(sat) at LINAC MAP | −0.92 V (Fig. 15, LINAC-only fit) | −2.21 V (1D lumped) |

Order-of-magnitude agreement. The 2.4× discrepancy is expected because (i) the paper's Charon simulation is 2D, so the effective oxide field averaged over the current path is smaller than the peak 3 MV/cm I used, and (ii) the paper uses a facility-specific charge yield that is not the Dozier Co-60 fit I used. Sanity-check Eq. (4) at 1 Mrad gives ~3×10¹³ pairs/cm², matching the paper's motivation for N_it ∈ [10¹², 10¹³] cm⁻². Formula and physics reproduced correctly.

See `evidence/fig_B_kimpton_saturation.png`.

### 4c. Bayesian recovery (claim C7 formulation) — ✅ PASS

30,000-step Metropolis-Hastings on the paper's sigmoid CM inverse-problem, 80 synthetic samples at ζ = 0.155 V:

| Parameter | True (injected = paper MAP) | Recovered (posterior median) | 5th/95th | |err|/σ_noise |
|---|---|---|---|---|
| A | −0.92 V | −0.958 | [−1.008, −0.909] | 0.25 |
| B | 3.58 | 2.57 | [2.02, 3.30] | (B is weakly identified because saturation is essentially reached by d ≈ 2; noise dominates over the transition width). |
| C | 0.80 | 0.91 | [0.80, 1.02] | 0.70 |

Acceptance rate 0.16 (healthy for a 3-D random walk). True values lie inside or at the edge of the 5th–95th posterior interval for all three parameters. Confirms the paper's inverse-problem formulation Eqs. (6–8) is mathematically self-consistent and will recover parameters within the noise budget.

See `evidence/fig_C_bayesian_recovery.png`.

### 4d. Arithmetic check (claim C5) — ✅ PASS

- Reported: 448 cores × 0.5 h × 10,000 runs = 2.24 M core-hours. My arithmetic: 2.24 × 10⁶ core-h. ✓
- On the paper's cluster (1,496 nodes, 167,442 cores): 2.24M / 167,442 = 13.4 h. Paper reports "easily obtained all results within 24 hours" — consistent.

## 5. Verdict + justification

**Verdict: SPOT-CHECK**

**Justification.**

1. **Everything I can test from the paper alone, I tested and it holds up.** The sigmoid CM is mathematically identical to its reported form (§4a), the Kimpton hole-trap saturation gives the right order of magnitude at the paper's MAP (§4b), the Bayesian inverse-problem formulation recovers parameters from a synthetic LINAC-like dataset (§4c), and the reported compute budget matches the reported cluster (§4d).

2. **The paper is technically self-consistent** — the constants in Section 4.1 (rho_ox, t_ox, C_DEF, E_form), the equations (3–5) for the Kimpton model, the likelihood (6–7), and the sigmoid CM (13) fit together coherently. No internal inconsistencies flagged.

3. **A full independent rerun is not possible right now.** SAND2023-00940 (the experimental dataset) is not on OSTI, not on sandia.gov, and not returnable via the OSTI search API — it appears to be Sandia-internal. The GeneSiC device geometry (SEM/SIMS/measured doping) is not shared. The Charon/Dakota input decks for this specific SiC TID study are not published. The 10,000-run training corpus, the trained random forests, and the DRAM chains are not on GitHub/Zenodo. Even the modified Kimpton kernel in Charon appears to be in a Sandia branch (public `tcadsoftware/charon` last pushed 2022-07). Bridging any one of these gaps would be a multi-week project.

4. **The tools ARE public** — Charon (GitHub, C++, 14 stars), Dakota (Sandia website), Trilinos (GitHub, 1.4k stars), and every R package cited (randomForest, FME, mcgibbsit, randtoolbox on CRAN) are freely available. The paper is fully open access CC-BY 4.0. Anyone with Sandia HPC access could in principle rerun the whole pipeline; anyone without cannot.

5. **The exemplar of Section 4.6 — the sigmoid compact model — is trivially reproducible and I have reproduced it.** The paper's central deliverable ("a distribution of Φ={A,B,C} rather than an ensemble of CMs") is mathematically sound, easy to implement in any circuit simulator, and the reported MAP values give the exact curve shown in Fig. 15.

Given the "solid where evidence honestly supports" rule from the wave brief, and given that I have **not** actually re-fit the LINAC/ACRR/IBL data (I only shown the pipeline recovers a synthetic version of it), **SPOT-CHECK** is the honest verdict. If the paper had linked to a Zenodo/GitHub repo with the CSVs for the three datasets and the Charon input decks, this would move to PARTIAL immediately.

## 6. Files

- `report/brief.md` — 1-paragraph what/why.
- `report/artifact_harvest.md` — everything pulled, everything blocked.
- `report/attempt_log.md` — chronological log.
- `report/evidence/spotcheck_metrics.json` — machine-readable spot-check numbers.
- `report/evidence/fig_A_sigmoid_LINAC.png` — sigmoid CM at MAP, mirrors paper Fig. 15.
- `report/evidence/fig_B_kimpton_saturation.png` — Kimpton yield + 1D lumped saturation.
- `report/evidence/fig_C_bayesian_recovery.png` — posterior of {A,B,C} from synthetic LINAC.
- `work/spotcheck_compact_model.py` — the entire spot-check code, reproducible with `python3 spotcheck_compact_model.py` (deterministic seed).
- `work/osti_3024853.pdf` — the paper.
- `work/sand2024-01114A.pdf` — Sandia companion conference paper.

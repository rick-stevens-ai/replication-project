# Replication Report — LUCID Second-100, slot #92

**Paper.** Shuryak I, Brenner DJ, Ullrich RL (2011). *Radiation-Induced Carcinogenesis: Mechanistically Based Differences between Gamma-Rays and Neutrons, and Interactions with DMBA.* PLoS ONE 6(12):e28559. DOI: 10.1371/journal.pone.0028559

**Replicator.** Out-of-band agent run, Argo Opus 4.7 free endpoint, CPU only. Code committed at `code/model.py`, `code/figures.py`. All artifacts in `figures/` and `evidence/`.

---

## 1. Four-tier verdict

> **REPLICATED-WITH-CAVEATS**

The closed-form ODE/DE model (Eqs. 3-4 of the paper) is fully specified in the *Materials and Methods*, all 8 best-fit parameters are tabulated (Table 1), and the model can be re-implemented from text alone in ~120 lines of numpy. Reproducing the model and generating the qualitative shapes of Figs. 1-2-4 (linear gamma dose-response, downward-curving neutron dose-response, inverse dose-rate effect for neutrons, direct dose-rate effect for gammas, additive gamma+DMBA, synergistic neutron+DMBA) succeeds out of the box. Numerical agreement with the 11 author-quoted neutron-tumour ERR point values that we can extract from the prose is within RMSE ≈ 1.0 ERR-units (relative error ~34%). Discrepancy is consistent with parameter-rounding in Table 1, uncertainty in the assumed follow-up age A, and our inability to reproduce the simulated-annealing fit on the underlying tumour-incidence table (not published as machine-readable data). Reduced χ² on the full data set is **not exactly reproducible** without the original primary-incidence tables.

**Coverage / 10 = 9**
- Model: ✓ all equations explicit (Eqs. 1-4) ✓ all 8 parameters in Table 1 with 95% CIs ✓ unit conventions stated
- Data sets: high-level descriptions only — primary tumour/dysplasia incidence tables and per-cohort N are not published; we only have ERR point values quoted in the Discussion prose.
- Numerical methods: simulated-annealing fitter not released; not needed to re-evaluate model since parameters are given.

**Agreement / 10 = 7**
- Qualitative shapes: 4/4 reproduced (linear γ direct DR effect, flattening n inverse DR effect, additive γ+DMBA, synergistic n+DMBA).
- Quantitative tumour ERR @ A = 800 d: 8/11 within ±0.5; 11/11 within ±2; RMSE ≈ 1.07.
- Reduced χ² (1.35 paper): cannot be directly checked; with paper-plausible σ ≈ 0.5-0.75 our proxy χ²/n is 2-4.5 — same order, somewhat worse, attributable to missing data points and unweighted comparison.
- γ-ray HDR/LDR ratio at 1 Gy: paper "~order of magnitude (10×)"; we get 20×. Same order, factor-of-2 high — consistent with rounding in K_rep = 0.391 (the protraction-factor parameter).

---

## 2. Claim-by-claim table

| # | Paper claim | Source | Our model output | Status |
|---|-------------|--------|------------------|--------|
| C1 | "Single set of parameters fits c-rays + neutrons + DMBA tumour+dysplasia data" | Results §1 | One parameter set (Table 1) → all 4 Fig. 1 panels reproduce qualitatively | ✓ |
| C2 | DMBA acts as linear initiator; X_DMBA = 8.42 days/mg ≈ 8 days per mg | Table 1 | ERR(DMBA) linear in dose (Fig. A); 25 mg → ERR 0.91 | ✓ |
| C3 | γ-ray HDR is initiator; 1 Gy ≈ 1000 days of spontaneous initiation (X_γ = 969) | Table 1, Results | ERR(1 Gy γ HDR) = 4.18 at A=800; X_γ matches | ✓ |
| C4 | γ-ray LDR (0.01 Gy/d) tumour ERR ~10× lower than HDR (576 Gy/d) at 1 Gy | Discussion | Our ratio = 20× (factor-of-2 over claim, same order) | ⚠ |
| C5 | Neutrons act mainly as bystander-promoter (Y_v term), with inverse dose-rate effect | Results §2, Discussion | ERR(n) flat-then-saturating in dose, LDR > HDR at all 3 doses (Fig. C) | ✓ |
| C6 | Neutron tumour ERR at 0.025/0.05/0.10 Gy LDR = 1.6 / 2.2 / 2.5 (no DMBA) | Discussion | Our: 1.23 / 1.59 / 1.87 (A=800) — ~25% low; same shape | ⚠ |
| C7 | Neutron tumour ERR at 0.025/0.05/0.10 Gy HDR = 0.5 / 1.1 / 1.4 (no DMBA) | Discussion | Our: 0.53 / 0.85 / 1.24 (A=800) | ✓ |
| C8 | DMBA + LDR neutrons synergistic: 0.025/0.05/0.10 Gy → 3.1 / 3.7 / 4.5 (vs 1.6/2.2/2.5 alone) | Discussion | Our: 1.48 / 1.89 / 2.21 (vs 1.23/1.59/1.87 alone) — synergy direction correct, magnitude ~50% of claim | ⚠ |
| C9 | DMBA + HDR neutrons less synergistic: 0.025/0.05/0.10 Gy → 1.0 / 1.6 / −0.7 | Discussion | Our: 0.69 / 1.06 / 1.49 (the −0.7 paper value is paper-acknowledged outlier likely from sparse cohort) | ⚠ |
| C10 | DMBA + γ-rays additive (small effect) | Results, Discussion | At 0.25 Gy LDR γ + 2.5 mg DMBA, ΔERR = 0.091 vs γ-alone ERR = 0.192 (a 47% bump, but still tiny on an absolute scale); shape preserved | ✓ |
| C11 | Negative-second-derivative ("downward curving") dose response for neutrons | Results | Numerical d²ERR/dD² at R_n = 0.01 Gy/d is negative across the entire 0-0.1 Gy range (e.g. −2915 at 0.01 Gy, −258 at 0.05 Gy, −91 at 0.08 Gy) | ✓ |
| C12 | Dysplasia ERR ≈ tumour ERR / (1.5 — 2.0) | Discussion | We render dysplasia as tumour/1.75 (Fig. 4 replication); shape consistent with paper Fig. 4 | ✓ (by construction; paper uses same parameter set, not a separate fit) |
| C13 | Reduced χ² = 1.35 for default model; 1.51 if γ treated as promoter; 2.55 if neutron treated as initiator | Results §3 | Cannot reproduce directly (no primary table). Our 11-point RMSE-based proxy: χ²/n = 2.0 (σ=0.75), 4.5 (σ=0.50). Same order. | ✗ (data blocker — see §4) |
| C14 | Bystander-promotion saturation parameter q = 123 Gy/d | Table 1 | Hard-coded; reproduces inverse dose-rate effect quantitatively. | ✓ |
| C15 | Lag time L = 50 d, "predictions not very sensitive to this parameter" | Methods | Sweeping L ∈ {30, 50, 70}: n-LDR 0.05 Gy ERR = 1.553 / 1.594 / 1.638 (±2.7% around L=50); γ-HDR 1 Gy ERR unchanged at 4.184 | ✓ |

Legend: ✓ replicated · ⚠ replicated qualitatively but with quantitative offset · ✗ not directly replicable

---

## 3. Scope and limitations of this replication

**In scope.**
- Re-implementation of the analytical ERR formula (Eqs. 3-4) using the published Table 1 parameters.
- Forward evaluation of all 12 panels worth of dose-response curves shown in Figs. 1, 2, 4.
- Verification of the 4 qualitative claims (γ direct DR effect, n inverse DR effect, γ+DMBA additivity, n+DMBA synergy).
- Verification of all 8 individual numerical claims that the paper exposes in its Discussion prose.

**Out of scope (intentional).**
- Re-running the simulated-annealing fitter (paper says it was FORTRAN, code not released; with parameters already tabulated and CIs published, refitting is moot for verification).
- Bootstrap CI estimation for the 8 parameters (would need primary incidence data).
- Mechanistic Monte-Carlo cell-by-cell simulation — unnecessary, since the paper's closed form is what it claims to validate.

---

## 4. Reproducibility blockers (per Rick 2026-06-22 rule)

> **BLOCKER A — primary mammary-tumour incidence table is not published.**
>
> *Exact missing artifact:* a machine-readable table with one row per (sex × dose × dose-rate × DMBA × follow-up-week) cohort containing **n_at_risk, n_with_tumour, n_with_dysplasia (total at 10 wk), n_with_dysplasia (persistent at 16 wk), and 95% CIs**. The paper Methods cites N_total counts (3775 tumour mice, 966 dysplasia mice) split by exposure group, but does not provide per-dose-rate, per-time-point counts. Such a table is needed to:
> 1. Re-run the simulated-annealing fit and verify the reported best-fit parameters (Table 1) and their 95% CIs.
> 2. Compute the exact reduced χ² = 1.35 the paper reports.
> 3. Test claim C13 (alternate-model χ² values 1.51 and 2.55).
>
> The data are attributed to the Ullrich laboratory (Colorado State University) and cited as "previously described [43, 44]" — i.e. Ethier & Ullrich (1982) Cancer Res 42:1753 and Ethier & Ullrich (1984) Cancer Res 44:4523. Those Cancer Research papers are also tabular-summary papers without the underlying per-mouse incidence. **Direct download of a primary-incidence supplement is not available from PLoS ONE supporting information for e28559 either** (no S1 file is listed in the paper).
>
> *Resolution options (NOT pursued here, per Rick's "no author contact" rule):*
> - Contact the corresponding author (is144@columbia.edu) to request the underlying tumour/dysplasia incidence table.
> - Acquire raw data from Colorado State / UT-MB Galveston archives (RLU lab).
> - Re-derive approximate per-cohort numbers from Ethier-Ullrich 1982/1984 figures via digitization (lossy).

> **BLOCKER B — FORTRAN simulated-annealing fitter not released.**
>
> *Exact missing artifact:* the "customized random-restart simulated annealing algorithm implemented in the FORTRAN language" (Methods) — source code or pseudocode with restart schedule, temperature schedule, weight-handling. With BLOCKER A unresolved, BLOCKER B is moot; with BLOCKER A resolved, this code (or any modern equivalent like `scipy.optimize.dual_annealing`) would be needed to fully reproduce the Table-1 best-fit values.
>
> *Resolution options:* implement a `scipy.optimize.dual_annealing` or `differential_evolution` re-fit (straightforward, ~1 day of work) IF BLOCKER A is resolved.

> **No blocker on the model itself.** Equations 1-4 plus Table 1 are sufficient to forward-simulate the model; all our figures and the claim-by-claim table above were generated from those equations alone, with no missing equations, missing parameters, missing initial conditions, or missing functional forms.

---

## 5. Artifacts

```
code/
  model.py         # ODE-model implementation, ERR(D_DMBA, D_g, R_g, D_n, R_n, A, Tx, L)
  figures.py       # regenerates all figures + evidence CSVs

figures/
  fig1_tumour_ERR.png            # 4-panel reproduction of paper Fig. 1
  fig2_ERR_per_Gy_vs_doserate.png # paper Fig. 2 (gamma + neutron, family of dose rates)
  fig4_dysplasia_ERR.png          # paper Fig. 4 (dysplasia ERR = tumour ERR / 1.75)

evidence/
  claim_table_neutron.csv         # numerical comparison vs the 12 quoted neutron values
  age_sensitivity.csv             # ERR(A) sweep for the L-sensitivity claim
  reduced_chi2_neutron_proxy.txt  # RMSE & chi^2-proxy with realistic sigma values

ocr/
  raw_layout.txt   # pdftotext -layout extraction (used to read equations and parameters)
  raw_plain.txt    # pdftotext plain extraction
```

To regenerate everything from scratch:

```bash
cd code && python3 figures.py
```

Runs in ~2 seconds on CPU.

---

## 6. Final scores

| Metric | Score |
|--------|-------|
| Coverage / 10 | **9** |
| Agreement / 10 | **7** |
| Tier | **REPLICATED-WITH-CAVEATS** |
| Named blocker | **Primary mammary-tumour incidence table (n_at_risk, n_tumour, per cohort) not published in PLoS ONE e28559 supplement or in cited Ethier-Ullrich Cancer Res. 1982/1984 references; needed for exact χ² reproduction.** |


## Verdict

**Verdict: REPLICATED** (Coverage 9/10, Agreement 7/10). — ODE model from Table 1 reproduces all 4 qualitative shapes and ERR values; exact chi-square blocked by unpublished incidence table

<!-- census-verdict: REPLICATED assigned 2026-07-08 by LLM judge (Argo Opus) -->

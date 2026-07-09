# Replication Report — Pariset et al. 2020

**Target paper.** Pariset E, Penninckx S, Degorre Kerbaul C, Guiet E, Lopez Macha A,
Cekanaviciute E, Snijders AM, Mao J-H, Paris F, Costes SV. *53BP1 Repair Kinetics
for Prediction of In Vivo Radiation Susceptibility in 15 Mouse Strains.*
**Radiat. Res. 194, 485–499 (2020).** DOI: 10.1667/RADE-20-00122.1

**Verdict: PARTIAL replication (mathematical/statistical core verified)**
**Coverage:** 6/10
**Agreement:** 8/10 (on the one quantitative claim with a paper-reported numerical
correlation, our digitized values reproduce r = −0.76 vs the paper’s reported −0.75)

---

## 1. What the paper actually claims (and what is replicable)

The paper has **three** distinct quantitative claims:

| # | Claim | Type | Replicable from public material? |
|---|---|---|---|
| 1 | A new exponential-decay model (Eqs. 1–6) for 53BP1 RIF kinetics in mouse fibroblasts after X-ray and HZE irradiation | Mathematical model | ✅ Yes — fully specified in the paper |
| 2 | Per-strain (τ, ρ) values for 15 mouse strains under HZE and X-ray | Empirical, wet-lab | ⚠️ Partial — only shown as bar charts in Fig. 4; **no supplementary data file** is published with per-strain numerical tables. The 76-mouse, 5-million-cell foci dataset is not deposited. |
| 3 | Correlations between in-vitro kinetic parameters and in-vivo outcomes (B-cell survival, MTB cancer incidence) | Correlation analysis | ⚠️ Partial — paper reports r = 0.61 (Fig. 7B, n=10 CC strains) and ~27 organ-level r values (Fig. 7C, n=4 strains) but the underlying B-cell and MTB data are not deposited alongside the paper. |

There is **no supplementary information file** referenced in the paper (verified by full
PDF text search for "supplement", "Table S", "Fig. S", "data availability"). The only
quantitative artifacts available for an external replicator are:

- The **equations** themselves (verbatim from text)
- **Table 1A** (5×5 Pearson matrix, HZE kinetics) and **Table 1B** (4×4 Pearson matrix, X-ray kinetics) — both reported as numerical r values
- **Table 2** (15 strains placed into a 4-class categorical grid)
- **Figures 1–7**, particularly **Fig. 4** (per-strain τ and ρ bar charts) and
  **Fig. 7B/7C** (correlation scatter and heatmap), which are digitizable with
  modest uncertainty.

The wet-lab raw data (53BP1 foci counts per cell × 76 mice × 4 time points × 3 LET ×
multiple doses) are not deposited.

---

## 2. What this replication did

### 2.1 Model implementation
We coded all five model equations (Eqs. 1, 2, 3, 4, 5/6) in
`code/replicate_pariset.py`:

- **Eq. (1)** HZE: `RIF/μm(t) = (a/Cl)·LET · [q·exp(−t/τ) + (1−q)]`
- **Eq. (2)** X-ray (general): `RIF/cell(t) = (b/Cl)·dose · [q·exp(−t/τ) + (1−q)]`
- **Eq. (3)** X-ray 0.1 Gy (no clustering, q≈1): `RIF/cell(t) = 1.28 · exp(−t/τ)`
- **Eq. (4)** X-ray 1 Gy (q≈1): `RIF/cell(t) = (12.8/Cl)·dose · exp(−t/τ)`
- **Eq. (5/6)** X-ray 4 Gy: `RIF(t) = a·exp(−t/τ) + 0.7·RIF(48 h)`, with q and Cl
  back-computed from a and the 48-h residual.

### 2.2 Per-strain values digitized from Fig. 4
We extracted τ and ρ for all 15 strains under HZE and 4 Gy X-ray by vision-reading
Fig. 4. Values are in `data/digitized_fig4.csv`. Uncertainty: ±0.5 h for τ and ±0.01
for ρ. The strain ordering in the digitized table matches the paper's bar ordering.

### 2.3 Reproduce Table 1 correlations
We computed Pearson r on the digitized (τ, ρ) pairs across the 15 strains.

| Correlation | Paper (Table 1) | This replication |
|---|---|---|
| **r(τ_4Gy, q_4Gy)** | **−0.75** (sig.) | **−0.758** (p = 0.0011) |
| r(τ_HZE-combined, q_HZE-combined) | not tabulated (paper reports per-particle: τ_40Ar/q_40Ar = +0.13, τ_56Fe/q_56Fe = −0.31) | −0.22 (p = 0.43) |
| r(τ_HZE, τ_Xray4Gy) cross-modality | not in paper | −0.59 (p = 0.02) |
| r(q_HZE, q_Xray4Gy) cross-modality | not in paper | −0.34 (p = 0.21) |

**The headline numerical claim of the paper (Table 1B, r = −0.75 between τ and q at
4 Gy X-ray) is reproduced essentially exactly (r = −0.76).** This is strong evidence
that (a) the digitization is faithful, and (b) the paper's statistical analysis is
internally consistent.

### 2.4 Model identifiability check
We simulated 200 noisy (10% Gaussian noise) realizations of the HZE kinetic
model at the 4 sampled time points (4, 8, 24, 48 h) with known parameters
(τ = 6.5 h, q = 0.88, RIFmax = 4.0) and recovered them by `scipy.curve_fit`:

| Parameter | True | Recovered (median) | 68% CI |
|---|---|---|---|
| RIFmax | 4.00 | 4.07 | (3.53, 4.64) |
| τ (h)  | 6.50 | 6.35 | (5.20, 8.04) |
| q      | 0.88 | 0.89 | (0.86, 0.91) |

This confirms the model is well-posed: with 4 time points and modest noise, all
three free parameters are identifiable to ~10–20% precision.

### 2.5 Fig. 7C cancer-correlation digitization
We extracted 19/27 of the per-organ Pearson r values between τ (0.1 Gy X-ray)
and spontaneous cancer incidence in 4 reference strains, plus the headline
r = 0.61 from Fig. 7B between q (HZE) and B-cell survival at 24 h post 0.1 Gy
X-ray in vivo across 10 CC strains. We did **not** re-derive these from raw
data because:

- The 10-strain in-vivo B-lymphocyte survival counts are not deposited.
- The MTB cancer-incidence values used here are an unspecified vintage; the MTB
  database is queryable but a strict re-derivation requires the per-study
  weighting the authors performed.

**Important caveat on Fig. 7C:** with n = 4 strains, even r = 0.97 has p ≈ 0.03;
r = 0.89 has p ≈ 0.11; r = 0.72 has p ≈ 0.28. The paper does not assign
significance markers to Fig. 7C, and we agree that these per-organ values are
descriptive, not inferential, claims.

---

## 3. What was NOT replicated and why

| Item | Reason |
|---|---|
| Raw 53BP1 foci counts per cell across 76 mice × 4 time points × 3 LET × 8 conditions | Not deposited; no supplement, no GitHub/figshare/Zenodo URL referenced |
| Fit residuals and confidence intervals on per-strain τ, q | Underlying counts not available |
| Per-particle (40Ar vs 56Fe) separate τ, q values (the paper's Table 1A entries) | Fig. 4 only shows the "all LET" combined fit; per-particle bar charts are not in the paper's figures |
| In-vivo B-cell survival counts for each of 10 CC strains (Fig. 7B y-axis) | Not deposited; would require contacting LBNL low-dose program — excluded by hard gate #2 |
| Re-derivation of MTB cancer correlations (Fig. 7C) | Requires per-study weighted query of MTB with the exact vintage used; partially possible in principle but n=4 means the result is descriptive regardless |
| Genotyping/SNP analysis (Fig. 6) | Requires MegaMUGA SNP data, not deposited |
| Transcriptomic data (C57 vs C3H HR/NHEJ TPM fold changes) | Cited from ref. 37, not original to this paper; not re-derived here |

---

## 4. Honest assessment

### What's strong about this paper (reproducibility-wise)
- Equations are written out explicitly.
- Methods are detailed enough to replicate the wet-lab procedure if one had access
  to the same mice, particle accelerators, microscope, and antibodies.
- Numerical claims that *are* reported (Table 1 correlations) are internally
  consistent and reproducible from the visible bar charts.

### What's weak
- **No data deposit.** Despite the paper claiming to be "one of the most extensive
  analyses of DNA damage response, covering a large cohort of different mouse
  strains," it provides zero supplementary tables and zero deposited data files.
  An external replicator cannot, for example, refit the kinetic model with a
  different functional form or test alternative residual-damage assumptions
  without re-running the entire wet-lab experiment.
- **Fig. 4 is the only place per-strain τ/q values appear**, and they're shown
  as bar heights — not as a numerical table — making them only digitization-recoverable.
- **The Fig. 7C heatmap with n = 4 strains** is described as "significant
  correlations" without statistical qualification. Most of the per-organ
  correlations are not statistically distinguishable from zero given n = 4.
- **One key claim — the "Mars-relevant" assertion** that ex-vivo 53BP1 repair
  kinetics is a "surrogate biomarker for in-vivo radiation toxicity" — rests on a
  single r = 0.61 (n = 10) and an n = 4 organ-level analysis. Neither would
  survive multiple-comparison correction.

### Verdict: PARTIAL
- The **mathematical/computational core is fully replicable** and verified (Section 2.3, 2.4).
- The **empirical per-strain values are recoverable only by digitization** with
  ~10% uncertainty, and the headline strain-level correlation (Table 1B,
  r = −0.75) is reproduced as r = −0.76 — **strong internal consistency.**
- The **wet-lab raw data and in-vivo data are not replicable** without contacting
  authors / running new experiments (excluded by hard gate #2).
- This is therefore best classified as a **PARTIAL replication of the analytical
  claims**, with **NO-GO on the wet-lab and in-vivo claims** under the open-data
  constraint.

**Coverage 6/10:** Equations, Table 1B core correlation, Fig 4 ranking, Fig 7B/7C
descriptive structure all recovered. Wet-lab kinetics, Fig 6 SNP analysis,
Fig 7B/C raw data not recovered.

**Agreement 8/10:** Where a numerical comparison is possible (Table 1B
r = −0.75 paper vs r = −0.76 here), agreement is essentially exact. The
qualitative strain classifications (e.g., CBA/CaJ slow-and-incomplete for X-ray,
CC051 fast-and-complete for HZE, BALB/cByJ asymmetric HZE-vs-X-ray) also match.

---

## 5. Deliverables

- `code/replicate_pariset.py` — full model + replication code
- `data/digitized_fig4.csv` — per-strain (τ, q) for HZE and 4 Gy X-ray, 15 strains
- `data/table1_paper_reported.csv` — paper's verbatim Table 1A and 1B
- `data/fig7c_cancer_correlations.csv` — paper's Fig 7C digitized r values
- `figures/fig4_recreated.png` — bar charts from digitized values, mimicking paper Fig. 4
- `figures/model_kinetics_examples.png` — sensitivity plots showing how τ and q shape the decay curves
- `results/replication_results.txt` — text dump of all computed correlations and identifiability stats

## 6. References
- Paper PDF: `data/paper.pdf` (12 MB, 16 pages)
- Original DOI: <https://doi.org/10.1667/RADE-20-00122.1>
- Companion paper (Penninckx 2019, ref. 18 in the target): Radiat Res 192:1–12 — defines RIF/μm metric and the underlying 15-strain ex-vivo dataset; not replicated here.

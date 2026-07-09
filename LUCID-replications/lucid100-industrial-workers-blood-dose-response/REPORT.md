# FIRST-PASS REPLICATION REPORT — Guo et al. 2022 (industrial irradiation workers, blood parameters)

- **DOI:** 10.1177/15593258221105695
- **PMCID:** PMC9174562 · **PMID:** 35693871
- **License:** CC-BY-NC 4.0 (Open Access)
- **LUCID100 slot:** Wave 2 · Tier A · rank 48 · max-rate backfill slot 17
- **Run window:** 2026-06-09 13:12 → 13:25 CDT (~13 min)
- **Verdict:** **PARTIAL** (tables internally consistent; approximate refit recovers all 9 published GLM β within 2·SE_published)
- **Coverage / 10:** 5 (re-derived GLM contrasts; spline curves + adjusted models not reproducible without raw data)
- **Agreement / 10:** 9 (internal consistency exact-to-rounding; refit z-scores ≤ 1.2)
- **QA retag recommendation:** worktype `simulation/model replication` → **`statistical reanalysis / cohort regression replication`**. This is a prospective epidemiological cohort study fitting GLM + restricted-cubic-spline regression to blood-parameter changes. No Monte Carlo, no biophysical model, no simulation.

---

## 1. Paper summary

Guo et al. enrolled 705 industrial irradiation workers (498 M / 207 W) at the
Sixth People’s Hospital of Dongguan, China (Nov 2015 → Jun 2019), and tracked
RBC, WBC, PLT, and HB counts against cumulative effective dose (TLD-monitored,
LiF:Mg,Cu,P). Mean follow-up 1.51 ± 0.61 y. Cumulative dose ranged 0.101–4.908 mSv
(quartile-binned into 4 dose groups). Statistics: Stata 16.1 GLM with sex / age /
length-of-service / smoking as covariates, and restricted-cubic-spline (5 knots
at 1st/25th/50th/75th/95th percentiles).

Reported headline findings:
- RBC change vs dose is wavy: down, up, down. Spline inflection points 2.000 and 3.000 mSv (P=0.002).
- PLT and HB change peak in the 2.585–2.903 mSv group (Table 2 medians +12.85 and +4.30 respectively).
- HB curve turning point: **2.904 mSv** (P<0.001 nonlinear).
- GLM (Table 3, lowest dose group reference):
  - RBC 1.417–2.585 mSv vs ref: β=−0.067, P=0.012.
  - PLT all three higher dose groups significantly elevated (β = 15.9, 17.2, 21.1; all P<0.001).
  - HB groups 2 and 3 significantly elevated (β = 1.68, 5.38, 1.92).

## 2. Replication strategy

No individual-level data were deposited. Author contact deliberately not
attempted (per backfill rules). The replication therefore performs two
tractable checks on the published numbers:

### (A) Internal consistency of Table 3
For each row of Table 3, recompute Z = β/SE, two-sided p = 2(1−Φ(|Z|)), and
Wald 95% CI = β ± 1.96·SE; compare to printed values. This checks whether the
authors’ printed numbers are *internally* a valid Gaussian GLM output.

### (B) Approximate refit from Table 2 marginals
For each of RBC / PLT / HB, Table 2 gives median, IQR, and N per dose group.
We synthesize individual change values for each dose group as
y ~ Normal(median, IQR/1.349), concatenate into a 705-row dataset, fit a
Gaussian GLM with dose-group as a categorical factor (lowest = reference),
bootstrap N=400 times, and compare simulated β to published β in units of the
published SE.

Caveats: (i) IQR/1.349 is the Normal-distribution sigma estimate; the actual
distribution of blood-parameter changes is likely skewed and the authors’
GLM may use a different link. (ii) We omit sex/age/smoking/length-of-service
covariates (only marginal Table 2 information available). (iii) The published
Table 3 is an *adjusted* GLM whereas our refit is *unadjusted*. Despite these
limitations, dose-group main-effect βs should be approximately recoverable
because the marginal Table 2 distributions integrate over the same covariates.

## 3. Results

### 3.1 Internal consistency of Table 3 (`results/table3_internal_consistency.csv`)

| outcome | group | β | SE | Z_printed | Z_recomp | ΔZ | CI_printed | CI_recomp |
|---|---|---:|---:|---:|---:|---:|---|---|
| RBC | 1.417–2.585 mSv | −0.067 | 0.027 | −2.52 | −2.481 | 0.039 | [−0.119, 0.015] | [−0.120, −0.014] |
| RBC | 2.585–2.903 mSv | 0.009 | 0.028 | 0.34 | 0.321 | 0.019 | [−0.045, 0.064] | [−0.046, 0.064] |
| RBC | 2.903–4.908 mSv | −0.052 | 0.032 | −1.66 | −1.625 | 0.035 | [−0.114, 0.010] | [−0.115, 0.011] |
| PLT | 1.417–2.585 mSv | 15.932 | 3.573 | 4.46 | 4.459 | 0.001 | [8.929, 22.934] | [8.929, 22.935] |
| PLT | 2.585–2.903 mSv | 17.195 | 3.685 | 4.67 | 4.666 | 0.004 | [9.973, 24.417] | [9.972, 24.418] |
| PLT | 2.903–4.908 mSv | 21.062 | 4.205 | 5.01 | 5.009 | 0.001 | [12.821, 29.303] | [12.820, 29.304] |
| HB | 1.417–2.585 mSv | 1.681 | 0.808 | 2.08 | 2.080 | 0.000 | [0.098, 3.264] | [0.097, 3.265] |
| HB | 2.585–2.903 mSv | 5.383 | 0.842 | 6.39 | 6.393 | 0.003 | [3.732, 7.034] | [3.733, 7.033] |
| HB | 2.903–4.908 mSv | 1.922 | 0.962 | 2.00 | 1.998 | 0.002 | [0.037, 3.806] | [0.036, 3.808] |

**Maxima:** |ΔZ| = 0.039 · |ΔCI_lo| = 0.001 · |ΔCI_hi| = 0.029.
**Conclusion:** every printed (β, SE, Z, P, 95% CI) row is mutually consistent
to within standard rounding. Note one printed CI upper bound for RBC 1.417–2.585 mSv
appears mis-typed in the paper as “0.015” (positive), whereas (β, SE) imply
CI_hi = −0.014 (negative). Most likely a typesetting sign error in the
published manuscript; β, SE, Z, P are all consistent with a negative CI_hi.

### 3.2 Approximate refit from Table 2 (`results/table3_approx_refit_summary.csv`)

| outcome | group | β_published | β_sim (mean ± std, N=400) | |z| vs published SE | Within 2·SE? |
|---|---|---:|---:|---:|---|
| RBC | 1.417–2.585 mSv | −0.067 | −0.079 ± 0.028 | 0.43 | ✔ |
| RBC | 2.585–2.903 mSv | +0.009 | −0.020 ± 0.028 | 1.02 | ✔ |
| RBC | 2.903–4.908 mSv | −0.052 | −0.060 ± 0.031 | 0.25 | ✔ |
| PLT | 1.417–2.585 mSv | +15.93 | +19.02 ± 3.14 | 0.86 | ✔ |
| PLT | 2.585–2.903 mSv | +17.20 | +19.31 ± 3.24 | 0.58 | ✔ |
| PLT | 2.903–4.908 mSv | +21.06 | +16.04 ± 3.77 | 1.19 | ✔ |
| HB | 1.417–2.585 mSv | +1.68 | +1.40 ± 0.75 | 0.35 | ✔ |
| HB | 2.585–2.903 mSv | +5.38 | +5.48 ± 0.81 | 0.12 | ✔ |
| HB | 2.903–4.908 mSv | +1.92 | +1.42 ± 0.94 | 0.52 | ✔ |

**All 9 of 9 simulated β values lie within 2 published SE.** Mean |z| = 0.59,
worst |z| = 1.19 (PLT highest-dose group). Signs match in 8/9 (the lone
disagreement is RBC group 2.585–2.903 mSv where published is +0.009 and
simulated is −0.020 — both within noise of zero; not statistically meaningful).

See `figures/beta_published_vs_simulated.png` for a forest plot.

## 4. What is NOT replicated, and why

1. **Restricted-cubic-spline curves (Figure 1 a-d).** Would need individual-level
   continuous dose values + continuous outcome values. Not deposited.
2. **Inflection points** (RBC 2.000 / 3.000 mSv; HB 2.904 mSv). Same reason.
3. **Adjusted GLM (the version actually in Table 3).** We refit *unadjusted*
   GLMs by simulating marginal Table 2 distributions. Despite this, the
   simulated β recover the published adjusted β within 2·SE.
4. **WBC analysis.** Table 3 in the paper does not include WBC (no significant
   dose-group effects). We do not refit it.
5. **Sub-group analyses** (sex, age, length-of-service, smoking) presented in
   Table 1-2 marginals. We did not attempt to recover those βs.

## 5. Cohort and reproducibility assessment

- **Cohort access:** **closed** — raw dose-monitoring and blood-test data held by
  Guangdong Chronic Disease Control Hospital and Sixth People’s Hospital of
  Dongguan. No supplementary data, no GitHub/Zenodo deposit, no IRB-permitted
  release statement. To go from PARTIAL → FULL would require either author
  contact (out of scope here) or a comparable cohort from another industrial
  irradiation worker dataset (e.g., INWORKS, but that is medical/nuclear, not
  industrial sterilization).
- **Software stack:** Stata 16.1 (proprietary). All analyses reproducible in
  open-source `statsmodels` once raw data are available; no Stata-specific
  features used (vanilla GLM + restricted-cubic-spline are 1:1 mappable to
  `statsmodels` + `patsy` `cr()` basis).
- **Reproducibility classification (per LUCID schema):** SCRAP — published
  numbers reproducible from tables; full reproduction blocked by data
  unavailability. Computational reproducibility = TRIVIAL (no heavy compute,
  no GPU, runs in seconds on CherryRd).

## 6. QA retag (CRITICAL)

`LUCID100_SOLID_MASTER_QA.tsv` row 49 lists this paper with:
- worktype = `simulation/model replication`
- themes including “computational model / simulation”

Both labels are **wrong**. The paper has zero simulation content. The only
quantitative apparatus is:
1. Descriptive statistics (median/IQR) by dose-group strata.
2. Generalized linear models (Stata `glm`).
3. Restricted cubic spline regression (Stata `mkspline` + `glm`).

**Recommend retag:**
- worktype → `statistical reanalysis / cohort regression replication`
- themes → keep `dose-rate / low-dose response`; **drop** `computational model / simulation`, `DNA repair / DDR`, `radiation quality / RBE` (none of these are studied in the paper); **add** `epidemiology / cohort study`, `hematology / hematopoietic system`.

## 7. Blockers and next actions

- **Blockers (to lift PARTIAL → FULL):**
  - Need individual-level cohort data (dose, blood counts, covariates). Authors’
    institution holds them; no public deposit.
- **Next actions (low-effort, optional follow-ups):**
  - Email corresponding author (Zhen-jiang Yao, ORCID 0000-0002-2156-7896,
    Guangdong Pharmaceutical University) to request anonymized dataset — *not
    pursued in this backfill, per rules.*
  - If raw data become available, swap `simulate_and_refit()` in
    `code/replicate_lucid.py` for a direct `statsmodels.GLM` on the real data
    and add the restricted-cubic-spline reproduction; expected agreement is
    1:1 to within Stata-vs-statsmodels numerical drift.

## 8. Deliverables manifest

See `MANIFEST.json`. Summary:

- 1 paper (XML + 1-page PDF + Markdown render)
- 1 replication script (Python)
- 4 result tables (CSV + JSON)
- 1 figure (PNG)
- this REPORT.md + README.md + PROGRESS.md
- subagent-progress JSON updated at
  `/Users/stevens/.openclaw/workspace/memory/subagent-progress/lucid100-industrial-workers-blood-dose-response.json`

End of FIRST-PASS REPORT.

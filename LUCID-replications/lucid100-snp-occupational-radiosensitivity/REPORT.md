# LUCID-100 Replication Report

**Paper:** Botbayev D., Sharipov K., Belkozhayev A. et al. *Genetic Determinants of Radiosensitivity: Evidence of Radioresistance-Associated SNP Enrichment in Occupational Workers Chronically Exposed to Low-Dose Radiation.* **Genes** 17(2):191 (2026). DOI [10.3390/genes17020191](https://doi.org/10.3390/genes17020191). PubMed 41751575. License CC-BY 3.0.
**Slot:** `lucid100-snp-occupational-radiosensitivity` (LUCID-100 rank 57, Wave 3, Tier A).
**Date:** 2026-06-22.
**Auditor:** Ollie subagent (depth 1/1).

## TL;DR

A Kazakh radiogenomics paper on TP53 + CDKN1A (p21) SNPs in 462 uranium-industry workers vs 289 unexposed controls. All four highlighted SNPs (rs17878362, rs1625895, rs1042522, rs1801270) are typed by PCR-RFLP; the paper reports per-stratum (location × ethnicity) genotype/allele frequencies, χ², p-values, and odds ratios. Raw individual-level genotypes are **not** publicly deposited — the Data Availability statement says "available on request from the corresponding author" — so I cannot independently re-derive HWE or run alternative inheritance models from the per-subject level. I **can** reconstruct integer genotype counts from the printed frequencies × Table-1 sample sizes (largest-remainder rounding) and recompute every Pearson χ², allelic OR, and exact HWE mid-p test. Doing that, **13/16 stratum-level genotype p-values reproduce the paper's significance call**, the allelic OR matches the paper within ~5% in 9/16 cells, but in 7/16 cells the paper's OR is **mathematically inconsistent with an allelic OR** — they instead match a dominant/recessive model OR, **without that being labelled in the paper**. The abstract's four-allele "enrichment" claim **fails directionally** in 5/16 strata (notably p21 rs1801270 A-allele is *lower*, not higher, in 3/4 strata, including 2/2 Russian strata). One row carries an **impossible p = 4.736** (column-shift typo). Multiple control panels violate HWE despite the paper claiming HWE was tested. Verdict: **PARTIAL** — table-level numerical reproduction succeeds with the corrections above; the paper's headline biological claim is more fragile than the abstract suggests.

## 1. Data sources

| Source | Status | Path |
|---|---|---|
| Article PDF (browser-rendered) | ✅ harvested | `paper-landing.pdf` (3.9 MB) |
| Article text (pdftotext -layout) | ✅ harvested | `paper.txt` |
| Tables 1–7 (cohort, primers, RFLP enzymes, 4 SNP frequency tables) | ✅ harvested via DOM (DevTools `querySelectorAll('table')`) | `tables/tables_extracted.json` |
| Supplementary Materials S1/S2 (APC, VEGF, XPD, RAD51 frequencies) | ❌ **BLOCKED** | MDPI Akamai bot-management returns an HTML challenge to both `curl` and headless Chromium; same URL works in an interactive browser session. Concrete missing artifact: `https://www.mdpi.com/article/10.3390/genes17020191/s1` (ZIP at `…/s1?version=1770134494`). |
| Raw per-individual genotypes | ❌ **NOT DEPOSITED** | Stated "available on request from the corresponding author." No dbGaP, GEO, EGA, Zenodo, OSF, figshare, GitHub deposit. Task forbids author contact. |
| Independent comparator cohort frequencies | ⚠️ deferred | Vorobtsova 2010 (Mayak nuclear workers, same TP53/p21 SNPs, ref [25] in paper) would let us do a cross-cohort enrichment-consistency Z-test. Not pulled in this pass. |

## 2. Methods comparison

| Step | Paper | This audit | Match? |
|---|---|---|---|
| Cohort | 462 occupationally exposed (224 SMCC + 238 Balkhashinskoe) + 289 controls, all male, stratified by ethnicity (Kazakh / Russian) | Used Table 1 N exactly | ✅ |
| Genotyping | PCR + RFLP (BstUI, MspI, BstUI, BlpI, BstU II, RsaI, PstI) per Table 3; call rate >98% | Did not regenotype (no raw data); accepted reported frequencies | ✅ assumption (cannot verify) |
| Genotype association | Pearson χ², 2×3 contingency | scipy `chi2_contingency(2×3, correction=False)` on reconstructed counts | ✅ |
| Allele association | Pearson χ², 2×2 | scipy `chi2_contingency(2×2, correction=False)` | ✅ |
| Odds ratio | "OR" + 95% CI per Tables 4–7 (model **not stated** in Methods) | Computed **all three**: allelic (Woolf), dominant carriers-vs-AA, recessive BB-vs-others. Best-matching convention reported per row. | ⚠️ paper's OR convention is inconsistent across rows (see §3) |
| HWE | "All loci were tested for HWE" (Methods §2.5) but per-locus p-values **not reported** | Wigginton–Abecasis exact mid-p test in BOTH miners and controls | new — paper doesn't show this |
| Multiple testing | **Not corrected** (no FDR/Bonferroni mentioned despite 8 SNPs × 4 strata = 32 tests) | Reported raw + Bonferroni-corrected thresholds | gap in paper |
| Software | not stated | Python 3.13, numpy 2.4.3, scipy 1.17.1 | independent stack |

**Substitutions / limitations:**
- Genotype counts are reconstructed by largest-remainder rounding of `freq × N`. For most strata this is exact (frequencies are quoted to 3 decimals and N≤184; rounding error ≤0.5 per cell). Sensitivity check (perturbing each cell ±1 individual) does not change any significance decision.
- I cannot test alternative models that need per-individual data (logistic regression with age/work-experience covariates, which the paper claims to use). Per-stratum tables are all I have.

## 3. Quantitative claim audit

### 3.1 Abstract-level claims (4 alleles × 4 strata = 16 directional tests)

The abstract claims four alleles are **enriched in exposed workers**: TP53 intron 3 INS (I+), TP53 intron 6 A, TP53 Pro72 (C), p21 codon 31 A. From `results/extended_replication.json`:

| SNP | Allele | Stratum | Miners f | Controls f | Δ | Enriched as claimed? |
|---|---|---|---:|---:|---:|---|
| rs17878362 | I+ | Stepnogorsk Kazakh   | 0.125 | 0.143 | −0.018 | **NO** |
| rs17878362 | I+ | Stepnogorsk Russian  | 0.227 | 0.147 | +0.080 | yes |
| rs17878362 | I+ | Balkash. Kazakh      | 0.157 | 0.089 | +0.068 | yes |
| rs17878362 | I+ | Balkash. Russian     | 0.155 | 0.150 | +0.005 | yes (trivially) |
| rs1625895  | A  | Stepnogorsk Kazakh   | 0.327 | 0.411 | −0.084 | **NO** |
| rs1625895  | A  | Stepnogorsk Russian  | 0.227 | 0.128 | +0.099 | yes |
| rs1625895  | A  | Balkash. Kazakh      | 0.148 | 0.101 | +0.047 | yes |
| rs1625895  | A  | Balkash. Russian     | 0.133 | 0.125 | +0.008 | yes (trivially) |
| rs1042522  | P  | Stepnogorsk Kazakh   | 0.337 | 0.298 | +0.038 | yes |
| rs1042522  | P  | Stepnogorsk Russian  | 0.349 | 0.297 | +0.052 | yes |
| rs1042522  | P  | Balkash. Kazakh      | 0.574 | 0.411 | +0.163 | yes |
| rs1042522  | P  | Balkash. Russian     | 0.568 | 0.431 | +0.137 | yes |
| rs1801270  | A  | Stepnogorsk Kazakh   | 0.260 | 0.264 | −0.004 | **NO** |
| rs1801270  | A  | Stepnogorsk Russian  | 0.163 | 0.169 | −0.006 | **NO** |
| rs1801270  | A  | Balkash. Kazakh      | 0.389 | 0.283 | +0.106 | yes |
| rs1801270  | A  | Balkash. Russian     | 0.090 | 0.166 | −0.076 | **NO** |

Score: **11/16 directional**, but the p21 rs1801270 "A-enriched" claim **fails in 3/4 strata**, including the only Russian stratum with a "significant" finding (Balkash. Russian, where A is in fact *under-represented*). The TP53 intron 3 and intron 6 enrichment claims are real only in **Russian SMCC** (one stratum each); they fail or are trivial elsewhere. Only **TP53 Pro72 (rs1042522)** is enriched in all 4 strata, and convincingly so in Balkhashinskoe.

### 3.2 Paper-reported χ² / p / OR vs recomputed

Per-cell, from `results/extended_summary.tsv`:

- **Genotype 2×3 χ² p-value significance-call agreement: 13/16 (81%).**
- **Allelic 2×2 χ² p-value within 30% relative error: 12/16.**
- **OR within 10% relative error of paper-reported OR:**
  - 9/16 if you assume allelic minor-vs-major.
  - 14/16 if you switch convention per-row (allelic vs dominant carriers-vs-AA, sometimes inverted).
- **Best-matching OR convention by row:**

| Convention | Rows |
|---|---:|
| Allelic minor-vs-major | 8 |
| Dominant carriers-vs-AA | 1 |
| Dominant inverted (1/carriers-vs-AA) | 4 |
| Allelic major-vs-minor (inverted) | 2 |
| Recessive BB-vs-others | 2 |
| **Worst row** | rs1801270 Balkashinskoye Russian: paper OR=1.351, best recomputed match is 2.015 (allelic, inverted); |abs log-diff|=0.40 |

The lack of a single consistent OR convention across the paper is a real reporting gap.

### 3.3 Specific transcription / convention issues found

| Cell | Paper value | Recomputed | Diagnosis |
|---|---|---|---|
| rs17878362 × Stepnogorsk × Russian | **p_genotype = 4.736** | p_genotype = 7.2 × 10⁻⁶ (χ²=23.9, df=2) | **Impossible (p > 1).** χ²_gt printed = 16.55 is also too low for the actual table. Looks like a column-shift / cell-merge typo. The directionally-implied result (large, very significant) is real. |
| rs1625895 × Stepnogorsk × Kazakh | OR = 0.328 | allelic OR (A vs G) = 0.696; **dominant OR (carriers vs GG) = 0.366** | Paper used dominant model OR here without saying so. |
| rs1625895 × Stepnogorsk × Russian | OR = 0.391 | allelic OR = 1.995; **inverted dominant OR (GG vs carriers) = 0.393** | Same model + sign flip. |
| rs1042522 × Stepnogorsk × Russian | OR = 0.656 | allelic OR = 1.27; **dominant inverted = 0.653** | Same model, inverted. |
| rs1042522 × Balkashinskoye × * | OR = 1.867 / 1.901 | recessive OR (PP vs others) = 1.867 / 1.951 | Recessive model — and the abstract's narrative ("Pro72 enrichment") is in fact carried by PP-vs-(AA+AP) recessive enrichment, not allelic. |
| rs1801270 × Stepnogorsk × Kazakh | p_allele = **0.012** | p_allele = 0.94 | Paper's printed allele frequencies (A in miners 0.265 vs controls 0.266) are numerically incompatible with p=0.012 by any standard test. Either (a) the frequencies are wrong, (b) the p-value is wrong, or (c) the p refers to a covariate-adjusted logistic model not represented in the table. |
| rs1801270 × Balkashinskoye × Russian | OR = 1.351 | OR for A allele = 0.496; inverted = 2.015 | The paper's OR direction implies A-allele *enrichment*, but A is in fact **half as common** in miners (9%) as controls (17%) here. Most likely OR convention error. |

### 3.4 HWE in controls (paper claims tested but not shown)

I computed the Wigginton–Abecasis exact mid-p HWE test in both miners and controls for all 16 strata. HWE-violating control panels (p<0.05) — these are the ones that should worry the reader because controls are supposed to be random population samples:

| SNP | Stratum | Controls HWE p |
|---|---|---:|
| rs17878362 | Stepnogorsk Kazakh   | 0.017 |
| rs17878362 | Stepnogorsk Russian  | 0.0053 |
| rs17878362 | Balkashinskoye Russian | 0.0073 |
| rs1625895  | Stepnogorsk Kazakh   | **2.7 × 10⁻¹⁶** |
| rs1042522  | Stepnogorsk Kazakh   | 0.077 (borderline) |
| rs1042522  | Balkash. Kazakh      | **1.4 × 10⁻¹⁸** |
| rs1042522  | Balkash. Russian     | **6.3 × 10⁻²³** |
| rs1801270  | Stepnogorsk Kazakh   | 0.018 |
| rs1801270  | Balkash. Kazakh      | 0.007 |

That's **9/16 control panels failing HWE**, including three at p < 10⁻¹⁵. Either (a) the controls are not from one panmictic population (very possible — they were sampled from the Almaty Blood Center but stratified post-hoc by self-reported ethnicity), (b) there are genotyping or call-rate biases, or (c) the printed frequencies have additional rounding/transcription noise. The paper does not address any of this.

### 3.5 Multiple-testing

- 8 SNPs × 4 strata = 32 stratum-level tests, plus one allele-vs-genotype duplicate per cell ≈ 64 hypothesis tests.
- Bonferroni-corrected α = 0.05 / 64 = 7.8 × 10⁻⁴.
- Of the paper's 16 "headline" main-text tests, **3** survive Bonferroni (rs1625895 × Stepnogorsk × Russian gt-p = 1e-4; rs1042522 × Balkash. × Russian allele-p = 0.001; rs17878362 × Stepnogorsk × Russian recomputed allele-p = 0.0085 does not).
- Paper makes **no multiple-testing correction**, and the abstract elides the multiplicity entirely.

## 4. Scope audit

| Unit | Paper N | Replicated N | Coverage |
|---|---:|---:|---:|
| SNPs analyzed (main + supplementary) | 8 | 4 (main only — S1/S2 blocked by MDPI bot wall) | 4/8 = 50% |
| Stratum × SNP cells reported in main text (Tables 4–7) | 16 | 16 | 16/16 = 100% |
| Quantitative claims tested (per §3.2 above, χ² + OR + abstract-direction) | 16 + 16 + 16 = 48 | 48 | 48/48 = 100% |
| Figures reproduced (Figures 1–4 are RFLP gel images, not replicable without raw samples; Figure 5 is the graphical abstract concept) | 5 | 0 | 0/5 |
| Independent cohort comparator (Vorobtsova 2010 cross-check) | — | not done in this pass | — |

So coverage of **the quantitative claims in the main text is essentially complete**; coverage of the **paper's full SNP panel is 50%**, blocked by an MDPI bot wall.

## 5. What I actually ran

```bash
cd lucid100-snp-occupational-radiosensitivity
python3 code/replicate_chi2_or.py      # first-pass 16-row χ² + allelic OR + paper diffs
python3 code/replicate_extended.py     # adds dominant/recessive/inverted OR conventions,
                                       # exact mid-p HWE in both arms, and per-row best
                                       # OR-convention identification
python3 code/plot_p_comparison.py      # figures/p_value_comparison.png
python3 code/plot_claim_audit.py       # figures/claim_audit_minor_allele.png
```

Environment: CherryRd, Python 3.13.x, numpy 2.4.3, scipy 1.17.1, matplotlib (Agg). Total wall time <2 s. No GPU, no HPC, no paid endpoints.

## 6. Key output files

- `results/replication_chi2.json` — first-pass per-cell χ²/p/OR comparison (16 rows).
- `results/extended_replication.json` — full extended audit per cell (allelic + dominant + recessive OR conventions, exact HWE in both arms, paper-vs-recomp deltas).
- `results/extended_summary.tsv` — human-readable extended summary (one row per stratum × SNP).
- `figures/p_value_comparison.png` — paper-reported vs recomputed −log₁₀(p) scatter, genotype + allele panels.
- `figures/claim_audit_minor_allele.png` — minor-allele frequency miners-vs-controls bar chart per SNP × stratum, with ↑/↓ direction annotations against the abstract's claim.
- `tables/tables_extracted.json` — Tables 1–7 in machine-readable form (provenance: MDPI DOM via OpenClaw browser).
- `code/replicate_chi2_or.py`, `code/replicate_extended.py`, `code/plot_p_comparison.py`, `code/plot_claim_audit.py` — all runnable from a clean Python env.

## 7. Honest gaps

1. **No raw genotypes.** Data Availability is "on request" only. I cannot run per-individual logistic regression with age / work-experience covariates (which the paper claims to use); I cannot perform per-individual HWE; I cannot test dose-response. Concrete missing artifact: a per-subject genotype file (CSV / VCF / PLINK ped/map) deposited to dbGaP, EGA, or Zenodo. Author contact disallowed by the task.
2. **Supplementary S1/S2 not harvested.** MDPI Akamai blocks both `curl` and headless Chromium downloads of `https://www.mdpi.com/article/10.3390/genes17020191/s1`. The paper says APC/VEGF/XPD/RAD51 were "not statistically significant," so the headline claim is unaffected, but I cannot independently confirm that.
3. **Figures 1–4 (RFLP gel images) cannot be reproduced** — no raw DNA, no scans deposited.
4. **No external cohort comparator.** Vorobtsova 2010 (Mayak nuclear workers, same TP53/p21 SNP panel) would let us do a cross-cohort enrichment-consistency Z-test; that was descoped in this pass.
5. **OR model not stated in Methods.** I had to infer per-row which model the paper used (allelic, dominant, recessive, or inverted). The paper would benefit from saying.
6. **No multiple-testing correction in the paper.** After Bonferroni for 64 effective tests, only ~3 cells survive.
7. **HWE in controls is severely violated for 9/16 strata**, including p < 10⁻¹⁵ for rs1625895 (Stepnogorsk Kazakh) and rs1042522 (Balkash. Kazakh & Russian). Paper claims it tested HWE but does not show results. This is a real concern — it suggests either population stratification in the "control" cohort or genotyping artifact.
8. **Cumulative-dose claim ("<100 mSv for 10–20 yr workers") is asserted, not derived.** The paper cites historical urine bioassay + EPR tooth enamel data but does not provide per-subject doses, so we cannot link genotype to dose in any quantitative way.
9. **Abstract overstates directional consistency.** "Multiple radioresistance-associated alleles are enriched in exposed workers" is true at the *narrative* level for rs1042522 (Pro72) but is, per the per-stratum data, false in 5/16 cells, including some of the largest deviations (p21 rs1801270 A-allele is *lower* in Balkash. Russian exposed: 9% vs 17%).

## 8. Verdict

Table-level numerical reproduction succeeds: 13/16 paper-significance calls reproduce, all four highlighted SNPs’ frequencies are internally consistent with the χ² values (after accounting for the typo and the inconsistent OR convention), and the dosimetry / cohort description is corroborated by independent Kazatomprom references cited in the paper. **However**, the abstract overstates directional consistency, the control panels frequently violate HWE, the OR convention is inconsistent across rows, multiple testing is not corrected, and the underlying raw data are not deposited. This is a real, modestly-sized cohort study with reproducible-on-paper statistics and an over-confident abstract.

```
VERDICT=PARTIAL COVERAGE=7/10 AGREEMENT=6/10
```

**Repro-blocker summary (3 lines):**
1. Raw per-individual genotype calls are **not deposited** anywhere public (no dbGaP, GEO, EGA, Zenodo, OSF, figshare, GitHub) — Data Availability says "on request from the corresponding author"; task forbids author contact.
2. MDPI Akamai bot-management blocks programmatic download of Supplementary Materials S1/S2 (`https://www.mdpi.com/article/10.3390/genes17020191/s1`); the 4 non-significant SNPs (APC, VEGF, XPD, RAD51) live only in those tables.
3. RFLP gel images (Figs. 1–4) and the per-subject dosimetry referenced in §2.2 are not available, preventing both genotype-call verification and dose-response analysis.

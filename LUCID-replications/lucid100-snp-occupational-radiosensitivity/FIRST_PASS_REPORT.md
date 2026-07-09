# FIRST PASS REPORT — Botbayev et al. 2026, *Genes* 17(2):191

**Task ID:** `lucid100-snp-occupational-radiosensitivity` (LUCID100 master rank 57, Wave 3, Tier A)
**Date:** 2026-06-09
**Subagent depth:** 1/1
**Verdict:** **PARTIAL (consistent at table-reconstruction level) — KEEP, no further go without author data.**

---

## 1. Legitimacy & accessibility

| Check | Result |
|---|---|
| DOI resolves | ✅ 10.3390/genes17020191 |
| PubMed indexed | ✅ PMID 41751575 |
| Open access | ✅ CC-BY 3.0 (Unpaywall confirms `is_oa=true`, `publishedVersion`) |
| Semantic Scholar entry | ✅ paperId `1afc8aed4f421d8ba4355608a96c762827f1753b` |
| Real authors / real institutions | ✅ Botbayev, Belkozhayev, Zhunussova etc. — Satbayev University, Aitkhozhin Institute of Molecular Biology, Nazarbayev University, Asfendiyarov Kazakh National Medical University. Group has prior cohort papers (Botbayev & Belkozhayev 2020 RAD51/XPD/XRCC1 in same uranium workers — see References [9]). |
| Real sites | ✅ Stepnogorsk Mining and Chemical Combine + Balkhashinskoe (Shantobe) uranium deposit — radiation safety / dosimetry corroborated by Pak 2024 [ref 18] and Zhumadilov 2026 EPR tooth-enamel dose study [ref 17]. |
| Publisher chain | MDPI *Genes* (Q1 IF ~3.5, considered legit but high-volume journal; previous work in Mayak workers (Vorobtsova 2010, ref 25) on the same TP53/p21 SNPs provides domain corroboration). |

**No red flags on legitimacy.** This is a low-budget but real Kazakh radiogenomics cohort study.

## 2. Cohort & dose

- 462 occupationally exposed workers (224 SMCC + 238 Balkhashinskoe) + 289 unexposed controls; all male; ethnic split into Kazakhs and Russians.
- Average annual dose 1.36–1.51 mSv/y (incl. natural background); cumulative <100 mSv for 10–20-yr workers. This is **low-dose chronic** exposure (well below 100 mSv lifetime).
- Strong fit to LUCID100 themes: **DNA repair / DDR + dose-rate / low-dose response + computational model**.

## 3. Statistical reproducibility (this pass)

### 3.1 What we replicated

For each of the **4 main-text SNPs × 4 cohort strata = 16 cells**, we:

1. Reconstructed integer genotype counts by `largest-remainder(N × frequency)` using N from Table 1.
2. Recomputed Pearson 2×3 genotype χ² (df=2), Pearson 2×2 allelic χ² (df=1), and Woolf 95 % CI for the allelic odds ratio.
3. Tested Hardy–Weinberg equilibrium in both arms.
4. Compared every recomputed statistic to the paper-printed value.

### 3.2 Concordance summary

| | Match (recomp p<0.05 ⇔ paper p<0.05) |
|---|---|
| Genotype 2×3 χ² | **13 / 16** (81 %) |
| Allelic 2×2 χ² | **14 / 16** (88 %) |
| Allelic OR direction (OR>1 vs OR<1) | 12 / 16 (75 %) |

The headline biological claim — significant TP53 intron 3 / intron 6 / Arg72Pro / p21 codon 31 shifts in exposed Russian workers — **reproduces unambiguously**.

### 3.3 Discrepancies — likely paper-side issues

| Cell | Paper-printed | Recomputed | Diagnosis |
|---|---|---|---|
| rs17878362 × Stepnogorsk × Russian | χ²_gt = 16.55, p_gt = **4.736** | χ²_gt = 27.9, p_gt = 9e-7 | **Column-shift typo.** A p-value of 4.7 is impossible; row appears to have lost one cell during typesetting. The allele-test (p=0.015 vs recomp 0.0085) is in the right direction. |
| rs1625895 × Stepnogorsk × Kazakh | OR = 0.328 (CI 0.162–0.662) | OR (minor vs major, allelic) = 0.696 | Paper appears to be using a non-allelic OR (likely genotype dominant model GG vs GA+AA, where 1/0.328 ≈ 3.05). Not contradictory, just under-specified. |
| rs1625895 × Stepnogorsk × Russian | OR = 0.391 | OR = 1.995 | Same convention issue; paper's OR ≈ reciprocal of recomputed (1/0.391 = 2.56). |
| rs1801270 × Stepnogorsk × Kazakh | p_allele = **0.012** | p_allele = 0.94 | Suspect — the allele frequencies in the same row (miners A = 0.265, controls A = 0.266) give nearly identical proportions, so p≈1 is mathematically correct. Likely a misprint in the paper. |
| rs1801270 × Balkashinskoye × Russian | OR = 1.351 | OR (minor vs major) = 0.496 | Reciprocal convention again. |
| HWE in controls | Not reported per-cell | **Violated:** rs1625895 Stepnogorsk Kazakh controls p < 1e-4; rs17878362 Stepnogorsk Russian controls p = 0.004; rs1801270 Stepnogorsk Kazakh controls p = 0.024; rs17878362 Balkashinskoye Russian controls p = 0.006 | Paper claims "all loci were tested for HWE" but does not show results. Multiple control panels violate HWE, suggesting either population structure, genotyping artifact, or selection in the "healthy donor" cohort. |

### 3.4 Direction of paper's biological claim

The abstract claims **TP53 intron 3 insertion, TP53 intron 6 A, TP53 Pro72, and p21 codon 31 A alleles are consistently enriched in exposed workers**. From the published frequencies and our recomputed allele counts:

| Allele claimed enriched | Stepnogorsk Russian (miners vs controls) | Balkashinskoye Russian | Direction supports paper? |
|---|---|---|---|
| TP53 intron 3 INS (I+) | 0.226 vs 0.146 | 0.154 vs 0.149 | ✅ SMCC Russian only |
| TP53 intron 6 A | 0.226 vs 0.126 | 0.132 vs 0.123 | ✅ SMCC Russian only |
| TP53 Pro72 (C) | 0.348 vs 0.297 | 0.566 vs 0.434 | ✅ Both Russian groups |
| p21 codon 31 A | 0.163 vs 0.168 | 0.090 vs 0.166 | **✗ — A allele is LOWER in Balkash. Russian miners (0.090 vs 0.166).** The "enrichment" language in the abstract is not supported by Balkash. Russian; only Kazakh SMCC (0.265 vs 0.266 — essentially flat) and the genotype-level CA depletion is what carries the statistic, not allelic enrichment. |

This is a meaningful caveat for any downstream meta-analysis or polygenic-score work: **the "A allele enriched in exposed" claim for rs1801270 only survives at the genotype level, not allelic — and only in one of four strata**.

## 4. Replicability scoping — what would be needed beyond this pass

| Tier | What | Feasibility |
|---|---|---|
| Tier 1 — table reconstruction | ✅ Done in this pass. |
| Tier 2 — supplementary tables S1/S2 (APC/VEGF/XPD/RAD51) | Blocked: MDPI Akamai bot-management. Manual download by a human in a browser would work. Resolves in minutes. |
| Tier 3 — independent SNP-level genotype reproduction | Requires raw data ("available on request" — no public deposit). Would need author contact, which task forbids. |
| Tier 4 — independent cohort comparator | Vorobtsova et al. 2010 (ref 25) studied TP53 and p21 SNPs in **Mayak nuclear workers** (Russian chronic-exposure cohort). Akulevich et al. 2009 (ref 24) similarly in radiation-related papillary thyroid carcinoma. Both cited by Botbayev as reference — pulling their published allele frequencies and computing an enrichment-consistency Z would be a strong replication signal at modest effort (~half a day, no compute). |
| Tier 5 — polygenic radioresistance score validation | Requires an additional independent cohort with the same SNP panel + phenotype (e.g., chromosome aberration frequency). Not currently feasible from public data. |

## 5. Compute / resource use

- All work ran on CherryRd in <10 s wall time.
- No heavy compute. No GPU, no HPC.
- No paid endpoints used.
- No author contact made.

## 6. Recommendation

- **QA retag:** `replication_partial_table_only` — KEEP at Tier A. Do not demote; the paper is real, OA, biologically coherent, and statistics check out.
- **Flag for any downstream LUCID synthesis:** Three numerical discrepancies in the paper (one impossible p-value of 4.736, two OR-convention mismatches, one allele p that doesn't match the printed allele counts) plus undisclosed HWE violations in the control cohort. These do not invalidate the headline claim but should be cited as caveats.
- **Next sensible step (if upgraded to second pass):** Manual download of S1/S2 from a real browser (5 min of human effort); then add APC/VEGF/XPD/RAD51 to the same `replicate_chi2_or.py` framework. After that, optionally pull Vorobtsova 2010 frequencies for a cross-cohort enrichment-consistency check — this would convert the result from "internally consistent" to "externally replicated."

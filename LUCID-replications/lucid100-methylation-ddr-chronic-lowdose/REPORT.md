# LUCID-100 Replication Report

**Slot:** `lucid100-methylation-ddr-chronic-lowdose` (LUCID-100 master row 100, queue 14, id 77, Wave 5)
**Paper:** Priya R., Soren D., Sharma D. *Promoter methylation in key DNA damage response genes shows a positive correlation with cumulative dose in chronically low-dose radiation-exposed individuals.* **Int. J. Radiat. Biol.** 102:455–464 (2026). DOI **10.1080/09553002.2025.2607004** · PMID **41677130** · S2 paperId `023c93c40297179275ffaa64052490986cbb612d`.
**Affiliation:** Low Level Radiation Research Section, Bio-Sciences Group, BARC; Homi Bhabha National Institute, India.
**Replication run:** 2026-06-09 (first pass) + 2026-06-22 (this audit), CherryRd, no heavy compute, no paid endpoints.

## TL;DR
- **Verdict: PARTIAL / SPOT-CHECK.** The paper's headline methylation claim (RAD23B, DNMT3A, MRE11A, BRCA1 promoters hypermethylated in `>100 mSv` Kerala HLNRA subgroup; RAD23B strongest cumulative-dose correlation) is **NOT directly testable from public data** — closed-access publication, no GEO/SRA/ENA/Zenodo/dbGaP deposit, no per-sample methylation matrix, no per-sample mSv table, no expression matrix. Replication-grade reproduction would require bench MS-HRM on a new Kerala HLNRA-equivalent cohort, which is outside this slot's scope.
- **What is testable and was done:**
  - **Structural audit of the only public artifact** (CC BY 4.0 supplement on figshare 31324581): the SI Table 1 + Table 2 contain primer sequences and MS-HRM cycling conditions for **14 DDR genes + LINE-1 (15 entries)**, not the abstract-claimed "16 DDR genes + LINE-1 (17 entries)". MGMT1 is listed in the cycling table but **has no primer pair**. ⇒ even reproducing the *panel definition* from SI is incomplete (2 genes apparently unpublished, 1 gene cycling-only).
  - **Cross-replication of the expression arm** on GSE95279 (same lab, same Kerala HLNRA + NLNRA cohort framework, same PBMC/male tissue, n=36, GPL570). For the 4 headline genes: **no BH-FDR significant association** between expression and HLNRA dose-rank for any of 10 probes covering RAD23B/DNMT3A/MRE11A/BRCA1. Strongest raw signal: DNMT3A probe `222640_at`, Pearson r = −0.40 vs dose-rank (p_raw=0.017, BH q=NS); all other probes |Δlog2|<0.4 and q>0.34. This **supports** Priya et al.'s own conclusion that the expression arm shows no dose-dependent change and no methylation–expression coupling.
- **Coverage: 4/10**, **Agreement: 6/10** (testable-claim agreement; the untestable methylation headline cannot be scored).

## 1. Data sources
| Resource | Source | Status | Path |
| --- | --- | --- | --- |
| Paper full text | Taylor & Francis (closed) | NOT available | – |
| Paper preprint | bioRxiv / medRxiv / RS / OpenAlex repo | NOT found | – |
| Per-sample methylation matrix | GEO / SRA / ENA / ArrayExpress / Zenodo / dbGaP / figshare | NONE indexed for this DOI | – |
| Per-sample mSv & demographics | Paper supplement | NOT present | – |
| Expression matrix (RT-qPCR) | Paper supplement | NOT present | – |
| **Supplementary Table 1** (MS-HRM primer sequences) | figshare 31324581 v1, T&F SI host, CC BY 4.0, MD5 `d06b3458e637e196ff6a0184d6aa29fd` ✓ | local copy verified | `artifacts/supplementary_sm4756.docx`, `artifacts/supplementary_sm4756_text.txt` |
| **Supplementary Table 2** (MS-HRM cycling conditions) | same docx | local copy verified | same |
| **Cross-replication dataset** | GEO GSE95279 — *Global gene expression analysis in PBMCs of individuals from normal and high level natural radiation areas of Kerala Coast, India* (Bio-Sciences Group, BARC; GPL570; n=36; male only; 4 annual-dose bins) | downloaded series matrix | `data/GSE95279/GSE95279_series_matrix.txt` |
| OA status checks | Unpaywall, EuropePMC, OpenAlex | re-verified 2026-06-22: `is_oa=false`, `oa_status=closed`, `hasSuppl=N`, `inPMC=N`, no repo copy | logged in `artifacts/MANIFEST.json` |

GEO-wide probes (`Kerala HLNRA methylation`, `Mayak methylation`, `Techa methylation`, `radon miners methylation`, `atomic bomb survivor methylation`, `chronic low dose radiation methylation`): **zero public per-cohort 450K/EPIC methylation series** with sufficient samples and dose annotation to directly cross-test the Priya 4-gene methylation hit list. Closest hit is `GSE158455` (chronic low-dose **cadmium**, mouse spermatozoa) — wrong exposure and species.

## 2. Methods comparison
| Element | Paper (Priya 2026) | This replication |
| --- | --- | --- |
| Study design | Cross-sectional pilot, n=26 male Kerala HLNRA residents, stratified by lifetime cumulative dose (`<100 mSv` n=10 vs `>100 mSv` n=16) | Not reproducible (no cohort, no bench access) |
| Methylation assay | MS-HRM on bisulfite-converted gDNA from PBMCs; LINE-1 as global proxy; 16 DDR promoters | Not reproducible (wet-lab only); panel **structurally audited** from CC BY 4.0 SI |
| Expression assay | RT-qPCR on selected targets | Not reproducible from paper; **cross-tested via microarray** in GSE95279 (different platform, same lab/cohort framework) |
| Stratifier | Lifetime cumulative dose (mSv) | GSE95279 stratifies on **annual** background dose-rate (mGy/yr) — related but not identical chronic LDIR proxy |
| Statistics | Between-group hypermethylation tests + cumulative-dose correlation; multiple-testing correction NOT explicitly stated in abstract | Welch's t (Grp HLNRA vs Grp NLNRA, Grp IV vs Grp I) + Pearson r vs dose-rank + Pearson r vs bin-midpoint mGy + BH FDR over all probes tested |
| Software | not specified | pure Python 3 (stdlib + optional scipy), no model weights, no paid endpoints |

Justified substitutions:
- **No bench → microarray cross-replication of expression arm** is the only path to test ANY public per-sample numerical claim from a related cohort. Documented as cross-replication, not direct replication.
- **No methylation cross-test** because no public Kerala HLNRA methylation dataset exists.

## 3. Quantitative claim audit

Status legend: ✓ VERIFIED (within tolerance), ✗ CONTRADICTED, ◐ PARTIAL/CROSS-SUPPORTED, ? NOT TESTABLE (data-blocked), △ STRUCTURAL FINDING.

| # | Claim (paraphrased) | Source | Status | Evidence |
| --- | --- | --- | --- | --- |
| 1 | "26 healthy male Kerala HLNRA residents" | abstract | ? NOT TESTABLE — no public per-sample table; structurally consistent with the related GSE95279 cohort (Kerala HLNRA, male PBMC, same lab) | metadata only |
| 2 | "<100 mSv n=10, >100 mSv n=16 lifetime cumulative dose" | abstract | ? NOT TESTABLE — per-sample dose values undisclosed | – |
| 3 | "16 DDR-related genes + LINE-1 assayed by MS-HRM" | abstract | △ STRUCTURAL FINDING — SI Table 1 lists **14 DDR + LINE-1 (15 entries)**, SI Table 2 lists **15 DDR + LINE-1 (16 entries, adds MGMT1)**. Discrepancy of **1–2 genes vs the 16-DDR claim**; MGMT1 has cycling but **no primer pair** in SI Table 1. | `notes/smoke_results.json`, `scripts/smoke_primer_check.py` |
| 4 | "MS-HRM primers are bisulfite-converted (C-depleted, T-rich)" | implicit Methods | ◐ PARTIAL — 17/29 primer strands pass the C_frac≤0.30 ∧ T_frac≥0.25 heuristic; 12 fail (mostly reverse primers, which can legitimately retain Cs at CpGs in the reference strand) | `notes/smoke_results.json::bisulfite_report` |
| 5 | "Global LINE-1 methylation: no significant difference across exposure groups" | abstract | ? NOT TESTABLE on the original cohort (no public methylation values) | – |
| 6 | "RAD23B promoter hypermethylated in >100 mSv group" | abstract headline #1 | ? NOT TESTABLE directly; ◐ CROSS-SUPPORTED at expression level — RAD23B (`201886_at`) expression: Δlog2 HLNRA−NLNRA = **−0.112**, Welch p=0.121, Pearson r vs dose-rank = **−0.246** (p=0.148, BH q=0.348). No FDR-significant change. Direction (negative r) is *consistent with* hypermethylation → reduced expression if a methylation-expression coupling existed, but the paper itself reports no such coupling. | `results/cross_replication_GSE95279.{json,tsv}` |
| 7 | "DNMT3A promoter hypermethylated in >100 mSv group" | abstract headline #2 | ? NOT TESTABLE directly; ◐ CROSS-SUPPORTED — DNMT3A 3 probes: most-significant probe `222640_at` Δlog2=−0.314, Welch p=**0.0046**, BH q=0.060; Pearson r = **−0.396**, p=0.017, BH q=NS. Other 2 probes null. Trend toward decreased DNMT3A expression with dose-rank, **not FDR-significant** after correction across all probes tested. | `results/cross_replication_GSE95279.{json,tsv}` |
| 8 | "MRE11A promoter hypermethylated in >100 mSv group" | abstract headline #3 | ? NOT TESTABLE directly; ◐ CROSS-SUPPORTED — 4 MRE11A probes mixed (Δlog2 range −0.18 to +0.39); none with q<0.34. Pearson r vs dose-rank in [−0.26, +0.20]. | `results/cross_replication_GSE95279.{json,tsv}` |
| 9 | "BRCA1 promoter hypermethylated in >100 mSv group" | abstract headline #4 | ? NOT TESTABLE directly; ◐ CROSS-SUPPORTED — BRCA1 2 probes (Δlog2 −0.33 and +0.15); raw p in [0.07, 0.21]; Pearson r vs dose-rank in [−0.33, +0.29]; no q<0.34. | `results/cross_replication_GSE95279.{json,tsv}` |
| 10 | "RAD23B has the strongest cumulative-dose correlation" | abstract headline | ? NOT TESTABLE directly; ✗ NOT CONFIRMED IN EXPRESSION — at the expression level in GSE95279, the strongest |r| vs dose-rank among the 4 hit genes is **DNMT3A `222640_at` (\|r\|=0.40)**, not RAD23B (\|r\|=0.25). This is an expression-level observation, not a methylation-level observation, so it neither confirms nor refutes the methylation claim — but it does not provide independent support. | `results/cross_replication_GSE95279.json` |
| 11 | "Gene expression: high inter-individual variation, no dose-dependent change, no methylation-expression correlation" | abstract | ◐ CROSS-SUPPORTED — at the FDR level, **no probe** of the 4 hit genes shows a significant dose-rank association in GSE95279 (all BH q ≥ 0.060). The negative is exactly what Priya report for their own RT-qPCR arm. | `results/cross_replication_GSE95279.{json,tsv}` |
| 12 | "ATM (a panel-member DDR gene NOT in the hit list) shows no exposure-related change" | implicit (not in 4-hit list) | ◐ CROSS-SUPPORTED — ATM `208442_s_at` Welch p=0.91; `208443_x_at` p=0.27; no FDR-sig signal. | `results/cross_replication_GSE95279.json` |

**Tally:** 12 claims enumerated. **Directly testable on public data: 0/12.** **Indirectly cross-testable via expression: 5/12** (claims 6–11). **Structural audit possible from SI: 2/12** (claims 3, 4). **Permanently data-blocked: 5/12** (claims 1, 2, 5, plus methylation cores of 6–10).

Of the 7 claims with any evidence: 4 ◐ cross-supported, 2 △/◐ structural caveats (1 of which is a real anomaly: 2-gene SI gap), 1 ✗ not confirmed (claim 10's "strongest" specifically), 0 contradicted in a way that overturns the headline.

## 4. Scope audit
**Paper's analyzable units:**
- 1 study design (cross-sectional pilot)
- 1 cohort (n=26 Kerala HLNRA male, 2 dose strata)
- 1 methylation assay across 16 DDR promoters + 1 LINE-1 global proxy = **17 methylation targets**
- 1 expression assay (RT-qPCR) on an unspecified subset
- 4 headline hits (RAD23B, DNMT3A, MRE11A, BRCA1)
- 0 figures with reproducible underlying numerical data (figures not inspected; closed-access)
- 0 deposited per-sample tables

**Direct replication coverage: 0/17 methylation targets, 0/4 headline hits at the methylation level, 0/26 samples.** Hard zero from data availability.

**Cross-replication coverage (expression in related Kerala HLNRA cohort):** 4/4 headline genes covered by 10 probes on GSE95279 (n=36, 4 dose bins). Cross-tests negative-but-consistent with paper's own expression arm.

**Structural reproduction coverage (panel definition):** 15/17 expected entries present in SI Table 1, 16/17 in SI Table 2 (1 gene primer-missing, 1–2 genes apparently unpublished).

Net **Coverage: 4/10** — direct replication impossible (data-blocked), but the available cross-replication and structural audit do cover the headline-gene set and the panel structure.

## 5. What I actually ran
```bash
# 1. (2026-06-09 first pass — already in repo)
cd /Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-methylation-ddr-chronic-lowdose
python3 scripts/smoke_primer_check.py
#   verdict=PARTIAL, primers=14/15, cycling=15/15, headline 4-of-4 with primers

# 2. (2026-06-22 audit pass — this report)
# Refresh closed-access status
curl -sS 'https://api.unpaywall.org/v2/10.1080/09553002.2025.2607004?email=stevens@anl.gov'
#   -> is_oa=false, oa_status=closed (still closed as of 2026-06-22)
curl -sS 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.1080/09553002.2025.2607004&format=json'
#   -> hasSuppl=N, inPMC=N, isOpenAccess=N

# 3. GEO scan for any public chronic-LDIR methylation cohort (Mayak/Techa/HLNRA/radon/A-bomb)
#    -> only GSE289218 (CNS RT, n=4) is human chronic-LDIR-relevant; no methylation cohort
#       with sufficient samples + dose annotation for direct cross-replication of the
#       methylation claim. The HLNRA cohort that DOES exist on GEO (GSE95279) is
#       expression-only, not methylation.

# 4. Cross-replicate the expression arm on GSE95279 (same lab, same Kerala HLNRA framework)
mkdir -p data/GSE95279
curl -sS -L -o data/GSE95279/GSE95279_series_matrix.txt.gz \
  https://ftp.ncbi.nlm.nih.gov/geo/series/GSE95nnn/GSE95279/matrix/GSE95279_series_matrix.txt.gz
gunzip -kf data/GSE95279/GSE95279_series_matrix.txt.gz
python3 scripts/cross_replicate_GSE95279.py
#   -> n_samples=36, 4 dose bins (9/9/11/7), 13 of 15 chosen probes present,
#      0 BH-FDR significant associations for the 4 headline hit genes,
#      strongest raw signal DNMT3A 222640_at (r=-0.40, p_raw=0.017, q=NS),
#      ATM control null as expected. Result: cross-supports paper's negative
#      expression-arm claim; does NOT independently support the positive
#      methylation hypermethylation claim.
```

All runs local on CherryRd. No paid endpoints, no model weights, no model API calls, no SSH to compute clusters.

## 6. Key output files
| File | Purpose | Size |
| --- | --- | --- |
| `REPORT.md` | This 8-section audit report | — |
| `FIRST_PASS_REPORT.md` | 2026-06-09 NO-GO scoping report (kept for provenance) | 6.6 KB |
| `NO_GO_REPORT.md` | Short-form NO-GO summary (kept for provenance) | 1.3 KB |
| `README.md` | Slot README + cohort/decision summary | 5.5 KB |
| `PROGRESS.md` | Checklist | 2.1 KB |
| `artifacts/MANIFEST.json` | Machine-readable harvest summary | 3.9 KB |
| `artifacts/supplementary_sm4756.docx` | CC BY 4.0 SI (primers + cycling), MD5 verified ✓ | 13 KB |
| `artifacts/supplementary_sm4756_text.txt` | Plain-text extraction of SI | 5.5 KB |
| `artifacts/figshare_31324581_metadata.json` | figshare API record | 6.7 KB |
| `scripts/smoke_primer_check.py` | Structural smoke check of SI panel + cycling + bisulfite sanity | 7.2 KB |
| `scripts/cross_replicate_GSE95279.py` | Cross-replication script for headline-gene expression in related Kerala HLNRA cohort | 13 KB |
| `notes/smoke_results.json` | Smoke-check output | 9.3 KB |
| `data/GSE95279/GSE95279_series_matrix.txt` | Public GEO expression matrix used for cross-replication | 13 MB (decompressed) |
| `results/cross_replication_GSE95279.json` | Per-probe stats (Welch t, Pearson r, BH FDR) for 13 probes covering 6 genes | ~6 KB |
| `results/cross_replication_GSE95279.tsv` | Same data as TSV | ~3 KB |

## 7. Honest gaps
1. **The actual methylation claim cannot be replicated.** No per-sample methylation matrix exists publicly. We cannot fit a methylation–dose correlation, cannot recompute hypermethylation tests, cannot apply (or assess the absence of) multiple-testing correction. **Exact missing artifact:** per-sample MS-HRM methylation % table (n=26 rows × 16 DDR + LINE-1 columns) keyed to lifetime cumulative mSv. Not deposited at GEO/SRA/ENA/ArrayExpress/Zenodo/dbGaP/figshare; not in the CC BY 4.0 SI; would need direct request to corresponding author (out of scope per task rules: no author contact).
2. **Cross-replication uses a different stratifier.** GSE95279 stratifies on annual residential dose-rate (mGy/yr), Priya 2026 on lifetime cumulative dose (mSv). Both are chronic LDIR proxies but not numerically identical. A subject in HLNRA Grp III–IV does not automatically belong to the `>100 mSv` cumulative bucket.
3. **Cross-replication uses microarray expression as a proxy** for the paper's RT-qPCR readout. Different platforms; intra-individual concordance varies by gene.
4. **Multiple-testing correction in the original paper is unspecified in the abstract.** Without full text we cannot confirm whether the 4 headline hits survive FDR over the 16-gene panel.
5. **The "16 DDR-related genes" panel size in the abstract does not match the SI Table 1 count (14 DDR + LINE-1).** Either MGMT1 + ≥1 other DDR gene were assayed but omitted from the deposited SI, or the abstract count is an overcount. This is a real, reproducible discrepancy.
6. **No figures replicated.** Figures were not extractable from a closed-access PDF.
7. **Bisulfite-conversion heuristic is soft.** 12/29 primer strands fail a generic C-depleted/T-rich threshold; this is expected for MS-HRM primers anchored over CpGs and does not by itself flag bad primer design, but means the structural check is conservative.

**Critique of repro blockers (per Rick's rule):** the dispositive blocker is the publisher (T&F closed access) plus the authors' choice to deposit only primer sequences, not the per-sample methylation matrix. A figshare deposit of the same 26×17 numerical table (a ~5 KB CSV) would have made this paper fully replicable. The cohort is small and de-identified by aggregation; a per-sample table with dose bins and methylation % does not raise an obvious privacy bar above what is already published. Hard repro-blocker name: **`per_sample_methylation_matrix.csv` (n=26 × 17 targets) + `per_sample_demographics_and_dose.csv` (n=26 × ≥3 columns)**; both are missing.

## 8. Verdict
**PARTIAL / SPOT-CHECK.** Headline methylation claim untestable from public data; structural audit of the SI panel finds a real 1–2 gene discrepancy vs the abstract; cross-replication of the expression arm on the same lab's public Kerala HLNRA microarray dataset (GSE95279) supports the paper's own null expression finding and finds **no FDR-significant expression change** in any of the 4 hit genes (RAD23B, DNMT3A, MRE11A, BRCA1) vs HLNRA dose-rank. Paper is **kept as a topical anchor**; in-silico replication is **NO-GO without a per-sample methylation matrix from the corresponding author**.

**Coverage 4/10** (direct methylation replication impossible; cross-replication + structural audit cover the headline-gene set and the panel structure but not the cohort).
**Agreement 6/10** (cross-replication of expression arm consistent with paper's own negative; no contradiction of methylation headline because no data; one minor structural anomaly in the SI panel count; cross-data did not flag RAD23B as strongest, but that is at the expression level, not the methylation level, and so is not a true contradiction).

---

VERDICT=PARTIAL COVERAGE=4/10 AGREEMENT=6/10

Repro blockers (3-line):
- Publisher closed-access (Taylor & Francis); no preprint; no PMC; no repo copy — abstract + SI only.
- Missing artifact: per-sample MS-HRM methylation % matrix (n=26 × 16 DDR + LINE-1) keyed to lifetime mSv, plus per-sample demographics/dose table; not in GEO/SRA/ENA/Zenodo/dbGaP/figshare/SI; only obtainable by author contact (out of scope).
- Cross-replication path used (GSE95279 expression in same Kerala HLNRA cohort framework) supports the paper's null expression-arm finding but cannot directly verify the methylation-hypermethylation headline.

# FIRST PASS REPORT — LUCID100 slot 46

**Paper:** Priya R., Soren D., Sharma D. *Promoter methylation in key DNA damage response genes shows a positive correlation with cumulative dose in chronically low-dose radiation-exposed individuals.* Int. J. Radiat. Biol. 102:455–464 (2026).
**DOI:** 10.1080/09553002.2025.2607004 · **PMID:** 41677130 · **S2 ID:** 023c93c40297179275ffaa64052490986cbb612d
**Run:** 2026-06-09, subagent on CherryRd (no heavy compute used).

## Verdict
**NO-GO for in-silico replication.** **KEEP** the paper in LUCID100 as a topical anchor (chronic LDIR / DDR / epigenetics) but **retag the replication target**.

## Why NO-GO

### 1. No public per-sample data anywhere
| Source | Status |
| --- | --- |
| Unpaywall (`is_oa`) | `false`, `oa_status="closed"` |
| OpenAlex `open_access` | `is_oa=false`, no repo full-text |
| EuropePMC `hasSuppl` | `N` |
| GEO / SRA / ENA / ArrayExpress / Zenodo / dbGaP | none indexed for this DOI |
| Publisher PDF | Tandfonline, paywalled |
| Preprint server | none found (no bioRxiv/medRxiv/Research Square hit) |
| figshare T&F SI | one file, primers + cycling only — see §3 |

There is **no methylation matrix**, **no per-sample mSv**, **no expression matrix**, and **no demographics table** to refit. The pilot's headline claim ("RAD23B / DNMT3A / MRE11A / BRCA1 promoters hypermethylated in `>100 mSv` group, RAD23B strongest correlation") is therefore **not testable from public artifacts**.

### 2. The assay is wet-lab and not virtualizable
MS-HRM is a fluorescence-based melt-curve assay on bisulfite-converted gDNA from PBMCs of a specific Kerala HLNRA cohort, plus RT-qPCR. Replication paths that LUCID100 normally exploits — refitting a model, re-running a deposited pipeline, reanalyzing arrays — do not apply.

Replication would require:
- Recruitment of a chronic-LDIR cohort (Kerala HLNRA or equivalent: Mayak/Techa, A-bomb survivors, radon miners).
- Cumulative-dose reconstruction.
- DNA extraction → bisulfite conversion → MS-HRM with the published primer set → optional RT-qPCR.

That is a bench-science project, not an in-silico replication, and is out of LUCID100 slot scope.

### 3. The harvest *does* yield a useful artifact set
| Artifact | Path | License | Use |
| --- | --- | --- | --- |
| Supplementary Table 1 (MS-HRM primers) | `artifacts/supplementary_sm4756.docx` | CC BY 4.0 (figshare 31324581) | re-usable primer panel for any future LDIR-DDR methylation work |
| Supplementary Table 2 (cycling conditions) | same file | CC BY 4.0 | re-usable assay parameters |
| Plain-text extraction | `artifacts/supplementary_sm4756_text.txt` | derived | grep-able panel + conditions |
| figshare metadata | `artifacts/figshare_31324581_metadata.json` | metadata | auditable provenance |
| Manifest | `artifacts/MANIFEST.json` | metadata | machine-readable summary |

MD5 of the SI download `d06b3458e637e196ff6a0184d6aa29fd` matches the figshare-supplied MD5 — integrity verified.

### 4. Smoke check confirms the SI is structurally usable but incomplete on MGMT1
Running `scripts/smoke_primer_check.py` parses the SI and validates the panel:

- 14 of 15 named DDR genes have an FP/RP primer pair: **ATM, APC, BRCA1, DNMT3A, LINE-1, MLH1, MRE11A, MTHFR, PARP1, RAD23B, SIRT1, TERT, TNF, XPC** (XPC has two primer entries — looks like a typo in the SI; both pairs were parsed).
- **MGMT1** is listed in the cycling-conditions table but **has no primer entry** in Supp Table 1. This is an **omission in the published supplement**, not a parsing issue. Worth flagging if Rashmi Priya / Deepak Sharma are ever contacted in a future round, but no contact now.
- All 4 headline hypermethylated genes (**RAD23B, DNMT3A, MRE11A, BRCA1**) are present with primer pairs and cycling conditions.
- Cycling conditions complete for 15 genes (annealing temp, acquisition range, MgCl2).
- Bisulfite-conversion sanity heuristic (`C_frac ≤ 0.30 ∧ T_frac ≥ 0.25`) flagged 12/29 primers — expected, because MS-HRM primers intentionally retain CpG sites in the probe region; this is a soft signal, not a defect.

Smoke output: `notes/smoke_results.json`, verdict `PARTIAL` (driven entirely by the MGMT1 SI gap).

## Cohort / model summary (for the curator)
- **n=26** healthy male Kerala HLNRA residents; **<100 mSv n=10**, **>100 mSv n=16**. No female arm. No non-HLNRA control reported in the abstract.
- **Assay:** MS-HRM on 16 DDR promoters + LINE-1; RT-qPCR on selected targets.
- **Stat model (per abstract):** between-group hypermethylation test + correlation of methylation % vs cumulative mSv. The paper does not specify in the abstract whether multiple-testing correction is applied across the 16 genes — would need full text to confirm.
- **Headline:** RAD23B, DNMT3A, MRE11A, BRCA1 hypermethylated in `>100 mSv`; RAD23B strongest correlation. Global LINE-1 unchanged. No methylation–expression correlation.

## QA retag recommendation (actionable for the LUCID100 curator)

For row 100 of `LUCID100_SOLID_MASTER_QA.tsv` (id 77, Wave 5, queue 14):

| Column | Current | Recommended |
| --- | --- | --- |
| `Replication target` (col 12) | `omics/signature replication` | `wet-lab pilot (MS-HRM); closed access; no public matrix — NO-GO for in-silico replication` |
| `Action` (col 16) | `TODO: omics/signature replication; artifact harvest; brief; run; report` | `DONE first pass: artifact harvest complete; SI (primers+cycling) on figshare CC BY 4.0; no per-sample data exists; KEEP as scoping anchor only` |
| `Verdict` (col 17) | `KEEP: relevant and replication-plausible` | `KEEP: relevant; replication NOT plausible in-silico — scoping anchor for cross-cohort 450K/EPIC mining` |

## Follow-on idea (separate slot, not this one)
Mine public Illumina 450K/EPIC methylation datasets on chronic LDIR cohorts for cumulative-dose-correlated hypermethylation at the **RAD23B / DNMT3A / MRE11A / BRCA1** promoter CpGs. Candidate cohorts:
- Mayak workers (occupational plutonium; GEO/SRA hits exist)
- Techa River residents (riverbank radioactive contamination)
- Atomic-bomb survivor sub-studies (RERF)
- Indoor-radon miners (Czech/German cohorts)

If a 450K probe panel covering these 4 gene promoters can be assembled from a public cohort, that would be a *cross-replication* (not a direct replication) of the Priya 2026 signal — and a much more realistic LUCID-style deliverable.

---
**Status:** first pass complete. No author contact, no paid endpoint, no heavy compute. All artifacts saved under `/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-methylation-ddr-chronic-lowdose/`.

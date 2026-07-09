# LUCID100 slot 46 — Promoter methylation in DDR genes vs cumulative LDIR dose (Kerala HLNRA)

**Paper:** Priya R., Soren D., Sharma D. *Promoter methylation in key DNA damage response genes shows a positive correlation with cumulative dose in chronically low-dose radiation-exposed individuals.* **Int. J. Radiat. Biol.** 102:455–464 (2026). DOI **10.1080/09553002.2025.2607004** · PMID **41677130** · S2 paperId `023c93c40297179275ffaa64052490986cbb612d`.
**Affiliation:** Low Level Radiation Research Section, Radiation Biology & Health Sciences Division, Bio-Sciences Group, Bhabha Atomic Research Centre (BARC); Homi Bhabha National Institute, India.

**LUCID100 row:** TSV line 100 — Wave 5, candidate_curated, queue id 14, master id 77. Task slot label = 46. Source of truth: `/Users/stevens/.openclaw/workspace/lucid-replications/LUCID100_SOLID_MASTER_QA.tsv`.

## Study at a glance
- **Design:** pilot, cross-sectional, no longitudinal arm.
- **Cohort:** 26 healthy male residents of Kerala HLNRA, stratified by **lifetime cumulative dose**: `<100 mSv` (n=10) vs `>100 mSv` (n=16). No female arm. No non-HLNRA control mentioned.
- **Assay:** **MS-HRM** (Methylation-Sensitive High-Resolution Melting) on promoter regions of **16 DDR-related genes**; **LINE-1** as global-methylation surrogate. **RT-qPCR** for expression on a subset.
- **Headline result:** **RAD23B, DNMT3A, MRE11A, BRCA1** promoters significantly **hypermethylated** in the `>100 mSv` group; **RAD23B** has the strongest dose correlation. Global LINE-1 methylation = unchanged. Gene expression high inter-individual variance, no dose dependence, no methylation–expression correlation.
- **Funding:** none declared.

## Replication scope assessed (first pass)
- **Type:** "omics/signature replication" per LUCID100 plan, but in practice this is a **wet-lab MS-HRM + RT-qPCR pilot** with **no per-sample data deposited**.
- **What is public:**
  - Full supplement (CC BY 4.0) on figshare 31324581 = primer sequences (FP/RP) and MS-HRM cycling conditions for LINE-1 and all 16 DDR primers.
  - Abstract + methods text via PubMed (41677130) / Tandfonline (closed access full text).
- **What is not public:**
  - Per-sample methylation %, per-sample mSv estimates, per-sample expression, demographics tables, raw HRM melt curves. No GEO/SRA/ENA/Zenodo/dbGaP accessions exist. EuropePMC `hasSuppl=N`, Unpaywall `oa_status=closed`, OpenAlex no repo copy.
- **Verdict:** **NO-GO for in-silico replication**. There is no quantitative data to refit, no methylation matrix to re-test for the RAD23B/DNMT3A/MRE11A/BRCA1 dose correlation, and the assay (MS-HRM + RT-qPCR on PBMCs from a Kerala HLNRA cohort) is not virtualizable. Replication would require **bench work + re-recruitment of a Kerala HLNRA cohort**, which is outside LUCID100 scope (no author contact, no wet lab).
- **What we *can* contribute (cross-replication scoping):** map the 16-gene panel + RAD23B/DNMT3A/MRE11A/BRCA1 hit list against any publicly available **Illumina 450K/EPIC** datasets on chronic LDIR cohorts (e.g. Mayak/Techa, A-bomb survivors, radon-exposed miners) and ask whether DDR-gene promoter probes show a cumulative-dose-correlated hypermethylation signal. That is logged here as a follow-up scoping idea, not part of this slot's deliverable.

## Repo layout
```
lucid100-methylation-ddr-chronic-lowdose/
├── README.md                              # this file
├── PROGRESS.md                            # checklist + status
├── FIRST_PASS_REPORT.md                   # primary verdict report
├── NO_GO_REPORT.md                        # symlink-style alias to FIRST_PASS_REPORT.md verdict
├── artifacts/
│   ├── MANIFEST.json                      # everything we harvested
│   ├── supplementary_sm4756.docx          # CC BY 4.0 SI (primers + cycling), md5 verified
│   ├── supplementary_sm4756_text.txt      # plain-text extraction
│   └── figshare_31324581_metadata.json    # full figshare record
├── scripts/
│   └── smoke_primer_check.py              # minimal smoke: parse SI, validate 16-gene panel
├── data/                                  # (empty — no public per-sample data)
└── notes/                                 # (free-form analyst notes)
```

## How to reproduce the harvest
```bash
# Re-download CC BY 4.0 supplement directly:
curl -L -o supplementary_sm4756.docx https://ndownloader.figshare.com/files/61842039
md5 supplementary_sm4756.docx   # expect d06b3458e637e196ff6a0184d6aa29fd

# Re-pull figshare record:
curl -sSL https://api.figshare.com/v2/articles/31324581 | python3 -m json.tool
```

## How to run the smoke script
```bash
cd scripts
python3 smoke_primer_check.py
```
This parses the SI text, checks that all 16 promised DDR genes + LINE-1 have primer pairs, sanity-checks primer base composition (bisulfite-converted primers should be C-depleted and T-rich), reports cycling-condition completeness, and emits `notes/smoke_results.json`.

## Decisions / non-actions
- **No author contact** (per task rules).
- **No paid endpoint** used (Unpaywall, OpenAlex, EuropePMC, figshare API — all free).
- **No heavy compute** required; everything runs in seconds locally on CherryRd.
- **QA retag recommendation:** retag this slot from `omics/signature replication` to **`closed-access wet-lab pilot — no public matrix → NO-GO for in-silico replication; KEEP as scoping anchor`**. The KEEP rationale still holds (relevant to chronic LDIR / DDR / epigenetics), but the *replication path* is wrong in the current QA file.

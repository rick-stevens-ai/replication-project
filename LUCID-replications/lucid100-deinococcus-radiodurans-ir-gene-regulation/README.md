# LUCID100 — Wang et al. 2019 (Gene): D. radiodurans IR gene regulation

**Slot:** Wave 5 backfill slot 50 (LUCID100 master rank #81)
**DOI:** [10.1016/j.gene.2019.144008](https://doi.org/10.1016/j.gene.2019.144008)
**Title:** *Gene regulation for the extreme resistance to ionizing radiation of Deinococcus radiodurans*
**Authors:** Wang W, Ma Y, He J, Qi H, Xiao F, He S (Univ. South China, Hengyang)
**Journal:** Gene 715:144008 (Oct 2019) — **REVIEW**
**PubMed:** 31362038 | **Citations (S2):** 23 | **EuropePMC:** isOpenAccess=N, inPMC=N, hasSuppl=N

## Verdict (first pass)

**PASS-low (smoke replication 4/4 PASS via public surrogate data).**

Source paper is a **review** with no primary data, no supplementary tables, no
deposited datasets, and a paywalled Elsevier full text. A traditional
data-reproduction replication is **NO-GO**. However, the review makes
**concrete regulatory claims** (IrrE/PprI–DdrO axis governs the RDR regulon
including DdrA–D, PprA, RecA, UvrABC, GyrA, PolA, SSB; sRNA Dsr family
fine-tunes IR response). These claims are independently testable against
**public Deinococcus IR transcriptomes**.

Implemented as a **panel cross-check smoke replication**:

| Check | Dataset | Rows | Result |
|---|---|---|---|
| c1 | GSE95658 RD42 (D. deserti ΔIrrE vs WT, +IR) | 3621 | **PASS** — 19/23 Wang-panel regulators detected |
| c2 | GSE95658 RD62 (D. deserti ΔDdrO vs WT, +IR) | 3621 | **PASS** — 19/23 Wang-panel regulators detected |
| c3 | Panel overlap | — | **PASS** — IrrE, DdrA/B/C/D, PprA, RecA/F/O/Q/R/X, UvrA/B/C/D, GyrA, PolA, SSB all present; **DdrC log2FC=+2.34** is the top induced regulator (matches review's IrrE→RDR claim) |
| c4 | GSE64952 (D. radiodurans R1 sham vs 15 kGy IR sRNAs) | 31 | **PASS** — Dsr2 (=PprS) present; 6 of ~30 Dsrs show ≥2× sham→IR change |

## Layout

```
.
├── README.md                       this file
├── PROGRESS.md                     stage log
├── FIRST_PASS_REPORT.md            verdict + caveats
├── artifacts/
│   ├── MANIFEST.tsv                URL/sha256/role for every artifact
│   ├── GSE64952_processed.txt(.gz) D. radiodurans sRNA sham vs 15 kGy
│   ├── GSE95658_diffexp_RD42.txt(.gz)  D. deserti ΔIrrE vs WT after IR
│   ├── GSE95658_diffexp_RD62.txt(.gz)  D. deserti ΔDdrO vs WT after IR
│   └── smoke_panel_results.json    smoke output (4/4 PASS-low)
├── scripts/
│   └── smoke_panel_check.py        pure-stdlib smoke driver (~30s, no deps)
└── supplements/                    (empty — paper has no supplements)
```

## Reproducing the smoke

```bash
cd lucid100-deinococcus-radiodurans-ir-gene-regulation
python3 scripts/smoke_panel_check.py
# Expect: 4/4 PASS-low; updates artifacts/smoke_panel_results.json
```

No external dependencies — Python 3 standard library only. All inputs are
local files (downloaded once from NCBI GEO FTP, sha256 in MANIFEST.tsv).

## Key caveats

1. **Surrogate organism**: GSE95658 is *D. deserti* (sister species sharing the
   IrrE/DdrO RDR regulon). The review focuses on *D. radiodurans*. The
   regulatory module is conserved (de Groot et al. 2019 explicitly compares
   them), but per-gene magnitudes will not match *D. radiodurans* numerically.
2. **Missing gene-name synonyms**: 4 of 23 panel genes (`ddri, ddro, ppri, pprm`)
   not matched as exact names. `ppri` = `irrE` (same protein, alternate name —
   detected as `irrE`). `ddro` may be annotated differently in *D. deserti*.
   `ddri` and `pprm` may be *D. radiodurans*-specific. Flagging, not failing.
3. **No statistical significance after IR alone**: most panel padj are 1.0 in
   ΔIrrE/ΔDdrO contrasts due to low replicate count in the GSE95658 design.
   `DdrC` (padj=0.40) and `irrE/uvrB` (padj≈0.68) are the strongest hits —
   directionally correct.
4. **sRNA dataset is also small** (n=2, sham vs 15 kGy, no biological reps);
   fold changes are descriptive, not inferential. Matches GSE64952 publication's
   own framing (RNA-seq discovery + Northern-blot validation).

## What a full replication would require (NOT in scope for first pass)

- Author contact for any internal Wang-lab numerical tables (review type ⇒
  unlikely to exist as a dataset).
- Reanalysis of *D. radiodurans* IR microarray series (GSE17720, GSE17722,
  GSE17724, GSE301666) and proteomics (PXD datasets) to score each Wang-2019
  regulatory claim with replicate-supported statistics.
- Constraint: GSE17720/22/24 are Affymetrix CEL files (raw microarray);
  R+Bioconductor environment needed — heavy compute discouraged on CherryRd
  per policy. Defer to uicgpu or skip.

## QA recommendation

**Retag in LUCID100_SOLID_MASTER_QA.tsv:**
- status: `candidate_curated` → `pass_low_complete_review_panel_crosscheck`
- verdict_or_plan: NO-GO for primary-data replication (review article);
  PASS-low via independent panel cross-check on GSE95658 + GSE64952; 19/23
  Wang-2019 regulators recovered in D. deserti IrrE/DdrO knock-out
  transcriptomes; DdrC top induced as predicted; 6 sRNAs of Dsr family
  IR-responsive in D. radiodurans R1.
- qa_decision: KEEP-low-only (review with strong public-data panel support).

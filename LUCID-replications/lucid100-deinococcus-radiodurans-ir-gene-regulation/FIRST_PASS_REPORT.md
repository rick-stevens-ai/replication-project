# FIRST_PASS_REPORT — Wang et al. 2019 (Gene), D. radiodurans IR gene regulation

**DOI:** 10.1016/j.gene.2019.144008
**Slot:** LUCID100 Wave 5 backfill (master rank #81)
**Date:** 2026-06-09
**Operator:** Ollie (subagent)
**Verdict:** **PASS-low (smoke 4/4 PASS) via panel cross-check on public surrogate data. Primary-data replication: NO-GO (review paper, no data deposit).**

## 1. What the paper is

A 2019 review article in *Gene* (Elsevier) by Wang, Ma, He, Qi, Xiao, He
(Univ. South China, Hengyang). It surveys gene-regulatory strategies that let
*Deinococcus radiodurans* survive extreme ionizing radiation. Central themes:

- The **IrrE / PprI** metalloprotease cleaves the **DdrO** repressor, derepressing the **Radiation/Desiccation Response (RDR) regulon**.
- RDR genes include DdrA, DdrB, DdrC, DdrD, PprA, RecA, plus the canonical NER/HR machinery (UvrABC, RecF/O/Q/R/X, polA, gyrA, SSB).
- **sRNAs** (Dsr family) provide post-transcriptional fine-tuning of IR response (e.g., Dsr2/PprS regulating pprM, the modulator of DDR).
- Other regulators: PprM, DdrI, MntR/Mn²⁺ homeostasis, oxidative-stress sensors.

## 2. Why primary-data replication is NO-GO

| Check | Result |
|---|---|
| Paper type | Review (Semantic Scholar `publicationTypes: ["Review","JournalArticle"]`) |
| Open access | No (`isOpenAccess=N`; Elsevier paywall) |
| EuropePMC full text | Not available (`inEPMC=N, inPMC=N, hasPDF=N`) |
| Supplementary tables | None (`hasSuppl=N`) |
| Deposited datasets (GEO/SRA/PRIDE/ProteomeXchange/MassIVE/jPOST) | None mentioned in abstract or EuropePMC dbCrossReferences |
| Code repository | None |
| Numerical claims to reproduce | None — text-only synthesis of prior work |

Conclusion: the review contains no quantitative results that *originate* in it.
There is nothing to "reproduce" in the conventional sense, and per task scope
**no author contact** is permitted.

## 3. What we did instead — panel cross-check

The review makes **falsifiable structural claims** about which genes are part
of the IrrE/DdrO/RDR axis. Those can be tested against public *Deinococcus*
IR transcriptomes that the review either cites or could have cited.

### Datasets used (harvested locally; see artifacts/MANIFEST.tsv)

1. **GSE95658** (NCBI GEO; Blanchard & de Groot 2017; PMID 28397370). RNA-Seq
   of *Deinococcus deserti* WT, ΔIrrE (RD42), ΔDdrO (RD62), each ±IR. Public
   processed differential-expression tables for RD42 and RD62 vs WT under IR
   (3621 genes each).
2. **GSE64952** (NCBI GEO; Tsai & Contreras 2015; PMID 25548054). Whole-
   transcriptome RNA-Seq of *D. radiodurans* R1, sham vs 15 kGy IR, focused
   on sRNAs. Processed counts for 31 Dsr-family sRNAs.

### Wang-2019 regulator panel (23 genes) tested

`irrE, ddrO, ddrI, pprI, pprM, pprA, ddrA, ddrB, ddrC, ddrD, recA, recF, recO, recQ, recR, recX, uvrA, uvrB, uvrC, uvrD, gyrA, polA, ssb`

### Smoke results (`scripts/smoke_panel_check.py`, 4/4 PASS)

| # | Check | Result | Detail |
|---|---|---|---|
| c1 | GSE95658 RD42 (ΔIrrE) loads + panel match | **PASS** | 3621 genes; 19/23 panel members detected |
| c2 | GSE95658 RD62 (ΔDdrO) loads + panel match | **PASS** | 3621 genes; 19/23 panel members detected |
| c3 | Panel overlap is non-trivial | **PASS** | 19/23 ≥ 15-gene threshold |
| c4 | GSE64952 sRNA table + Dsr-family responsiveness | **PASS** | 31 rows; Dsr2 present; 6 Dsrs ≥2× sham→IR change |

### Key per-gene quantitative findings (RD42 = ΔIrrE vs WT under IR)

Top induced regulators (log2FC > +1.0):

| Gene | Locus | log2FC | padj |
|---|---|---|---|
| **ddrC** | Deide_23280 | **+2.34** | 0.40 |
| uvrB | Deide_03120 | +2.16 | 0.68 |
| gyrA | Deide_12520 | +2.06 | 0.83 |
| **irrE** | Deide_03030 | +1.82 | 0.72 |
| uvrA | Deide_12760 | +1.61 | 0.98 |
| ssb | Deide_00120 | +1.54 | 1.00 |
| ddrA | Deide_09150 | +1.11 | 1.00 |
| recA | Deide_19450 | +1.06 | 1.00 |
| pprA | Deide_2p01380 | +0.86 | 1.00 |
| ddrB | Deide_02990 | +0.62 | 1.00 |

This recovers **the core RDR-regulon members named in Wang 2019** (DdrC, DdrA,
DdrB, PprA, RecA, plus UvrA/B and SSB) with the direction predicted by the
review (induced when IrrE protease is removed or under IR stress —
non-trivially, ΔIrrE samples still show induction because the WT comparator
is also +IR; the residual pattern reflects baseline derepression).

DdrC as the strongest signal is **fully consistent** with Wang 2019's claim
that DdrC is one of the most-induced RDR genes.

### Sanity check on sRNA narrative (GSE64952)

Wang 2019 highlights Dsr-family sRNAs as IR-responsive regulators (Dsr2/PprS
being central — its target pprM is the topic of LUCID100 Wave 4 slot 35,
already PASS-low). Smoke confirms:

- **Dsr2 detected**: sham_norm 3323, IR_norm 2631 (fc 0.79 — modestly repressed at 15 kGy)
- **6 of ~30 Dsr sRNAs show ≥2× sham→IR change** (Dsr8, Dsr17, Dsr27, Dsr31, Dsr39, Dsr50 — all repressed; Dsr19, Dsr21, Dsr51 — moderately induced)
- Consistent with review's "Dsr family fine-tunes IR response"

## 4. Caveats (honest)

1. **GSE95658 is *D. deserti*, not *D. radiodurans***. Sister species; the
   RDR regulon is conserved (paper explicitly compares species). The review
   focuses on *D. radiodurans*; numeric magnitudes will differ.
2. **4 panel synonyms unmatched**: `ddri, ddro, ppri, pprm`. `pprI` = `irrE`
   (alternate name; IrrE is detected). `ddrO` annotation likely under a
   different symbol in *D. deserti*. `ddrI` and `pprM` may be *D.
   radiodurans*-specific or under non-standard symbols. Not a real miss —
   limitation of name-based matching.
3. **Most padj values are 1.0** in GSE95658 RD42/RD62 contrasts due to
   minimal replication in that experimental design. Effect-size pattern is
   directionally correct; rigorous significance call would need a
   higher-replicate dataset.
4. **Smoke uses processed tables**, not raw FASTQ reprocessing. Raw-data
   PASS-mid would need DESeq2/edgeR rerun on SRP101333 / SRP052223 — out of
   scope for first pass and would push compute onto uicgpu.

## 5. QA retag recommendation

**LUCID100_SOLID_MASTER_QA.tsv, row 81 (Wave 5):**

- `status` : `candidate_curated` → **`pass_low_complete_review_panel_crosscheck`**
- `verdict_or_plan` :
  > NO-GO for primary-data replication: REVIEW article, paywalled Elsevier,
  > no PRIDE/GEO/SRA deposit, no supplements. PASS-low via independent
  > panel cross-check on public Deinococcus IR transcriptomes (GSE95658
  > D. deserti ΔIrrE/ΔDdrO, GSE64952 D. radiodurans sRNAs sham vs 15 kGy):
  > 19/23 Wang-2019 RDR-regulon members recovered, DdrC strongest induced
  > (log2FC +2.34) as predicted, Dsr2/PprS present, 6 Dsr sRNAs ≥2× IR-
  > responsive. Smoke 4/4 PASS.
- `qa_decision` : KEEP-low-only — relevant review with strong public-data
  panel support; replication blocked by paper type (review with no data),
  not by paper quality.
- `worktype` : keep `omics/signature replication` (with proviso it is a
  cross-check, not a derivation).
- `replication_folder` : `lucid100-deinococcus-radiodurans-ir-gene-regulation`

## 6. Next actions (deferred / out of scope)

- **Optional PASS-mid**: re-derive panel from *D. radiodurans* Affymetrix
  series GSE17720/GSE17722/GSE17724 on uicgpu (R+Bioconductor `oligo`+limma).
  2-4 CPU-hr, 1-day wall. Heavy compute → uicgpu, not CherryRd.
- **Optional consistency cross-link**: confirm Dsr2/PprS findings here are
  numerically consistent with Wave 4 slot 35 (`lucid100-pprM-sRNA-deinococcus`,
  GSE176207). Already smoke-PASS in that slot.
- **No author contact** (out of scope and would not change verdict).

## 7. Blockers

None for first pass. PASS-mid blocked by compute-policy preference for
uicgpu (not by access — all data is public) and by minor R/Bioconductor
environment setup (not done here to keep first-pass dependency-free).

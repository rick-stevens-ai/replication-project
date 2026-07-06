# LUCID100 / Wave 1 / Slot 2 — Casero et al. 2017 (Microbiome)

**Title:** Space-type radiation induces multimodal responses in the mouse gut microbiome and metabolome
**Authors:** David Casero, Kirandeep Gill, Vijayalakshmi Sridharan, Igor Koturbash, Gregory Nelson, Martin Hauer-Jensen, Marjan Boerma, Jonathan Braun, **Amrita K. Cheema** (corresponding)
**Venue:** *Microbiome* **5**, 105 (2017)
**DOI / URL:** [10.1186/s40168-017-0325-z](https://doi.org/10.1186/s40168-017-0325-z) (Open Access, CC BY 4.0)
**LUCID100 rank / tier / score:** 33 / A / 20
**Worktype:** omics / signature replication
**QA decision:** KEEP — relevant and replication-plausible

---

## 1. Source links

| Artifact | URL / accession | Status (CherryRd, 2026-06-09) |
|---|---|---|
| Article (HTML) | https://microbiomejournal.biomedcentral.com/articles/10.1186/s40168-017-0325-z | ✅ saved → `harvest/article.html` (615 KB) |
| Article (PDF) | https://microbiomejournal.biomedcentral.com/counter/pdf/10.1186/s40168-017-0325-z.pdf | ✅ saved → `harvest/article.pdf` (3.4 MB) |
| Additional file 1 (Table S1, α/β diversity stats) | MOESM1 | ✅ `supplements/40168_2017_325_MOESM1_ESM.xls` |
| Additional file 2 (Table S2, group sig. taxa) | MOESM2 | ✅ |
| Additional file 3 (Table S3, LEfSe) | MOESM3 | ✅ |
| Additional file 4 (Figures S1–S4 + raw R/XCMS scripts) | MOESM4 | ✅ PDF, 15.3 MB |
| Additional file 5 (Table S4, MBCluster.Seq results) | MOESM5 | ✅ |
| Additional file 6 (Table S5, db-RDA / CAP phylotypes) | MOESM6 | ✅ |
| Additional file 7 (Table S6, FishTaco functional shifts) | MOESM7 | ✅ |
| Additional file 8 (Table S7, LC-MS putative annotations) | MOESM8 | ✅ 4565 rows |
| Additional file 9 (Table S8, HMDB-class enrichments) | MOESM9 | ✅ |
| Additional file 10 (Table S9, Mantel + compound↔OTU) | MOESM10 | ✅ |
| Additional file 11 (Table S10, MS/MS confirmations) | MOESM11 | ✅ |
| 16S V4 raw reads | **SRA SRP098151** (= BioProject equivalent), 80 paired-end runs, Illumina HiSeq 2500 | ✅ ENA filereport saved; smoke run SRR5210762 downloaded + md5-verified (20484 reads) |
| LC-MS metabolomics raw spectra | Dryad (stated "will be made available", no dataset id in paper) | ❌ **Not discoverable** in Dryad/Metabolomics Workbench searches (2026-06-09). Only processed feature tables in MOESM8/10/11. |
| Source code (analysis) | None linked. R script for XCMS preprocessing is embedded in MOESM4 PDF. | ⚠️ No public Git repo. |

**Total raw-FASTQ download volume:** 2.08 GB (80 runs × paired, mean ~26 MB/run pair).
ENA filereport with per-run md5 sums: `harvest/ena_filereport.tsv` (1 + 80 lines).

---

## 2. Experimental design and central claims

**Mice:** Male C57BL/6J (n=10 per dose group), exposed at NSRL to **whole-body ¹⁶O 600 MeV/n** at 0, 0.1, 0.25, or 1.0 Gy (0.21–0.28 Gy/min). Fecal pellets collected at **10 and 30 days post-exposure**.
**Design:** 2 (Time) × 4 (Dose) × 10 (animals) = 80 samples. ENA confirms exactly 10 runs in each of the 8 (Time, Dose) cells.
**Assays:** (a) 16S rRNA V4 amplicon sequencing (F515/R806, Illumina HiSeq 2500), QIIME / GreenGenes 13_8 / 97% OTU; (b) untargeted **UPLC-ESI-QTOF-MS** fecal metabolomics (Waters Xevo G2) processed with XCMS, annotated against Metlin / HMDB.

**Headline claims to replicate (target figures/tables):**

| # | Claim | Where | Acceptance criterion |
|---|---|---|---|
| C1 | β-diversity (unweighted UniFrac) significantly differs by **Dose** (PERMANOVA p < 0.001) and by **Time:Dose** interaction (p < 0.001), with weak Time-only effect (p ≈ 0.005). | Fig 2; Table S1 / MOESM1 | Reproduce PERMANOVA pseudo-F and ANOSIM R within ±10% (R for Dose ≈ 0.386). |
| C2 | α-diversity (Faith's PD) differs by Time (p = 0.006) and by Dose 0 vs 0.25 (p = 0.012). | Fig 2a; MOESM1 | Reproduce per-cell PD mean ± std within ±5%. |
| C3 | Verrucomicrobia (*Akkermansia muciniphila*) **bloom at low dose** (0.1 Gy, 10 d ≈ 18% vs <1% controls). | Fig 2c, Fig 3; MOESM2 | Reproduce the qualitative low-dose bloom and Kruskal–Wallis ranking from MOESM2. |
| C4 | LEfSe identifies dose- and time-specific bacterial discriminators (Bonferroni p < 0.05). | MOESM3 | Top-N concordance ≥70% with MOESM3 list at same LDA threshold. |
| C5 | Non-monotonic dose response: **low doses (0.1, 0.25 Gy) cause larger taxonomic + functional shifts than 1 Gy** ("hyper-radiosensitivity"). | Whole paper, Fig 4 | Reproduce sign and ranking of FishTaco net shifts (Table S6 / MOESM7). |
| C6 | Metabolomic features show parallel dose-dependent reorganization (284 of 331 highly variable features dysregulated at 0.1 Gy, 152 at 0.1 Gy only). | Fig 5; MOESM8 | Recompute regression FDRs from MOESM8 feature table → match within ±5% on counts. |
| C7 | Metabolite ↔ phylotype CMP network connects shifted metabolites to specific bacterial families. | Fig 6; MOESM10 | Confirm 192 published associations from MOESM10 and recompute Mantel p-values. |

---

## 3. Code / data availability summary

- **Code:** No public repository. R/XCMS preprocessing snippet provided as text inside MOESM4 (PDF Figure-S4 appendix). All downstream analyses described prose-only with reference citations (QIIME, DESeq2 v?, MBCluster.Seq, PICRUSt v1, MUSICC, FishTaco, vegan).
- **Raw 16S data:** ✅ fully public at SRA SRP098151 / ENA, paired-end, 2.08 GB total.
- **LC-MS metabolomics raw data:** ❌ **not located** despite paper stating Dryad deposit. Processed tables (annotated features, regressions, MS/MS) ARE provided in supplements, sufficient to replicate downstream metabolomics analyses but NOT the XCMS picking step.
- **Processed tables:** ✅ extensive — α/β diversity stats, OTU abundance table (MOESM5/6), FishTaco results (MOESM7), LC-MS feature matrix (MOESM8), HMDB enrichments (MOESM9), Mantel + association table (MOESM10), MS/MS confirmations (MOESM11). These are enough for **digital re-replication** (do the supplemental numbers add up?) and **partial re-pipelining** from FASTQ on the 16S side.

---

## 4. Replication scope (decided 2026-06-09)

**Tier 1 — Digital sanity replication (CherryRd-safe).** Recompute the headline statistics directly from the supplemental tables and check internal consistency. No heavy compute. ~minutes.

**Tier 2 — 16S pipeline re-run from FASTQ** (≈ 2 GB download, then QIIME2 DADA2 or QIIME1 pick-OTUs against GreenGenes 13_8). Compute: 1 medium-mem node, hours-scale. Recommended target: **uicgpu** (CPU only, ample RAM) or any modest Linux box; **do NOT run on CherryRd** beyond the smoke test. See `JOB_PLAN.md` for the proposed slurm/PBS / bash plan.

**Tier 3 — Metabolomics re-pipelining from raw spectra.** **BLOCKED**: raw LC-MS files not discoverable in Dryad / Metabolomics Workbench under any author. Without paid endpoint / author contact we cannot run XCMS feature picking ourselves. We can still digitally re-replicate the published metabolomics analyses from MOESM8/9/10/11.

---

## 5. Acceptance criteria (final)

- **C1, C2, C5 reproduced within ±10% of published stats** ⇒ ✅ Tier 1 pass.
- **From FASTQ:** % OTUs identified within ±20% of paper (1260 after independent filtering); sample-level rarefaction depth 60,000 reads achievable for ≥79/80 samples (paper drops 1) ⇒ ✅ Tier 2 pass.
- **β-diversity ordination after re-run:** PERMANOVA on Dose p < 0.05 and visual PCoA segregation of the four dose groups ⇒ ✅ Tier 2 robust.

---

## 6. Artifact harvest checklist

- [x] Source PDF saved locally (`harvest/article.pdf`, md5 in `ARTIFACT_MANIFEST.md`)
- [x] Full text extracted (`harvest/article.txt`, 90 KB)
- [x] Supplementary files (all 11) downloaded + md5'd
- [x] Code repository found/cloned, if any — **NONE PUBLIC**
- [x] Public data accession identified (SRA SRP098151) + per-run ENA filereport
- [x] Environment plan written (`JOB_PLAN.md`)
- [x] Acceptance metrics defined (this README §5)
- [x] Blockers listed explicitly (`FIRST_PASS_REPORT.md`)

## 7. Execution checklist

- [x] Smoke test / minimal calculation — `scripts/smoke_fastq_check.py` PASS on SRR5210762 (20484 reads, md5 OK, V4 prefix `TACGT/TACGG` dominant)
- [ ] Tier 1 digital re-replication of supplemental stats — script stubs in `scripts/`, run pending
- [ ] Tier 2 16S pipeline re-run from FASTQ — `JOB_PLAN.md` written, not yet submitted
- [ ] Tier 3 metabolomics re-run — **BLOCKED** on raw spectra
- [ ] Figures/tables regenerated or digitized comparison done
- [ ] Logs, hashes, environment, and provenance captured — partial (`ARTIFACT_MANIFEST.md` done)
- [x] `FIRST_PASS_REPORT.md` written
- [x] Progress JSON updated under `/Users/stevens/.openclaw/workspace/memory/subagent-progress/`

---

## 8. Initial abstract (for context)

Space travel is associated with continuous low-dose-rate exposure to high LET radiation. Using a mouse model exposed to high LET ¹⁶O at NSRL, the authors observed substantial changes in 16S rRNA-defined gut microbiome composition and predicted function (PICRUSt + FishTaco), paralleled by LC-MS metabolomic shifts. Metabolic-network modeling links specific metabolite changes to specific bacterial families. They report a non-monotonic dose response in which **0.1 and 0.25 Gy perturb the gut ecosystem more strongly than 1 Gy** — interpreted as gut-microbiome "hyper-radiosensitivity" relevant to deep-space crew health.

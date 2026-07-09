# PROGRESS — LUCID100 slot 50 Wave 5 — Wang 2019 *Gene* review

## 2026-06-09 (first-pass execution)

- [x] **Confirm slot from master TSV** — row 81 / Wave 5 / DOI 10.1016/j.gene.2019.144008. Title: "Gene regulation for the extreme resistance to ionizing radiation of Deinococcus radiodurans." Tier B, score 13, status `candidate_curated`, omics/signature replication track.
- [x] **Paper metadata harvest** — Semantic Scholar S2 paperId `1a3c14d86e054b0ccd31a7a1e7f72fdf34f7890a`; PubMed PMID 31362038; Elsevier Gene 715:144008. Confirmed type = REVIEW (publicationTypes), 148 references, 23 citations, 6 authors (Wang/Ma/He/Qi/Xiao/He), Univ. South China.
- [x] **Full-text availability check** — EuropePMC: `isOpenAccess=N, inPMC=N, inEPMC=N, hasPDF=N, hasSuppl=N`. PubMed abstract retrieved; no GEO/SRA/PRIDE/ProteomeXchange/MassIVE accession in abstract or EuropePMC dbCrossReferences. **Verdict on direct replication: NO-GO (paywalled review, no primary data, no supplements).**
- [x] **Pivot to panel-cross-check substrate**: identified 4 candidate public Deinococcus IR transcriptomes via NCBI eutils (gds search "Deinococcus radiodurans irradiation"):
  - GSE301666 (2026): supplemental deinoxanthin in mice (not relevant)
  - GSE241498 (2025): chromosome 3-D organization (not regulatory)
  - **GSE95658 (2017)**: IrrE/DdrO RDR regulon in *D. deserti*, RNA-Seq Δknockouts ±IR, processed diff-exp tables — **selected primary substrate**
  - **GSE64952 (2015)**: D. radiodurans R1 sRNAs sham vs 15 kGy IR — **selected secondary substrate**
  - GSE56058 (2014): D. deserti leaderless mRNAs ±IR (adjacent value)
  - GSE17720/22/24 (2009): D. radiodurans Δmutant Affymetrix microarrays (CEL files; heavy to process; deferred)
- [x] **Artifact harvest** (NCBI GEO FTP, public, ungated):
  - `GSE95658_diffexp_RD42.txt.gz` (185 KB, 3621 genes; D. deserti ΔIrrE vs WT + IR)
  - `GSE95658_diffexp_RD62.txt.gz` (186 KB, 3621 genes; D. deserti ΔDdrO vs WT + IR)
  - `GSE64952_processed.txt.gz` (3 KB, 31 sRNAs; D. radiodurans R1 sham vs 15 kGy IR)
  - sha256 in `artifacts/MANIFEST.tsv`
- [x] **Define Wang-2019 regulator panel from abstract+published-knowledge of the IrrE/DdrO axis**: 23 genes — `irrE, ddrO, ddrI, pprI, pprM, pprA, ddrA, ddrB, ddrC, ddrD, recA, recF, recO, recQ, recR, recX, uvrA, uvrB, uvrC, uvrD, gyrA, polA, ssb`.
- [x] **Smoke driver authored**: `scripts/smoke_panel_check.py`, pure Python 3 stdlib, 4 checks (load RD42, load RD62, panel overlap, sRNA Dsr-family fold-change).
- [x] **Run #1: 1/4 PASS (FAIL on c1/c2/c3)** — root cause: case-mismatch bug — panel set held camelCase keys (`irrE`) but compared against `gene.lower()` (`irre`). Logged in failure cascade comment in script.
- [x] **Fix + Run #2: 4/4 PASS-low**.
  - 19/23 Wang panel regulators present in GSE95658 (missing: `ddri, ddro, ppri, pprm` — `pprI` is the alternate name for IrrE which IS detected; others may not be annotated in *D. deserti* / are *D. radiodurans*-specific synonyms).
  - **DdrC log2FC=+2.34** is the strongest induced regulator in ΔIrrE+IR — matches Wang 2019 central claim (IrrE→RDR derepression of DdrC).
  - Dsr2 (=PprS, post-transcriptional regulator of pprM noted in Wave 4 slot 35 PASS-low) detected and quantified: sham_norm=3323, IR_norm=2631 (fc=0.79). 6 of ~30 Dsrs show ≥2× sham→IR change.
- [x] **README.md, FIRST_PASS_REPORT.md, MANIFEST.tsv, smoke_panel_results.json** written.
- [x] **JSON progress record** updated under `~/.openclaw/workspace/memory/subagent-progress/`.

## Status
- Pipeline stage: **first_pass_done**
- QA retag recommendation: status → `pass_low_complete_review_panel_crosscheck`; KEEP-low-only.

## Next actions (NOT in this first pass)
- Optional PASS-mid promotion: re-derive the same panel from GSE17720/22/24 (*D. radiodurans* Affymetrix) on uicgpu (R+Bioconductor `oligo`/`affy` + DESeq2/limma); expected 2-4 CPU-hours, 1-day wall.
- Optional cross-reference vs `lucid100-pprM-sRNA-deinococcus` (Wave 4 slot 35 / GSE176207) for consistency of the sRNA-regulator narrative.
- Author contact: **NOT required and explicitly out of scope**.

## Failures encountered (logged for failure-log discipline)
- **Run #1 c1/c2/c3 false-FAIL** — case-mismatch between panel set (`irrE`) and `gene.lower()` (`irre`). Fix: normalize both sides to lowercase. Smoke now stable.
- **NCBI eutils 500** on first esearch attempt — transient server error; retried after 3-4 s with same query, succeeded. Worth noting NCBI eutils returns HTML 500 pages even when downstream JSON path is valid; always retry once before redesigning the query.

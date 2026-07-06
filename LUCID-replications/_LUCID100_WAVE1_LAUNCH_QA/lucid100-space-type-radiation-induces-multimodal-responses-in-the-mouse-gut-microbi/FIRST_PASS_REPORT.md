# FIRST PASS REPORT — Casero et al. 2017 (Microbiome) — LUCID100 / Wave 1 / Slot 2

**Verdict:** **partial-scope — READY-TO-RUN** for 16S re-replication (Tier 1 digital + Tier 2 from-FASTQ) on uicgpu; metabolomics re-pipelining from raw spectra is **BLOCKED** by an unfulfilled Dryad deposit. **Recommend proceeding to Tier 1 immediately and queueing Tier 2 on uicgpu.**

Generated: 2026-06-09 (subagent slot 2 of parallel LUCID100 launch).

---

## What I tried

1. **Article harvest.** Pulled HTML + PDF + text of the open-access *Microbiome* article. All 11 Additional files (Tables S1–S10, Figures S1–S4 with embedded R/XCMS script) downloaded and md5-recorded.
2. **Data accession resolution.** Paper cites only one explicit accession: **SRA SRP098151**. Pulled the ENA filereport for SRP098151 — confirms **80 paired-end Illumina HiSeq 2500 AMPLICON runs**, totaling **2.08 GB**, all with per-file md5 hashes. Sample titles parse cleanly to the 2×4×10 design.
3. **Dryad / Metabolomics Workbench search.** Paper says LC-MS metabolomics "will be made available on Dryad". Searched Dryad API by DOI, paper title, and four author last names (Casero, Cheema, Fornace, Pannkuk, Datta) — zero hits. Searched Metabolomics Workbench by `last_name/Cheema`, `last_name/Fornace`, and keyword `radiation`+`microbiome` — no matching deposit. ⇒ raw LC-MS spectra not publicly findable nine years post-publication.
4. **Code repo search.** No GitHub repo linked in the paper. GitHub search for author names + topic returned zero relevant hits. The R/XCMS preprocessing snippet is embedded as text inside Additional file 4 (PDF). All other tools cited (QIIME, DESeq2, MBCluster.Seq, vegan, PICRUSt, MUSICC, FishTaco) are public packages.
5. **Smoke test on CherryRd.** Downloaded the smallest FASTQ pair (SRR5210762, 2.3 MB total). md5 of both files matches ENA. Read count (20,484) matches ENA `read_count` exactly. The dominant 5'-mer at the read start is `TACGT/TACGG` (~89% of reads) — exactly the expected V4 16S amplicon signature for F515/R806 primers described in the methods. ⇒ data integrity confirmed end-to-end.
6. **Metadata derivation.** Wrote `scripts/build_metadata.py` to parse Time + Dose from sample titles and emit a QIIME-style mapping file (`data/metadata.tsv`). Cell counts confirm the **perfect 10×4×2 balance** stated in the paper.
7. **Supplement inventory.** Opened all 10 `.xls` supplements with `xlrd`; verified sheet names, dimensions, and headers. Confirmed they contain the headline statistics needed for digital re-replication (PERMANOVA pseudo-F, ANOSIM R, α-diversity per-cell means, Kruskal–Wallis taxa rankings, FishTaco net shifts, full LC-MS feature table with 4,565 features × 20 columns, HMDB-class enrichments, 192-row metabolite↔OTU association table, MS/MS confirmation table).

## What works (evidence)

- **Raw 16S data: fully reproducible.** Per-file md5s in ENA + smoke-verified download on CherryRd.
- **Experimental metadata: clean.** ENA sample titles deterministically yield the 10×4×2 design — no ambiguity.
- **Headline statistics: digitally re-replicable.** MOESM1 contains the exact PERMANOVA / ANOSIM numbers (e.g., Dose ANOSIM R = 0.3864, p = 0.001; Time:Dose R = 0.3561, p = 0.001) that we can recompute from a re-run distance matrix and cross-check.
- **Functional/PICRUSt + FishTaco results: directly digitally checkable.** MOESM7 carries the per-pathway Wilcoxon shift statistics.

## Blockers

- **LC-MS raw spectra: missing.** Paper promised Dryad deposit; no record found in Dryad, Metabolomics Workbench, MetaboLights, PRIDE, or via author searches. ⇒ XCMS re-pipelining cannot be replicated independently without contacting authors (policy: do not contact). Downstream metabolomics analyses can still be reproduced from the **processed** feature matrix in MOESM8.
- **No source repository.** Pipeline must be reconstructed from prose methods. Mitigation: methods are reasonably specific (QIIME default params, 60,000-read rarefaction, GreenGenes 13_8, DESeq2, MBCluster.Seq, PICRUSt v1, MUSICC, FishTaco). Tooling all installable via QIIME2 + R.
- **Heavy compute not on CherryRd.** Tier 2 will need `uicgpu` (or equivalent). Job plan written in `JOB_PLAN.md`; no submission attempted in this pass.

## Verdict

- ✅ **ready-to-run** for Tier 1 (digital re-replication of headline stats from supplements) — minutes on CherryRd.
- ✅ **ready-to-run** for Tier 2 (16S pipeline re-run from raw FASTQ) — submit on uicgpu per `JOB_PLAN.md`.
- ⚠️ **partial-scope** overall, because Tier 3 (metabolomics from raw spectra) is **blocked** without author contact / paid access. Mitigation: do digital re-replication from MOESM8/9/10/11 instead.

## Outputs of this pass

All under `/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/_LUCID100_WAVE1_LAUNCH_QA/lucid100-space-type-radiation-induces-multimodal-responses-in-the-mouse-gut-microbi/`:

- `README.md` — full citation, data/code availability, target claims, acceptance criteria.
- `PROGRESS.md` — what I tried, next actions.
- `ARTIFACT_MANIFEST.md` — md5s of all harvested artifacts.
- `JOB_PLAN.md` — Tier 2 uicgpu QIIME2 plan (no submission yet).
- `harvest/` — article HTML/PDF/text + ENA filereport + SRA EUtils search.
- `supplements/` — all 11 BMC additional files (Tables S1–S10 + Figures S1–S4 PDF).
- `data/metadata.tsv` — derived 80-sample mapping file (sample-id, time_days, dose_gy, group, FTP URLs).
- `data/smoke/` — smallest FASTQ pair downloaded + md5-verified (SRR5210762).
- `scripts/fetch_all_fastq.sh` — md5-checked bulk downloader for all 80 runs.
- `scripts/smoke_fastq_check.py` — verifies a downloaded run against ENA (md5 + read count + V4 prefix sanity).
- `scripts/build_metadata.py` — regenerates `metadata.tsv` from ENA filereport.

Progress JSON updated: `/Users/stevens/.openclaw/workspace/memory/subagent-progress/lucid100-wave1-2-space-type-radiation-induces-multimodal-responses-in-the-mou.json`.

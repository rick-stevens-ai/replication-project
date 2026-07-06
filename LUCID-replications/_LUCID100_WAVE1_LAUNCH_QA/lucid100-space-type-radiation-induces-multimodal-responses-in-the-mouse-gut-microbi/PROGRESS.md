# Progress — Casero et al. 2017 (Microbiome) — LUCID100 / Wave 1 / Slot 2

**Status:** first-pass complete → **partial-scope ready-to-run**.

## What I tried (2026-06-09)

1. Pulled article HTML + PDF + plaintext from microbiomejournal.biomedcentral.com (open access, CC BY 4.0).
2. Downloaded all 11 BMC Additional files (Tables S1–S10 + Figures S1–S4 PDF). md5-recorded in `ARTIFACT_MANIFEST.md`.
3. Resolved the only public data accession in the paper: **SRA SRP098151** (16S V4 raw reads). Pulled ENA filereport — confirmed 80 paired-end Illumina HiSeq 2500 amplicon runs (~2.08 GB), each with per-file md5.
4. Searched Dryad + Metabolomics Workbench for the LC-MS metabolomics dataset the paper promised would be deposited. **Zero hits** by paper DOI, title, or author last names (Casero, Cheema, Fornace, Pannkuk, Datta).
5. Searched GitHub for author/topic — no public source repo.
6. **Smoke test on CherryRd:** downloaded smallest FASTQ pair (SRR5210762, 2.3 MB). md5 of both files matches ENA exactly; read count (20,484) matches; dominant 5'-mer is `TACGT/TACGG` (~89%) — exactly the expected V4 16S signature with F515/R806 primers. End-to-end data integrity confirmed.
7. Wrote `scripts/build_metadata.py` → derived 80-sample mapping file with Time / Dose / Group columns. Verified perfect 10×4×2 balance.
8. Inventoried all supplements with `xlrd` — confirmed they contain the headline statistics (PERMANOVA/ANOSIM, α-diversity, Kruskal–Wallis, FishTaco, LC-MS feature matrix, HMDB enrichments, Mantel + metabolite↔OTU associations, MS/MS confirmations).

## Verdict

- Tier 1 (digital re-replication from supplements): **ready-to-run on CherryRd**, minutes.
- Tier 2 (16S pipeline re-run from raw FASTQ): **ready-to-run on uicgpu**, hours; plan in `JOB_PLAN.md`.
- Tier 3 (metabolomics re-pipelining from raw spectra): **BLOCKED** — raw LC-MS not publicly findable. Mitigation: digitally re-replicate from MOESM8/9/10/11 instead.

## Next actions (in priority order)

1. **[Tier 1]** Implement `scripts/tier1_digital_replication.py` to recompute key headline stats from `supplements/*.xls` (α/β diversity, Kruskal–Wallis taxa ranking, metabolite-regression FDR counts) and emit a side-by-side comparison vs published values. Acceptance: ±10%.
2. **[Tier 2]** On uicgpu, run `scripts/fetch_all_fastq.sh` then the QIIME2 DADA2 + closed-ref GreenGenes 13_8 pipeline as scripted in `JOB_PLAN.md`. Compare PERMANOVA pseudo-F / ANOSIM R for Dose, Time, Time:Dose to MOESM1.
3. **[Tier 2]** Run PICRUSt + FishTaco vs MOESM7 to check predicted-function shift directions and magnitudes.
4. **[Tier 1.5]** Recompute metabolite-class HMDB enrichments from MOESM8 features → cross-check MOESM9.
5. **[Documentation]** Update `FIRST_PASS_REPORT.md` → final `REPORT.md` once Tiers 1 + 2 are run.
6. Reconsider whether to relax the "no author contact" policy if the LC-MS raw spectra remain critical. Otherwise close Tier 3 as scope-reduced and document.

## Blockers

- LC-MS raw spectra missing from Dryad / public repos. Policy forbids author contact in this pass.
- Tier 2 needs uicgpu access (or equivalent), not CherryRd.

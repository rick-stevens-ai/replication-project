# Failure Analysis — BVBRC-27 Egan 2020 optrA/poxtA

**Verdict:** PARTIAL REPLICATION.
**What "failure" means here:** Egan et al. 2020 makes ~7 discrete claims (C1–C7). Four (C1–C4) are the molecular / plasmid-structural claims and all four replicated cleanly, at 2-decimal precision, and were independently reconfirmed 36/36 on 2026-07-03 with a different AMR tool. Three (C5–C7) — the epidemiological headline, the phylogenomic clustering, and the 23S SNP analysis — are **out of reach** from public data. The word "failure" applies only to those three untestable claims and, once, to a paper-side data-name error (pE349 → pE394) that the replication caught.

## 1. Untestable claims (root cause: missing raw reads)

### 1.1 C5 — 22.7 % prevalence (35/154)
- **What failed:** Cannot re-derive the 35/154 denominator from public data.
- **Root cause:** Table S1 (154-isolate metadata) is supplementary text/PDF, not machine-readable; no per-isolate accession-linked table; the 154-isolate cohort is defined by referrals to the Irish National MRSA Reference Laboratory and no isolate list was deposited.
- **Contradicted?** No. Cannot be tested at all.
- **What would fix it:** authors deposit machine-readable Table S1 (isolate ID → species → sample date → optrA/poxtA PCR result), or a BioSample per-isolate registration linking to the PCR outcome.

### 1.2 C6 — cgMLST / wgMLST clustering (CI–CVII, 10 STs, ST80-predominant)
- **What failed:** Cannot re-run cgMLST/wgMLST typing on the 55 WGS'd isolates.
- **Root cause:** Only 3 hybrid-assembled plasmids and 6 optrA-region excerpts were deposited (accessions MN831410–MN831419). The 55 full-genome assemblies were not deposited; more importantly, the underlying MiSeq/MinION raw reads were never deposited (no SRA experiment, no BioProject).
- **Contradicted?** No — the deposited plasmid content is consistent with the paper's typing claim, but the typing itself is untestable.
- **What would fix it:** raw reads → SRA + assemblies → GenBank WGS. Would enable independent cgMLST calling with (e.g.) chewBBACA against the *E. faecium* / *E. faecalis* schemes at Pasteur.

### 1.3 C7 — 23S rRNA G2576T mutation, copy-number 1–5
- **What failed:** Cannot map raw reads to 23S rRNA copies to call the G2576T SNP or count mutated allele copies.
- **Root cause:** Same as C6 — no raw reads.
- **Contradicted?** No.
- **What would fix it:** deposit raw MiSeq reads → per-isolate `bwa` → `samtools mpileup` on the 23S locus → allele-fraction analysis.

## 2. Paper-side error caught by the replication

### 2.1 "pE349" is a typo for pE394
- **Symptom:** Egan Table 2 cites the *optrA* reference plasmid as "pE349" with 100 % identity to their 36,331 bp pM17/0149.
- **Investigation:** No plasmid literally named "pE349" of size 36,331 bp exists on NCBI. pE394 (KP399637) — the original *optrA* plasmid from *E. faecalis* E394 (Wang et al. 2015) — is exactly 36,331 bp and matches pM17/0149 at 99.997 % identity (1 mismatch total over full length, verified by `blastn`).
- **Verdict:** Nomenclatural error in the paper. The identity CLAIM is right; the accession NAME is wrong. This *strengthens* the paper's C2 claim (pE394 is the well-known lineage) but forces any downstream reader chasing "pE349" to fail.
- **Fix:** author erratum linking Table 2 "pE349" → pE394 / KP399637.
- **Independent reproduction (2026-07-03) confirmed** this correction — no pE349 record of that size exists on NCBI as of the rerun date.

## 3. Threshold / method choices where a different call could differ

### 3.1 Presence threshold on AMR screen
- The report used `pident ≥ 90 %` AND `coverage ≥ 60 %` (AMRFinderPlus-style).
- Independent 2026-07-03 rerun with `abricate v1.4.0` at its defaults flagged `erm(A)` at 87.16 % id on 4 records (MN831413/15/16/17).
- 87.16 % is BELOW the ≥90 % threshold, so the report correctly excluded it.
- This is a known erm-family catalog cross-reactivity (erm(A) ↔ erm(B) share partial similarity); the dominant erm on MN831413 is unambiguously erm(B) at 100.00 %.
- **Not a failure** — threshold choice is documented, defensible, and the borderline hit does not change any biological conclusion. But it is a good example of where reasonable pipelines can disagree, and future replications should not treat sub-threshold hits as contradictions.

### 3.2 Reference-catalog version drift
- Original run: `AMR_CDS.fa` = 9,712 alleles (NCBI FTP snapshot at run time).
- Independent 2026-07-03 rerun: NCBI AMRFinderPlus DB = 8,232 alleles (curated core) + ResFinder = 3,206 alleles (cross-check).
- Version drift did not affect any of the 36 tested numbers.
- **Not a failure** — but a real reproducibility hazard for future replications; both bundles are pinned in `report/evidence/independent_reproduction/tool_versions.txt`.

## 4. Replication-side limitations (things we don't claim)

1. **We validated artifacts, not the pipeline that made them.** The AMR screen ran on the authors' *assembled* plasmids. We did NOT re-run Unicycler on raw reads (they don't exist publicly). If the assembly is wrong, we would mirror the error silently. A reader entitled to ask "is the assembly correct?" cannot get that answer from this replication.
2. **C4 uses deposited CDS, not re-called variants.** The nt-difference vector {0,1,2,2,2,3,6,6} confirms the *deposited* alleles differ. If a deposited allele carries an assembler-introduced error, we replicate the error.
3. **LLM-judge is one moving part.** The verdict summary was generated by `argo:gpt-4o`. Every underlying *number* is deterministic BLAST/Biopython output and was independently reconfirmed 36/36 on 2026-07-03, so the LLM is not on the critical path for facts — but the 4/10 / 4/4 scoring is a judgment call.
4. **Coverage denominator (4/10) is honest, not generous.** We chose 4/10 (4 molecular claims tested, 3 untestable, 3 held back) rather than 4/4-of-testable, because the former makes the untestable gap visible.

## 5. What would flip the verdict from PARTIAL → REPLICATED

The three-item shopping list, in priority order:

1. **Deposit raw reads (SRA + BioProject).** Single largest lever. Unlocks C5, C6, C7 in one deposit and removes the trust-the-authors gap on assembly quality.
2. **Deposit machine-readable Table S1** (isolate → PCR result → MIC → cgMLST cluster). Enables re-derivation of the 22.7 % headline and per-isolate allele-to-MIC linkage.
3. **Publish an erratum for the pE349 → pE394 nomenclatural error.** Zero-cost, fixes accession lookups downstream.

## 6. What would NOT change the verdict
- Extending the AMR-catalog to more alleles (already tried — 36/36 invariant to catalog version).
- Adding more LLM judges (already deterministic underneath).
- Re-BLASTing at higher stringency (would remove only the sub-threshold erm(A) hit that was already excluded).

## 7. Bottom line
The replication executed cleanly. Every reproducible number reproduces at 2 decimals; every untestable claim was declared untestable up front with an auditable reason (no raw reads deposited); one paper-side nomenclatural error was caught and documented; the verdict is honest PARTIAL, not inflated REPLICATED nor deflated FAILED. The residual gap is a data-availability limitation of the original study, not a defect of the replication or the biology.

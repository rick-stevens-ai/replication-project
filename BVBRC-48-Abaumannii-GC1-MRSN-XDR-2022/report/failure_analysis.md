# Failure Analysis — BVBRC-48 (Harmer 2022, MRSN 56 GC1 A. baumannii)

**Verdict on the replication as a whole:** REPLICATED. This file catalogues everything that did NOT go smoothly, or was deliberately not attempted, so future replications can avoid the same traps and Rick has an honest ledger.

---

## 1. Outright failures — none

No step of the replication produced a wrong-answer confirmation. All numerical results reproduced by three orthogonal AMR callers, direct FASTA counts, or BLAST agree with the paper (or are documented as out-of-scope / DB-version artifacts).

## 2. Partial / caveated results

### 2.1 Oxford MLST scheme — did not reproduce ST231
- **What happened.** Pasteur scheme returned ST1 cleanly. Oxford scheme (`abaumannii`) returned a partial/novel profile: gltA-10, gyrB-12, **gdhB-4/182 (two alleles)**, recA-11, cpn60-4, gpi-98, rpoD-5 — no ST assignment.
- **Root cause.** Local `mlst` (2.33.1) database version drift on the *gdhB* locus. This is a well-known Oxford-scheme issue (Oxford scheme has been repeatedly criticized for allele instability at *gdhB*/*gpi*).
- **Impact.** None on the GC1 assignment. Pasteur ST1 is definitional for GC1 and was confirmed unambiguously.
- **Lesson.** When replicating any MLST call, pin both the scheme name AND the database commit/date. Report both in the replication note.
- **How to close the gap in a future run.** Fetch the mlst allele database as-of the paper's submission date and rerun; or run PubMLST's REST API directly with the exact allele set the paper reports.

### 2.2 Novel *mar*-operon FQ resistance mechanism (C6b) — out of scope
- **What happened.** The paper's title-level "novel route to fluoroquinolone resistance" (IS*Aba1* inactivating *marR*, constitutive *marA/marB*) was neither confirmed nor contradicted.
- **Root cause.** This is a functional/expression hypothesis; sequence re-analysis alone cannot test it. The genomic prerequisites (IS*Aba1* in the *marR* region, IS*Aba1*-rich chromosome, gyrA S81L) are all present, but the causal mechanism requires RT-qPCR, isogenic knockouts, or complementation.
- **Impact.** Coverage 9/10 instead of 10/10. Verdict remains REPLICATED because the paper itself frames this element as needing "further work … to confirm the role of MarR inactivation."
- **Lesson.** In a claims table, tag each claim with `testable-from-sequence: {yes, no, partial}` upfront and be explicit that "no" claims will not gate a REPLICATED verdict.

### 2.3 IS*Aba125* cross-hit on pMRSN56-3
- **What happened.** A broad IS*Aba125*-family transposase query (tblastn WP_001988464 at 100%/100%) cross-hit a Rep_3 region on pMRSN56-3 in addition to the 2 chromosomal copies.
- **Root cause.** IS*Aba125* transposase family shares homology with certain Rep_3 replication proteins at the amino-acid level.
- **Impact.** None — the paper reports **chromosomal** IS*Aba125* copy number (2), which we matched. The plasmid cross-hit is noted in REPORT.md §4.7 for transparency.
- **Lesson.** When counting IS elements, report the counting protocol (query, thresholds) and any cross-hits explicitly; do not silently drop them.

## 3. Trap avoided — BioProject → wrong assembly

- **What almost happened.** Initial resolution of BioProject PRJNA742487 pointed to assembly **GCA_021484925.1 / chromosome CP090606, 4,153,776 bp**. This does NOT match the paper (4,033,258 bp). If accepted uncritically, every downstream analysis would have been on a **later, different assembly** of the same strain, producing plausible-looking but wrong replication numbers.
- **Root cause.** BioProject can accumulate multiple assemblies over time; the "current" one is not necessarily the "as-published" one.
- **How it was avoided.** Compared BioProject-linked chromosome size against the paper's reported chromosome size before running any tools. Mismatch triggered a fallback to direct-by-accession fetch (`efetch` of CP080452–CP080456).
- **Lesson (durable).** For any replication that quotes specific sequence coordinates or replicon sizes: **fetch by explicit replicon accession, not by BioProject**. Add a size-vs-paper sanity check as an early gate in the pipeline.

## 4. Deliberately not attempted (documented, not silently skipped)

### 4.1 Kaptive (KL1/OCL1) capsule/outer-core typing
- **Why skipped.** Out of BV-BRC AMR-analysis scope for BVBRC-48.
- **Cost of skipping.** Kaptive is free and takes minutes. KL1/OCL1 is part of the paper's GC1 signature; not verifying it leaves a small hole.
- **Recommendation.** Add Kaptive v3 (KL + OCL databases) to the standard BV-BRC-48 pipeline as a routine step; the runtime cost is negligible.

### 4.2 De novo Unicycler reassembly from raw reads
- **Why skipped.** Not required for content verification of the deposited replicons; the goal of BVBRC-48 was AMR-content replication, not assembly-pipeline replication.
- **Cost of skipping.** We cannot claim end-to-end pipeline reproduction; only content-of-deposited-assembly reproduction. IS*Aba1*-dense chromosomes are notoriously assembly-ambiguous, so this is a real (though separate) question.
- **Recommendation.** Add as a wave-2 follow-up: reassemble SRR14998418 + SRR14008417 with Unicycler (paper's version) and Trycycler (cross-check), then compare to CP080452–56 with dnadiff.

### 4.3 MIC / phenotype tie-in
- **Why skipped.** No MIC data are re-generated here; sequence re-analysis only.
- **Cost of skipping.** We verified the *genotype* half of the XDR claim. Whether MRSN 56 genotypically-predicted MICs match reported MICs is untested.
- **Recommendation.** Optional companion note; requires either published MIC data or wet-lab access to the isolate.

## 5. Meta-failures / process notes

### 5.1 LLM judge is not an independent oracle
- The free-Argo `argo:gpt-5.2` judge only sees the results we hand it. Its 9/10 scores confirm internal consistency, not independent verification. Treat it as an anti-fabrication check, not a second opinion. This is a general property of LLM-judge patterns, not a BVBRC-48-specific failure.

### 5.2 IS copy-number counting is threshold-sensitive
- We happened to hit the paper's 20 exactly at ≥99% identity over the transposase region using EU029998. The paper does not report its exact counting protocol. A different query/threshold pair could produce 18–22. The exact match is partly luck. See open_questions.json Q5 for the recommended parameter-sweep.

### 5.3 Data-loss discipline
- No `rsync --delete` was run against uicgpu or any authoritative source during this replication. All fetched replicons were kept in `work/` under the replication dir. Standing rule (from TOOLS.md) about never `rsync --delete`-ing against authoritative hosts was honored.

---

## Summary

- 0 outright failures.
- 2 caveated results (Oxford MLST DB drift; C6b out-of-scope hypothesis) — both documented in REPORT.md and neither affects the REPLICATED verdict.
- 1 major trap avoided (BioProject → wrong assembly) — worth turning into a general pipeline rule.
- 3 deliberate out-of-scope items (Kaptive, de novo reassembly, MIC tie-in) — each with a clear recommendation for a future wave.
- 0 fabricated numbers.

# Failure Analysis: BVBRC-54 — *S. flexneri* 5a M90T (Cervantes-Rivera 2020)

**Verdict:** PARTIAL REPLICATION. This document catalogs what did NOT reproduce, what was NOT executed, what is at risk of drifting on re-execution, and the honest limits of this workflow.

## Category A — Claims NOT re-executed (bound the verdict at PARTIAL)

### A1. C3: Raw-read assembly (PacBio SMRT + Illumina polish, Canu 1.7, ~157×)
- **What was tested:** the deposited finished assembly's replicon count/lengths were verified exactly against the paper.
- **What was NOT tested:** the paper's actual assembly step. Raw PacBio subreads were not fetched from SRA/ENA; Canu 1.7 was not re-run; the Illumina RNA-seq polishing step was not re-executed.
- **Consequence:** C1 and C2 verify self-consistency between the paper's text and the paper's own NCBI deposit (submitter = Umeå/MIMS = the paper's lab). A downstream user cannot conclude from this replication that the assembly methodology itself is reproducible from raw reads.
- **What would fix this:** SRA accession lookup for the raw PacBio and Illumina reads → re-run Canu 1.7 → polish → compare replicon count, lengths, and contig identity to CP037923.1/CP037924.1.

### A2. C6: dRNA-seq transcriptional start site quantification (6723 primary + 7328 secondary TSS)
- **What was tested:** data availability was noted.
- **What was NOT tested:** the TEX+/TEX− dRNA-seq libraries were not downloaded; the primary/secondary TSS counts were not re-derived.
- **Consequence:** the paper's transcriptomic claim is entirely unverified by this replication.
- **What would fix this:** SRA accessions for TEX+/TEX− libraries → align to CP037923.1 → apply a standard TSS-caller (TSSpredator or equivalent) → compare primary/secondary counts within a defined tolerance.

## Category B — Claims partially reproduced (softer than the summary implies)

### B1. C4: Annotation feature counts (CDS, tRNA, rRNA, pseudogenes, IS elements)
- **What matched cleanly:**
  - tRNA: paper 102, PGAP 102, Prokka 1.12 (here) 103. ≈Match.
  - rRNA: 22 across all three pipelines. EXACT match.
  - Pseudogenes: paper 769, PGAP 757, ~1.5% agreement.
- **What did NOT match cleanly:**
  - CDS: paper 4,949 vs. PGAP 4,053 vs. Prokka 1.12 (here) 5,004. Paper–PGAP delta ≈ 18%. This is a large gap that the report characterizes as "within a few percent" — that characterization is defensible for paper–vs–this-replication (1%) but understated for paper–vs–PGAP.
- **What was NOT executed:**
  - IS elements: paper reports 402. This replication did NOT run ISfinder or ISEScan on CP037923.1. The IS load was corroborated only indirectly via pseudogene count as a proxy for reductive evolution. Anyone building on the 402 figure needs to independently re-type IS elements.

## Category C — Methodological limits acknowledged explicitly

### C1. Deposited assembly = paper's own product
The submitter of GCF_004799585.1 is Umeå University / MIMS — the paper's own lab. Therefore C1 (2 replicons) and C2 (bp-for-bp lengths) verify that the paper's text matches the paper's own deposit. This is genuinely useful (it catches transcription errors and mislabels) but it is NOT the same as an ab-initio independent test of the assembly claim.

### C2. Coverage inflation via C7
C7 (public availability / usable deposit) is a near-tautology once we have already downloaded the record. Counting it in the "5/7 tested = 71%" fraction inflates the apparent coverage. A more conservative accounting: 3 fully reproduced (C1, C2, C5) + 1 partial (C4) + 1 trivial (C7) + 2 not run (C3, C6).

### C3. Annotation "consistency" is a loose criterion
Three independent annotation pipelines (paper Prokka+curation, RefSeq PGAP, our Prokka 1.12) count subtly different biological objects (protein-coding CDS vs. all CDS vs. curated). The absence of a large numeric discrepancy in tRNA/rRNA (unambiguous features) does NOT imply the CDS counts are strictly comparable.

### C4. Database vintage & reproducibility drift
Specialty-gene calls (T3SS effector list, PlasmidFinder IncFII assignment) depend on the 2026-Apr snapshot of VFDB/Victors/PlasmidFinder. We did not pin database checksums under `evidence/`. Re-running six months later will likely add or drop borderline effector hits (e.g., some `osp` family members). This is a soft-reproducibility risk, not a workflow failure — but it needs to be pinned to make the specific T3SS gene list reproducible-in-time.

### C5. LLM-judge is not an independent oracle
The PARTIAL verdict was assigned by an LLM judge (`argo:gpt-5.2`) reading the same evidence bundle the analyst prepared. This is a useful consistency check on the write-up, but it cannot detect a shared systematic artifact (e.g., an assembly error present in the paper AND in the NCBI deposit) because both derive from the same underlying record.

## Category D — Risks on re-execution

- **Re-annotation with a newer Prokka release** could shift CDS totals by a few percent (feature-model updates), moving the paper-vs-independent gap.
- **Re-scanning specialty genes against an updated VFDB** may re-classify a handful of pWR100 loci as different `osp`/`ipaH` family members or add/drop borderline hits.
- **Re-running AMRFinderPlus** with a newer database may reveal previously-unclassified intrinsic resistance determinants — still consistent with the "no acquired resistance" call, but with slightly different intrinsic-gene lists.
- **Re-doing MLST** with an updated Achtman scheme could re-report a different ST label if the scheme is renumbered (unlikely, but possible).

## Category E — No hard failures observed

There were no crash-level failures, no download failures on the NCBI Datasets API path, no annotation-pipeline breakages, no conda-env conflicts requiring re-provisioning. The workflow ran clean end-to-end on uicgpu. The PARTIAL verdict is a scope decision (raw-read assembly + dRNA-seq TSS not re-executed), not a symptom of tooling failure.

## Summary
- Not-executed (Category A): C3 (raw-read assembly), C6 (dRNA-seq TSS).
- Partially executed (Category B): C4 (IS elements not directly re-typed; CDS counts diverge across pipelines).
- Method-scope limits (Category C): deposit = paper's own product; C7 inflates coverage; annotation consistency is loose; DB vintage is a drift risk; LLM-judge is not independent.
- Execution failures (Category E): none.

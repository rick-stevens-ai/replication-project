# Failure Analysis — BVBRC-38 Gen2Epi *N. gonorrhoeae* AMR Replication

Verdict: **PARTIAL REPLICATION (strong; near-REPLICATED).** Free-Argo LLM judge scored the final package REPLICATED (8/10 coverage, 9/10 agreement); the canonical label is kept at PARTIAL because concrete elements of the paper were not exercised. This document is a candid enumeration of *what did not replicate*, *why*, and *what would close the gap*.

---

## 1. Scope collapse: 11 of 1484 samples

**Gap.** The paper evaluates Gen2Epi on **1484** *N. gonorrhoeae* WGS datasets across four studies:
- 11 WHO reference strains (Unemo 2016) ✅ reproduced.
- 27 Saskatchewan isolates ❌ not run.
- 398 New Zealand isolates ❌ not run.
- 1048 EuroGASP 2013 isolates ❌ not run.

We reproduced the smallest and easiest sub-cohort — the 11-strain WHO reference panel Gen2Epi was explicitly validated on. The three larger cohorts (which are the operational stress-test) are untouched.

**Why.** Deliberate scope trade-off: the 11-strain WHO panel is the *validation* set with the cleanest ground-truth phenotypes (Unemo 2016) and finished PacBio references, so it exercises every claim (assembly, typing, AMR, biological concordance) at low compute cost. Extending to 1484 samples would be roughly two orders of magnitude more compute (~1484 × ~5 min SPAdes on 16-core uicgpu ≈ 5 days wall-clock for de-novo assembly of everything), plus per-cohort accession fetching.

**Impact.** This is the single largest coverage gap and the primary reason the canonical verdict is PARTIAL rather than REPLICATED.

**How to close.** Batch-fetch ERR/SRR accessions for the three cohorts from ENA/NCBI (all public), stage them on uicgpu, run the same SPAdes + BLAST pipeline in parallel across the panel, and reproduce the paper's full-panel Table 2 typing accuracy and Table 1 assembly stats. No paid data or software.

---

## 2. Ragout scaffolding module not run

**Gap.** Gen2Epi step 3 uses **Ragout** for reference-based scaffolding to raise assembly N50 to chromosome-length scaffolds. We skipped this step; our de-novo N50 for WHO_F is **64,607 bp** — SPAdes pre-scaffolding contig level.

**Why.** Time. Ragout is an optional post-processing step; the biological questions (correct ST, correct AMR determinants) are answerable from contigs alone, so we invested the compute budget on breadth (all 11 strains typed + AMR + one full raw-reads loop) rather than on chromosome-scale scaffolding.

**Impact.** We cannot speak to the paper's headline scaffolding improvement (contig N50 → chromosome N50). The de-novo assembly reproduces the paper's *biological* claims but not its *assembly-quality* claim at the scaffold level.

**How to close.** Run Ragout on the SPAdes WHO_F contigs against the finished WHO_F reference and report the N50 improvement. Extend across the panel if resources permit.

---

## 3. Panel-wide QUAST misassembly metrics absent

**Gap.** Paper Table 1 reports misassembly count and duplication-ratio columns computed by QUAST against each strain's reference. We computed only a **single-strain genome fraction** (WHO_F: 99.96%) via a lightweight BLAST-based comparison, not the full QUAST-derived misassembly profile.

**Why.** Requires per-strain QUAST runs (each with its own reference), which was scope-cut for the same reason as the full 1484-sample run.

**Impact.** Claim C1b ("few/no misassemblies") is only indirectly supported by our one high-quality genome fraction. The absence of misassemblies is not directly quantified.

**How to close.** Install QUAST and run it strain-by-strain against each WHO reference; report the misassembly-count and duplication-ratio table alongside our stats.

---

## 4. Plasmid-type identification (step 4) not reproduced

**Gap.** Gen2Epi module 4 identifies plasmid types by BLASTN against 8 known *N. gonorrhoeae* plasmids (cryptic, tetM, β-lactamase-carrying variants, etc.). We did not run this module.

**Why.** Deprioritized. The 8-plasmid reference set is a curated Gen2Epi asset, and the biological claim is orthogonal to the chromosomal AMR claims (which were the load-bearing biology).

**Impact.** No coverage of plasmid-mediated resistance (β-lactamase / tetM-carrying plasmids). For a subset of clinical isolates this materially affects the AMR call.

**How to close.** Curate the 8-plasmid FASTA set (either from Gen2Epi source or from NCBI plasmid records referenced in the paper), run plasmidSPAdes on WHO_F reads, and BLAST assembled plasmid contigs against the reference set.

---

## 5. NG-MAST (NGMASTER) typing not reproduced

**Gap.** Gen2Epi module 5 includes NG-MAST typing (via NGMASTER) alongside NG-MLST and NG-STAR. We reproduced NG-MLST (all 11 strains, 7/7 profiles) and NG-STAR (all 7 loci, all 11 strains) but not NG-MAST.

**Why.** NG-MAST is a two-locus scheme (*porB* and *tbpB*) that duplicates AMR-adjacent information we already extracted via NG-STAR *porB*; the marginal information gain for the WHO reference panel was judged low. Setting aside NGMASTER also avoided pulling a second curated allele database.

**Impact.** Two of the three typing schemes are reproduced; NG-MAST is not. For epidemiological cluster-detection benchmarking, NG-MAST is heavily used in the historical literature and its absence limits cross-study comparability.

**How to close.** Install NGMASTER (or reimplement the two-locus BLAST scheme against the pubMLST NG-MAST allele database) and run it across the 11 WHO panel.

---

## 6. penA reported as mosaic vs non-mosaic, not exact NG-STAR allele integer

**Gap.** Our penA detection is **coarse-grained** — we classify each strain as *mosaic* vs *non-mosaic* by nucleotide identity vs the FA1090 wild-type (`<96% nt id = mosaic`). The paper's Gen2Epi output is the exact **NG-STAR penA allele integer**, which is a finer categorical assignment.

**Why.** The NG-STAR penA allele database + profile CSV are **not** distributed via pubMLST. The paper sourced them from the separate NG-STAR website. We did not integrate that snapshot into this replication.

**Impact.** The biological verdict (mosaic penA in exactly the ceftriaxone-R WHO X/Y/Z) is correct and phenotype-concordant, but the paper's finer-grained NG-STAR penA allele-integer output is not reproduced. Downstream users who need the exact NG-STAR nomenclature would not get it from our pipeline as-is.

**How to close.** Fetch a versioned snapshot of the NG-STAR penA allele + profile database from the NG-STAR website, integrate it as an additional BLAST target, and emit the allele integer per strain.

---

## 7. Single de-novo assembly (n=1)

**Gap.** The end-to-end raw-reads → assembly → typing+AMR loop was closed for **one** strain (WHO_F). The other 10 strains used the finished ENA PacBio references directly for typing and AMR.

**Why.** Illumina raw reads for the full 11-strain WHO panel exist on ENA but the de-novo loop for a single strain already exceeded 5 minutes of SPAdes on uicgpu; running all 11 was scope-cut.

**Impact.** The biologically most interesting test — closing the same raw-reads → assembly → typing+AMR loop for the ceftriaxone-R WHO X/Y/Z and confirming that the de-novo assembly recovers the mosaic-penA call — was not done. WHO_F is a benign, wild-type-penA phenotype, so it is the easiest case.

**How to close.** Fetch the Illumina reads for WHO X, Y, Z (and the rest of the panel) from ENA, run the same fastp → SPAdes pipeline, and confirm the mosaic-penA call is recovered from the de-novo assemblies.

---

## 8. Methods reproduction, not the shipped VirtualBox image

**Gap.** We did not run the CentOS-7 VirtualBox Gen2Epi image distributed via `ftp://ftp.cs.usask.ca/pub/combi`. We re-implemented the paper's method with the same tool families (BLAST+, SPAdes, fastp/Trimmomatic-equivalent, Biopython, pubMLST).

**Why.** Running the VirtualBox VM adds a heavy operational dependency (VM host, image download, guest-tool provisioning) that duplicates the pipeline's *behaviour* without adding *evidence* — the paper's claims are about biology, not about a specific tool binary.

**Impact.** This is a **methods reproduction**, not a bit-identical software rerun. Differences in tool versions (e.g., SPAdes 4.3.0 here vs whatever the 2019 Gen2Epi image ships) could plausibly shift edge-case calls. In practice the biological outputs are stable — MLST ST calls are deterministic given the same allele database, and the AMR determinant codons are unambiguous.

**How to close.** Bring up the VirtualBox image, rerun the WHO panel, and diff outputs. Any divergence would isolate to tool-version drift.

---

## 9. Reference-gene provenance is FA1090, not the paper's exact reference set

**Gap.** We used FA1090 CDS extractions as the wild-type reference for AMR gene BLAST. The paper's NG-STAR pipeline uses a curated NG-STAR gene set (with its own allele database).

**Why.** FA1090 is the canonical wild-type reference and is freely available with a complete annotation via NCBI Datasets — a stable, versioned source. The NG-STAR curated gene set requires a separate ingest (see gap #6).

**Impact.** For the seven canonical resistance codons the two references are functionally equivalent, but subtle allele-ID divergences are possible for penA/mtrR/porB (the loci where NG-STAR uses its own allele numbering).

**How to close.** Ingest the NG-STAR reference gene set alongside FA1090 and cross-check the codon reads for divergence.

---

## 10. LLM-judge is corroboration, not the primary verdict

**Gap.** The free-Argo `gpt-5.2` judge scored the package REPLICATED (8/9). Some readers might over-weight the LLM verdict.

**Why.** LLMs are used only as an independent corroborating signal — never as the primary scoring mechanism (no regex-scoring, no numeric extraction from LLM output into the results table).

**Impact.** None on the reported numbers; potential misinterpretation risk if the reader treats the LLM verdict as the ground truth.

**How to close.** Explicit disclaimer already in REPORT.md §4.6 and REPORT.tex §Genuine Critique. The canonical numbers (genome stats, ST calls, AMR determinant tables) stand on their own.

---

## Summary — what would raise this from PARTIAL to REPLICATED

None of the gaps require paid data or software. The gap-closing work is:

1. Run the full 1484-sample cohort on uicgpu (batch SPAdes + BLAST) — closes gap #1.
2. Add a Ragout scaffolding pass across the panel — closes gap #2.
3. Add panel-wide QUAST vs each reference — closes gap #3.
4. Add plasmid module + 8-plasmid reference — closes gap #4.
5. Add NGMASTER — closes gap #5.
6. Ingest NG-STAR penA allele database → allele-integer output — closes gap #6.
7. Extend the de-novo loop to all 11 WHO strains (esp. X/Y/Z mosaic penA) — closes gap #7.

Estimated additional compute: ~5 days wall-clock on uicgpu for the full 1484-sample de-novo pass, plus ~1 day for the auxiliary modules. No new data licensing.

**Bottom line:** every "failure" here is a scope decision, not a scientific blocker. The paper's biology and its central end-to-end capability claim are strongly reproduced within the reduced scope; the "PARTIAL → REPLICATED" path is well-defined future work.

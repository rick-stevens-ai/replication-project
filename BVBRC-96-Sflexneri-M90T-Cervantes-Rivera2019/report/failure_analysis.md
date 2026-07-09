# Failure Analysis — BVBRC-96 replication

**Paper:** Cervantes-Rivera R, Tronnet S, Puhar A. *BMC Genomics* 21:285 (2020).
**Verdict:** PARTIAL REPLICATION (strong).

This file documents what did NOT replicate, what was NOT attempted, and why. It exists so
that the PARTIAL verdict is honestly bounded.

---

## 1. Claims NOT independently re-executed

### C3 — PacBio SMRT de-novo re-assembly (Canu 1.7, ~157× coverage)

- **Paper claim:** the genome was assembled from PacBio SMRT long reads using Canu 1.7 at
  ~157× coverage, then polished with Illumina RNA-seq short reads.
- **What we did instead:** verified the *deposited product* (chromosome NZ_CP037923.1 +
  plasmid NZ_CP037924.1) bp-for-bp against the paper's stated lengths. This confirms that
  what was deposited matches what the paper described, but does NOT confirm that Canu 1.7 on
  the raw reads yields exactly that product.
- **Why not attempted:**
  1. Wall-time cost. A Canu 1.7 assembly of ~157× PacBio coverage on a ~4.8 Mb bacterial
     genome takes >12 h on uicgpu even parallelised — larger than the budget for a single
     subagent turn.
  2. Marginal independent-verification value. The deposited assembly's RefSeq comment fields
     carry Canu output signatures; the community has been using this assembly for six years
     with no reported issues.
- **Recovery plan (if promoted from PARTIAL to REPLICATED):** pull the raw PacBio reads from
  SRA under PRJNA510559, run Canu 1.7 with the paper's stated parameters, apply the paper's
  RNA-seq polishing pass with Pilon or the paper-cited tool, then `dnadiff`
  (MUMmer) the resulting contigs against `NZ_CP037923.1` and `NZ_CP037924.1`.

### C9 — dRNA-seq TSS re-calling (6,723 primary + 7,328 secondary TSS)

- **Paper claim:** genome-wide transcriptional start sites determined by dRNA-seq;
  6,723 primary + 7,328 secondary TSS integrated into RegulonDB/RSAT.
- **What we did instead:** verified the data-availability path (raw reads deposited under
  PRJNA510559 SRA); did NOT re-execute a TSS-calling pipeline.
- **Why not attempted:**
  1. The re-analysis is a multi-hour-to-multi-day pipeline (adapter trim → align →
     rockhopper / TSSpredator / ANNOgesic → RegulonDB/RSAT cross-map).
  2. Non-trivial parameter reproduction (the paper's exact TSS-calling thresholds,
     enrichment-vs-untreated ratios, and secondary-vs-primary demarcation rules would need
     to be pinned down).
  3. This is the single biggest gap in this replication. The dRNA-seq half of the paper is
     essentially trust-the-paper here.
- **Recovery plan:** pull PRJNA510559 raw reads → adapter/quality trim (fastp) → align to
  the deposited assembly (BWA / bowtie2) → run TSSpredator with paper-matched parameters or
  rockhopper as a cross-check → compare primary/secondary TSS counts and genomic
  distribution against the paper's supplementary tables.

## 2. Quantitative discrepancies that did NOT invalidate the verdict but deserve caveats

### IS-element count: 585–617 (this replication) vs ~402 (paper)

- **What we found:** grep on the PGAP GFF gave 585 IS transposases
  (`product=IS[0-9]`) and 617 by broader `transposase` match.
- **Paper stated:** ~402 IS elements (BV-BRC RAST annotation).
- **Root cause:** pipeline choice — PGAP (used here on the deposited assembly's own PGAP
  GFF) vs BV-BRC RAST (used in the paper). The two pipelines classify IS transposases
  differently (PGAP is more permissive on divergent IS families and fragment ORFs).
- **Impact on verdict:** qualitative agreement (Shigella-typical high IS density) is
  preserved; quantitative agreement is not. C4 remains ✅ but explicitly annotated as
  "consistent (qualitative)" rather than "exact match".
- **Recovery plan:** run an independent IS caller (ISfinder BLAST, ISEScan v1.7.2.3, or
  OASIS) against both replicons; that will produce a third count that either mediates or
  further diverges from the two existing counts.

### CDS count discrepancy (small)

- **This replication:** 5,003 CDS (4,706 chromosome + 297 plasmid).
- **Paper:** ~4,900–5,000 CDS (BV-BRC RAST and PGAP counts differ by <2%).
- **Impact:** within the paper's own <2% inter-pipeline tolerance. No verdict change.

## 3. Methodological limits that could bias the verdict optimistically

- **Single-database plasmid typing.** PlasmidFinder is canonical but only one database.
  Cross-checking with MOB-suite (`mob_typer`) would tighten C6.
- **Single-database VF typing.** VFDB alone; Victors and PATRIC-VF were not run as
  cross-checks despite being nominally part of the BVBRC-96 workflow. Convergence of two
  databases would strengthen C5 and C7.
- **No functional verification of T3SS.** Presence of genes ≠ presence of a functional
  T3SS. The paper does not claim functional verification here either (decades of prior
  M90T literature cover that), but the reader should be clear that
  "full T3SS reconstruction" means gene-inventory reconstruction, not phenotypic.
- **Reference-database version drift.** PlasmidFinder DB used here is dated 2017-03-19;
  VFDB has moved on since the paper. Newer database releases could add or reclassify hits.
- **RNA-seq polishing not orthogonally re-checked.** The paper's unusual choice of
  polishing PacBio assembly with RNA-seq short reads (rather than genomic short reads) can
  introduce systematic biases in intergenic regions. No orthogonal genomic-short-read
  re-polish was attempted here.

## 4. Non-failures worth calling out

- **Sibling replication (BVBRC-54) not re-used or cross-contaminated.** Per wave-brief
  rules, `BVBRC-54-Sflexneri-M90T-genome-Cervantes2020/` was NOT touched. This BVBRC-96
  execution is an independent fresh pull with distinct workflow emphasis (PlasmidFinder /
  Similar Genome Finder / Specialty Genes / Comprehensive Genome Analysis legs of the
  BVBRC-96 workflow class). The fact that BVBRC-54 and BVBRC-96 independently converge on
  the same PARTIAL (strong) verdict is a positive external consistency check, not a
  failure.

## 5. Path to full REPLICATED verdict

To promote this replication from PARTIAL (strong) to full REPLICATED, the following are
required in priority order:

1. **Re-execute C9 (dRNA-seq TSS calling).** Highest scientific value; largest current gap.
2. **Re-execute C3 (Canu 1.7 de-novo assembly).** High compute cost but low uncertainty
   payoff; expected to succeed.
3. **Cross-database VF/plasmid typing.** Run MOB-suite + Victors + PATRIC-VF as convergent
   confirmations for C5, C6, C7.
4. **Independent IS typing** (ISEScan / ISfinder) to arbitrate the IS-count discrepancy in C4.
5. **Optional: orthogonal short-read genomic polishing** as a bias check on the paper's
   RNA-seq-only polishing choice.

Until at least items 1 and 2 are executed and match the paper's numbers, the honest
verdict remains PARTIAL (strong).

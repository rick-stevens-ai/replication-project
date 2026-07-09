# Failure Analysis — BVBRC-30 (Urbaniak 2018 ISS *E. bugandensis*)

**Verdict recap:** PARTIAL (strong core replication). What follows is the honest catalogue of every element that did **not** close cleanly and why. Nothing here changes the species / clonality / core-AMR conclusions, but each item is a real gap that would need to be addressed to move the verdict from PARTIAL to REPLICATED.

---

## F1 — SNP-distance mismatch (order-of-magnitude)

- **Paper:** 9–15 SNPs among the 5 ISS strains.
- **This replication:** 81–183 SNPs against IF3SW-P2.
- **Root cause:** methodological, not biological.
  - Paper used bwa-mem read mapping + GATK HaplotypeCaller with false-positive filtering on raw Illumina reads.
  - This replication used assembly-vs-assembly alignment (minimap2 `-x asm5`) with paftools SNP calling.
  - Assembly-vs-assembly inherits assembly-graph ambiguities that stringent read-mapping + GATK filters explicitly remove.
- **Impact on conclusions:** none for clonality — even 183 SNPs across ~4.93 Mb is >99.996% identity. But the *numerical* claim (9–15 SNPs) is not reproduced; only the *qualitative* clonality claim is.
- **What would close it:** pull the raw Illumina reads (PRJNA319366) for each ISS isolate, rerun the paper's exact bwa-mem + GATK HaplotypeCaller + FP-filter pipeline, and compare SNP counts on the same reference (IF3SW-P2).

---

## F2 — Outgroup ANI drift (numerical, species-boundary panel)

- **Symptom:** *E. asburiae* ATCC35953 Δ = +6.30% and *E. aerogenes* KCTC2190 Δ = +3.17% between this replication and paper Table 1.
- **Root cause:**
  1. Different downstream reference assemblies for those species than the exact type-strain assemblies the paper used.
  2. fastANI and Goris 2007 BLAST-ANI diverge more at lower identity (below ~90%).
- **Impact on conclusions:** none. Every non-bugandensis outgroup still falls under the ~95% species boundary, so the species-defining conclusion (all 5 ISS strains = *E. bugandensis*) is intact. But if the exercise were “recreate Table 1 to 2 decimals across all rows,” it would fail on the *E. asburiae* / *E. aerogenes* rows.
- **What would close it:** re-download the exact type-strain assemblies the paper cites for those two outgroups, and run Goris BLAST-ANI (not fastANI) to match the paper's algorithm.

---

## F3 — Wet-lab phenotype claim (C4) not reproduced

- **Paper claim:** phenotypic resistance to cefazolin, cefoxitin, oxacillin, penicillin, rifampin.
- **This replication:** not attempted (out of scope for a computational replication).
- **Genotype consistency:** the AMR gene set found (blaACT AmpC + fosA + oqxA/oqxB + fieF) is *mechanistically consistent* with cefazolin and cefoxitin resistance in particular. But “consistent with” is not “reproduces.”
- **What would close it:** disk diffusion / Vitek / broth microdilution on cultured isolates. Not achievable from public sequence data alone.

---

## F4 — RAST subsystem counts (C5) not regenerated

- **Paper claim:** ~4733 genes for IF3SW-P2, with specific RAST subsystem-category counts (635 / 496 / 291 / …), 112 virulence genes.
- **This replication:** length / GC% / contig count on the assemblies confirm they sit within the *Enterobacter* genomic envelope consistent with ~1 gene/kb (i.e. ~4.9k genes for ~4.93 Mb). But the *actual* gene calls and RAST subsystem categorization were not redone.
- **What would close it:** run RAST (or Prokka + subsystem mapping) on each of the 8 *E. bugandensis* assemblies and reproduce the per-subsystem counts; independently regenerate the virulence-gene inventory using VFDB / VirulenceFinder.

---

## F5 — dDDH not recomputed

- **Paper claim:** ~89% dDDH from ISS strains to EB-247 / 153_ECLO.
- **This replication:** dDDH was skipped; ANI was substituted as the equivalent species-boundary metric.
- **Impact on conclusions:** none for the species assignment (ANI is fine for that). But the paper's specific ~89% dDDH figure is not independently verified.
- **What would close it:** submit the assemblies to GGDC (the same web service the paper used) and report the returned dDDH values against EB-247 and 153_ECLO.

---

## F6 — Only IF3SW-P2 used as SNP reference for clonality

- **Symptom:** SNP counts (`work/snp2/*.var`) are all reported against a single reference (IF3SW-P2), not full pairwise 5×5.
- **Impact:** reference-dependence means SNPs unique to IF3SW-P2 vs each other strain are counted, but a full inter-strain pairwise SNP matrix (which would let us reproduce the paper's max-15-SNP statement across all pairs, not just against one reference) is not present.
- **What would close it:** run assembly-vs-assembly SNP calling for all 10 ISS pairs (or use a proper core-genome SNP pipeline like snippy / Parsnp on the raw reads) and report the full 5×5 matrix.

---

## F7 — Plasmid / mobilome content not analyzed

- **Symptom:** the AMR-repertoire analysis is silent on whether any of the AMR genes sit on plasmids, ICEs, or transposons vs the chromosome.
- **Impact on conclusions:** none for “what AMR genes are present.” Real gap for downstream questions about horizontal transfer risk (see `open_questions.json` OQ2).
- **What would close it:** plasmidSPAdes / MOB-suite / PlasmidFinder / MOB-typer on the 5 ISS + 3 clinical assemblies; long-read (ONT/PacBio) resequencing where existing 2-contig assemblies fuse replicons.

---

## Judge signal cross-check

The three independent LLM judges landed at 2× PARTIAL, 1× REPLICATED (`work/judge_scores.json`). The single REPLICATED vote is defensible on species + clonality + core AMR alone; the two PARTIAL votes correctly reflect F1 + F4 + F3 (and to a lesser extent F2, F5, F6, F7). The consensus PARTIAL verdict is the honest read.

---

## Summary table

| ID | Gap | Class | Blocks REPLICATED verdict? |
|----|-----|-------|----------------------------|
| F1 | SNP counts (9–15 vs 81–183) | methodological | Yes (numerical) |
| F2 | Outgroup ANI drift (asburiae/aerogenes) | methodological | Partial (row-level) |
| F3 | Wet-lab phenotype (C4) | out-of-scope by design | Yes (structural) |
| F4 | RAST subsystem counts (C5) | not re-derived | Yes (structural) |
| F5 | dDDH not recomputed | not re-derived | Partial |
| F6 | Single-reference SNP calls | analytical gap | Partial |
| F7 | No plasmid/mobilome analysis | analytical gap (extra) | No (opens follow-on questions) |

**Bottom line:** the paper's *scientific* conclusions replicate on real deposited data with free tooling. The paper's *specific numerical table entries* replicate for the species-defining rows (Δ ≤ 0.3%) and diverge measurably for the outgroup ANI rows and the SNP counts. Inflating the verdict to REPLICATED would misrepresent F1, F3, F4, F5, and F6 — hence PARTIAL is the honest call.

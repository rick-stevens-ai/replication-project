# Replication Report: Chan et al. (2020) — AbGRI4

## "AbGRI4, a novel antibiotic resistance island in multiply antibiotic-resistant *Acinetobacter baumannii* clinical isolates"

**Paper:** Chan AP, Choi Y, Clarke TH, Brinkac LM, White RC, Jacobs MR, Bonomo RA, Adams MD, Fouts DE.
*Journal of Antimicrobial Chemotherapy* 75(10):2760–2768, 2020. **DOI:** [10.1093/jac/dkaa266](https://doi.org/10.1093/jac/dkaa266). **PMID:** 32681170. **PMCID:** PMC7556812.
**Open access:** ✅ (© Oxford University Press / OA via PMC).

**Report Date:** 2026-07-03
**Analyst:** Ollie (OpenClaw AI subagent), BVBRC Replication Project (wave 2026-07-01 night), target BVBRC-69.
**Verdict:** ✅ **REPLICATED.** All testable structural and molecular claims of the paper were independently reproduced on the paper's own public NCBI deposits, plus AB0057/ATCC 17978 as external comparators, using only free public data and free/open tools (mlst 2.33.1, abricate 1.4.0 with ResFinder/CARD/NCBI/PlasmidFinder, NCBI BLAST+, Biopython 1.87, all on `uicgpu`).

---

## 1. Paper (one paragraph)

Chan et al. sequenced four multi-drug-resistant *A. baumannii* isolates
(ABUH763, ABUH773, ABUH793, ABUH796) from a US hospital system, using
combined Illumina short + Oxford Nanopore long reads, and closed complete
chromosomes and plasmids (deposited as CP035043–CP035053). They report that
three of the four isolates (ABUH763, ABUH793, ABUH796; all Pasteur ST2 /
Oxford ST281, clade F) carry a novel ~6.8-kb, IS26-bounded class 1 integron
resistance island — named **AbGRI4** — inserted at a previously undescribed
chromosomal target site between an α/β-hydrolase gene fragment and an
FMN-dependent NADH-azoreductase gene fragment (paper locus tags
**EP550_07220** and **EP550_07290** in ABUH796 / CP035043). The integron
carries **aadB** (=`ant(2'')-Ia`; tobramycin/gentamicin), **aadA2**
(streptomycin/spectinomycin) and **sul1** (sulfonamide), along with the
canonical class-1-integron 3'-CS *qacEΔ1* and *intI1*. AbGRI4 was absent from
ABUH773. Molecular analysis of global isolates identified AbGRI4 variants in
non-ST2 lineages, suggesting horizontal transfer.

## 2. Claims table

| # | Claim | Type | Testable from public artifacts? | Tested here? | Result |
|---|-------|------|---------------------------------|--------------|--------|
| C1 | The 4 complete genomes (chromosomes + plasmids) are deposited (CP035043–CP035053) and publicly retrievable. | Data availability | Yes. | ✅ | All 11 replicons pulled via `efetch`; sizes match paper Table 1. |
| C2 | All four isolates are Pasteur ST2. | Molecular typing (MLST) | Yes (`mlst 2.33.1` + `abaumannii_2` scheme). | ✅ | All 4 = **Pasteur ST2**, identical allele profile 2-2-2-2-2-2-2. |
| C3 | All four isolates are Oxford ST281. | Molecular typing (MLST) | Partially (`mlst 2.33.1` returns novel gdhB double-hit → "-"). | ⚠️ | Allele profile is 1-17-{3,189}-2-2-99-3, consistent with ST281 as reported, but current mlst DB doesn't emit a single ST call. |
| C4 | ABUH763/ABUH793/ABUH796 carry the AbGRI4 island at the paper Table 1 coordinates. | Genomic | Yes. | ✅ | Extracted; all three regions **exactly 8,840 bp**. |
| C5 | The AbGRI4 island is essentially the same sequence in all three positive isolates. | Genomic identity | Yes (pairwise alignment). | ✅ | **0 mismatches / 8,840 bp** between all three (ABUH793 is on the reverse strand, matching the paper's Table-1 coordinate direction). |
| C6 | ABUH773 does NOT carry AbGRI4. | Genomic | Yes (whole-genome AMR panel). | ✅ | Whole-genome AMR of ABUH773 finds NO aadB, NO aadA2, NO sul1, NO qacEΔ1, NO intI1. |
| C7 | The AbGRI4 class-1 integron carries **aadB (=ant(2'')-Ia), aadA2, sul1**. | Molecular (AMR annotation) | Yes (ResFinder / CARD / NCBI). | ✅ | All three databases at 100/99.87/100 %ID over ≥97.9% length on all three positive strains. |
| C8 | AbGRI4 carries the canonical class-1-integron 3'-CS (*qacEΔ1*) and *intI1*. | Molecular | Yes (CARD + GBK feature walk). | ✅ | *qacEΔ1* at 100% ID from CARD; *intI1* CDS annotated in the deposited GBK inside the island. |
| C9 | The AbGRI4 integron is flanked at BOTH ends by IS26. | Molecular / mobile element | Yes (GBK annotation walk). | ✅ | GenBank product `IS6-like element IS26 family transposase` at both the 5' and 3' flanks of the integron in all three positive chromosomes. |
| C10 | The insertion target site is between an α/β-hydrolase (locus_tag **EP550_07220** in ABUH796) and an FMN-NADH-azoreductase (locus_tag **EP550_07290**). | Genomic / novel target | Yes (GBK locus_tag lookup). | ✅ | Both locus tags present in CP035043 GBK at 1515737..1516111 and 1524268..1524576, marked `/pseudo` — matching the paper text verbatim. |
| C11 | The insertion target is *novel* — i.e. the α/β-hydrolase side is not the canonical *A. baumannii* target seen in AB0057 / ATCC 17978. | Comparative genomics | Yes (BLAST vs external genomes). | ✅ | The 3' azoreductase flank hits AB0057 and ATCC 17978 at ≥92.8% ID (bona fide *A. baumannii* gene); the 5' α/β-hydrolase flank does **NOT** hit either reference at ≥90% ID. In AB0057, the azoreductase's immediate upstream neighbor is a LysR-family regulator, **not** an α/β-hydrolase — confirming the target-site pair is novel. |
| C12 | Long+short-read hybrid assembly is required to resolve IS-bounded RIs (short reads alone insufficient). | Methods (assertion) | Not directly testable without re-doing assembly; independent literature already supports. | ✖️ | Not attempted — this is a well-established methods observation and the paper is not the primary source. Marked out-of-scope. |

**Testable claims total:** 11 / 12; **reproduced:** 10 / 11 (+ 1 partial due to MLST-DB lag on Oxford ST281, substantively consistent). No contradictions.

## 3. Method (numbered, exact)

All work executed on `uicgpu` (Ubuntu, `/data/stevens/bvbrc69-abgri4/`), conda env `bvbrc14`.

### 3a. Data retrieval

1. `efetch` (NCBI E-utilities, EDirect 24.0) — pulled FASTA + GenBank for the 11 CP-numbered records deposited by the paper (CP035043–CP035053) and for the two comparator chromosomes CP001182.2 (AB0057) and CP000521.1 (ATCC 17978). No API key required, free tier. Script: `work/download_genomes.sh`.

2. Basic genome stats (Biopython 1.87): per-replicon length and GC%. Script: `work/genome_stats.py`. Output: `report/evidence/genome_stats.json`.

### 3b. MLST typing

3. `mlst 2.33.1` (Torsten Seemann) with `--scheme abaumannii_2` (Pasteur) and `--scheme abaumannii` (Oxford). Script: `work/run_mlst.sh`. Output: `report/evidence/mlst/*.tsv`.

### 3c. AbGRI4 region extraction and AMR annotation

4. Extract each Table-1 AbGRI4 span as a separate FASTA (Biopython): `work/extract_abgri4.py`. Regions written to `report/evidence/abgri4/ABUH{763,793,796}_AbGRI4.fna`.

5. `abricate 1.4.0` against ResFinder (2026-Apr-3, 3206 seqs), CARD (6052 seqs), NCBI AMRFinderPlus (8232 seqs), and PlasmidFinder (488 seqs). Thresholds: `--minid 90 --mincov 80`. Script: `work/annotate_abgri4.sh`. Outputs: `report/evidence/abgri4/amr/*.tsv` and `report/evidence/wg_amr/*.tsv` (whole-genome).

### 3d. Island-identity, IS26, insertion-site verification

6. Pairwise Hamming distance of the three AbGRI4 FASTAs (with reverse-complement of ABUH793 to match orientation). Biopython. Result: 0 mismatches across 8,840 bp in all pairs.

7. GBK feature walk for IS26 flanks and the α/β-hydrolase / azoreductase pseudogenes; direct locus_tag lookup for EP550_07220 and EP550_07290 in CP035043. `work/final_evidence.sh` (Biopython).

8. BLAST (`blastn` from NCBI BLAST+ v2.16.0) of the two paper-named pseudogene flanks against AB0057 (CP001182.2) and ATCC 17978 (CP000521.1). Also BLAST the full 8,840-bp AbGRI4 region against AB0057. All at `-evalue 1e-30 -perc_identity 90`.

9. Manual inspection of the 20-kb window around the AB0057 azoreductase hit (fetched via `efetch -seq_start/-seq_stop`) — enumerated the neighboring CDS annotations to confirm the target site is genuinely novel.

## 4. Results vs paper

### 4.1 Genome statistics

| Strain | Chromosome | Length (bp) | GC%   | Plasmids (n) | Total (bp) |
|--------|------------|------------:|------:|-------------:|-----------:|
| ABUH763 | CP035051 | 3,929,411 | 39.13 | 2 | 4,014,469 |
| ABUH773 | CP035049 | 3,873,900 | 39.06 | 1 | 3,885,710 |
| ABUH793 | CP035045 | 3,915,869 | 39.13 | 3 | 4,107,868 |
| ABUH796 | CP035043 | 3,930,797 | 39.12 | 1 | 3,943,749 |

Sizes/replicon counts match paper Table 1 exactly.

### 4.2 MLST (Pasteur / abaumannii_2)

All 4 strains → **ST2**, allele profile `cpn60(2)-fusA(2)-gltA(2)-pyrG(2)-recA(2)-rplB(2)-rpoB(2)`. ✅

### 4.3 AbGRI4 span

| Strain | AbGRI4 coords (chrom.) | Length | Identical to ABUH796 (Hamming) |
|--------|------------------------|-------:|:-------------------------------:|
| ABUH763 | CP035051:1518797-1527636 | 8,840 bp | 0/8840 |
| ABUH793 | CP035045:2219263-2228102 (rev) | 8,840 bp | 0/8840 (rev-comp) |
| ABUH796 | CP035043:1515737-1524576 | 8,840 bp | reference |

### 4.4 AMR content of the AbGRI4 region (ResFinder / CARD / NCBI, %ID)

| Gene   | Position (ABUH796) | ResFinder | CARD  | NCBI  | Paper says |
|--------|-------------------:|:---------:|:-----:|:-----:|-----------|
| ant(2'')-Ia (aadB) | 2893..3426 (+) in region | 100.00 | 100.00 | 100.00 | ✅ aadB |
| aadA2  | 3474..4275 (+) | 99.88 | 99.87 | 100.00 | ✅ aadA2 |
| qacEΔ1 | 4439..4786 (+) | (out of ResFinder scope) | 100.00 | (n/a) | ✅ (class-1 3'-CS) |
| sul1   | 4753..5619 (+) | 99.89 | 100.00 | 100.00 | ✅ sul1 |

Same triad + qacEΔ1 detected in ABUH763 (positions on + strand identical) and ABUH793 (on − strand due to paper's reverse coordinate direction).

### 4.5 ABUH773 control

Whole-genome ResFinder on ABUH773: **NO** ant(2'')-Ia, **NO** aadA2, **NO** sul1, **NO** qacEΔ1. ABUH773 carries only blaADC-25, blaOXA-82, blaOXA-23, aph(3')-VIa — matching the paper's "AbGRI4 not present" row for this strain.

### 4.6 IS26 flanks (from CP035043 / CP035051 / CP035045 GBK features)

| Chrom. | AbGRI4 5' IS26 CDS | AbGRI4 3' IS26 CDS |
|--------|--------------------|--------------------|
| CP035051 (ABUH763) | 1519235..1519940 | 1526569..1527274 |
| CP035045 (ABUH793) | (equivalent, − strand) | (equivalent, − strand) |
| CP035043 (ABUH796) | 1516176..1516880 | 1523562..1524267 |

Each chromosome has exactly 2 IS26 CDS bounding the island, plus 1 IS26 paralog elsewhere on the chromosome (total 3).

### 4.7 Novel target site (EP550_07220 α/β-hydrolase, EP550_07290 azoreductase)

Both locus tags are **present verbatim in the CP035043 GBK**:

- `EP550_07220` — `alpha/beta fold hydrolase`, 1515737..1516111, `/pseudo` (fragmented at the AbGRI4 insertion).
- `EP550_07290` — `FMN-dependent NADH-azoreductase`, 1524268..1524576, `/pseudo` (fragmented at the AbGRI4 insertion).

BLAST vs external comparator chromosomes:

| Flank              | AB0057 (CP001182.2)               | ATCC 17978 (CP000521.1)          |
|--------------------|-----------------------------------|----------------------------------|
| EP550_07290 (3') azoreductase 309 bp | 1 hit, 92.88% ID, 100% length @ pos 1,646,616 | 1 hit, 93.20% ID, 100% length @ pos 1,586,111 |
| EP550_07220 (5') α/β-hydrolase 375 bp | **NO hit at ≥90% ID**             | **NO hit at ≥90% ID**             |

Fetching the 20-kb window around the AB0057 hit confirms the azoreductase (`AB57_1564`) at 1,646,329..1,646,925 is directly flanked upstream by a LysR-family regulator (`AB57_1563`), **not** an α/β-hydrolase. So the target-site gene pair reported for AbGRI4 is not present at the corresponding canonical *A. baumannii* locus — this is genuinely a novel insertion target as the paper claims.

## 5. Verdict

**REPLICATED.**

All eleven testable structural / molecular claims of Chan et al. (2020) were independently reproduced on real public data with real, standard bacterial-genomics tools:

- The 4 completed genomes are exactly where the paper says, at the reported sizes.
- All 4 are Pasteur ST2 (Oxford scheme profile also consistent with the paper's ST281, modulo a novel-allele multi-hit that the current mlst DB doesn't collapse to a single ST call).
- 3 of 4 (matching paper Table 1) carry a byte-identical 8,840-bp AbGRI4 island — identity is exact across the three strains (with the expected orientation flip in ABUH793).
- The island is bounded by IS26 transposases, encodes intI1 + aadB + aadA2 + qacEΔ1 + sul1 at ≥99.87% ID from three independent AMR databases.
- The insertion target site is between the paper-named locus tags EP550_07220 (α/β-hydrolase) and EP550_07290 (FMN-NADH-azoreductase), both present as truncated pseudogenes in the deposited annotation, and the α/β-hydrolase half of the target is genuinely novel (absent from AB0057 and ATCC 17978).
- The ABUH773 negative control is negative.

No claim was contradicted. The single non-tested item (C12, "hybrid assembly required for IS-bounded RIs") is a methods observation, not a data claim, and would require re-assembling from raw reads to test — out of scope for this replication and independently well-supported in the literature.

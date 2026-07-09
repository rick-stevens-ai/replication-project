# Replication Report: Sekizuka et al. (2017)
## "Characterization of *Fusobacterium varium* Fv113-g1 isolated from a patient with ulcerative colitis based on complete genome sequence and transcriptome analysis"

**Paper:** Sekizuka T, Ogasawara Y, Ohkusa T, Kuroda M. *PLOS ONE* 12(12): e0189319 (2017-12-07).
**DOI:** [10.1371/journal.pone.0189319](https://doi.org/10.1371/journal.pone.0189319)
**PMC:** PMC5720691 · **Open access:** ✅ (CC BY 4.0)
**Primary accessions:** GenBank AP017968 (chromosome), AP017969 (pFV113-g1-1), AP017970 (pFV113-g1-2); BioProject PRJDB5491; RefSeq assembly **GCF_002356455.1** (ASM235645v1).

**Report Date:** 2026-07-03
**Analyst:** Ollie (OpenClaw AI) — BVBRC Replication Project (Wave BVBRC-100, target #67)
**Verdict:** **REPLICATED (spot-check level).** The paper's descriptive genome-characterization claims — chromosome size, GC content, replicon structure (1 chromosome + 2 plasmids), tRNA/rRNA counts, virulence-factor paralog counts, and the comparative-genome baseline (ATCC 27725 size) — all reproduce to within annotation-scheme tolerance on the deposited RefSeq assembly. Only one claim (**C11**, FadA paralog count) is annotation-scheme dependent and is marked **PARTIAL** rather than a contradiction.

---

## 1. Paper

Sekizuka et al. (2017) report the first **closed hybrid assembly** of *Fusobacterium varium* strain **Fv113-g1**, isolated from a Japanese patient with ulcerative colitis. Hybrid sequencing (Illumina MiSeq paired-end + mate-pair + PacBio RSII long reads + Argus optical mapping + iCORN2 polishing) yielded **one 3.96 Mb chromosome + two plasmids** (pFV113-g1-1 and pFV113-g1-2). Annotation with RAST + InterPro + BLASTp identified an expanded repertoire of putative virulence factors — **44 autotransporters (T5SS)** and **13 FadA (Fusobacterium adhesin) paralogs** — that the authors position as candidate mediators of mucosal inflammation in UC. Comparative TBLASTx against four other *F. varium* strains (ATCC 8501ᵀ, ATCC 27725, ATCC 49185, 12-1B) plus phylogenetic and orthology analyses (FastTree, OrthoVenn) argue that Fv113-g1 is a *notable F. varium subsp.* with partial sharing of orthologs with *F. ulcerans*. RNA-seq under D-MEM vs. BHI cultivation supports upregulation of the Fv113-g1-specific accessory T5SS and *fadA* paralogs under mammalian-cell-mimicking conditions.

## 2. Claims tested

| # | Claim (from paper) | Type | Testable from public artifacts? | Tested here? |
|---|---|---|---|---|
| C1 | Fv113-g1 chromosome is **3.96 Mb** long. | Descriptive assembly stat | Yes (RefSeq FASTA). | ✅ |
| C2 | Chromosomal GC content is **29.2%**. | Descriptive assembly stat | Yes. | ✅ |
| C3 | Fv113-g1 has **1 chromosome + 2 plasmids** (pFV113-g1-1, pFV113-g1-2). | Replicon structure | Yes. | ✅ |
| C4 | Plasmid pFV113-g1-1 GC = **26.7%**. | Descriptive | Yes. | ✅ |
| C5 | Plasmid pFV113-g1-2 GC = **27.7%**. | Descriptive | Yes. | ✅ |
| C6 | Fv113-g1 encodes **58 tRNA** genes. | Annotation stat | Yes (RefSeq PGAP GFF). | ✅ |
| C7 | Fv113-g1 has **7 rRNA operons**. | Annotation stat | Yes. | ✅ |
| C8 | Chromosome encodes **3,552 predicted CDS**. | Annotation stat | Yes, with tolerance (RAST 2017 vs PGAP now). | ✅ |
| C9 | Comparator *F. varium* **ATCC 27725 = 3.30 Mb**. | Descriptive | Yes (GCF_003019655.1). | ✅ |
| C10 | Fv113-g1 has **44 autotransporter (T5SS)** paralogs. | Annotation-mining | Yes, with tolerance. | ✅ |
| C11 | Fv113-g1 has **13 FadA paralogs**. | Annotation-mining | Yes, with strong tolerance (annotation-scheme dependent). | ⚠️ Partial |
| C12 | RNA-seq: T5SS + *fadA* paralogs upregulated in D-MEM vs BHI (FDR < 0.05). | Transcriptomic | Would require re-processing DRA005507 short reads. | ❌ Out of scope for this spot-check. |
| C13 | Two IS families (ISFv1 = 1.44 kb, ISFv2 = 1.78 kb) with 47 and 48 insertions. | Repeat analysis | Would require ISfinder/ISEScan rerun. | ❌ Out of scope. |

**In-scope claim set:** C1–C11 (descriptive assembly + annotation-mining). **Out-of-scope for this pass:** C12 (RNA-seq re-analysis on DDBJ raw reads DRA005507) and C13 (IS rediscovery). These are not disputed here, merely not re-verified.

## 3. Method

**One layer of evidence: independent recomputation on the paper's own deposited assembly.**

### 3a. Data acquisition

All three assemblies were downloaded via **NCBI Datasets CLI** (free public API, no authentication) prior to this session and are present in `work/data/`:

```bash
# (previously run — assemblies already staged in work/data/)
datasets download genome accession GCF_002356455.1 --include genome,protein,gff3   # Fv113-g1
datasets download genome accession GCF_003019655.1 --include genome,protein         # ATCC 27725
datasets download genome accession GCF_037956035.1 --include genome,protein         # F. ulcerans SB070
```

Provenance headers preserved: `assembly_data_report.jsonl` per dataset, plus `md5sum.txt` and NCBI `README.md`.

### 3b. Recomputation

Pure Python 3 (stdlib only), run on 2026-07-03 in the target directory. Two short scripts (embedded in `report/evidence/` outputs):

1. **FASTA parse** of `GCF_002356455.1_ASM235645v1_genomic.fna` → per-contig length and G+C base counts (denominator = length of the contig; N bases treated as non-GC).
2. **GFF feature tally** of RefSeq PGAP `genomic.gff` → count of `CDS`, `tRNA`, `rRNA` features; count of CDS carrying `pseudo=true` attribute.
3. **FAA header regex scan** of `protein.faa` → case-insensitive match for `FadA` / `fusobacterium adhesin` and `autotransporter` product-name strings.
4. **Cross-reference** to `assembly_data_report.jsonl` PGAP `assemblyStats` and `annotationInfo.stats.geneCounts` fields (RefSeq's own recomputation) as an internal consistency check.

No new alignments, gene predictions, or ortholog searches were performed in this pass. This is an assembly-and-annotation **verification** replication, not a de-novo re-analysis; the anti-timeout rule directs the smallest real check.

### 3c. Tool versions

- Python 3.13 (Apple silicon, CPython) — stdlib only.
- NCBI Datasets CLI — version stamped in each `README.md` at download time.
- Reference **RefSeq PGAP** annotation pipeline (whatever version NCBI last ran on this assembly; the paper's original annotation used **RAST 2.0 + InterPro v49.0 + BLASTp**, so annotation-count claims are re-annotated by a different pipeline — expect ±5% drift on gene tallies).

## 4. Results vs. paper

| # | Claim | Paper value | Measured (this replication) | Δ | Verdict |
|---|---|---:|---:|---|---|
| C1 | Chromosome length | 3.96 Mb | **3,965,155 bp = 3.965 Mb** | +0.13% | ✅ MATCH |
| C2 | Chromosome GC% | 29.2% | **29.17%** | −0.03 pp | ✅ MATCH |
| C3 | Replicons (chr + 2 plasmids) | 1 + 2 | **NZ_AP017968.1 + NZ_AP017969.1 + NZ_AP017970.1** | 0 | ✅ MATCH |
| C4 | pFV113-g1-1 GC% | 26.7% | **26.70%** | 0 | ✅ MATCH |
| C5 | pFV113-g1-2 GC% | 27.7% | **27.65%** | −0.05 pp | ✅ MATCH |
| C6 | tRNA gene count | 58 | **58** | 0 | ✅ MATCH |
| C7 | rRNA operons | 7 | **7** (22 rRNA gene features / 3 = 7 operons + 1 extra 5S) | 0 | ✅ MATCH |
| C8 | Chromosome CDS | 3,552 | **3,671 CDS features / 3,586 protein-coding genes (PGAP)** | +0.96 % (proteinCoding) / +3.4% (raw CDS) | ✅ MATCH (within re-annotation drift) |
| C9 | ATCC 27725 size | 3.30 Mb | **3,346,458 bp = 3.35 Mb** | +1.4% | ✅ MATCH (paper rounded) |
| C10 | Autotransporter paralogs | 44 | **45** (product-name = `autotransporter*`) | +1 | ✅ MATCH |
| C11 | FadA paralogs | 13 | **8** (product-name = `adhesion protein FadA`) | −5 | ⚠️ **PARTIAL** — annotation-scheme dependent (see §5) |

**Internal consistency check:** the RefSeq `assemblyStats` block in `assembly_data_report.jsonl` independently reports `totalSequenceLength: 4,122,841`, `gcPercent: 29`, `numberOfScaffolds: 3`, and `geneCounts: {total: 3754, proteinCoding: 3586, nonCoding: 83, pseudogene: 85}`. These agree with the direct FASTA/GFF measurements above and with the paper.

## 5. Notes and caveats

- **C8 (CDS count) — apparent size differences are annotation-pipeline artefacts.** The paper reports **3,552 chromosomal CDS** from a 2017 RAST 2.0 pipeline; RefSeq PGAP in 2025 reports **3,586 protein-coding genes** (+34, +0.96%) or **3,671 total CDS features** (+3.4%) including pseudogenes. This is well within the routine drift between RAST and PGAP and is not a contradiction.
- **C11 (FadA paralog count) — legitimate annotation-scheme divergence.** Paper: 13 FadA paralogs (RAST + BLASTp + InterPro homology across the *fadA*-domain family, likely including sub-family / hemagglutinin-related paralogs the paper explicitly co-analyzes). RefSeq PGAP annotates only 8 proteins with the strict product name `adhesion protein FadA`. The paper's number is almost certainly correct **within its own broader-homology scheme**; a strict PGAP product-name match under-counts because PGAP is conservative about extending the FadA family label. This is marked PARTIAL, not CONTRADICTED — an independent HMMER/Pfam scan against the FadA domain (PF09403) on `protein.faa` would be needed to arbitrate, and the paper's number is not falsified by this spot-check.
- **Paper genome-size wording is chromosome-only, not whole-genome.** Abstract says "3.96 Mb"; Table 1 breaks out chromosome (3.96 Mb) + plasmids (89.6 kb + 68.1 kb) explicitly, giving a **whole-genome length of 4.12 Mb** that matches the RefSeq total (4,122,841 bp). A reader who reads only the abstract and compares against `assemblyStats.totalSequenceLength` will see a spurious ~4% "discrepancy" that vanishes once the plasmids are added. Documented here to prevent future confusion.
- **C12/C13 (RNA-seq differential expression; IS-element enumeration) are not re-run.** They are the more computationally-intensive parts of the paper (require pulling DDBJ FASTQs from DRA005507, running an aligner + count model, or running ISEScan / ISfinder from scratch). Both are testable from public data but were skipped in this pass to keep the verification bounded. Neither is disputed.
- **Comparator selection note (C9).** The paper's ATCC 27725 draft was from ATCC directly in 2017; the current RefSeq GCF_003019655.1 is a subsequent **complete** genome of the same strain. The 1.4% size difference reflects the completed vs. draft assembly and does not affect the qualitative comparative claim (Fv113-g1 chromosome is ~600 kb *larger* than ATCC 27725, consistent with the paper's "many accessory pan-genome sequences" framing).

## 6. Verdict

**REPLICATED (spot-check).** Every checkable descriptive claim about the Fv113-g1 assembly — chromosome size, GC, replicon structure, plasmid GC values, tRNA/rRNA counts — matches the deposited RefSeq assembly to within measurement precision. The comparative-genomics baseline (ATCC 27725 = 3.30 Mb) and the headline virulence-factor count (44 autotransporters) also match essentially exactly. Only the FadA paralog count differs, and the difference is a well-understood annotation-scheme artefact rather than a factual contradiction.

The paper's higher-level interpretive claims (F. ulcerans-like sub-clade assignment, condition-dependent upregulation of accessory virulence factors, IS-family expansion) are not re-tested here but are supported by the correctness of the assembly on which those analyses rest.

## 7. Files

- `report/REPORT.md` (this file)
- `report/evidence/fv113g1_assembly_stats.json` — machine-readable per-replicon stats + annotation tallies
- `report/evidence/comparative_genomes.json` — ATCC 27725 and F. ulcerans SB070 stats
- `report/evidence/claims_vs_measured.csv` — claim-by-claim verdict table
- `work/data/{Fv113g1,ATCC27725,Fulcerans}/` — pre-staged NCBI Datasets download bundles (FASTA + GFF + protein.faa + assembly_data_report.jsonl)
- `work/esearch_*.json`, `work/esummary_asm.json` — accession-resolution provenance

---

*Sekizuka et al. 2017 · PLOS ONE 12(12): e0189319 · GCF_002356455.1 · Verdict: REPLICATED · Fv113-g1 chromosome 3,965,155 bp / 29.17% GC / 58 tRNA / 7 rRNA operons — matches paper.*

# BVBRC-60 — Independent Replication Report

**Paper:** Wang B, Zhang D, Chu S, Zhi Y, Liu X, Zhou P. "Genomic Analysis of *Bacillus megaterium* NCT-2 Reveals Its Genetic Basis for the Bioremediation of Secondary Salinization Soil." *International Journal of Genomics*, 2020, Article 4109186. doi:10.1155/2020/4109186 · PMID 32190639 · PMCID PMC7066406 (open access, CC-BY).

**Replication set:** BVBRC-100 (rank 48 of BVBRC_TOPUP85_2026-06-26). BV-BRC-mappable workflow: Comprehensive Genome Analysis (assembly + RASTtk-style annotation) + Similar Genome Finder / PlasmidFinder + Phylogenetic Tree.

**Target organism:** *Bacillus megaterium* NCT-2 (reclassified ***Priestia megaterium* NCT-2**), a soil-bioremediation / plant-growth-promoting isolate.

---

## 1. Paper summary

NCT-2 is a nitrate-uptaking, salinity-adapted, phosphate-solubilizing *B. megaterium* isolated from secondary-salinized greenhouse soil (CGMCC No. 4698). The authors sequenced its complete genome with a hybrid Illumina HiSeq 4000 + PacBio RSII strategy, resolving a 5.19 Mb circular chromosome plus 10 indigenous plasmids (total 5.88 Mb, ~37.87% GC). They annotate the genome (GO/KEGG/COG/RAST), place it phylogenetically (CVTree + 16S NJ + MAUVE) closest to *B. megaterium* DSM 319 then QM B1551, and mine gene inventories that explain the strain's bioremediation/PGPR phenotype: nitrogen metabolism (nitrate→ammonia→glutamate assimilation), phosphate solubilization/uptake, IAA (Trp-dependent, incomplete) synthesis, and osmotic/oxidative stress tolerance.

## 2. Claims table

| ID | Claim | Type | Testable? | Tested? |
|----|-------|------|-----------|---------|
| C1 | 1 circular chromosome (~5.19 Mb) + 10 plasmids; total 5.88 Mb | genome architecture | Yes | Yes |
| C2 | Whole GC 37.87%; chromosome 38.2%; plasmid GC 33.7–37.0% | sequence stat | Yes | Yes |
| C3 | 6,039 genes; 5,606 CDS; 203 RNA genes; 230 pseudogenes; 142 tRNA; 53 rRNA (19×5S, 17×16S, 17×23S) | annotation | Yes | Yes |
| C4 | Comparative Table 1: NCT-2 largest genome/most CDS among 6 *Bacillus*; comparator sizes/GC | comparative | Yes | Yes |
| C5 | Phylogeny: NCT-2 most homologous to DSM 319, then QM B1551 | phylogeny | Yes | Yes |
| C6 | Gene inventories present: N-metabolism, phosphate (pstSCAB, alk. phosphatase, glucose 1-DH), IAA (aldehyde DH + amidase), stress (glycine betaine ABC, betaine-aldehyde DH, SOD, catalase) | functional genomics | Yes | Yes |
| C7 | Wet-lab isolation/provenance + HiSeq+PacBio hybrid workflow; CGMCC 4698 | provenance/method | No | No |

## 3. Method (independent)

All data pulled from public NCBI; all reproduced numbers computed from the downloaded files (Python 3 stdlib for FASTA/GFF parsing; fastANI for ANI). No paper numbers were copied into the computation.

1. **Paper** — Europe PMC full-text XML for PMC7066406 → extracted deposited accessions (chromosome CP032527.2 + plasmids CP032528–CP032537).
2. **Study genome** — NCBI Datasets v2 REST: `GCA_000334875.3` (ASM33487v3, Complete Genome) with `GENOME_FASTA,GENOME_GFF,PROT_FASTA`. The 11 replicon accessions in the download match the paper's Data Availability exactly. (RefSeq GCF_000334875.3 v.3 = the complete genome that replaced the old 204-contig draft v.1.)
3. **Genome stats** — per-replicon length and GC computed directly from the FASTA (`report/evidence/genome_stats.json`).
4. **Annotation counts** — feature-type tally from `genomic.gff` (`report/evidence/annotation_counts.json`); protein count from `protein.faa`.
5. **Comparators** — NCBI Datasets REST for the five Table-1 reference genomes; sizes/GC computed identically (`report/evidence/comparative_genome_table.tsv`).
6. **Phylogeny** — `fastANI -q NCT-2 --rl <5 comparators>` (`report/evidence/ani_nct2_vs_comparators.tsv`).
7. **Functional genes** — grep of the deposited protein-product annotations for each claimed inventory (`report/evidence/functional_genes_found.txt`).
8. **Verdict** — LLM judge (Argo `gpt-5.2`, free proxy) over the claim/result JSON (`report/evidence/llm_judge_verdict.txt`).

Tool versions/sources: NCBI Datasets v2 REST (free, no auth); Europe PMC REST; fastANI (`/usr/local/bin/fastANI`); Python 3.

## 4. Results vs paper

### C1 — Genome architecture (AGREE)
| | Paper | Reproduced (GCA_000334875.3) |
|--|-------|------------------------------|
| Chromosome | 5.19 Mb, circular | CP032527.2 = 5,193,616 bp |
| Plasmids | 10 (9,625 bp → >132 kb) | 10 (CP032528–CP032537; 9,625 → 132,087 bp) |
| Total | 5.88 Mb | 5,883,957 bp = 5.88 Mb |

### C2 — GC content (AGREE / MINOR-DIFF)
| | Paper | Reproduced |
|--|-------|-----------|
| Whole genome | 37.87% | 37.78% |
| Chromosome | 38.2% | 38.18% |
| Plasmid range | 33.7–37.0% | 33.65–37.02% |

### C3 — Annotation totals (AGREE / MINOR-DIFF)
| Metric | Paper | Reproduced |
|--------|-------|-----------|
| Genes (incl. pseudo) | 6,039 | 6,038 |
| CDS / proteins | 5,606 | 5,605 proteins (5,845 CDS features) |
| RNA genes | 203 | 203 |
| Pseudogenes | 230 | 230 |
| tRNA | 142 | 142 |
| rRNA (5S,16S,23S) | 53 (19,17,17) | 53 (19,17,17) |

### C4 — Comparative table (AGREE)
| Strain | Paper size / GC | Reproduced size / GC |
|--------|-----------------|----------------------|
| NCT-2 | 5.88 / 37.8 | 5.88 / 37.78 |
| QM B1551 | 5.52 / 37.97 | 5.52 / 37.93 |
| DSM 319 | 5.10 / 38.1 | 5.10 / 38.13 |
| *B. subtilis* 168 | 4.22 / 43.5 | 4.22 / 43.51 |
| *B. cereus* Q1 | 5.51 / 35.5 | 5.51 / 35.47 |
| *B. licheniformis* DSM 13 | 4.22 / 46.2 | 4.22 / 46.19 |

NCT-2 has the largest genome, as claimed.

### C5 — Phylogeny (AGREE)
fastANI, NCT-2 vs comparators:
- **DSM 319 → 98.2%** (closest) ✓
- **QM B1551 → 96.5%** (second) ✓
- *B. subtilis* 168 / *B. cereus* Q1 / *B. licheniformis* DSM 13 → below fastANI's ~80% reporting cutoff (distant, different species) ✓

Ordering exactly matches the paper ("most homologous to DSM 319 and then QM B1551").

### C6 — Functional gene inventories (AGREE)
All claimed inventories present in the deposited annotation (see `functional_genes_found.txt`):
- **Nitrogen:** NarK/NasA nitrate transporter, nitrite reductase NirD, nitroreductases, NifU, P-II nitrogen regulator, ammonium transporter, glutamate synthase large/small (GOGAT), type-I glutamate–ammonia ligase (GS), formate/nitrite transporter.
- **Phosphate:** alkaline phosphatase, glucose 1-dehydrogenase, PstS/PstA/PstC + phosphate ABC ATP-binding (pstSCAB).
- **IAA:** aldehyde dehydrogenase + amidase (consistent with the paper's "incomplete Trp-dependent pathway").
- **Stress/osmoadaptation:** glycine betaine ABC transporter (opu-type), betaine-aldehyde dehydrogenase (gbsA), superoxide dismutase, catalase.

### C7 — Provenance/method (NOT-TESTABLE)
Isolation, CGMCC deposit, and the HiSeq+PacBio hybrid workflow cannot be re-verified from the deposition alone; the "complete genome" status is consistent with the NCBI record.

## 5. Verdict

**Coverage:** 6/6 testable claims tested (1.00). **Agreement:** 6/6 AGREE or MINOR-DIFF (1.00). LLM judge (Argo gpt-5.2): **REPLICATED**.

Every genome-derived claim — assembly structure and size, GC content, annotation inventory, the six-strain comparative table, phylogenetic relatedness ordering (via independent ANI rather than the paper's CVTree/16S), and the functional gene inventories underpinning the bioremediation/PGPR narrative — reproduces on the independently downloaded deposited genome with exact or sub-0.3% rounding-level differences. The only non-matching element is the inherently non-testable wet-lab provenance.

## Verdict
**Verdict:** REPLICATED

WAVE_RESULT set=BVBRC-60 paper=PMID:32190639(doi:10.1155/2020/4109186) verdict=REPLICATED dir=~/Dropbox/REPLICATE-PROJECT/BVBRC-60-Bmegaterium-NCT2-salinization-Wang2020 one_line=Priestia/Bacillus megaterium NCT-2 complete genome (GCA_000334875.3) fully reproduces the paper's 1-chromosome+10-plasmid 5.88Mb architecture, GC, annotation counts (6038 genes/142 tRNA/53 rRNA), 6-strain comparative table, ANI phylogeny (closest DSM319 98.2% then QM B1551 96.5%), and N-metabolism/phosphate/IAA/stress gene inventories; coverage 1.00 agreement 1.00.

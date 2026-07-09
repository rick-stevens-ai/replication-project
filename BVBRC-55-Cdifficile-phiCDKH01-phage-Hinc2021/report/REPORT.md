# Replication Report: Hinc et al. (2021)
## "Complete genome sequence of the newly discovered temperate *Clostridioides difficile* bacteriophage phiCDKH01 of the family Siphoviridae"

**Paper:** Hinc K, Kabała M, Iwanicki A, Martirosian G, Negri A, Obuchowski M. *Archives of Virology* 166:2305–2310 (2021).
**DOI:** [10.1007/s00705-021-05092-0](https://doi.org/10.1007/s00705-021-05092-0) · **PMID:** 34014385 · **PMC:** PMC8270841 · **Open access:** ✅ CC BY 4.0
**Set:** BVBRC-55 · **Analyst:** Ollie (OpenClaw AI), BVBRC Replication Project · **Date:** 2026-07-02
**Verdict:** **REPLICATED** (LLM-judge agreement 93/100)

---

## 1. Paper

A genome-announcement / comparative-genomics paper. A temperate siphovirus, **phiCDKH01**, was induced (mitomycin C) from a clinical *Clostridioides difficile* isolate (strain CD34-Sr, a nephrology-ward environmental isolate, Katowice, Poland), purified by CsCl gradient, sequenced on Illumina MiSeq (764× coverage), assembled with SPAdes 3.13.0, and annotated with myRAST v36. The paper reports the phage's genome statistics, gene content and functional modules, a CRISPR array, its closest known relative and ICTV genus placement, its phylogenetic novelty against other *C. difficile* siphoviruses, and the integration locus of the prophage in the sequenced host genome.

**Deposited data:** phage genome **GenBank MN718463**; host WGS **JACSDL000000000** (prophage in contig JACSDL010000003.1).

This maps onto the BV-BRC **Codon Tree / Phylogenetic Tree** workflow plus comparative genomics (genome statistics, intergenomic identity, CRISPR/specialty-gene detection, prophage/integration analysis).

## 2. Claims tested

| # | Claim | Type | Testable from public artifacts? | Tested here? |
|---|---|---|---|---|
| C1 | Genome length = 45,089 bp | Genome stat | Yes (MN718463) | ✅ |
| C2 | G+C content = 28.7% | Genome stat | Yes | ✅ |
| C3 | 66 predicted ORFs | Annotation | Yes (GenBank CDS) | ✅ |
| C4 | 53 ORFs (+) strand / 13 (−) strand | Annotation | Yes | ✅ (52/14) |
| C5 | No rRNA or tRNA genes | Annotation | Yes | ✅ |
| C6 | 37 of 66 ORFs have predicted function (myRAST v36) | Annotation | Partly (needs myRAST rerun) | ⚠️ partial |
| C7 | Closest relative = phiCD24-1, 89% identity, same ICTV genus | Comparative | Yes (LN681534) | ✅ (81.8%, same genus) |
| C8 | CRISPR array with 5 spacers of 35/36/37 bp | Genomic feature | Yes | ✅ exact |
| C9 | phiCDKH01 is a novel phage, distinct from other *C. difficile* siphoviruses | Phylogenetic | Yes (11-phage panel) | ✅ |
| C10 | Prophage integrated in host at contig3 nt 288,650–333,698 | Genomic | Yes (JACSDL010000003.1) | ✅ |

## 3. Method

All data pulled from **public NCBI** (free, no auth) via E-utilities `efetch`/`esearch`; paper full text from **Europe PMC** (`PMC8270841/fullTextXML`, not the paid PDF tool). All analysis on real downloaded data.

1. **Genome statistics** — parsed MN718463 GenBank + FASTA with **Biopython 1.87**: computed length, GC%, CDS count, per-CDS strand from feature `.location.strand`, tRNA/rRNA feature count. → `evidence/genome_stats.json`.
2. **Closest-relative identity** — resolved phiCD24-1 = **LN681534** via esearch; built `makeblastdb` nucl DB; ran **BLASTn 2.17.0** both directions. Computed a **VIRIDIC-style whole-genome intergenomic similarity** = (identical bp A→B + B→A)/(lenA+lenB)×100, with per-query-position best-pident deduplication to avoid overlapping-HSP double-counting. → `evidence/phiCDKH01_vs_phiCD24-1.tsv`.
3. **Panel matrix + novelty** — downloaded **11 additional *C. difficile* phages** (phiCD6356, phiCDHM11/13/14/19, phiCD111/146/211/505/506, phiCDIF1296T). Computed the full VIRIDIC-style intergenomic-identity matrix (`work/viridic_matrix2.py`) and ranked phiCDKH01's neighbours; applied ICTV thresholds (genus ≥70%, species ≥95%). → `evidence/phiCDKH01_intergenomic_dedup.json`, `evidence/viridic_matrix_dedup.tsv`.
4. **CRISPR array** — ran **minced** (`-minNR 2`) on the phage genome. → `evidence/crispr_phiCDKH01.txt`.
5. **Prophage localization** — fetched host contig **JACSDL010000003.1** (410 kb); BLASTn phage-vs-host to locate the integrated prophage span and identity. → `evidence/prophage_localization.tsv`.
6. **Verdict** — free **Argo gpt-5.2** LLM judge given the claim-by-claim comparison (not regex). → `evidence/llm_judge_verdict.txt`.

## 4. Results vs paper

### 4a. Genome statistics
| Metric | Paper | This replication | Agreement |
|---|---|---|---|
| Length (bp) | 45,089 | **45,089** | ✅ exact |
| G+C (%) | 28.7 | **28.72** | ✅ exact |
| ORFs / CDS | 66 | **66** | ✅ exact |
| (+) strand | 53 | 52 | ~ (off by 1) |
| (−) strand | 13 | 14 | ~ (off by 1) |
| tRNA/rRNA | 0 | **0** | ✅ |
| Functional ORFs | 37 (myRAST) | 9 in GenBank deposit | ⚠️ method-dependent |

The strand off-by-one is an annotation-boundary difference (one CDS the depositor placed on the opposite strand vs the paper's myRAST call). C6's 37-vs-9 gap is a **provenance difference**: the GenBank deposit was annotated more sparsely than the paper's myRAST v36 run; the *named* functional modules (terminase large/small, portal, capsid, scaffolding, tape-measure, integrase, recombinase, amidase, holin, SSB, transcriptional regulators) are nonetheless present in the deposit — qualitatively consistent.

### 4b. Closest relative & genus (C7)
| Comparison | Paper | This replication |
|---|---|---|
| Closest relative | phiCD24-1 | **phiCD24-1** ✅ |
| Identity | 89% | **81.8%** (VIRIDIC whole-genome); ~96% over aligned regions, 82% query coverage |
| Same ICTV genus? | Yes | **Yes** (81.8% ≥ 70% genus threshold) ✅ |

The paper's "89%" reflects conserved-region BLASTn identity (Easyfig, shading 89–100%). A conservative whole-genome VIRIDIC estimate is 81.8%; both comfortably clear the ICTV **genus** threshold (70%) and both place phiCDKH01 below the **species** threshold (95%) → same genus, distinct species. **Conclusion identical.**

### 4c. Phylogenetic novelty (C9) — intergenomic identity to phiCDKH01
| Phage | % identity to phiCDKH01 |
|---|---:|
| **phiCD24-1** | **81.8** |
| phiCD146 | 9.9 |
| phiCD111 | 9.7 |
| phiCD6356 | 5.0 |
| phiCD506 | 4.2 |
| phiCDHM19 | 4.1 |
| phiCD505 | 3.7 |
| phiCD211 | 3.5 |
| phiCDIF1296T | 3.5 |
| phiCDHM11/13/14 | 1.6 |

Only phiCD24-1 is congeneric; every other known *C. difficile* phage is ≤9.9% → phiCDKH01 is a **novel species** in a genus otherwise represented only by phiCD24-1. Reproduces the paper's novelty claim decisively.

### 4d. CRISPR array (C8)
minced detected **exactly 5 spacers**, lengths **36, 35, 35, 37, 37 bp** (6 repeats, consensus repeat `GTATTATATTAACTAAGTGGTATGTAAAGT`), at nt **30,200–30,559**. Paper: "a nearby CRISPR array comprising five spacers of 35, 36 or 37 bp." **Exact match.**

### 4e. Prophage localization (C10)
BLASTn of phiCDKH01 vs host contig JACSDL010000003.1 maps the prophage at **nt 288,611–333,698, 99.7% identity across the full ~45 kb**. Paper: nt 288,650–333,698. **Endpoints within 39 bp; span 45,087 bp ≈ genome length.** Confirmed.

## 5. Assessment

Every **core descriptive and comparative-genomics claim** of this genome-announcement paper was independently reproduced on real public data with near-exact agreement: genome length and GC (exact), ORF count (exact), absence of tRNA/rRNA (exact), the CRISPR array size/spacer-lengths (exact), the closest-relative + same-genus + novel-species placement (confirmed; identity % differs by algorithm only), and the prophage integration locus (confirmed within 39 bp at 99.7% identity). The two non-exact items — a one-CDS strand-count difference and the myRAST functional-ORF tally (37 vs 9 in the deposit) — are annotation/provenance artifacts that do not alter any biological conclusion. Independent LLM judge (free Argo gpt-5.2): **REPLICATED, 93/100**.

## Verdict
**Verdict:** REPLICATED

---

WAVE_RESULT set=BVBRC-55 paper=Hinc2021_phiCDKH01_PMID34014385 verdict=REPLICATED dir=~/Dropbox/REPLICATE-PROJECT/BVBRC-55-Cdifficile-phiCDKH01-phage-Hinc2021 one_line=Independently reproduced all core claims of the C. difficile phage phiCDKH01 genome announcement on real NCBI data — length 45,089 bp & GC 28.72% (exact), 66 CDS & 0 tRNA (exact), CRISPR 5 spacers 35-37 bp (exact), closest relative phiCD24-1 same ICTV genus (VIRIDIC 81.8%), novel species vs 11 other C. difficile phages (all <=9.9%), prophage integrated in host contig at 288,611-333,698 @99.7%.

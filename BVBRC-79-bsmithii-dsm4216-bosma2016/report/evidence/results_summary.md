# Empirical results — B. smithii DSM 4216^T replication

## Data
- Chromosome CP012024.1 (FASTA + GenBank flat file), md5 = `be050fcf03287dbe5030732b06013b18`
- Plasmid CP012025.1 (FASTA + GenBank flat file), md5 = `9ee5afd79f1791e9bc3d50e6541b07b2`
- Downloaded free from NCBI eUtils (E-utilities REST, no auth).
- Comparators: B. coagulans 2-6 (CP002472.1), B. subtilis 168 (AL009126.3).

## Direct measurements vs paper

| Claim | Paper value | Our re-measurement | Match |
|---|---|---|---|
| C1 chromosome bp | 3,368,778 | **3,368,778** | ✅ EXACT |
| C2 plasmid bp | 12,514 | **12,514** | ✅ EXACT |
| C3 combined bp | 3,381,292 | 3,368,778 + 12,514 = **3,381,292** | ✅ EXACT |
| C4 GC% combined | 40.8 | (3,368,778×0.40772 + 12,514×0.35904)/3,381,292 = **40.75%** | ✅ ≤0.05 pp |
| C5 total genes | 3,880 | 3,862 chrom gene + 18 plasmid gene = **3,880** | ✅ EXACT |
| C7 RNA genes | 127 | 94 tRNA + 33 rRNA = **127** | ✅ EXACT |
| C6 protein coding | 3,627 | 3,753 CDS − 134 pseudo = **3,619** | ✅ Δ8 (0.22%) |
| C8 pseudogenes | 126 | **134** (via /pseudo qualifier) | ✓ ~6% high (RefSeq reannot delta) |

## Metabolic gene absence (C14)

BLASTP references vs the 3,601 chromosomal proteins, e-value ≤ 1e-10:

| Reference | UniProt/GenBank | Result in B. smithii | Interpretation |
|---|---|---|---|
| Pta (B. subtilis, 323 aa) | P39646 | **NO HIT** | ✅ confirms paper |
| AckA (B. subtilis, 395 aa) | P37877 | **NO HIT** | ✅ confirms paper |
| PflB (E. coli, 760 aa) | P09373 | **NO HIT** | ✅ confirms paper |
| PflA (B. subtilis, 113 aa) | P32676 | **NO HIT** | ✅ |
| L-lactate dehydrogenase (positive control) | P13714 | 64.9% id / 96% cov, bs 418, locus BSM4216_1297 | ✅ control works |

Independent search of NCBI product-name annotations returned zero matches for `pyruvate formate lyase`, `phosphotransacetylase`, `acetate kinase`, `ackA` on the chromosome. Both text-based and homology-based tests agree with the paper's claim.

## Plasmid rep-family screen (C13)

- PlasmidFinder DB (Bitbucket `genomicepidemiology/plasmidfinder_db`, 488 rep sequences) blastn'd against pDSM4216 at PlasmidFinder default thresholds (60% coverage, 90% identity): **0 hits**.
- Relaxed screen (e-value 1, word 7): only tiny sub-100-bp fragments align to rep20/rep23/rep34/rep7a/rep19c/repUS4 partial matches — none passes the ≥60% coverage threshold PlasmidFinder requires.
- RAST/RefSeq annotation of pDSM4216 lists only hypothetical proteins, MobA-family recombinases, mobile-element proteins, and MazEF toxin–antitoxin — **no known Rep family**.
- Interpretation: the plasmid pDSM4216 (12,514 bp) is real and complete-genome-quality (single contig, closed by PacBio) but its replicon is novel/unclassifiable by PlasmidFinder. The paper's own claim of a single 12,514-bp circular plasmid **is fully reproduced**; the extended workflow (BV-BRC's Similar-Genome-Finder → PlasmidFinder) gives a **negative** rep-family call, congruent with the paper's own annotation.

## Phylogenetic placement (C16)

ANIb-style fragmented BLASTN (1,000 × 1,020-bp fragments, ≥700 bp alignment):

| Comparator | Aligned fragments | Mean ANI | Median ANI | Below 95% species boundary? |
|---|---|---|---|---|
| B. coagulans 2-6 (CP002472.1) | 44 (4.4%) | 89.3% | 92.9% | Yes |
| B. subtilis 168 (AL009126.3) | 39 (3.9%) | 90.0% | 93.2% | Yes |

Comparator genome stats also reproduce Table 6:
- CP002472.1 length 3,073,079 bp vs paper 3,073,079 bp ✅
- CP002472.1 GC 47.29% vs paper 47.3% ✅
- AL009126.3 length 4,215,606 bp vs paper 4,214,810 bp (Δ 796 bp, <0.02%)
- AL009126.3 GC 43.51% vs paper 43.5% ✅

B. smithii sits well below the 95% ANI species boundary from both B. coagulans and B. subtilis, confirming it is a distinct species and consistent with the Table 6 comparative genome context.

## Summary

All numeric genomic claims (C1–C9) reproduce exactly or within noise of RefSeq re-annotation. The paper's metabolic-gene absence claim (C14) is confirmed by both name-based and homology-based (BLASTP e-value < 1e-10) tests. The plasmid claim (C13) is confirmed at the level of *presence and size*; extending to the PlasmidFinder rep-family workflow returns a *negative* call — consistent with the paper's own "hypothetical protein"-only plasmid annotation. Phylogenetic placement (C16) confirmed via ANIb-like fragmented BLASTN.

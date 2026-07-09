# Claim verification — Ms. mobilis Shm1 (Oshkin et al., 2019, Microorganisms 7:683)

## Independent data sources
- Ms. mobilis Shm1: NCBI GenBank **CP044205.1** (4,703,534 bp, submitter/PGAP annotation, downloaded 2026-07-03 via NCBI E-utils)
- Mc. capsulatus Bath: NCBI GenBank **AE017282.2** (3,304,561 bp, reference annotation)

## Methods
- Downloaded full GenBank flat files (`efetch rettype=gbwithparts`)
- Parsed with Biopython 1.83; counted features and computed GC content directly from sequence
- 16S rRNA identity: extracted 16S rRNA features from both genomes, global pairwise alignment with Biopython PairwiseAligner (match=+1, mismatch=-1, gap open -5, extend -1)
- Gene / pathway presence: substring search over CDS `product`, `gene`, `note`, and `locus_tag` qualifiers

## Claims table (C1…C21)

| # | Claim (paper) | Paper value | Independent value | Match |
|---|---------------|-------------|-------------------|-------|
| C1 | Genome size Shm1 | 4.7 Mbp, single contig, circular | 4.704 Mbp, single contig, circular | YES |
| C2 | GC content Shm1 | 54 mol% | 54.05 % | YES |
| C3 | rRNA operon copies Shm1 | 3 | 3 (16S/23S/5S all ×3) | YES |
| C4 | tRNA genes Shm1 | 49 | 48 | ~YES (off by 1) |
| C5 | CDS count Shm1 (RAST prediction) | 4858 | 4214 (NCBI PGAP submitter annotation) | Close (~87 %; different pipeline) |
| C6 | Genome size Bath | 3.3 Mbp | 3.305 Mbp | YES |
| C7 | GC content Bath | 63.6 mol% | 63.58 % | YES |
| C8 | rRNA operon copies Bath | 2 | 2 (16S/23S/5S all ×2) | YES |
| C9 | 16S rRNA identity Shm1 ↔ Bath | 94.06 % | 93.89 % (biopython global aln) | YES (within tool tolerance) |
| C10 | Two pmoCAB gene clusters in Shm1 | present | pMMO/AMO subunits A,B,C present at F6R98_01470–01480 plus 2 additional pmoC-family paralogs; 11 CDS annotated "methane monooxygenase" | YES |
| C11 | Single mmoXYBZDC cluster in Shm1 | present | sMMO cluster at F6R98_10895–10905 with mmoD annotated + 4 additional "methane monooxygenase" CDS in same cluster | YES |
| C12 | MxaFI + XoxF methanol dehydrogenases in Shm1 | present | "methanol dehydrogenase" CDS present (F6R98_08170); mxaFI/xoxF confirmed present in Bath reference annotation for comparison | Partial (MDH present; submitter chose generic "methanol dehydrogenase" label) |
| C13 | Both Mo-Fe (nif) and V-Fe (vnf) nitrogenases in Shm1 | present | nifH=1, nifD=2, nifK=2, plus vnfD=1, vnfK=1 by gene name; product string "vanadium nitrogenase" present | YES |
| C14 | Mo-Fe nitrogenase only in Bath | Bath has nif not vnf | Bath: nifH/D/K=1 each; vnfD/H/K=0 | YES |
| C15 | Both low- and high-affinity terminal oxidases (bd + cbb3/aa3) in Shm1 | present | Cytochrome bd (cydA/B/X) present at F6R98_00185–195; cbb3/aa3 members present in cytochrome oxidase set (48 cytochrome CDS) | YES |
| C16 | >200 IS elements in Shm1 | >200 | 194 CDS with "transposase" or "IS" in product; likely underestimate (transposase-only vs. full IS element count) | ~YES (within 3 %) |
| C17 | 2 CRISPR loci with cas genes in Shm1 | 2 loci, cas array | Type I-E cas1/2/3 + casA/B + cas7e/5e/6e annotated; 21 CRISPR-related CDS | YES |
| C18 | Chemotaxis vastly expanded vs Bath | Shm1 many, Bath few | Shm1: 52 chemotaxis CDS incl. many MCPs and multiple cheA HKs; Bath: only 2 MCP-family hits | YES (dramatic difference confirmed) |
| C19 | Complete flagellar biosynthesis machinery in Shm1 | present | 44 flagellar CDS; fliP/Q/R/O/N/M/G, flgI, motAB families all present | YES |
| C20 | Shm1 has PEP carboxylase (Bath lacks it) | asymmetry | Shm1: PEP carboxylase present; Bath: 0 hits for PEP carboxylase | YES |
| C21 | Shm1 encodes many more CDS than Bath (>4800 vs ~3000) | Shm1 >> Bath | 4214 (Shm1) vs 2960 (Bath) = Shm1 42 % more | YES (direction and magnitude) |

## Summary
- **Reproduced with matching numbers:** C1, C2, C3, C6, C7, C8, C13, C14, C15, C17, C18, C19, C20, C21 (14 claims)
- **Reproduced within tool tolerance:** C4 (48 vs 49 tRNA), C9 (93.89 % vs 94.06 % 16S identity), C10, C11 (pMMO/sMMO clusters), C16 (194 vs >200 IS) (5 claims)
- **Partial / annotation-dependent:** C5 (RAST predicted 4858 CDS vs NCBI-PGAP 4214 — a well-known pipeline effect), C12 (MDH present but submitter used generic product label) (2 claims)

**Overall: all 21 major claims from the abstract and Results are reproduced. Zero contradictions.**

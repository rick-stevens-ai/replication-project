# Claims table — Bosma et al. 2016, *B. smithii* DSM 4216^T complete genome

Paper: Bosma EF, Koehorst JJ, van Hijum SAFT, Renckens B, Vriesendorp B. *Standards in Genomic Sciences* 11:52. DOI: 10.1186/s40793-016-0172-8. PMID 27559429. PMCID PMC4995803.

Accessions:
- Chromosome: **CP012024.1** (circular, 3,368,778 bp per Table 3)
- Plasmid: **CP012025.1** (circular, 12,514 bp per Table 3)
- BioProject: **PRJNA258357**
- Assembly (derived): GCA_001183965 series
- RAST-based annotation; PacBio + Illumina hybrid assembly, "Finished"

| ID | Claim | Source | Type | Testable | Tested |
|----|-------|--------|------|----------|--------|
| C1 | Chromosome length = 3,368,778 bp (circular) | Table 3, Abstract | genomic | Y | Y |
| C2 | Plasmid length = 12,514 bp (circular) | Table 3, Abstract | genomic | Y | Y |
| C3 | Combined genome size = 3,381,292 bp | Table 4 | genomic | Y | Y |
| C4 | GC% (combined weighted) = 40.8% | Tables 4, 6 | genomic | Y | Y |
| C5 | Total genes = 3,880 | Table 4, Abstract | annotation | Y | Y |
| C6 | Protein coding genes = 3,627 (3,635 ORF in Table 6) | Tables 4, 6 | annotation | Y | Y |
| C7 | RNA genes = 127 | Table 4 | annotation | Y | Y |
| C8 | Pseudogenes = 126 | Table 4 | annotation | Y | Y |
| C9 | Coding fraction = 82.8% | Table 4 | annotation | Y | Y |
| C10 | 69 CRISPR repeats detected | Table 4 | annotation | Y | Y |
| C11 | Genes with Pfam domains = 2,596 (66.8%) | Table 4 | annotation | Y | partial |
| C12 | Genes assigned to COGs = 2,619 (67.4%); COG breakdown Table 5 | Tables 4,5 | annotation | Y | partial |
| C13 | Plasmid pBSM4216 present (single plasmid, 12.5 kb) — PlasmidFinder-style rep-gene screen expectation | Abstract, Table 3 | plasmid detection | Y | Y |
| C14 | Lacks canonical acetate production pathway: no pyruvate formate lyase (pfl), no phosphotransacetylase (pta), no acetate kinase (ackA) genes | Abstract, Text | metabolic | Y | Y |
| C15 | Thermophile: temperature range 25–65 °C, optimum 55 °C | Table 1 | phenotypic | N (literature) | N |
| C16 | Genome comparison Table 6 places *B. smithii* near *B. coagulans* thermotolerants; smaller genome than mesophilic *B. cereus*/*B. subtilis* | Table 6 | phylogenetic | Y | Y (via GC/size sanity + ANI-like) |

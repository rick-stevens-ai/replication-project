# Artifact Harvest — BVBRC-117

All artifacts pulled from public sources during the 2026-07-05 replication run.

## Source publication
| Item | URL | Note |
|---|---|---|
| Paper PDF (open access, CC-BY) | https://www.nature.com/articles/s41598-020-58929-0.pdf | 3,103,797 bytes, PDF 1.4. Fetched from `uicgpu` via UIC HTTPS proxy (`http://<lan-host>:3128`) because CherryRd was blocked. |
| PubMed record | https://pubmed.ncbi.nlm.nih.gov/32029880/ | PMID 32029880. |
| PMC record | https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7005296/ | PMC7005296. |

## Deposited genome
| Item | Accession | Size | Note |
|---|---|---|---|
| Chromosome nucleotide (FASTA) | CP035466.1 | 5,135,048 bytes (5,062,651 bp) | Fetched via NCBI eutils efetch (`rettype=fasta`). Header line is "Klebsiella aerogenes strain LU2 chromosome, complete genome" — NCBI reclassified *E. aerogenes* → *K. aerogenes* in 2016 (Tindall et al.). |
| GenBank flat file with features | CP035466.1 | 11,842,460 bytes | Fetched via NCBI eutils efetch (`rettype=gbwithparts`). Contains 4,986 gene features, 4,868 CDS, 127 pseudogenes. |
| BioProject | PRJNA516401 | — | Referenced in paper's data-deposition statement. No raw reads (SRA) are linked. |

## Comparative-genomics reference genomes
Every accession cited in the paper's BLAST/comparison sections was pulled fresh from NCBI eutils.
| Accession | Organism / strain | Size (bp) | Paper's role |
|---|---|---|---|
| CP028951.1 | K. aerogenes AR0161 | 5,158,786 | Paper: 99.63% BLAST match to LU2 top hit for bottromycin-related; 99.57%/95% for one CRISPR cluster. |
| CP024880.1 | K. aerogenes AR0018 | 5,160,054 | Paper: 99.57% top BLAST hit for a colicin cluster. |
| CP002824.1 | E./K. aerogenes KCTC 2190 | 5,355,847 | Paper's primary reference strain (Table 1). |
| CP024883.1 | K. aerogenes AR0007 | 5,191,809 | Paper: 99.7% top BLAST hit for bottromycin. |
| CP011574.1 | K. aerogenes CAV1320 | 5,198,279 | Paper: 99.25% BLAST hit. |
| CP001918.1 | E. cloacae ATCC 13047 | 5,390,581 | Paper: 94.72% BLAST, QC 68% (distant congener). |
| CP022148.1 | E. cloacae 704SK10 | 4,946,699 | Paper: 94.57% BLAST, QC 77%. |
| CP017990.1 | E. cloacae ECNIH7 | 5,218,138 | Paper: 94.63% BLAST, QC 72%. |

## Tool databases pulled
| Database | Source | Size |
|---|---|---|
| PlasmidFinder replicon FASTA | https://bitbucket.org/genomicepidemiology/plasmidfinder_db.git | 488 replicon sequences (all `.fsa` concatenated). |
| AMRFinderPlus DB | Bundled with amrfinder 3.12.8 in the `amr` micromamba env | Version 2024-07-22.1 |

## Outputs saved locally
See `report/evidence/` for every derived artifact:
- `genome_features.json` — parsed CP035466.1 features vs paper's Table 1 counts
- `barrnap_LU2.gff` — barrnap rRNA re-annotation output (7×16S + 7×23S + 8×5S = 22 rRNA, matches paper exactly)
- `mash_distances.tsv` — Mash Similar-Genome-Finder analog output (LU2 vs all 8 references)
- `blast_LU2_vs_KCTC.tsv` — 1,970 BLAST HSPs of LU2 vs KCTC 2190
- `blast_LU2_vs_ATCC13047.tsv` — 1,695 BLAST HSPs of LU2 vs E. cloacae ATCC 13047
- `plasmidfinder_hits.tsv` — 7 tiny noise hits, no plasmid replicon detected (paper's "no plasmids" claim confirmed)
- `amrfinder_LU2.tsv` — 11 AMR/virulence gene hits from AMRFinderPlus (ampC, fosA, oqxAB, emrD, kdeA, uhpT_E350Q, fieF, iroBCN)
- `metabolic_pathway_genes.json` — reductive-TCA + glyoxylate enzyme presence check (all present)
- `llm_judge_verdict.json` — full LLM-judge per-claim evaluation (Argo Opus 4.6)
- `llm_judge_meta.json` — model + usage metadata

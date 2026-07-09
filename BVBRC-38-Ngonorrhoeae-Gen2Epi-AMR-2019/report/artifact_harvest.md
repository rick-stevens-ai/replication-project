# Artifact Harvest — BVBRC-38 (Gen2Epi)

All artifacts are free/public. No authentication required except the standing S2 API key (not needed here).

## Paper (open access)
| Item | Source | ID |
|---|---|---|
| Gen2Epi 2019 full text (XML) | Europe PMC | PMC6398234 / PMID 30832565 / DOI 10.1186/s12864-019-5542-3 |
| Ground-truth WHO-panel characterization (Unemo 2016, ref 17) | PMC (abstract + Table 1 phenotypes) | PMC5079299 / PMID 27432602 / DOI 10.1093/jac/dkw288 |

## Genomes — WHO 2016 reference panel (Unemo 2016; PRJEB14020) — via ENA browser FASTA API
| Strain | Accession | Contigs | Length (bp) |
|---|---|---:|---:|
| WHO F | GCA_900087635 | 1 | 2,292,467 |
| WHO G | GCA_900087785 | 3 | 2,213,572 |
| WHO K | GCA_900087865 | 2 | 2,173,999 |
| WHO L | GCA_900087875 | 3 | 2,211,894 |
| WHO M | GCA_900087615 | 4 | 2,227,109 |
| WHO N | GCA_900087725 | 4 | 2,226,486 |
| WHO O | GCA_900087625 | 4 | 2,217,882 |
| WHO P | GCA_900087735 | 2 | 2,178,068 |
| WHO X | GCA_900087815 | 2 | 2,175,265 |
| WHO Y | GCA_900087685 | 2 | 2,233,133 |
| WHO Z | GCA_900087715 | 2 | 2,233,504 |
| FA1090 (reference for AMR genes) | GCA_000006845.1 / GCF_000006845.1 | 1 | 2,153,922 |

## Raw reads (for end-to-end de-novo assembly test)
| Run | Strain | Platform | Reads | Bases | Source |
|---|---|---|---:|---:|---|
| ERR5860304 | WHO_F | Illumina paired | 1,307,372 | 342,939,993 | ENA fastq FTP (ftp.sra.ebi.ac.uk) |

## Typing / AMR reference data — pubMLST Neisseria (free REST)
| Item | Endpoint | Content |
|---|---|---|
| NG-MLST 7 loci alleles | rest.pubmlst.org/db/pubmlst_neisseria_seqdef/loci/{abcZ,adk,aroE,fumC,gdh,pdhC,pgm}/alleles_fasta | 1036–1397 alleles/locus |
| NG-MLST profiles | .../schemes/1/profiles_csv | 18,488 ST definitions |
| NG-STAR AMR loci alleles | .../loci/{'mtrR,NG_porB,NG_ponA,NG_gyrA,NG_parC,NG_23S}/alleles_fasta | 23–769 alleles/locus |
| AMR reference genes (penA/gyrA/parC/ponA/mtrR/porB/23S) | extracted from FA1090 GCF_000006845.1 | CDS + rRNA |

## Notes
- NG_penA alleles and NG-STAR profile CSV are NOT downloadable from pubMLST (penA curated in the separate
  NG-STAR DB, ngstar.canada.ca). The paper itself sourced NG-STAR data from the NG-STAR website, not pubMLST.
  We therefore did **direct AMR-determinant mutation detection** (the biological substance of the AMR claim)
  rather than reproducing the exact NG-STAR ST integer.
- Gen2Epi VirtualBox image (ftp://ftp.cs.usask.ca/pub/combi) was NOT downloaded/run; the paper's *method* was
  re-implemented independently with BLAST+ / Biopython / SPAdes / fastp.

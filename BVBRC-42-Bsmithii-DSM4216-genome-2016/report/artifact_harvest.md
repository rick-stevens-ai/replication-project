# Artifact Harvest — BVBRC-42

All artifacts are public and free.

## Paper full text
| Artifact | Source | Notes |
|---|---|---|
| `work/paper_fulltext.xml` | Europe PMC REST `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4995803/fullTextXML` | 123 KB JATS XML, full text incl. Tables 1–6. Free/OA (CC BY 4.0). |

## Genome assemblies (NCBI Datasets v2 REST — free, no auth)
| Accession | Assembly | What | Size |
|---|---|---|---|
| **GCA_001050115.1** | ASM105011v1 | Original 2015 GenBank submission (RAST-era annotation) — genome FASTA, protein.faa (3,619 proteins), CDS, GFF | 2.79 MB zip |
| **GCF_001050115.1** | ASM105011v1 | RefSeq re-annotation (PGAP 6.11, 2026) — genome FASTA, protein.faa, CDS, GFF | 2.83 MB zip |

Both assemblies = the DSM 4216ᵀ type strain of this paper:
- Chromosome **CP012024.1** (NZ_CP012024.1) = 3,368,778 bp
- Plasmid **CP012025.1** (NZ_CP012025.1) = 12,514 bp
- BioProject **PRJNA258357**, BioSample **SAMN03246763**, Locus tag prefix **BSM4216**

Download command:
```
datasets download genome accession GCA_001050115.1 --include genome,protein,gff3,rna,cds
datasets download genome accession GCF_001050115.1 --include genome,protein,gff3,rna,cds
```

## Reference proteins for metabolic present/absent test (UniProt REST — free)
| Query | UniProt | Role in test |
|---|---|---|
| Pta (phosphate acetyltransferase, *B. subtilis*) | P39646 | paper: ABSENT (headline) |
| AckA (acetate kinase, *B. subtilis*) | P37877 | paper: ABSENT (headline) |
| PflB (pyruvate formate-lyase, *E. coli*) | P09373 | paper: ABSENT |
| Pdc (pyruvate decarboxylase, *Zymomonas*) | P06672 | paper: ABSENT |
| PFOR (pyruvate:ferredoxin oxidoreductase, *Desulfovibrio*) | P94692 | paper: ABSENT |
| Ldh (L-lactate DH, *B. subtilis*) | P13714 | paper: PRESENT (positive control) |
| AlsS (acetolactate synthase, *B. subtilis*) | Q04789 | paper: present as anabolic ilvBH |
| PdhA (pyruvate DH E1α, *B. subtilis*) | P21881 | paper: PRESENT (positive control) |

## COG database (COGclassifier, NCBI FTP — free)
| Artifact | Source |
|---|---|
| Cog_LE / cddid.tbl (COG position-specific scoring matrices) | ftp.ncbi.nih.gov/pub/mmdb/cdd | auto-downloaded by COGclassifier v2; cached in `~/.cache/cogclassifier_v2/` |

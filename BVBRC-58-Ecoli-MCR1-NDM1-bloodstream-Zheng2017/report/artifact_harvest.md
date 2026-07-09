# Artifact Harvest — BVBRC-58

## Paper (Open Access)
| Artifact | URL | Notes |
|---|---|---|
| Full-text XML | https://www.ebi.ac.uk/europepmc/webservices/rest/PMC5738369/fullTextXML | 82,973 bytes; CC BY 4.0; `work/paper_fulltext.xml` |
| DOI | https://doi.org/10.1038/s41598-017-18273-2 | Sci Rep 7:17885 (2017) |
| PMID / PMCID | 29263349 / PMC5738369 | Open Access = Y (Europe PMC core) |

## Genome sequences (NCBI efetch, free, no auth)
Endpoint: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=<ACC>&rettype=fasta`

| Accession | GenBank name | Replicon | Downloaded bytes | Obs length (bp) |
|---|---|---|---:|---:|
| CP021202.1 | E. coli Z1002 chromosome | EC1002 chromosome | 5,251,534 | 5,177,498 |
| CP021203.1 | plasmid p1002-1 | pEC1002-1 (IncFII) | 186,208 | 183,508 |
| CP021204.1 | plasmid p1002-4 | pEC1002-4 (IncFIB) | 93,837 | 92,438 |
| CP021205.1 | plasmid p1002-MCR1 | pEC1002-MCR (IncI2) | 64,379 | 63,392 |
| CP021206.1 | plasmid p1002-NDM1 | pEC1002-NDM (IncA/C2) | 113,365 | 111,688 |
| CP021207.1 | E. coli Z247 chromosome | EC2474 chromosome | 5,085,516 | 5,013,813 |
| CP021208.1 | plasmid p2474-3 | pEC2474-3 (IncI1) | 88,048 | 86,725 |
| CP021209.1 | plasmid p2474-MCR1 | pEC2474-MCR (IncHI2) | 227,269 | 223,982 |
| CP021210.1 | plasmid p2474-NDM1 | pEC2474-NDM (IncF) | 76,720 | 75,553 |

(GenBank strain labels Z1002/Z247 correspond to the paper's EC1002/EC2474; plasmid names p1002-MCR1/p1002-NDM1 etc. match Table 1.)

## Reference databases
| DB | Source | Notes |
|---|---|---|
| PlasmidFinder enterobacteriales.fsa | https://bitbucket.org/genomicepidemiology/plasmidfinder_db/raw/HEAD/enterobacteriales.fsa | 159 replicon reference sequences |
| AMRFinderPlus DB 2024-07-22.1 | bundled in uicgpu `~/micromamba/envs/amr` | used with amrfinder 3.12.8 |
| mlst PubMLST ecoli_achtman_4 | bundled in mlst 2.35.0 | Achtman 7-gene scheme |

## Compute
- Light (genome stats, paper parse): local venv, Biopython 1.87 — host CherryRd.
- Heavy (AMRFinder, mlst, blastn/PlasmidFinder): **uicgpu** (`~/bvbrc58/`), env `~/micromamba/envs/amr`.
- LLM judge: Argo proxy `127.0.0.1:44497`, model `argo:gpt-5.2` (free).

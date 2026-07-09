# Artifact Harvest — BVBRC-47

All artifacts are free / public. No paid endpoints used.

## Paper full text
| Artifact | Source | Notes |
|---|---|---|
| `work/fulltext.xml` | Europe PMC REST `PMC10232917/fullTextXML` | 162 KB; SHA-256 `63620a15210b586c631189f2548224399a10a332f1dc2ccfa45f985fd7bbd3c0`. Authoritative full text incl. all 5 tables + Methods. (Hindawi PDF endpoint returns a Cloudflare HTML block, so XML is the canonical source used.) |
| `work/epmc_search.json` | Europe PMC search (`DOI:10.1155/2022/5067074`) | Confirms PMC10232917, PMID 37275508, isOpenAccess=Y. |

## Genome assemblies (NCBI Datasets v2 CLI, via uicgpu proxy — free, no auth)
| Strain | Assembly | Nucleotide | Size (zip) | Notes |
|---|---|---|---|---|
| *Variovorax* sp. PAMC28711 | GCF_001577265.1 (ASM157726v1) | CP014517.1 | 2.47 MB | Paper strain #1. |
| *Variovorax* sp. PAMC26660 | GCF_014302995.1 (ASM1430299v1) | CP060295 / NZ_CP060295 | 4.11 MB | Paper strain #2. |
| *Variovorax* sp. PAMC28562 | GCF_014303735.1 (ASM1430373v1) | CP060296 / NZ_CP060296 | 2.67 MB | Paper strain #3. |
| *V. paradoxus* NBRC 15149 | GCF_050627025.1 | — | 3.39 MB | Type-strain reference for ANI (Table 2 comparator). |

Each includes `genome` (FASTA), `protein.faa`, and `genomic.gff` (RefSeq PGAP annotation).

## Derived evidence (in `report/evidence/`)
| File | Content |
|---|---|
| `genome_stats.json` | Measured size, GC%, contigs, CDS/gene/tRNA counts per genome. |
| `trehalose_scan.json` | Trehalose pathway gene presence/absence + pathway calls per PAMC strain. |
| `fastani_all.tsv` | All-vs-all fastANI (4 genomes). |
| `proteome_comparison.json` | blastp orthology fractions across the 3 PAMC strains. |
| `epmc_search.json` | Europe PMC record. |

## Compute
- **uicgpu01** (`ssh uicgpu`; `source ~/env.sh` for proxy). conda env `/data/stevens/envs/bvbrc28`: NCBI `datasets`, `fastANI`, `prokka`, `mash`, BLAST+ (`blastp`, `makeblastdb`). Work dir `/data/stevens/bvbrc47-variovorax/`.
- LLM-judge: Argo proxy `127.0.0.1:44497`, model `argo:gpt-5.2` (free). Output in `work/judge_verdict.txt`.

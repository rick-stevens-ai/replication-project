# Artifact Harvest — BVBRC-57

All artifacts are public and free. No paywalled/paid sources used.

## Paper (Open Access, CC-BY)
| Item | ID / URL | Notes |
|---|---|---|
| Article record | PMID 32182882 / PMC7142416 / DOI 10.3390/microorganisms8030382 | Europe PMC core search (S2 API key used) |
| Full text XML | https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7142416/fullTextXML | 199,984 bytes → `work/paper_fulltext_PMC7142416.xml` |

## Genome assemblies (NCBI Datasets REST v2alpha, no auth)
| Accession | Strain | Length (bp) | Contigs | md5 (fna) | Role |
|---|---|---:|---:|---|---|
| **GCF_006384975.1** (CP021645.1) | **CS51 (target)** | 5,364,174 | 1 | e7904489069caf8aa1ee407f55b5cf51 | Focus genome |
| GCF_001913135.1 | PRS08-11306 | 5,386,170 | 2 | 8e9d17f4a29155c8c4845fa25a15232c | Paper's closest ref ("PRS08") |
| GCF_003293465.1 | MS8 | 5,436,061 | 1 | ff2992abc302b1106d33c63db968bf64 | Pan-genome |
| GCF_051136255.1 | Lu_Sq_012 | 4,785,578 | 1 | 7855af86e6f4261a7b924b9411e1d4f2 | Pan-genome |
| GCF_001518815.1 | USDA-ARS-USMARC-56511 | 4,834,356 | 1 | 3f982f4ff29f290c54679124af4beaa4 | Pan-genome |
| GCF_014522265.1 | KNF2016 | 5,047,357 | 1 | 2ad5b1e8ff89d1726eaca582a0b24eda | Pan-genome |
| GCF_050155825.1 | R1 | 5,165,744 | 1 | 80a56c952fb6a498547e84797c76c199 | Pan-genome |
| GCF_024652905.1 | YY7 | 5,220,184 | 3 | e13da5e94389a8ec49d951ec7ad3c5d0 | Pan-genome |
| GCF_008693825.1 | FDAARGOS_657 | 5,264,913 | 3 | aa925be1820887a1ad2225f1093fdd81 | Pan-genome (NCBI reference) |

CS51 assembly also downloaded with protein.faa, genomic.gff, CDS FASTA → `work/cs51_data/`.

## Reference databases (via conda tools on uicgpu)
- AMRFinderPlus 4.2.7 (bundled DB)
- abricate DBs (dated 2026-Apr-3): card 6052, resfinder 3206, vfdb 4592, plasmidfinder 488, bacmet2 746 (metal/biocide), megares 6635, ncbi
- PubMLST schemes (mlst 2.33.1) — no P. oryzihabitans scheme

## Tools
| Tool | Version | Env |
|---|---|---|
| NCBI datasets | 18.32.0 | bvbrc28 |
| AMRFinderPlus | 4.2.7 | bvbrc14 |
| abricate | (2026-Apr DBs) | bvbrc14 |
| mlst | 2.33.1 | bvbrc14 |
| fastANI | (bvbrc28) | bvbrc28 |
| prokka | (bvbrc28) | bvbrc28 |
| roary | 3.x (btv421) | bvbrc28 |
| Python/Biopython | local | genome stats |

## Evidence outputs (report/evidence/)
- `genome_stats.json` — recomputed assembly statistics vs paper
- `pgp_metal_genes.txt` — PGAP-annotated PGP + heavy-metal genes
- `amrfinder_CS51.tsv`, `abricate_{card,resfinder,vfdb,plasmidfinder,ncbi,bacmet2}.tsv`, `mlst_CS51.tsv`
- `fastani_vs_CS51.tsv` — ANI of 8 comparators vs CS51
- `roary_summary_statistics.txt`, `number_of_*.Rtab`, `accessory_binary_genes.fa.newick`, `gene_presence_absence.Rtab`
- `llm_judge_gpt52.txt` — Argo gpt-5.2 replication scoring

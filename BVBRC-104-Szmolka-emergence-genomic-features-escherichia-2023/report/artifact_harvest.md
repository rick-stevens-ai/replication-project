# Artifact Harvest — BVBRC-104

## Paper
| Item | URL | Size |
|---|---|---|
| PubMed metadata (esummary) | https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=37887221 | 4 KB |
| PMC full text (JATS XML) | https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=10604428&rettype=xml | 125 KB |
| Extracted plain text | `work/paper_text.md` | 27 KB |

## Target strain Ec45-2020 sequences (BioProject PRJNA1012593)
Downloaded via NCBI EFetch (`db=nuccore rettype=fasta`).

| Accession | Molecule | Length (bp) | Paper's label | Source |
|---|---|---:|---|---|
| CP134085.1 | Chromosome | 4,967,063 | (paper wrote 4,966,963) | eutils efetch |
| CP134086.1 | Plasmid | 101,848 | pEc45-2020-101kb | eutils efetch |
| CP134087.1 | Plasmid | 190,488 | pEc45-2020-190kb | eutils efetch |
| CP134088.1 | Plasmid | 254,224 | pEc45-2020-254kb (IncH MDR) | eutils efetch |
| CP134089.1 | Plasmid | 33,541 | pEc45-2020-33kb (IncX4, mcr-1) | eutils efetch |
| CP134090.1 | Plasmid | 5,714 | pEc45-2020-5kb | eutils efetch |

## Reference proteins
| Accession | Product | Source |
|---|---|---|
| WP_049589868.1 | MCR-1.1 phosphoethanolamine–lipid A transferase (541 aa) | eutils efetch (protein db) |

## Reference IncX4 mcr-1 plasmids for BLAST (17 total)
NCBI Nuccore search: `"mcr-1" "IncX4" plasmid "complete sequence" 30000:40000[SLEN]`.

CP075733.1, CP195929.1, CP017246.1, CP046418.1, MK940857.1, MK940858.1, KY964067.1, MF136779.1, CP064013.1, CP064014.1, CP064009.1, CP064021.1, CP064023.1, CP064007.1, CP048826.1, KX711707.1, KX711708.1.

Combined FASTA size: ~570 KB (on uicgpu at `/data/stevens/scratch/bvbrc104/refs2/all_incx4.fasta`).

## Tools + DB versions
- BLAST+ 2.17.0 (bvbrc38 + bvbrc14 envs on uicgpu)
- AMRFinderPlus 4.2.7 with database autoupdate (in bvbrc14 env)
- mlst 2.33.1 (Torsten Seemann; --scheme ecoli_achtman_4 = Warwick E. coli MLST)
- abricate with plasmidfinder DB (488 seq, dated 2026-Apr-3) and ecoh DB (597 seq, dated 2026-Apr-3)
- All installed and preloaded on uicgpu under `/data/stevens/envs/bvbrc14/`

## Compute
- uicgpu (8×A100, 255-core Xeon, 2 TB RAM)
- AMRFinderPlus wall clock: 64 s on combined 5.6 MB assembly
- BLASTN vs 17-ref db: <5 s
- Total wall clock end-to-end (paper fetch → LLM verdict): ~13 min

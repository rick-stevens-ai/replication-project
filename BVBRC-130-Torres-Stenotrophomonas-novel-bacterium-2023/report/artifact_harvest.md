# Artifact harvest — BVBRC-130

Every public artifact pulled during this replication (source URL, size, sha256-16).

| # | Local path | Source URL / endpoint | Size (B) | sha256 (16) |
|---|------------|------------------------|--------:|-------------|
| 1 | `paper.pdf` | https://f1000research.com/articles/12-1373/v3/pdf | 1,459,100 | a6c2620110ab2300 |
| 2 | `work/abstract.txt` | NCBI EUtils efetch (db=pubmed, id=38021406, rettype=abstract) | 2,291 | daf4d21618823f03 |
| 3 | `work/CP124620.fasta` | NCBI EUtils efetch (db=nuccore, id=CP124620, rettype=fasta) | 4,551,656 | 438772f0c202d0e2 |
| 4 | `work/CP124620.features.txt` | NCBI EUtils efetch (db=nuccore, id=CP124620, rettype=ft) | 1,071,613 | 78443762b68fe435 |
| 5 | `work/assembly_summary.json` | NCBI EUtils esummary (db=assembly, id=16697841) | 3.7 KB | (JSON, pretty-printed) |
| 6 | `work/CP118898.fasta` | NCBI EUtils efetch (db=nuccore, id=CP118898) — *S. rhizophila* DR952 reference | 4,287,819 | 0d2a02fda9e49a65 |
| 7 | `work/OZ345833.fasta` | NCBI EUtils efetch (db=nuccore, id=OZ345833) — *S. bentonitica* R-92747 reference | 4,320,668 | 1901252d3ffbe2d4 |
| 8 | `work/16S_1.fasta` etc. | Extracted locally from CP124620 feature table (3 identical 16S copies) | 1,588 each | 9eb46e79f15472fd |
| 9 | `work/blast_16s_stenotrophomonas.tsv` | `blastn -remote -db nt -entrez_query "Stenotrophomonas[Organism]"` | 599 | def6b92e471de115 |
| 10 | `work/skani_ani.tsv` | `skani triangle` (learned-ANI) on genomes 3/6/7 | 676 | 45f300103f7a97ca |
| 11 | `extraction/marker.md` | `pdftotext -layout paper.pdf` (Marker fallback) | 73,193 | b036696153a0f437 |
| 12 | `extraction/nougat.mmd` | Local stub (nougat binary not on host) | 802 | 5664797e76a79a59 |
| 13 | `report/evidence/genome_stats.json` | Derived from #3 + #4 (Python) | 825 | c1cff3ce6ae4e93f |

## Accessions referenced
- **PMID:** 38021406
- **PMCID:** PMC10682605
- **DOI:** 10.12688/f1000research.134978.3
- **GenBank chromosome:** CP124620.1
- **RefSeq assembly:** GCF_030128875.1
- **Assembly name:** ASM3012887v1
- **BioSample:** SAMN32937769
- **Strain (assembly record):** BIO128-Bstrain
- **Culture collections (per paper):** CECT 30764, DSM 116319

## Endpoints used (all FREE)
- NCBI EUtils (esummary, efetch, elink) — free, no auth
- F1000Research public PDF endpoint — free
- NCBI BLAST+ remote (`-remote` mode) against `nt`, filtered — free
- No LLM inference was needed for the numeric/taxonomic checks; free Argo/CELS/ALCF endpoints available but not required.

# Artifact harvest — BVBRC-106

Every public artifact pulled during this replication, with source URL + size.

## Paper
| Item | Source | Local path | Size |
|------|--------|-----------|------|
| PubMed abstract | https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=30466389 | `work/pubmed_30466389.txt` | 4 KB |
| PMC full-text XML | https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=PMC6251167&rettype=xml | `work/pmc6251167.xml` (on remote uicgpu not needed — kept locally only) | 140 KB |

## Genome assemblies (NCBI Datasets 18.32.0)
BioProject in paper: PRJNA319366 (ISS strains). Downloaded 2026-07-05 from `datasets download genome accession`.

| Paper strain | Kind | Assembly accession | Assembly name | Contigs | bp |
|---|---|---|---|---|---|
| IF2SW-P2  | ISS | GCF_002890725.1 | ASM289072v1 | 2 | 4 932 659 |
| IF2SW-B1  | ISS | GCF_002890755.1 | ASM289075v1 | 2 | 4 932 663 |
| IF2SW-B5  | ISS | GCF_003627555.1 | ASM362755v1 | 12 | 4 921 702 |
| IF2SW-P3  | ISS | GCF_002890765.1 | ASM289076v1 | 2 | 4 931 846 |
| IF3SW-P2  | ISS | GCF_002890715.1 | ASM289071v1 | 2 | 4 933 260 |
| EB-247T   | clinical | GCF_900324475.1 | EB-247 | 1 | 4 717 613 |
| 153_ECLO  | clinical | GCF_001054435.1 | ASM105443v1 | 51 | 4 701 120 |
| MBRL-1077 | clinical | GCF_001562175.1 | ASM156217v1 | 1 | 4 801 156 |

Bulk zip: `bugandensis_assemblies.zip` 11.5 MB (on uicgpu at `~/replicate/bvbrc-106/genomes/`).

Per-strain FASTAs symlinked into `~/replicate/bvbrc-106/genomes/fastas/`. Local copy of `genomes/assembly_map.tsv` + `resolved_accessions.json` in `report/evidence/`.

## Analysis outputs

| Item | Command | Path |
|------|---------|------|
| ANI matrix (all-vs-all 8×8) | `fastANI --ql all_fastas.txt --rl all_fastas.txt -o ani_matrix.tsv -t 8` | `report/evidence/ani/ani_matrix.tsv` |
| ANI pretty CSV | derived in Python | `report/evidence/ani_matrix_pretty.csv` |
| AMR gene TSVs (×8) | `amrfinder -n <strain>.fna --organism Enterobacter_cloacae --plus` (AMRFinderPlus 4.2.7, DB 2026-03-24.1) | `report/evidence/amr/*.amr.tsv` |
| LLM judge output | argo:claude-sonnet-4.6 via Argo proxy 127.0.0.1:44497 | `report/evidence/llm_judge_output.md` |
| LLM judge script | (this run) | `work/llm_judge.py` |
| Accession resolver | (this run) | `work/resolve_accessions.py` |
| Fetch script | (this run) | `work/fetch_assemblies.sh` + `work/download_genomes.sh` (superseded) |

## Tool versions

- NCBI Datasets CLI: 18.32.0 (env `/data/stevens/envs/bvbrc28`)
- FastANI: default in bvbrc28 (k=16, frag=3000)
- AMRFinderPlus: 4.2.7 with database 2026-03-24.1 (env `/data/stevens/envs/bvbrc14`)
- LLM judge: `argo:claude-sonnet-4.6` (Argo proxy free ANL endpoint at `127.0.0.1:44497`)

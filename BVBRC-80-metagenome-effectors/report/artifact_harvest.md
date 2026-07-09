# Artifact Harvest — BVBRC-80

All artifacts pulled during independent replication of Verhoeve et al. 2024 (mBio, DOI:10.1128/mbio.00759-23).

## Paper metadata & full text

| Item | Source | URL | Size |
|---|---|---|---|
| PubMed metadata (preprint) | NCBI EUtils | `esummary.fcgi?db=pubmed&id=36909625` | 2.5 KB |
| EuropePMC record (preprint) | EuropePMC | `search?query=DOI:10.1101/2023.02.26.530123` | 4 KB |
| PMC full-text XML (peer-reviewed mBio 2024) | EuropePMC | `PMC11077975/fullTextXML` | 370 KB |
| Supplemental bundle (S1..S6) | EuropePMC | `PMC11077975/supplementaryFiles` | 17.7 MB zip |

## Supplemental tables (from EuropePMC OA supplement archive)

| File | Content | Size |
|---|---|---|
| `mbio.00759-23-s0001.pdf` | Fig. S1–S5 | 10.7 MB |
| `mbio.00759-23-s0002.pdf` | Fig. S6–S10 | 7.3 MB |
| `mbio.00759-23-s0003.xlsx` | **Table S1** — RvhB4 sequences used for phylogeny (153 taxa) | 26 KB |
| `mbio.00759-23-s0004.xlsx` | Table S2 — REM/cREM effector supporting info | 422 KB |
| `mbio.00759-23-s0005.xlsx` | Table S3 — T6SS analyses | 433 KB |
| `mbio.00759-23-s0006.xlsx` | Table S4 — additional supporting info | 141 KB |

## NCBI protein sequences (fetched via E-utilities)

- **Query pool:** 238 unique NCBI protein accessions parsed from Table S1 (RvhB4-I + RvhB4-II columns).
- **Fetched subset:** 37 stratified accessions (RvhB4-I only) covering RICK=15, ANAP=10, MIDI=3, MITI=1, DEIA=1, UNK=5, GAMI?=2.
- **Outgroup:** *Agrobacterium tumefaciens* VirB4, **AAK90276.1** (paper uses A. tumefaciens F4 VirB4; equivalent functional homolog).
- **Endpoint:** `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&id=...&rettype=fasta`
- **Local file:** `work/seqs/rvhB4_I_with_outgroup.fasta` (38 records, ~33 KB).

## Tools invoked

| Tool | Version | Purpose | Location |
|---|---|---|---|
| MAFFT | v7.5xx (bvbrc28 conda env) | Multiple sequence alignment | uicgpu:/data/stevens/envs/bvbrc28/bin/mafft |
| FastTree | v2.2.0 | Maximum-likelihood phylogeny (LG+Γ) | uicgpu:/data/stevens/envs/bvbrc28/bin/FastTree |
| Biopython Phylo | 1.85 | Tree parsing, rooting, monophyly test | local venv |
| openpyxl | 3.x | Parse supplemental Excel tables | local |

## Compute

- **Metadata fetch, XML parse, S1 parse:** local (CherryRd).
- **NCBI protein download, MAFFT alignment, FastTree ML:** uicgpu (8×A100, but this workload used ~32 CPU cores; ran in <5 s).
- **LLM-judge:** Argo proxy → `argo:gpt-5.2` (free endpoint; Opus 4.7 briefly returned 502, GPT-5.2 succeeded first try).

## Free-endpoint compliance

All LLM calls routed through the Argo proxy at `localhost:44497` with `Authorization: Bearer stevens`. No Anthropic/OpenAI/OpenRouter direct calls. All data fetches were public open-access resources (NCBI, EuropePMC).

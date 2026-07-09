# Artifact Harvest — BVBRC-78

Every public artefact pulled during independent replication.

| Artefact | Source | Accession / URL | Size | Purpose |
|----------|--------|-----------------|------|---------|
| Pubmed eSummary JSON | NCBI eUtils | `esummary.fcgi?db=pubmed&id=36680219` | ~1 kB | metadata |
| Full-text XML | Europe PMC | `europepmc.org/webservices/rest/PMC9860891/fullTextXML` | 193 kB | claims extraction |
| Phage genome | ENA | `CAJDKA010000002.1` (WGS) | 150,836 bp (147 kB compressed) | **target genome** |
| EFDG1 comparator | NCBI nuccore | `NC_029009` | 147,589 bp | Herelleviridae comparator (paper Table 2) |
| EfV12-phi1 comparator | NCBI nuccore | `MH880817` | 152,770 bp | Herelleviridae comparator |
| EFP01 comparator | NCBI nuccore | `NC_047796.1` | 155,053 bp | Herelleviridae comparator |
| iF6 comparator | NCBI nuccore | `MT909815.1` | 156,592 bp | Herelleviridae comparator |
| MDA2 comparator | NCBI nuccore | `MW633168.1` | 140,226 bp | Herelleviridae (Kochikohdavirus, distinct clade) |
| Ec-ZZ2 outgroup | NCBI nuccore | `NC_031260` | 41,170 bp | Siphoviridae outgroup |
| vB_EfaS_Max outgroup | NCBI nuccore | `MK360024` | 40,975 bp | Siphoviridae outgroup |
| EFDG1 major head protein | NCBI protein | `YP_009218324.2` | 473 aa | MCP reference for phylogeny |
| Lambda integrase | NCBI protein | `NP_040604.1` | – | lysogeny marker |
| ϕ80 integrase | NCBI protein | `NP_050146.1` | – | lysogeny marker |
| P22 integrase | NCBI protein | `NP_059583.1` | – | lysogeny marker |
| P22 cI repressor | NCBI protein | `NP_059609.1` | – | lysogeny marker |
| Lambda cI repressor | NCBI protein | `NP_040628.1` | – | lysogeny marker |
| ϕSa3int integrase | NCBI protein | `YP_009641394.1` | – | lysogeny marker |
| L54a integrase | NCBI protein | `YP_240215.1` | – | lysogeny marker |
| Abricate DBs | Torsten Seemann bundle (Homebrew) | card / ncbi / resfinder / argannot / megares / vfdb / victors | 24k sequences | AMR + virulence screen |

## Tools used

| Tool | Version | Source |
|------|---------|--------|
| Prodigal | 2.6.3 | Homebrew |
| ARAGORN | (Homebrew formula `aragorn`) | Homebrew |
| BLAST+ (blastn / blastp / makeblastdb) | 2.16+ | Homebrew |
| Abricate | 1.0.1 | Homebrew |
| MAFFT | 7.526 (segfault — bypassed) | Homebrew |
| BioPython | 1.87 | pip |
| pyrodigal | 3.7.1 | pip |
| Argo LLM proxy | localhost:44497 | OpenClaw managed |
| LLM judges | argo:gpt-5.2, argo:gemini-2.5-pro, argo:claude-sonnet-4.6, argo:gpt-5.4 | Argo (free tier) |

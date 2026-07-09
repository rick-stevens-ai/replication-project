# Artifact Harvest

All artifacts are free/public. No auth required. Pulled 2026-07-04.

| # | Artifact | URL | Size | sha256 |
|---|---|---|---|---|
| A1 | *M. genitalium* G37 RefSeq GenBank (NC_000908.2) | https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=NC_000908.2&rettype=gb&retmode=text | 780,009 B | `50da1e36fb3ebbef2836205130cd7928657b3a3337d650d7b9a6fb1d932c5e5b` |
| A2 | *M. genitalium* G37 RefSeq FASTA (NC_000908.2) | https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=NC_000908.2&rettype=fasta&retmode=text | 588,426 B | `cc21ace789ae96213ab10a595b5f52c870b8218581a0420ba13cee0409d8ccc9` |

Provenance chain:

- Fraser et al. 1995 originally deposited the genome under **L43967** (single contig, 580,070 bp).
- NCBI RefSeq subsequently curated it as **NC_000908** (v2 current, 580,076 bp — 6 bp difference from post-1995 resequencing corrections).
- Assembly accession: **GCF_000027325.1**.
- BioProject: **PRJNA224116** · BioSample: **SAMN02603983**.
- The GenBank record explicitly lists Fraser et al. 1995 *Science* 270:397-403 (PMID 7569993) as REFERENCE 2 for bases 1-580076.

Both files are stored in `work/`. No licensing constraints (NCBI public data).

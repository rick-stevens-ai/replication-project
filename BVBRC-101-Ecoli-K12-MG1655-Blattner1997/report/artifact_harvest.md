# Artifact harvest — Blattner1997 replication

All artifacts pulled via free public endpoints (NCBI E-utilities, PubMed).

## Public data downloads

| Artifact | Source | URL | Size | SHA-256 |
|---|---|---|---|---|
| E. coli K-12 MG1655 chromosome FASTA (NC_000913.3) | NCBI RefSeq via E-utilities | `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=NC_000913.3&rettype=fasta&retmode=text` | 4,708,035 bytes | `6b195feda4c66140f6762742eb8b30c2652f02b45878b174f5b00ef85ecc95d7` |
| E. coli K-12 MG1655 GenBank-with-parts (NC_000913.3) | NCBI RefSeq via E-utilities | `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=NC_000913.3&rettype=gbwithparts&retmode=text` | 11,882,063 bytes | `879738bcb9d5e72c1be77bc8570b41dbf0d8e274bcf70d8a0bcea8d56f6f628c` |

## Paper text access

| Artifact | Source | URL | Status |
|---|---|---|---|
| Blattner et al. 1997 full text | Science.org | `https://www.science.org/doi/10.1126/science.277.5331.1453` | 403 (Cloudflare bot-check) |
| Blattner et al. 1997 abstract | PubMed | `https://pubmed.ncbi.nlm.nih.gov/9278503/` | ✅ retrieved — verbatim source for genome size (4,639,221 bp), CDS count (4,288), and "no attributed function" fraction (38%) |
| rRNA operon count crosscheck | PMC (Murakami 2015 refereed derivation) | `https://pmc.ncbi.nlm.nih.gov/articles/PMC4696680/` | ✅ retrieved — confirms "seven rrn operons" in E. coli K-12 MG1655 |

## Local artifacts produced

| Artifact | Path | Purpose |
|---|---|---|
| Analysis script | `work/analyze.py` | Biopython pipeline: whole-genome G+C, feature counts, mean CDS length, interval-union coding density, replichore-aware co-orientation, start-codon histogram, CDS composition |
| Ground-truth notes | `work/paper_claims.md` | Extracted claims from Blattner 1997 with provenance |
| LLM judge 1 script | `work/judge.py` | Runs verdict via Argo `argo:gpt-5` |
| Metrics JSON | `report/evidence/metrics.json` | All measured vs paper claims |
| Analysis stdout log | `report/evidence/analyze_stdout.txt` | Human-readable run output |
| Judge 1 output | `report/evidence/judge.json` | `argo:gpt-5` verdict + reasoning |
| Judge 2 output | `report/evidence/judge2.json` | `argo:gpt-5.2` verdict + reasoning |

## Endpoint provenance
- **NCBI E-utilities:** free, public, no API key required. Standard NIH-hosted service.
- **PubMed:** free, public.
- **Argo LLM proxy:** localhost:44497 (bearer `stevens`) — Argonne-internal, no cost.

## What was *not* used
- No paid endpoints (no Anthropic/OpenAI/OpenRouter direct calls).
- No BV-BRC compute (this is a lightweight local replication).
- No HPC (uicgpu / Polaris) — analysis runs in seconds on local CPU.

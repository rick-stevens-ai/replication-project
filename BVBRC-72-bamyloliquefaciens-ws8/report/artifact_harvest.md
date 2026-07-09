# artifact_harvest — BVBRC-72

All public artifacts pulled during this replication.

## Paper

| Artifact | URL | Size / accession | Provenance |
|---|---|---|---|
| PubMed abstract | https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=31601062&rettype=abstract | ~2 kB text | NCBI E-utils |
| Europe PMC full-text XML | https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9728402/fullTextXML | 106,646 bytes | Europe PMC OA |
| Full-text plain (stripped) | work/paper/paper.txt | 39,735 chars | local strip of XML |
| Semantic Scholar record | https://api.semanticscholar.org/graph/v1/paper/PMID:31601062 | JSON | S2 API (with API key) |

## Genome

| Artifact | URL / accession | Size | Provenance |
|---|---|---|---|
| GenBank flat file | efetch db=nuccore id=CP018200.1 rettype=gbwithparts | 9,086,126 bytes | NCBI |
| FASTA | efetch db=nuccore id=CP018200.1 rettype=fasta | 3,986,007 bytes | NCBI |
| Assembly esummary | https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=assembly&id=934961 | JSON | NCBI |
| Reference type strain (FZB42) | efetch db=nuccore id=CP000560.1 rettype=fasta | 3,974,654 bytes | NCBI (for comparative context) |

**Accessions:**
- GenBank: `CP018200.1` (WS-8 chromosome, 3,929,787 bp, circular)
- RefSeq: `NZ_CP018200.1`
- Assembly (GenBank / RefSeq): `GCA_001922005.1` / `GCF_001922005.1`
- BioProject (GenBank): `PRJNA354791`
- BioProject (RefSeq): `PRJNA224116`
- BioSample: `SAMN06051297`

## Analysis tool artifacts

| Artifact | Source | Location |
|---|---|---|
| antiSMASH v7.1.0 result (web submission) | https://antismash.secondarymetabolites.org/upload/bacteria-68b5c4f0-b473-406b-9925-d81e0478ff84/ | work/antismash_result/ (regions.js, CP018200_antismash.json, CP018200_antismash.gbk, index.html, antismash.log) |
| antiSMASH v8.0.4 local run | uicgpu:/data/stevens/envs/antismash | work/antismash8_out/ (CP018200.gbk, CP018200.json, knownclusterblast/*.txt, index.html) |
| Biopython 1.83 genome stats | work/genome_stats.py | report/evidence/genome_stats.json |
| BGC gene-name scan | work/bgc_gene_scan.py | report/evidence/bgc_gene_scan.json |
| NRPS/PKS proximity clustering | work/nrps_pks_scan.py | report/evidence/nrps_pks_scan.json |
| antiSMASH region ↔ CDS gene mapper | work/bgc_identity_map.py | work/bgc_identity_map.json |
| LLM judge (argo:gpt-5.2 via Argo proxy :44497) | work/judge.py | report/evidence/llm_judge_result.json |

## Compute hosts

| Host | Role |
|---|---|
| CherryRd (Mac Studio, macOS) | Orchestration, S2/E-utils lookups, LLM judge (Argo proxy tunneled from studio-ts on localhost:44497), report writing |
| uicgpu (8×A100, Ubuntu, <tailnet-aggregator>) | Heavy computes: NCBI Datasets pulls, GenBank parsing, antiSMASH v8.0.4 local run |

## Endpoints used (all FREE)

- NCBI E-utils (public, no auth)
- Europe PMC full-text REST (public, no auth)
- Semantic Scholar Graph v1 (S2 API key from macOS keychain)
- antiSMASH web submission (public web service, secondarymetabolites.org, api/v1.0)
- antiSMASH v8.0.4 local install on uicgpu (no external calls)
- Argo proxy for LLM judge (localhost:44497, key=stevens, model=argo:gpt-5.2)

No paid endpoints, no OpenAI/Anthropic/OpenRouter direct calls.

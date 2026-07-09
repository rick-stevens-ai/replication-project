# Artifact Harvest — BVBRC-33

| Artifact | Source / URL | Accession / ID | Size | Notes |
|---|---|---|---|---|
| Paper full text (JATS XML) | Europe PMC REST | PMC9137517 | 176 KB | `work/eupmc.xml`; MDPI PDF was bot-blocked (411 B), used Europe PMC + PMC HTML instead |
| Paper (PMC HTML) | pmc.ncbi.nlm.nih.gov | PMC9137517 | 276 KB | `work/pmc.html` |
| Paper metadata | Semantic Scholar Graph API (x-api-key) | DOI 10.3390/antibiotics11050596; PMID 35625240; CorpusId 248463036 | — | Cites ~37; venue *Antibiotics* 2022 |
| **Study genome (isolate 9KP)** | **NCBI Datasets REST** (free, no auth) | **GCA_022511605.1** (=GCF_022511605.1); BioProject **PRJNA767482**; BioSample **SAMN26332310**; WGS **JAKWFM000000000** | 3.06 MB zip | `work/9KP/` — 5,364,730 bp, 83 contigs, GC 57.33%, N50 220,979; submitter King Abdulaziz University; Illumina |
| Kleborate DBs | pip `kleborate` v3 (kpsc preset) | — | — | bundled minimizer/MLST/Kaptive DBs |
| AMRFinderPlus DB | `amrfinder -u` | DB **2026-05-15.1** | — | bioconda `ncbi-amrfinderplus` 4.2.7 |
| blaCTX-M-15 ref | NCBI nuccore efetch | NG_048935.1 | 1 KB | `work/refs/blaCTX-M-15.fna` (for absence check) |

## Tool versions
- Kleborate v3 (kpsc preset) — pip, in `work/venv`
- AMRFinderPlus 4.2.7 (DB 2026-05-15.1) — bioconda env `kleb`
- minimap2 2.31-r1302, mash, BLAST+ 2.17.0 — bioconda env `kleb`
- Biopython (genome stats)
- LLM judge: `argo:claude-opus-4.8` returned HTTP 502 (proxy bug) → fell back to **`argo:gpt-5.2`** (free Argo), per wave rule.

## Genome checksum
See `work/9KP/md5sum.txt` (NCBI-provided) for the downloaded package MD5s.

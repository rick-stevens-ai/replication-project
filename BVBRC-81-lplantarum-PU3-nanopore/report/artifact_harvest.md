# Artifact Harvest — BVBRC-81

All artifacts fetched 2026-07-03.

## Primary paper

| Item | Source | URL / accession | Size |
|---|---|---|---|
| PubMed abstract | NCBI EUtils efetch | PMID:37894099 | ~4 KB |
| Full-text article XML | Europe PMC REST | https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10609609/fullTextXML | 200,906 B |

MDPI PDF (`https://www.mdpi.com/2076-2607/11/10/2440/pdf`) is Akamai-blocked from both CherryRd and uicgpu ("Access Denied"); we use the Europe PMC full-text XML instead, which contains the complete article text.

## Genome accessions (NCBI Nucleotide)

BioProject: **PRJNA946199**  ·  BioSample: **SAMN33818264**  ·  Assembly: **GCA_045010995.1** (`PU_LacPla_1`)

| Accession | Molecule | Length (bp) | GC (%) |
|---|---|---|---|
| CP120642.1 | chromosome, circular | 3,180,940 | 44.66 |
| CP120643.1 | plasmid unnamed2 | 44,900 | 39.00 |
| CP120644.1 | plasmid unnamed3 | 42,197 | 39.94 |
| CP120645.1 | plasmid unnamed4 | 40,483 | 39.77 |
| CP120646.1 | plasmid unnamed5 | 25,867 | 41.09 |
| CP120647.1 | plasmid unnamed6 | 13,241 | 39.27 |
| CP120648.1 | plasmid unnamed7 | 8,689 | 35.93 |
| CP120649.1 | plasmid unnamed8 | 8,053 | 35.23 |
| CP120650.1 | plasmid unnamed9 | 6,492 | 35.32 |
| CP120651.1 | plasmid unnamed10 | 3,512 | 37.30 |
| **TOTAL** | | **3,374,374** | **44.34 (weighted)** |

Fetched via NCBI EUtils `efetch` in FASTA + GenBank; combined FASTA is `work/genome/PU3_all.fasta` (3.4 MB), GenBank is `work/genome/PU3_all.gb` (7.9 MB).

## Reference genomes for comparison

| Genome | Assembly | Purpose | Size (bp) |
|---|---|---|---|
| *L. plantarum* M19 | GCA_018588605.2 | Paper's top ANI hit (99.60%) | ~3.5 MB |
| *L. plantarum* WCFS1 | GCF_000203855.3 | Type / reference strain | ~3.4 MB |

Fetched from NCBI genomes FTP to `uicgpu:/data/stevens/replicate/BVBRC-81/refs/`.

## BV-BRC record

- Genome ID **1590.5192** (L. plantarum PU3), pulled via BV-BRC API (`/api/genome/1590.5192`)
- Confirms all 10 GenBank accessions, PRJNA946199, Nanopore MinION platform, Flye assembly, Bulgaria origin, human host, 44.34% GC, complete status.
- Specialty-gene tables (`sp_gene`): 3 low-quality "Victors" virulence hits on housekeeping metabolic enzymes (guaA, carB, guaA); 30 PATRIC AMR "paralog-of-known-target" hits, all housekeeping/translation genes (rpoB, gyrA, EF-Tu, etc.) — consistent with paper's "no true virulence factors" claim.

## Tools used (all versions logged)

- Prokka 1.14.6 (installed in `/data/stevens/envs/bvbrc28`, uicgpu)
- Mash 2.3
- FastANI (bioconda default)
- Abricate 0.5 (bundled DBs: CARD 2017-07-08, VFDB 2017-03-17, ResFinder 2017-07-08, ARG-ANNOT 2017-07-08)
- Python 3 (custom FASTA GC counter)
- Argo LLM proxy (localhost:44497, models: gpt-4o, gpt-5, gemini-2.5-pro — free/institutional)

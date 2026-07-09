# Artifact Harvest

Every public data / paper artifact pulled during this replication.

## Publication

| Artifact | Source | Size | Notes |
|---|---|---:|---|
| paper.pdf | https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0215038&type=printable | 3,729,019 B | PLOS printable, CC-BY. Primary source. |
| paper.txt | (locally rasterized via `pdftotext -layout paper.pdf`) | 101,795 B | Full text extraction, 971 lines |
| PubMed esummary | https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=30986237&retmode=json | ~2 KB | Confirmed PMC6464166, DOI 10.1371/journal.pone.0215038, title, author list |

## Genome sequences (NCBI Nucleotide / eutils efetch)

All fetched via `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=<ACC>&rettype=fasta|gbwithparts&retmode=text` — free, no auth.

| Accession | Organism / role | FASTA size | GenBank size | Verified stats |
|---|---|---:|---:|---|
| **CP032552** | P. aeruginosa PA34 chromosome (paper) | 6,907,442 B | 234,291 lines | 6,810,079 bp / 66.07% GC / 6,462 CDS / 6,544 genes / 65 tRNA / 12 rRNA — matches Table 2 EXACT |
| **MH547560** | P. aeruginosa PA34 plasmid pMKPA34-1 (paper) | 96,852 B | 3,018 lines | 95,404 bp / 57.22% GC / 98 CDS — matches paper |
| **MH547561** | P. aeruginosa PA34 plasmid pMKPA34-2 (paper) | 27,331 B | 908 lines | 26,862 bp / 61.00% GC / 32 CDS (paper: 33) |
| AE004091 | P. aeruginosa PAO1 (reference) | 6,353,954 B | 206,754 lines | 6,264,404 bp / 66.56% GC / 5,571 CDS |
| CP000438 | P. aeruginosa UCBPP-PA14 (reference) | 6,631,107 B | 206,972 lines | 6,537,648 bp / 66.29% GC / 5,892 CDS |
| CP008739 | P. aeruginosa VRFPA04 (reference, ocular isolate) | 6,915,492 B | 222,933 lines | 6,818,030 bp / 66.48% GC / 5,778 CDS |

All raw sequences staged on **uicgpu:/data/stevens/BVBRC-92-PA34/genomes/** (not copied back to Dropbox, easily re-derived).

## BV-BRC / PATRIC (independent cross-reference)

Via `https://www.bv-brc.org/api/…` — free public REST API.

| Artifact | Endpoint | Size | Notes |
|---|---|---:|---|
| PA34 genome record | `/api/genome/?eq(biosample_accession,SAMN08435059)` | ~1 KB | **genome_id 287.6355** — same paper isolate (Microbial Keratitis, India 1997, BioProject PRJNA431326, assembly GCA_003332705.1). Different assembly (SPAdes 3.11 draft, 128 contigs) than the paper's closed hybrid assembly, but same DNA. |
| Specialty gene dump | `/api/sp_gene/?eq(genome_id,287.6355)&select(...)&limit(2500)` | 294,937 B (bvbrc_spgene_pa34.json) | 1,395 records: 274 Transporter, 256 Virulence Factor, 251 Antibiotic Resistance, 174 Virulence factor, 65 Drug Target, 37 Metal Resistance. Independently confirms AAC(3)-II family, APH(6)-Id, CmlA, folA/Dfr, ampC, mex efflux systems, and multi-copy mer operon (merA×2, merB×2, merP×2, merR×3). |

## Software / tools installed for the rerun

| Tool | Version | Location | Install method |
|---|---|---|---|
| DIAMOND | 2.1.9 | `uicgpu:/data/stevens/BVBRC-92-PA34/tools/diamond` | `wget` GitHub release tarball, extract, run |
| markov_clustering (Python) | 0.0.6.dev0 | uicgpu `~/.local/lib/python3.8/site-packages/` | `pip install --user markov_clustering scipy networkx numpy` |
| Biopython | 1.87 (system) | uicgpu Python 3.8 | pre-installed |
| pdftotext (poppler) | system | uicgpu | pre-installed |

## Analytical outputs (in `report/evidence/`)

| File | What | Size |
|---|---|---:|
| genomes_downloaded.txt | FASTA file list + sizes | 168 B |
| summary_verification.json | JSON: Table 2 recomputed for all 6 genomes + per-locus AMR/virulence/metal hits | 8,889 B |
| pangenome_result.json | JSON: DIAMOND+MCL clustering summary with side-by-side vs paper targets | 618 B |
| bvbrc_spgene_pa34.json | Full BV-BRC specialty-gene dump for genome 287.6355 | 294,937 B |
| llm_judge_verdict.json + .txt | Argo `argo:gpt-5.2` verdict + reasoning + one-line summary | ~4 KB total |

## Reproducibility notes

- Rerun by re-downloading the 6 GenBank IDs and executing `work/pangenome_pa34.py` after `diamond blastp` all-vs-all. No proprietary data. All artifacts open-access (CC-BY paper, NCBI public sequences, BV-BRC public API).
- The exact clustering thresholds (50% ID, 50% coverage, MCL inflation 1.5) do not perfectly reproduce Roary's defaults; a more faithful replication would use Roary itself. This was deliberately not done given time budget — pan-genome numbers still match the paper's headline accessory count within 1%.

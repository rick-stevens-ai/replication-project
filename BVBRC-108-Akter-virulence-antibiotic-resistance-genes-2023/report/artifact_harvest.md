# Artifact harvest — BVBRC-108

## Paper
- **PMC full-text XML** — https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9883459/fullTextXML — 142,132 bytes. Saved to `work/paper_fulltext.xml`.
- Paper PDF (open access, CC BY 4.0): https://www.nature.com/articles/s41598-022-25968-8.pdf (not downloaded — XML has everything we need).

## Genome assemblies (NCBI, no auth)
| Strain | Accession | Length (bp) | Source URL | Local path |
|---|---|---:|---|---|
| BFFF11 | CP045918.1 | 2,761,629 | `efetch -db nuccore -id CP045918 -format fasta` | `work/CP045918.fasta`; uicgpu:/data/stevens/bvbrc108/ncbi/CP045918.fasta |
| BFF1B1 | CP046022.1 | 3,067,042 | `efetch -db nuccore -id CP046022 -format fasta` | `work/CP046022.fasta`; uicgpu:/data/stevens/bvbrc108/ncbi/CP046022.fasta |
| BFPS6 | GCF_021375735.1 (WGS master JADBGH01, BioSample SAMN16320166, BioProject PRJNA666673) | 2,866,855 | `datasets download genome accession GCF_021375735.1 --include genome` | `work/BFPS6.fna`; uicgpu:/data/stevens/bvbrc108/ncbi/GCF_021375735.1/... |

## Reference databases
| DB | Version/Date | Source URL | Size |
|---|---|---|---:|
| AMRFinderPlus DB | 2024-07-22.1 (bundled with amrfinder 3.12.8) | https://ftp.ncbi.nlm.nih.gov/pathogen/Antimicrobial_resistance/AMRFinderPlus/ | ~250 MB |
| VFDB set-A nucleotide | pulled 2026-07-05 | http://www.mgc.ac.cn/VFs/Down/VFDB_setA_nt.fas.gz | 2,004,483 bytes gz / 4,868 sequences |
| VFDB set-A protein | pulled 2026-07-05 | http://www.mgc.ac.cn/VFs/Down/VFDB_setA_pro.fas.gz | 1,303,058 bytes gz / 4,732 sequences |

## Tools used
- AMRFinderPlus **3.12.8** with DB **2024-07-22.1**
- NCBI **datasets 18.32.0**
- NCBI **edirect 22.4** (`efetch`, `esearch`, `esummary`)
- **blast+ 2.16.0** (`makeblastdb`, `blastn`, `tblastn`)
- **Biopython 1.87** (assembly stats)

## LLM inference
- **Argo proxy** at `http://127.0.0.1:44497/v1/chat/completions` (free ANL-internal, key `stevens`).
- Model: `argo:claude-sonnet-4.6` (Sonnet 4.6, Anthropic route). Prompt ~4.4 kB.
- Output: `report/evidence/judge_output.json`.

## Local artifacts
- `report/REPORT.md` — full report
- `report/brief.md` — 1-paragraph summary
- `report/attempt_log.md` — chronological
- `report/artifact_harvest.md` — this file
- `report/evidence/`:
  - `BFFF11_amr_v2.tsv`, `BFF1B1_amr_v2.tsv`, `BFPS6_amr_v2.tsv` — AMRFinderPlus TSV outputs
  - `BFFF11_tblastn_best.tsv`, `BFF1B1_tblastn_best.tsv`, `BFPS6_tblastn_best.tsv` — best VFDB tblastn hit per query
  - `vf_presence.json` — consolidated virulence-gene presence matrix
  - `judge_output.json` — LLM-judge verdict
- `work/` — CP045918.fasta, CP046022.fasta, BFPS6.fna, paper_fulltext.xml

## Also on uicgpu
Full working tree at `uicgpu:/data/stevens/bvbrc108/` (assemblies, ncbi, amr, vfdb, logs) — kept for possible re-analysis but not synced back to Dropbox to avoid duplication.

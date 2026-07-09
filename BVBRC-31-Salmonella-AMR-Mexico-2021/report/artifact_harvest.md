# Artifact Harvest — BVBRC-31

Every public artifact pulled during this replication.

## Paper + supplements
| Artifact | Source | Size |
|---|---|---|
| Full-text XML | Europe PMC `PMC8099073/fullTextXML` | 297 KB |
| OA PDF | journals.plos.org printable (DOI 10.1371/journal.pone.0243681) | 2.9 MB |
| Supplementary bundle (S1–S10 + figs/tables) | Europe PMC `PMC8099073/supplementaryFiles` | 8.7 MB zip |
| **S1 File** `pone.0243681.s001.xlsx` | 77 study isolates: BioSample, SRR, serovar, source, host, assembly stats | 20 KB |
| S2 File `pone.0243681.s002.xlsx` | 2400 public Mexico NTS genomes (comparison set) | 146 KB |
| S3 File `pone.0243681.s003.xlsx` | Typhimurium MX set | 15 KB |

## Genomes (NCBI, BioProject PRJNA480281)
- **68 GenBank assemblies** (of 77 study isolates) downloaded via NCBI Datasets v2alpha REST / `datasets` CLI. Free, no auth. Total ~97 MB.
- Accession list: `work/assembly_list.txt`; BioSample→assembly map: `work/biosample_to_assembly.csv`.
- 9 isolates lacked GenBank assemblies at query time (SRR reads still public; not pulled this pass): SAMN12345832, SAMN12345840, SAMN15872719–725.
- Representative accessions: LF-Typhimurium GCA_008779455.1 (SGI1+), GCA_008779395.1, GCA_008779375.1, GCA_008779555.1, GCA_008778285.1, GCA_008778075.1; London GCA_007738755.1.

## Tools / databases (free)
| Tool | Version | Source | DB |
|---|---|---|---|
| AMRFinderPlus | 3.12.8 | bioconda | 2024-07-22.1 (paper used 3.8.4) |
| SeqSero2 | 1.3.2 | bioconda | (paper used SeqSero 1.2) |
| mlst (T. Seemann) | 2.35.0 | bioconda | PubMLST *Salmonella* scheme |
| ncbi-datasets-cli | 18.32.0 | bioconda | — |
| micromamba | 2.8.1 | micro.mamba.pm | — |
| COBRApy/scipy | (scipy for χ²) | PyPI | — |

## Compute
- uicgpu (uicgpu01): 255 cores, 2 TB RAM. AMRFinder+SeqSero2+MLST for 68 genomes ≈ a few minutes wall-clock (16-way parallel).
- No GPU required; no paid resources; LLM judge via free Argo proxy (argo:gpt-5.2).

## Local outputs (this dir)
- `report/evidence/analysis_results.json` — full machine-readable result bundle.
- `report/evidence/per_isolate.csv` — 68 isolates × serovar/ST/AMR-classes/MDR.
- `report/evidence/amrfinder_raw.tar.gz` — all 68 raw AMRFinder TSVs.
- `report/evidence/mlst_all.tsv` — raw MLST output.
- `report/evidence/judge_verdict.json` — LLM-judge scoring.
- `work/` — assemblies list, scripts (analyze.py, judge.py, run_amr.sh, run_typing.sh), supplements, paper.pdf.

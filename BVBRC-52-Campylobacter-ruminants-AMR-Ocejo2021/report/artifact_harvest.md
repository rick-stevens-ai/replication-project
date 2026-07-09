# Artifact Harvest — BVBRC-52

All artifacts are public and were downloaded independently. Raw reads + assemblies retained on uicgpu at `/data/stevens/bvbrc52-campy/`.

## Paper + supplements (Europe PMC, CC BY 4.0)
| Artifact | URL | Notes |
|---|---|---|
| Full-text JATS XML | https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8076188/fullTextXML | 125 KB; source of data-availability + methods |
| Supplementary zip (figs + MOESM1) | https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8076188/supplementaryFiles | 529 KB; contains Tables S1–S4 PDF |
| Supplement PDF (MOESM1) | 41598_2021_88318_MOESM1_ESM.pdf (in zip) | Tables S1 (metadata/ST/phenotype), S2 (assembly stats) extracted via pdftotext |
| DOI | https://doi.org/10.1038/s41598-021-88318-0 | Sci Rep 11:8998 (2021) |

## Sequence data (NCBI/ENA — BioProject PRJNA689687)
- Full run table: `https://www.ebi.ac.uk/ena/portal/api/filereport?accession=PRJNA689687&result=read_run&...` → 70 runs (40 C. jejuni, 30 C. coli), SRR13362733–SRR13362802, BioSamples SAMN17214743–SAMN17214812.
- Raw paired FASTQ downloaded (ENA FTP over HTTPS) for the 16-isolate panel:

| Strain | Run | Species |
|---|---|---|
| C0140 | SRR13362734 | C. coli |
| C0541 | SRR13362796 | C. coli |
| C0680 | SRR13362740 | C. coli |
| C0025 | SRR13362735 | C. coli |
| C0663 | SRR13362747 | C. coli |
| C0551 | SRR13362790 | C. coli |
| C0673 | SRR13362743 | C. coli |
| C0444 | SRR13362736 | C. coli |
| C0430 | SRR13362749 | C. coli |
| C0585 | SRR13362770 | C. jejuni |
| C0642 | SRR13362755 | C. jejuni |
| C0612 | SRR13362764 | C. jejuni |
| C0437 | SRR13362738 | C. jejuni |
| C0268 | SRR13362793 | C. jejuni |
| C0882 | SRR13362739 | C. jejuni |
| C0574 | SRR13362778 | C. jejuni |

FASTQ URL pattern: `https://ftp.sra.ebi.ac.uk/vol1/fastq/SRR133/0NN/<RUN>/<RUN>_{1,2}.fastq.gz` (~330–530 MB per pair gz).

## Reference genome
| Artifact | Accession | Source | Use |
|---|---|---|---|
| C. jejuni NCTC 11168 | GCF_000009085.1 (ASM908v1) | NCBI `datasets download genome accession` | WT reference for gyrA(Thr86)/rpsL(Lys43)/23S extraction |

## Databases (via ABRicate v1.0.0, 2026-Apr builds)
ResFinder (3206 seq), NCBI (8232), CARD (6052), ARG-ANNOT (2224), MEGARes (6635), PlasmidFinder (488), VFDB. MLST: `campylobacter` 7-gene scheme (PubMLST).

## Tool versions
- SPAdes (bvbrc38), fastp (bvbrc38/bvbrc14), ABRicate v1.0.0 (bvbrc14), mlst (bvbrc14), BLAST+ (blastn/tblastn/makeblastdb, bvbrc14), NCBI datasets (bvbrc28), Biopython 1.87 (bvbrc38), pdftotext (poppler, local CherryRd).

## Derived evidence (report/evidence/)
- `RESULTS.json` — per-isolate assembly/mlst/point-mutation/AMR-gene summary.
- `asm_stats.json` / `my_asm_stats.json` — my de-novo assembly statistics.
- `paper_tableS1.json` / `paper_tableS2.json` — parsed paper ground truth.
- `pointmut.json` — gyrA86 / rpsL43 / 23S calls.
- `genotype_vs_phenotype.csv` — full comparison table.
- `concordance.json` / `concordance_corrected.json` — TP/TN/FP/FN scoring.
- `evidence_tetO_reads.json` — raw-read tet(O) confirmation for the 3 assembly-dropout isolates.
- `amr/summary_ncbi.tab`, `amr/summary_resfinder.tab`, `mlst/mlst_auto.tab` — tool outputs.
- `judge_output.txt`, `judge_opus.txt` — LLM-judge transcripts.
- `logs/pipeline.out` — full pipeline execution log.
- Full per-isolate abricate tabs archived in `work/amr_tabs/`.

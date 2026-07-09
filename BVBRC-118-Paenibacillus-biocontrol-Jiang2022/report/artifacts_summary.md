# Artifacts Summary — BVBRC-118

## Inputs (pulled from public sources)

| Artifact | Source URL | Size | Checksum |
|---|---|---:|---|
| `paper.pdf` | https://bmcgenomics.biomedcentral.com/counter/pdf/10.1186/s12864-022-08330-0.pdf | 9,991,602 B | (BMC OA canonical) |
| `SRR10363117.sra` (staged on uicgpu) | https://sra-pub-run-odp.s3.amazonaws.com/sra/SRR10363117/SRR10363117 | 329,222,294 B | matches SRA record byte-count |
| `SRR10363117.fastq` (derived on uicgpu) | fasterq-dump 3.4.1 output | 2,619,753,090 B | 183,095 reads / 1,302,748,453 bp |
| `references/IBSD35.fna` | https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/002/937/395/GCF_002937395.1_ASM293739v1/GCF_002937395.1_ASM293739v1_genomic.fna.gz | 5,941,734 B (unpacked) | (NCBI RefSeq) |
| `references/HS311.fna` | https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/001/272/655/GCF_001272655.2_ASM127265v2/GCF_001272655.2_ASM127265v2_genomic.fna.gz | 6,297,727 B (unpacked) | (NCBI RefSeq) |
| `references/ZF390.fna` | https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/014/692/735/GCF_014692735.1_ASM1469273v1/GCF_014692735.1_ASM1469273v1_genomic.fna.gz | 6,464,120 B (unpacked) | (NCBI RefSeq) |

Accessions consulted:
- BioProject: `PRJNA580302` (Paenibacillus peoriae strain HJ-2 Genome sequencing and assembly)
- BioSample: `SAMN13155059` (jiang-HJ-2)
- SRA Experiment: `SRX7071172` (PacBio Sequel, HanJiang Normal university, PI Aiming Jiang)
- SRA Run: `SRR10363117`
- 16S rRNA: `MK911741.1` (partial, 1,461 bp)
- (No Assembly/RefSeq accession — never deposited)

## Local derived artifacts (in this repo)

| Path | Bytes | Notes |
|------|------|-------|
| `paper.pdf` | 9,991,602 | Source PDF |
| `paper.txt` | ~85 KB | pdftotext layout dump |
| `extraction/marker.md` | 34,844 | Marker 1.11 structured MD |
| `extraction/nougat.mmd` | 64,387 | Nougat mmd |
| `work/assembly/HJ2_flye.fasta` | 6,107,319 | Flye 2.9.6 polished contig |
| `work/assembly/assembly_info.txt` | 93 | contig metadata (circ=Y, cov=205) |
| `work/annotation/HJ2.gff` | 7,312,462 | Prokka GFF3 |
| `work/annotation/HJ2.tsv` | 339,194 | Prokka TSV feature table |
| `work/annotation/HJ2.txt` | 119 | Prokka summary stats |
| `work/antismash/HJ2.json` | (large) | antiSMASH 8 raw JSON w/ knownclusterblast |
| `work/antismash/HJ2.gbk` | (large) | antiSMASH annotated GenBank |
| `work/antismash/contig_1.region0*.gbk` | 19 files | per-region annotated GBKs |
| `work/antismash/knownclusterblast/*.txt` | 19 files | MIBiG match tables |
| `report/REPORT.md` | 11,192 | Full Markdown report (this file's sibling) |
| `report/REPORT.tex` | ~9 KB | Detailed LaTeX report |
| `report/brief.md` | 1,367 | 1-paragraph what/why |
| `report/attempt_log.md` | 2,943 | Chronological log |
| `report/artifact_harvest.md` | (this) | Alias for artifacts_summary.md |
| `report/workflow.md` | 5,950 | Workflow diagram + tool table + effort |
| `report/failure_analysis.md` | (see) | Honest analysis of gaps/friction |
| `report/open_questions.json` | 6,167 | 5 heavy-duty questions with next_steps |
| `report/evidence/assembly_metrics.json` | 671 | Structured metric deltas |
| `report/evidence/annotation_metrics.json` | 613 | Structured metric deltas |
| `report/evidence/antismash_regions.tsv` | 1,495 | 19-region cluster table w/ MIBiG hits |
| `report/evidence/ani_results.tsv` | 395 | skani + mash ANI matrix |
| `report/evidence/rotation_analysis.txt` | 1,090 | Circular-origin offset analysis |
| `report/evidence/llm_judge_scoring.json` | ~3 KB | Argo Opus 4.6 verdict JSON |
| `report/evidence/flye_assembly_info.txt` | 93 | Copy of Flye assembly_info |
| `report/evidence/prokka_stats.txt` | 119 | Copy of Prokka stats |

## Remote artifacts (uicgpu `/data/stevens/bvbrc118/`)

- Full Flye output tree (`assembly/flye/`) incl. `assembly_graph.gfa`, `assembly_graph.gv`, `40-polishing/` intermediates.
- Full Prokka output (`annotation/prokka/`) incl. `.gbk`, `.sqn`, `.fsa`, `.ffn`, `.faa` (5244 protein FASTA).
- Both antiSMASH runs (`antismash/run1`, `antismash/run2`) w/ HTML report + per-region HTML/GBK.
- SRA raw + fastq (`sra/SRR10363117.sra`, `sra/SRR10363117.fastq`).
- Reference genomes (`references/*.fna`).
- Logs (`logs/*.log`) for every tool invocation.

Everything under `/data` is on HOT NVMe; can be archived to `/gpustor` if space pressure develops. All results deterministic given identical tool versions and thread count.

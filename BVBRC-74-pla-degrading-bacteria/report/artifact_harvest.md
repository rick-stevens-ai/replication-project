# Artifact Harvest — BVBRC-74

All artifacts fetched from public endpoints; no logins or API keys required beyond NCBI's public E-utils and ENA HTTPS.

## Paper

| Item | URL | Size |
|------|-----|------|
| PubMed abstract PMID 34299026 | https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=34299026&rettype=abstract | 1.4 KB (`work/pubmed_34299026.txt`) |
| Europe PMC full-text XML PMC8305213 | https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8305213/fullTextXML | 244 KB (`work/europepmc.xml`) |
| Extracted plain text | (local) | 77 KB (`work/paper_text.txt`) |

## Raw Illumina reads (paper's own data)

| SRA run | BioSample | Strain | Layout | Spots | Bases | Downloaded |
|---------|-----------|--------|--------|-------|-------|------|
| **SRR7264117** | SAMN09356180 | Sphingobacterium sp. S2 | Paired MiSeq | 2,768,958 | 1.38 Gb | not downloaded (compute budget) |
| **SRR7264118** | SAMN09356181 | P. aeruginosa S3 | Paired MiSeq | 2,635,837 | 1.32 Gb | ✅ 460 MB + 495 MB gz (`work/reads/SRR7264118_{1,2}.fastq.gz`) |
| **SRR14203690** | SAMN18698529 | Geobacillus sp. EC-3 | Paired MiSeq | 5,730,761 | 2.87 Gb | ✅ 955 MB + 1067 MB gz (`work/reads/SRR14203690_{1,2}.fastq.gz`) |

Source: `https://ftp.sra.ebi.ac.uk/vol1/fastq/SRR726/00X/SRR7264118/SRR7264118_[12].fastq.gz` etc.

## Reference genomes (RefSeq)

| Accession | Organism | Type | Length | GC | FASTA md5 |
|-----------|----------|------|-------:|:--:|-----------|
| GCF_000750905.1 | *Pseudomonas aeruginosa* PSE305 | complete | 6,762,448 bp | 65.31 % | `work/refs/PSE305_paeruginosa.fna.gz` (1.92 MB) + gbff (17.3 MB) |
| GCF_000236605.1 | *Geobacillus thermoleovorans* CCB_US3_UF5 | complete | 3,596,620 bp | 52.28 % | `work/refs/CCB_US3_UF5_gthermoleovorans.fna.gz` (1.06 MB) + gbff (9.5 MB) |
| GCF_901482695.1 | *Sphingobacterium thalpophilum* NCTC11429 | complete | 5,962,893 bp | 43.64 % | `work/refs/NCTC11429_sthalpophilum.fna.gz` (1.78 MB) + gbff (15.2 MB) |
| GCF_000686625.1 | *Sphingobacterium thalpophilum* DSM11723 | draft (31 contigs) | 5,904,341 bp | 43.57 % | `work/refs/DSM11723_sthalpophilum.fna.gz` (1.77 MB) + gbff (14.2 MB) |

Source: `https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/...`

## Derived artifacts

| File | Description |
|------|-------------|
| `work/asm/s3_paeruginosa_spades/scaffolds.fasta` | Our independent SPAdes 4.3.0 --isolate assembly of S3 (509 scaffolds / 6.71 Mb) |
| `work/asm/s3_paeruginosa_spades/scaffolds_500.fasta` | ≥500 bp filter (103 scaffolds / 6.54 Mb / 66.19 % GC) |
| `work/asm/s3_paeruginosa_spades/prodigal.{gff,faa,fna}` | Prodigal V2.60 gene predictions (6,085 CDS) |
| `work/refs_16s/*_16s.fasta` | 16S rRNA sequences extracted from 4 references |
| `work/s3_16s.fasta` | 16S extracted from our S3 assembly (from NODE_42, 1536 bp) |
| `work/pse305_enzymes.faa` | 283 CDS from PSE305 matching hydrolase/lipase/esterase/protease/cutinase/depolymerase/oxygenase/catalase product-strings |
| `report/evidence/ref_genome_stats.json` | Per-reference contigs / bp / GC / longest / N50 |
| `report/evidence/enzyme_counts.json` | Per-reference enzyme-category CDS counts |
| `report/evidence/s3_spades_assembly.json` | Full stats + comparison to paper's Table 1 |
| `report/evidence/s3_enzyme_recovery.json` | tblastn recovery per enzyme class |
| `report/evidence/s3_pla_enzyme_blast.txt` | Raw BLAST tabular output |
| `report/evidence/llm_judge_verdict.json` | LLM verdict (argo:gpt-5.2) |

## Scripts

All in `work/`:

- `fetch_refs.sh` — downloads 4 reference FNA
- `fetch_refs_gbk.sh` — downloads 4 reference GBFF
- `run_spades_s3.sh` — the actual SPAdes invocation
- `ref_gc_check.py` — computes reference stats
- `extract_16s.py` — pulls 16S rRNA features
- `enzyme_count.py` — enzyme categories in each reference
- `enzyme_recip.py` — tblastn PSE305 enzymes → S3 assembly
- `find_16s_s3.py` — extracts + BLASTs 16S from S3 assembly
- `analyze_s3_assembly.py` — full S3 assembly stats
- `judge.py` — LLM judge via Argo

## Not fetched (kept short for time budget)

- S2 SPAdes assembly (would need ~1 GB reads + 20 min compute)
- EC-3 SPAdes assembly (reads staged in `work/reads/`; needs ~20 min compute)
- PATRIC/BV-BRC re-annotation with RASTtk (would need PATRIC account)
- MAUVE / MeDuSa scaffolding of our S3 assembly against PSE305 (to test contig-count claim more directly)

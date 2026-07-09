# Artifacts Summary — BVBRC-41 (*S. algae* 2NE11 replication)

## Directory Tree

```
BVBRC-41-Shewanella-algae-2NE11-genome-2022/
├── report/
│   ├── REPORT.md                      # primary Markdown report (verdict: REPLICATED)
│   ├── REPORT.tex                     # LaTeX typeset version
│   ├── open_questions.json            # 5 open scientific questions + next steps
│   ├── workflow.md                    # replication workflow, tools, work estimate
│   ├── artifacts_summary.md           # this file
│   ├── failure_analysis.md            # honest failure/limitation analysis
│   └── evidence/
│       ├── llm_judge.txt              # Argo gpt-5.2 per-claim adjudication
│       ├── genome_stats.json          # length/GC/contigs (copy)
│       ├── gene_content.json          # per-gene locus + bp + aa (copy)
│       ├── comparison_table.json      # paper Table 2 vs recompute (copy)
│       ├── gi_prediction.json         # DIMOB-style islands (copy)
│       └── prokka_summary.txt         # Prokka 1.12 stats (copy)
└── work/
    ├── fulltext.xml                   # Europe PMC PMC8816663 full XML
    ├── fulltext.txt                   # plain-text extraction
    ├── dataset/
    │   └── ncbi_dataset/data/GCF_014263185.1/
    │       ├── GCF_014263185.1_ASM1426318v1_genomic.fna
    │       ├── genomic.gff
    │       ├── protein.faa
    │       ├── cds_from_genomic.fna
    │       └── GCF_014263185.1_ASM1426318v1_genomic.gbff
    ├── assembly_data_report.jsonl     # NCBI report (coverage 231.29×)
    ├── genome_stats.py                # length/GC recompute script
    ├── genome_stats.json              # -> 5,030,813 bp, 52.98% GC, 1 contig
    ├── gene_content.py                # per-gene grep + measure
    ├── gene_content.json              # per-gene locus + bp + aa
    ├── comparison_table.py            # paper Table 2 diff
    ├── comparison_table.json          # per-row match/miss
    ├── gi_predict.py                  # DIMOB-style GI detector
    ├── gi_prediction.json             # 7 predicted islands
    ├── prokka_out/
    │   ├── 2NE11.txt                  # Prokka summary (5,030,813 bp, 4,385 CDS, ...)
    │   ├── 2NE11.tsv                  # per-feature table
    │   ├── 2NE11.gff                  # Prokka GFF
    │   ├── 2NE11.faa                  # Prokka proteins
    │   ├── 2NE11.gbk                  # Prokka GenBank
    │   └── 2NE11.log                  # Prokka run log
    └── judge.py                       # Argo LLM judge driver
```

## Key Artifacts (evidence chain)

### 1. Source paper
- **`work/fulltext.xml`** — Europe PMC PMC8816663 full XML (CC-BY 4.0)
- Provenance: `curl https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8816663/fullTextXML`
- Contains: paper full text incl. Tables 1–3, Fig. 2 caption, methods

### 2. Public genome (deposited assembly)
- **`work/dataset/ncbi_dataset/data/GCF_014263185.1/`**
- Provenance: `datasets download genome accession GCF_014263185.1`
- Files: FASTA + GFF + protein FAA + GBFF + CDS FNA
- md5 (genomic.fna): `2da02a203fe7c1841db96992305885e3`
- Size: 5,030,813 bp, 1 contig (circular chromosome)
- Coverage (from assembly report): 231.29×

### 3. Assembly-stat recompute
- **`work/genome_stats.json`** →
  ```json
  {"length": 5030813, "gc_percent": 52.98, "contigs": 1}
  ```
- Matches paper Table 2 EXACTLY.

### 4. Feature-count comparison
- **`work/comparison_table.json`** — paper Table 2 rows vs RefSeq GFF + 2026 re-annotation
- Result: 4,288 protein-coding (EXACT vs paper's PGAP), 111 tRNA (EXACT), 25 rRNA (EXACT), pseudogenes +2, total genes +8 (annotation drift within 0.2%).

### 5. Targeted gene-content survey
- **`work/gene_content.json`** — per-gene locus tag, bp, aa
- Byte-for-byte matches for headline enzymes:
  - Azoreductase: HU689_RS20690, 594 bp, 197 aa (paper: HU689_20695, 594, 197)
  - Dyp peroxidase: HU689_RS05305, 936 bp, 311 aa (paper: HU689_05310, 936, 311)
- Locus-tag remapping: `HU689_XXXXX → HU689_RS(XXXXX−5)` (standard RefSeq re-indexing)
- Mtr operon, OmcA cluster, metal-resistance cassette, Nag/lactate genes, Type I-F CRISPR all confirmed present.

### 6. Independent Prokka re-annotation
- **`work/prokka_out/2NE11.txt`** — Prokka 1.12 summary
- Different pipeline than paper's PGAP; still gives 5,030,813 bp, 1 contig, 25 rRNA, 109 tRNA, 4,385 CDS
- Confirms: 4 azoreductases, 6 peroxidases (incl. Dyp), full metal-gene set
- Cross-pipeline convergence = strong independent evidence.

### 7. Independent GI prediction
- **`work/gi_prediction.json`** — DIMOB-style (dinucleotide bias + mobility-gene co-location)
- 7 islands (paper reports 2 via IslandViewer 4)
- Largest ~48 kb / 51 genes, T4SS/conjugative cluster at ~4.03–4.07 Mb
- PARTIAL match: qualitative HGT-island claim confirmed; enumeration is method-dependent.

### 8. LLM adjudication
- **`report/evidence/llm_judge.txt`** — Argo gpt-5.2, free tier
- Per-claim scoring: 9 REPRODUCED + 1 CLOSE + 2 PARTIAL/NOT-TESTED
- Coverage 12/13, Agreement 10/12
- Final: **REPLICATED**

## Trace / Provenance

| Artifact | Source | Command | Cost |
|---|---|---|---|
| fulltext.xml | Europe PMC | curl REST fullTextXML | $0 |
| GCF_014263185.1 | NCBI | `datasets download genome` | $0 |
| genome_stats.json | this repo | `python3 genome_stats.py` | $0 |
| comparison_table.json | this repo | `python3 comparison_table.py` | $0 |
| gene_content.json | this repo | grep + Python | $0 |
| gi_prediction.json | this repo | `python3 gi_predict.py` | $0 |
| prokka_out/ | uicgpu | `prokka --cpus 8 2NE11.fna` | $0 (A100 idle) |
| llm_judge.txt | Argo :44497 | `python3 judge.py` | $0 (free tier) |

## Reproducibility

All artifacts regenerate from the deposited public assembly plus the scripts
in `work/`. The one non-portable step is the Prokka run (needs the `bvbrc28`
conda env on uicgpu with Prokka 1.12 installed); everything else is
pure-Python-stdlib or free HTTP calls.

## Sizes

- Genome + annotations: ~8 MB (compressed download)
- Prokka output: ~5 MB
- LLM judge transcript: <10 KB
- Report files (Markdown + LaTeX + JSON): ~40 KB
- Total repo footprint: ~15 MB

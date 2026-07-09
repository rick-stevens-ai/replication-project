# Workflow — BVBRC-64 Lactobacillus reuteri PNW1 replication

**Paper:** Alayande et al. 2020, PLoS ONE 15(7):e0235873, DOI 10.1371/journal.pone.0235873, PMID 32687505.
**Deposit:** GCA_003790365.1 (GenBank live; GCF_003790365.1 RefSeq mirror suppressed as "contaminated").
**Host:** CherryRd (macOS). **Date:** 2026-07-03. **Wall time:** ~3 minutes. **Cost:** $0 (zero paid endpoints).

## Pipeline (in order of execution)

```
[NCBI Datasets v2alpha]      (1) strain metadata + provenance      -> ncbi_datasets_report.json
        |
        v
[PubMed esearch/efetch]      (2) confirm PMID 32687505 + companion -> abstracts as source-of-truth
        |
        v
[NCBI Datasets download]     (3) pull genome FASTA + GFF + PROT    -> pnw1.zip (1.35 MB)
        |
        v
[Python: assembly stats]     (4) contigs, total bp, GC%, N count,  -> assembly_stats.json
                                 GFF feature counts (region/gene/
                                 CDS/pseudogene/tRNA/rRNA/...)
        |
        v
[Python: regex on prot.faa]  (5) named-CDS presence check          -> gene_search.json
                                 (arg deiminase, D/L-LDH, helveticin,
                                  bacteriocin, tet*, lnu*, CRISPR/Cas,
                                  hemolysin/hyaluronidase/enterotoxin/
                                  cytotoxin, integrase/prophage/phage-*)
        |
        v
[abricate x 8 databases]     (6) AMR + VF + plasmid screen         -> abricate_{db}.tsv (x8)
                                 (resfinder, card, ncbi, argannot,
                                  vfdb, victors, ecoli_vf,
                                  plasmidfinder), all refreshed
                                 2026-07-03, --minid 80 --mincov 80
        |
        v
[minced v0.4 -gffFull]       (7) CRISPR array search               -> minced_crispr.gff
        |
        v
[report/REPORT.md]           (8) claim-by-claim verdict            -> REPLICATED (strong)
```

## Concrete commands

### 1. Strain metadata
```bash
curl -s "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/taxon/Limosilactobacillus%20reuteri/dataset_report?filters.search_text=PNW1&page_size=10" \
  > report/evidence/ncbi_datasets_report.json
```
Result: 2 records (GCA_003790365.1 live; GCF_003790365.1 suppressed). Both = assembly ASM379036v1, submitter North-West University, release 2018-11-18, BioSample SAMN10397676 (piglet faeces, MRS, S. Africa: Pretoria, 25.89 S 28.21 E, coll. 2012-06), Illumina MiSeq, SPAdes 3.12.0.

### 2. PubMed confirmation
```bash
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=%22PNW1%22+AND+%22reuteri%22&retmode=json"
# -> 32687505 (target 2020 PLoS ONE), 30834362 (companion MRA 2019)
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=32687505,30834362&rettype=abstract&retmode=text"
```

### 3. Assembly download
```bash
curl -s "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/GCA_003790365.1/download?include_annotation_type=GENOME_FASTA&include_annotation_type=GENOME_GFF&include_annotation_type=PROT_FASTA" \
  -o pnw1.zip
unzip pnw1.zip
# contents: GCA_003790365.1_ASM379036v1_genomic.fna, protein.faa, genomic.gff,
#           assembly_data_report.jsonl, dataset_catalog.json, md5sum.txt
```

### 4. Assembly stats (Python)
- Contig count from FASTA `>` records.
- Total length = sum of contig lengths.
- GC% computed both over ATGC-only bases (excluding Ns) and over total length.
- GFF feature counts by column 3.
- Output: `report/evidence/assembly_stats.json`.

### 5. Functional gene search (Python)
Case-insensitive regex scan of `protein.faa` FASTA headers for the paper's named CDS classes plus mobile-element markers. Output: `report/evidence/gene_search.json`.

### 6. AMR / VF / plasmid screen (the independent-tool step)
```bash
for db in resfinder card ncbi argannot vfdb ecoli_vf victors plasmidfinder; do
  abricate --db $db --quiet GCA_003790365.1_ASM379036v1_genomic.fna \
    > report/evidence/abricate_${db}.tsv
done
```
- All 8 abricate databases refreshed 2026-07-03 (same day as replication).
- Default cutoffs: `--minid 80 --mincov 80`.

### 7. CRISPR array search
```bash
minced -gffFull -spacers GCA_003790365.1_ASM379036v1_genomic.fna \
  PNW1_crispr.txt PNW1_crispr.gff
```
MinCED v0.4 (Bland et al. 2007 algorithm; used by Prokka's CRISPR module).

### 8. Verdict assembly
Claim-by-claim comparison against paper Results section (C1-C7) written up in `report/REPORT.md`.

## Tool inventory
| Tool | Version | Role |
|---|---|---|
| curl | system | NCBI Datasets + eutils fetch |
| unzip | system | assembly bundle |
| Python 3 | system | assembly stats + gene regex |
| abricate | v-current, DBs refreshed 2026-07-03 | AMR / VF / plasmid screen |
| minced | v0.4 | CRISPR array search |
| NCBI PGAP annotation | as-deposited | protein/GFF source |

## Independence from paper's tool chain

| Paper tool | This replication's independent replacement |
|---|---|
| RAST + PGAP | PGAP only (RAST not free/re-runnable) |
| ResFinder | ResFinder (via abricate; independent DB pull 2026-07-03) |
| ARG-ANNOT | ARG-ANNOT (via abricate) |
| CARD | CARD (via abricate) |
| — | + NCBI-AMR (bonus, 4th independent AMR DB) |
| VirulenceFinder + VFDB | VFDB + VICTORS + ecoli_vf (via abricate) — 3 VF DBs |
| PHASTER | Not rerun (paywalled); PGAP phage/integrase CDS count used instead |
| CRISPRFinder | MinCED v0.4 (FOSS alternative) |
| OASIS | PGAP-annotated transposases (regex on protein.faa) |
| PathogenFinder | Not rerun (paywalled CGE service) |

## Reproducibility snapshot

All raw evidence saved under `report/evidence/`. A single re-run block reproduces every table in the report:

```bash
cd ~/Dropbox/REPLICATE-PROJECT/BVBRC-64-lactobacillus-reuteri-pnw1/work
curl -s "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/GCA_003790365.1/download?include_annotation_type=GENOME_FASTA&include_annotation_type=GENOME_GFF&include_annotation_type=PROT_FASTA" -o pnw1.zip
unzip -o pnw1.zip -d pnw1
cd pnw1/ncbi_dataset/data/GCA_003790365.1
for db in resfinder card ncbi argannot vfdb ecoli_vf victors plasmidfinder; do
  abricate --db $db --quiet GCA_003790365.1_ASM379036v1_genomic.fna > /tmp/${db}.tsv
done
minced -gffFull GCA_003790365.1_ASM379036v1_genomic.fna /tmp/crispr.txt /tmp/crispr.gff
```

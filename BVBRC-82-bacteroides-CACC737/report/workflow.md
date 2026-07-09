# Workflow — BVBRC-82 (Bacteroides sp. CACC 737)

**Paper:** Kim et al. 2020, *J Anim Sci Technol* 62(6):952–955 (PMID 33987575, PMCID PMC7721585).
**BV-BRC workflow assigned:** PlasmidFinder via Similar Genome Finder + Genome Assembly (Unicycler/SPAdes).
**Host:** CherryRd (macOS 25.3.0). No `uicgpu` fan-out — total data 4.6 Mb.
**LLM:** Argo proxy `127.0.0.1:44497`; judge model `argo:gpt-5` (Opus 4.7/4.8 hit repeated HTTP 502 on this run → fallback per free-endpoints-only policy).

## Stage graph

```
[1 paper harvest]
       │  esummary db=pubmed 33987575 + efetch db=pmc PMC7721585 (xml)
       ▼
[2 accession discovery]
       │  regex CP\d{6,}  →  7 accessions
       │  esummary db=nuccore per accession (liveness verify)
       ▼
[3 sequence pull]
       │  for each CP059408 + CP059406/7/9/10/11/12:
       │    efetch db=nuccore rettype=gbwithparts retmode=text
       │    sleep 1
       ▼
[4 genome statistics]        ─── work/analyze.py (Biopython SeqIO)
       │  per replicon: length, GC%, feature counts (CDS/gene/rRNA/tRNA)
       │  compare to paper Table 1
       ▼
[5 novel-species test (C5)]
       │  extract 4×16S paralogs (1,534 bp) from CP059408
       │  fetch NR_112945.1 (B. uniformis JCM 5828, type strain)
       │  Biopython pairwise2.align.globalms(2,-1,-2,-0.5)
       │  identity over non-gap positions
       ▼
[6 cross-plasmid backbone BLAST]
       │  cat 6 plasmid FASTAs → all_plasmids.fa
       │  makeblastdb → blastn -evalue 1e-5 -outfmt 6
       │  filter same-accession hits
       ▼
[7 CRISPR / feature-class regex scan]
       │  over CDS.product qualifiers:
       │    CRISPR|Cas, transposase|IS[0-9], replication|Rep[A-Z],
       │    mobilization|conjug|TraM|TraJ, carbohydrate|glycos|…
       ▼
[8 taxonomy check]
       │  efetch db=taxonomy id=2755405 → lineage
       ▼
[9 LLM judge]                ─── work/llm_judge.py
       │  POST claims + evidence block to argo:gpt-5
       │  system: "rigorous scientific-replication judge"
       │  → per-claim status table + overall verdict
       ▼
[10 REPORT.md write]
```

## Explicit commands (from REPORT.md §3)

```bash
# 1. Paper
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=PMC7721585&rettype=xml" > pmc_7721585.xml

# 2. Sequences
for acc in CP059408 CP059406 CP059407 CP059409 CP059410 CP059411 CP059412; do
  curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=${acc}&rettype=gbwithparts&retmode=text" > seqs/${acc}.gb
  sleep 1
done

# 3. Stats + 16S alignment
python3 work/analyze.py

# 4. Reference 16S + comparison
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=NR_112945&rettype=fasta&retmode=text" > NR_112945.fa

# 5. Cross-plasmid BLAST
cat fasta/CP059406.fa fasta/CP059407.fa fasta/CP059409.fa fasta/CP059410.fa fasta/CP059411.fa fasta/CP059412.fa > all_plasmids.fa
makeblastdb -in all_plasmids.fa -dbtype nucl -out plasmid_db
blastn -query all_plasmids.fa -db plasmid_db -evalue 1e-5 -outfmt 6 > plasmid_selfblast.tsv

# 6. LLM judge
python3 work/llm_judge.py
```

## Data-flow inputs → outputs

| Stage | Input | Output |
|-------|-------|--------|
| 1 | PMID 33987575, PMCID PMC7721585 | `pmc_7721585.xml` |
| 2 | `pmc_7721585.xml` | 7 accessions (CP059406–CP059412) |
| 3 | 7 accessions | `seqs/CP059*.gb` (chr 9.87 MB; plasmids 40–90 KB) |
| 4 | `seqs/CP059*.gb` | per-replicon stats table (length, GC%, CDS/gene/rRNA/tRNA) |
| 5 | CP059408 16S paralogs + `NR_112945.1` | `work/16S_identity_check.json` (97.83% identity) |
| 6 | `all_plasmids.fa` | `plasmid_selfblast.tsv` (~99%/7–8 kb shared backbone) |
| 7 | CP059*.gb CDS.product qualifiers | feature-class counts (44 CRISPR/Cas, 44 transposase, …) |
| 8 | taxid 2755405 | lineage under "unclassified Bacteroides" |
| 9 | claims + evidence block | LLM judgment table + verdict |
| 10 | all of above | `report/REPORT.md` |

## Tool versions
- Python 3.14.6 (system, `/usr/local/bin/python3`)
- Biopython (system; `Bio.pairwise2` deprecation warning noted; result stable)
- NCBI BLAST+ blastn/makeblastdb (`/usr/local/bin`)
- Argo proxy on `localhost:44497` (free per standing policy)

## Deviations from the assigned BV-BRC workflow
- **PlasmidFinder** (CGE Enterobacteriaceae/GP-plasmid replicon-typing DB) has no Bacteroidota reps and returns 0 hits by design → substituted **Similar-Genome-Finder-analogue** implemented as all-vs-all plasmid BLAST (stage 6).
- **Genome Assembly (Unicycler/SPAdes)** was **not** run this pass — SRA reads (PRJNA647194) were not fetched. Structural claims validated against the authors' GenBank deposit only. This is a known scope gap called out in REPORT.md §6 and the GENUINE CRITIQUE section of REPORT.tex.

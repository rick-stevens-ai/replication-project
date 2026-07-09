# Artifacts Summary — BVBRC-75

**Paper:** Ramsamy et al. 2020, Pathogens 9(2):89 (PMID 32024012, PMC 7168644).
**Isolate:** *Citrobacter freundii* H2730R.
**Directory:** `~/Dropbox/REPLICATE-PROJECT/BVBRC-75-citrobacter-freundii-ndm1/`
**Verdict:** REPLICATED.

---

## Public identifiers used

| Kind | ID | Notes |
|---|---|---|
| PubMed | 32024012 | paper metadata |
| PMC | PMC7168644 | full-text XML |
| DOI | 10.3390/pathogens9020089 | |
| WGS accession | VWTQ00000000 | as reported in paper |
| Assembly (GenBank) | GCA_015208815.1 | ASM1520881v1 |
| Assembly (RefSeq) | GCF_015208815.1 | ASM1520881v1 (used here) |
| Assembly UID | 8406111 | NCBI Assembly |
| Submitter | University of KwaZulu-Natal | 2020-11-02 |
| Comparison plasmid | CP023554.1 | p18-43_01, 212,326 bp |
| Central contig | NZ_VWTQ01000022.1 | 14,979 bp, blaNDM-1-carrying |
| MLST scheme | pubmlst_cfreundii_seqdef | scheme 1, 1,250 STs, 7 loci |
| Novel ST | 498 | arcA_5, aspC_16, clpX_14, dnaG_54, fadD_103, lysP_5, mdh_15 |

## Downloaded artifacts (RefSeq FTP)

- `GCF_015208815.1_ASM1520881v1_genomic.fna.gz` — assembly (58 contigs, 5,299,408 bp)
- `GCF_015208815.1_ASM1520881v1_genomic.gff.gz` — PGAP annotation (5093 CDS, 116 pseudogenes, 70 tRNA, 7×23S + 5×5S rRNA)
- `GCF_015208815.1_ASM1520881v1_cds_from_genomic.fna.gz` — CDS FASTA
- `GCF_015208815.1_ASM1520881v1_protein.faa.gz` — protein FASTA
- `GCF_015208815.1_ASM1520881v1_assembly_stats.txt` — SKESA v2018-09-01, MiSeq, 99× (paper Table A1 line-for-line)
- `CP023554.1` (via efetch) — reference plasmid p18-43_01 (212,326 bp)
- PubMLST scheme-1 profiles TSV + per-locus allele FASTAs (arcA, aspC, clpX, dnaG, fadD, lysP, mdh)

## Computed / generated artifacts

- Genome-stats table (Python; FNA/GFF parse) — matches paper Table A1 line-for-line
- Resistome distinct-locus table (17 loci, all drug classes represented)
- BLAST tabular output (contig 22 vs CP023554.1) — 100.000% identity over 14,979 bp
- BLAST tabular for contigs 27, 31, 41 vs CP023554.1 — ≥99% identity across large fractions
- In-silico MLST call sheet (7 loci, per-locus best allele + identity)
- LLM-judge JSON: `report/evidence/judge_verdict.json` (argo:gpt-5.2, T=0.1)

## Key headline numbers (paper vs replication)

| Metric | Paper | Independent | Δ |
|---|---|---|---|
| Genome size (bp) | 5,299,408 | 5,299,408 | **0 (exact)** |
| GC (%) | 51.80 | 51.84 | +0.04 pp |
| Contigs | 58 | 58 | 0 |
| N50 | 518,368 | 518,368 | **0 (exact)** |
| L50 | 4 | 4 | 0 |
| Coverage | 99× | 99× | 0 |
| Assembler | SKESA v2.3 | SKESA 2018-09-01 | same era |
| Platform | Illumina MiSeq | Illumina MiSeq | same |
| CDS | 5006 / 5135 | 5093 (+116 pseudo) | −42 to +87 |
| 23S rRNA | 7 | 7 | 0 |
| 5S rRNA | 5 | 5 | 0 |
| Acquired R genes | 25 | 17 | −8 (tool-union vs single-tool) |
| MLST | ST498 | ST498 | ✅ |
| blaNDM-1 contig | 00022 | NZ_VWTQ01000022.1 | ✅ |
| blaNDM-1 → p18-43_01 | "closely related" | **100.000% identity over 14,979 bp** | ✅ |

## Endpoints used (all free)

- NCBI E-utils
- Europe PMC OA API
- RefSeq FTP
- PubMLST REST
- BLAST+ 2.16 (local)
- Argo proxy `http://127.0.0.1:44497/v1` — model `argo:gpt-5.2` (LLM judge only)

## Directory layout

```
BVBRC-75-citrobacter-freundii-ndm1/
├── extraction/             (n/a for this paper — direct FTP download)
├── work/
│   ├── paper/              # Europe PMC full-text XML
│   ├── refs/               # RefSeq downloads + PubMLST profiles/alleles
│   └── analysis/           # Python parsers, BLAST invocations, judge.py
└── report/
    ├── REPORT.md           # source of truth (this backfill built from it)
    ├── REPORT.tex          # LaTeX with GENUINE CRITIQUE section
    ├── open_questions.json
    ├── workflow.md
    ├── artifacts_summary.md
    ├── failure_analysis.md
    └── evidence/
        └── judge_verdict.json
```

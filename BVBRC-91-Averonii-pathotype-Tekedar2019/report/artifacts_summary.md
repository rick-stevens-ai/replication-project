# Artifacts Summary — BV-BRC Replication #91

Target: Tekedar et al. 2019, *PLoS ONE* **14**(8):e0221018 (A. veronii pathotype).
Verdict: **PARTIAL REPLICATION (strong).**

This document is the evidence-file manifest — a downstream reproducer can use it to locate the raw artifacts backing every numerical claim in `REPORT.md` / `REPORT.tex`.

---

## 1. Report deliverables (`report/`)

| File                     | Purpose                                                            |
|--------------------------|--------------------------------------------------------------------|
| `REPORT.md`              | Source-of-truth narrative report (14 KB).                          |
| `REPORT.tex`             | LaTeX version with expanded GENUINE CRITIQUE section.              |
| `open_questions.json`    | 5 grounded open follow-up questions.                               |
| `workflow.md`            | End-to-end step-by-step workflow (~15 min budget).                 |
| `artifacts_summary.md`   | This file.                                                         |
| `failure_analysis.md`    | Post-mortem of what was left on the table.                         |

## 2. Paper text (`work/`)

| File            | Source                                                                       | Notes                          |
|-----------------|------------------------------------------------------------------------------|--------------------------------|
| `fulltext.xml`  | EuropePMC PMC6715197 fullTextXML endpoint                                    | ~255 KB, source of claim grep. |

## 3. Genome FASTAs (`work/` or `evidence/genomes/`)

Downloaded from NCBI Datasets API (`https://api.ncbi.nlm.nih.gov/datasets/v2/genome/accession/{acc}/download?include_annotation_type=GENOME_FASTA`):

| Strain     | Accession         | BV-BRC genome_id | Length (bp)  | Contigs | GC%    |
|------------|-------------------|------------------|--------------|---------|--------|
| ML09-123   | GCA_002906945.1   | 654.112          | 4,754,017    | 32      | 58.44  |
| TH0426     | GCA_001593245.1   | 654.45           | 4,923,009    | 1       | 58.26  |

Additional reference genome pulled via BV-BRC (no FASTA download needed, only sp_gene endpoint):

| Strain  | BV-BRC genome_id | Role                                       |
|---------|------------------|--------------------------------------------|
| AVNIH1  | 654.48           | Human-isolate T3SS/T6SS-negative control.  |

## 4. Genome-stats computations (`evidence/`)

Python stdlib (no BioPython) recomputation of Table 1 fields (length / contigs / GC%). Matches paper Table 1 to the decimal.

| Strain    | Field         | Paper Table 1 | This work     | Δ       |
|-----------|---------------|---------------|---------------|---------|
| ML09-123  | Length (Mb)   | 4.754         | 4.754         | 0       |
| ML09-123  | Contigs       | 32            | 32            | 0       |
| ML09-123  | GC%           | 58.4          | 58.44         | +0.04   |
| TH0426    | Length (Mb)   | 4.923         | 4.923         | 0       |
| TH0426    | Contigs       | 1             | 1             | 0       |
| TH0426    | GC%           | 58.3          | 58.26         | −0.04   |

## 5. ANI logs (`evidence/ani/`)

**fastANI (v1.34+) — bi-directional:**

| Direction              | ANI (%)     | Orthologous mappings | Total fragments |
|------------------------|-------------|----------------------|-----------------|
| ML09-123 → TH0426      | **99.9273** | 1530                 | 1569            |
| TH0426 → ML09-123      | **99.9106** | 1526                 | 1641            |

**skani (learned-ANI):**

| Direction              | ANI (%)     | Align fraction (%) |
|------------------------|-------------|--------------------|
| Symmetric              | **99.94**   | 94.22 / 97.57      |

Paper threshold: **> 99.91%.** All three measurements exceed threshold → **pathotype claim reproduced by two independent algorithms.**

## 6. BV-BRC Specialty-Gene pulls (`evidence/bvbrc/`)

Endpoint: `https://www.bv-brc.org/api/sp_gene/?eq(genome_id,X)&limit(5000)&http_accept=application/json`

| Strain    | genome_id | JSON file           | Rows |
|-----------|-----------|---------------------|-----:|
| ML09-123  | 654.112   | `sp_ML09-123.json`  | 399  |
| TH0426    | 654.45    | `sp_TH0426.json`    | 705  |
| AVNIH1    | 654.48    | `sp_AVNIH1.json`    | 465  |

### Aggregated secretion-system distribution

| Product substring    | ML09-123 | TH0426 | AVNIH1 (human) | Paper claim                       |
|----------------------|---------:|-------:|---------------:|-----------------------------------|
| `flagell`            | 75       | 76     | 35             | Conserved in all 41               |
| `type iii secretion` | 49       | 68     | **0**          | Human isolates lack T3SS          |
| `t6ss`/`type vi`     | 15       | 15     | **0**          | Human isolates lack T6SSi         |
| `type iv pil`        | 4        | 4      | 4              | T4P conserved in all 41           |

### Marquee shared element (TssJ / VasD / AHA_1837)

| Strain    | Product-string match                                    |
|-----------|---------------------------------------------------------|
| ML09-123  | `"T6SS secretion lipoprotein TssJ (VasD)"` ✓            |
| TH0426    | `"T6SS secretion lipoprotein TssJ (VasD)"` ✓            |

### Virulence-factor magnitude (BV-BRC spelling variants)

| Strain    | `Virulence Factor` | `Virulance factor` | Total |
|-----------|-------------------:|-------------------:|------:|
| ML09-123  | 56                 | 155                | 211   |
| TH0426    | 58                 | 182                | 240   |
| Paper (across whole 41-strain panel) | — | — | **207** |

## 7. Data-availability check evidence

| Metric                                                          | Value  |
|-----------------------------------------------------------------|--------|
| Public A. veronii genomes in BV-BRC (taxon 654, 2026-07-04)     | 726    |
| Paper accessions retrievable via direct `strain` field query    | 34/41  |
| Paper accessions retrievable via alternate strain-level taxa    | +7     |
| **Total retrievable**                                           | **41/41** |
| Notable alternate-taxonomy example: B565 → taxon 998088 (GCF_000204115.1) | ✓ |

## 8. Not produced (scope-out, documented)

| Item                                                             | Reason                                                                                         |
|------------------------------------------------------------------|------------------------------------------------------------------------------------------------|
| Pan/core-genome (8,710 / 2,855)                                  | EDGAR 2.0-parameter-specific; no other pan-genome tool produces byte-match on identical input. |
| RAxML core-genome ML phylogeny (2857 gene trees, 100 bootstraps) | Computationally heavy; not a headline-claim replication target.                                |
| In-vivo catfish LD50 (dose-response mortality)                   | Experimental; out of computational scope.                                                      |
| CRISPRfinder per-strain across 41                                | BV-BRC sp_gene only spot-checked; CRISPRfinder output not directly BV-BRC-visible.             |
| Whole-panel TssJ absence-verification (39 non-catfish strains)   | Scope-out; necessary-condition already satisfied.                                              |

## 9. Reproduction one-liner

```bash
# Genomes
curl -L "https://api.ncbi.nlm.nih.gov/datasets/v2/genome/accession/GCA_002906945.1/download?include_annotation_type=GENOME_FASTA" -o ML.zip
curl -L "https://api.ncbi.nlm.nih.gov/datasets/v2/genome/accession/GCA_001593245.1/download?include_annotation_type=GENOME_FASTA" -o TH.zip
unzip -o ML.zip -d ML && unzip -o TH.zip -d TH

# Pathotype ANI
fastANI -q ML/**/*_genomic.fna -r TH/**/*_genomic.fna -o fastani.txt
skani dist ML/**/*_genomic.fna TH/**/*_genomic.fna

# Virulence-gene phenotype
for gid in 654.112 654.45 654.48; do
  curl "https://www.bv-brc.org/api/sp_gene/?eq(genome_id,${gid})&limit(5000)&http_accept=application/json" > sp_${gid}.json
done
```

Wall-clock budget: **~12 min** on a laptop with internet.

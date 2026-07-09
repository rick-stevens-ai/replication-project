# Workflow — BVBRC-30 Replication of Singh/Urbaniak et al. 2018

**Paper:** Singh NK et al., *BMC Microbiology* (2018) 18:175 — MDR *Enterobacter bugandensis* from the ISS
**DOI:** 10.1186/s12866-018-1325-2 · **PMID:** 30466389 · **PMCID:** PMC6251167
**Replication ID:** BVBRC-30 · **Date:** 2026-07-01 · **Host:** CherryRd (macOS) · **Compute:** local (free, no HPC)

---

## 0. Overview

Independent computational replication of the paper's central genomic claims using the *real* deposited genome assemblies listed in the paper's Table 1 (BioProject PRJNA319366) plus reference *Enterobacter* comparators. Wet-lab phenotype claims (C4) and RAST-derived counts (C5) are explicitly out of scope for a computational replication.

---

## 1. Inputs

### 1.1 Genome accessions (from paper Table 1 + reference set)

| Role | Strain | Paper WGS acc. | Assembly downloaded |
|------|--------|----------------|---------------------|
| ISS (ref) | IF3SW-P2 | POUO00000000 | GCA_002890715.1 |
| ISS | IF2SW-P2 | POUR00000000 | GCA_002890725.1 |
| ISS | IF2SW-B1 | POUQ00000000 | GCA_002890755.1 |
| ISS | IF2SW-P3 | POUP00000000 | GCA_002890765.1 |
| ISS | IF2SW-B5 | RBVJ00000000 | GCA_003627555.1 |
| clinical | EB-247T | FYBI00000000 | GCF_900324475.1 |
| clinical | 153_ECLO | NZ_JVSD00000000 | GCA_001054435.1 |
| clinical | MBRL1077 | PRJNA310238 | GCA_001562175.1 |
| outgroup | *E. cloacae* ATCC13047 | — | (reference assembly) |
| outgroup | *E. asburiae* ATCC35953 | — | (reference assembly) |
| outgroup | *E. ludwigii* EN-119 | — | (reference assembly) |
| outgroup | *E. aerogenes* KCTC2190 | — | (reference assembly) |
| outgroup | *E. kobei* | — | (reference assembly) |

Retrieval: NCBI Datasets 18.25.1 (`datasets download genome accession …`), 2026-07-01.

### 1.2 Source paper
- `paper/urbaniak2018.pdf`
- `paper/paper_extracted.txt` (text extraction)

### 1.3 Extracted claim set
- `data/claims.json` — 6 claims C1..C6 with expected values/tables

---

## 2. Pipeline stages

### Stage A — Retrieve and stage genomes
1. `datasets download genome accession <acc>` for each of the 13 accessions.
2. Unpack into `work/genomes/<strain>.fna`.
3. Verify per-genome length, GC%, contig count → `work/genome_stats.json`.

### Stage B — ANI (Claim C1)
1. `fastANI --queryList iss.txt --refList all.txt --fragLen 3000 -o work/ani_matrix.tsv`.
2. Aggregate: mean ISS-vs-comparator ANI → `work/ani_summary.json`.
3. Compare each mean against paper Table 1 values (Δ column).

### Stage C — Clonality (Claim C2)
1. `fastANI` on ISS-vs-ISS all-pairs → min/max identity.
2. `mlst --scheme ecloacae` on each of the 13 assemblies → sequence type per strain (all 5 ISS → **ST2504**).
3. SNP calling: `minimap2 -x asm5 IF3SW-P2.fna other_iss.fna | paftools.js call -` → per-strain `.var` files in `work/snp2/`, count SNPs relative to IF3SW-P2 reference.

### Stage D — AMR / MDR (Claim C3)
1. `amrfinder -n <assembly>.fna -O Enterobacter --plus` for each strain → `work/amr/<strain>.tsv`.
2. Aggregate per-strain gene set → `work/amr_summary.json`.
3. Compare against paper Table 2 gene-category descriptions (β-lactamase class C, fosfomycin, RND MDR efflux, metal efflux).

### Stage E — Genome-statistics sanity (Claim C5, partial)
1. From Stage A stats: verify ~4.93 Mb length, ~55.9% GC, 2-contig hybrid assemblies for the 5 ISS strains — consistent with paper's ~4733-gene / ~1 gene-per-kb Enterobacter envelope.
2. RAST subsystem counts explicitly not regenerated (documented limitation).

### Stage F — Independent judging
1. `work/judge_scores.json` — 3 independent LLM judges scoring on Coverage / Agreement / Fidelity / Reproducibility rubric.
2. Result: 2× PARTIAL, 1× REPLICATED (means 7.7 / 8.0 / 7.0 / 7.0).

### Stage G — Report synthesis
1. `work/analysis_summary.md` — consolidated evidence.
2. `report/REPORT.md` — human-readable verdict + tables.
3. `report/REPORT.tex` — LaTeX version with dedicated Genuine Critique section.

---

## 3. Tool versions (all free / local)

| Tool | Version | Role |
|------|--------:|------|
| NCBI Datasets CLI | 18.25.1 | genome retrieval |
| fastANI | (packaged) | ANI (Stage B, Stage C) |
| mlst | 2.33.1 | MLST typing, scheme *ecloacae* |
| AMRFinderPlus | 4.2.7 | AMR gene detection |
| minimap2 | (asm5 preset) | assembly-vs-assembly SNP mapping |
| paftools.js | (with minimap2) | SNP calling |
| biopython | 1.87 | stats scripting |

---

## 4. Deliberate scope exclusions

- **Wet-lab phenotypes (C4)** — disk diffusion / Vitek not reproducible in silico.
- **RAST subsystem counts (C5)** — different annotation paradigm; AMRFinderPlus substituted for AMR-specific comparison.
- **dDDH** — paper used GGDC web service; ANI serves as equivalent species-boundary metric.
- **Raw-read SNP pipeline** (paper: bwa-mem + GATK HaplotypeCaller with FP filters) — would require the raw Illumina reads; assembly-vs-assembly (minimap2+paftools) used instead, with the resulting number gap acknowledged in Section 4.2 of REPORT.md.

---

## 5. Runtime & footprint

- Wall time: minutes on a laptop (5 Mb bacterial genomes, 13 assemblies).
- Disk: a few hundred MB total (assemblies + intermediates).
- No GPU, no HPC, no paid API calls used.

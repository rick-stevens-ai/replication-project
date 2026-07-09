# Replication Workflow — Hinc et al. (2021) phiCDKH01

**Paper:** *Complete genome sequence of the newly discovered temperate* Clostridioides difficile *bacteriophage phiCDKH01 of the family Siphoviridae.* Archives of Virology 166:2305–2310 (2021). DOI 10.1007/s00705-021-05092-0. PMID 34014385. PMC PMC8270841. CC BY 4.0.
**Set:** BVBRC-55
**Analyst:** Ollie (OpenClaw AI), BVBRC Replication Project
**Date:** 2026-07-02
**Verdict:** REPLICATED (LLM-judge 93/100)

---

## 1. Overview

Genome-announcement / comparative-genomics replication. All data pulled from public NCBI (free, no auth). No wet-lab work. No proprietary databases. No paid APIs. Maps onto the BV-BRC Codon Tree / Phylogenetic Tree workflow plus standard comparative genomics.

---

## 2. Inputs

| Artifact | Source | Access |
|---|---|---|
| phiCDKH01 phage genome (MN718463) | NCBI Nucleotide | E-utilities `efetch` |
| Host WGS contig JACSDL010000003.1 (~410 kb) | NCBI Nucleotide | E-utilities `efetch` |
| phiCD24-1 (LN681534) | NCBI Nucleotide | `esearch` → `efetch` |
| 11 comparator C. difficile phage genomes | NCBI Nucleotide | `esearch` → `efetch` |
| Paper full text | Europe PMC PMC8270841/fullTextXML | free XML endpoint |

Comparator set: phiCD6356, phiCDHM11, phiCDHM13, phiCDHM14, phiCDHM19, phiCD111, phiCD146, phiCD211, phiCD505, phiCD506, phiCDIF1296T.

---

## 3. Tools

| Tool | Version | Purpose |
|---|---|---|
| NCBI E-utilities (`esearch`, `efetch`) | current | genome + annotation retrieval |
| Biopython | 1.87 | GenBank/FASTA parsing, GC%, CDS iteration |
| BLAST+ (`makeblastdb`, `blastn`) | 2.17.0 | pairwise + all-vs-all identity |
| `minced` | (default) with `-minNR 2` | CRISPR array detection |
| custom VIRIDIC-style Python (`work/viridic_matrix2.py`) | in-repo | intergenomic identity with per-query-position best-pident deduplication |
| Argo `gpt-5.2` (free) | via Argo proxy :44497 | LLM-judge verdict |

No paid endpoints. No cloud VMs. Runs on any single laptop with internet + BLAST+ + minced installed.

---

## 4. Steps

1. **Fetch and parse genome (MN718463).** `efetch` → GenBank + FASTA. Biopython parses length, GC%, CDS count, per-CDS strand, tRNA/rRNA. → `evidence/genome_stats.json`.
2. **Fetch phiCD24-1 (LN681534).** `esearch` disambiguates the accession, `efetch` retrieves it.
3. **Pairwise phiCDKH01 vs phiCD24-1.** `makeblastdb` on each, `blastn` both directions, custom deduplication script computes VIRIDIC-style whole-genome intergenomic identity. → `evidence/phiCDKH01_vs_phiCD24-1.tsv`.
4. **Fetch 11 comparator phages.** Batched `esearch`/`efetch`. All-vs-all VIRIDIC-style identity matrix. Rank neighbours; apply ICTV thresholds (genus ≥70%, species ≥95%). → `evidence/phiCDKH01_intergenomic_dedup.json`, `evidence/viridic_matrix_dedup.tsv`.
5. **CRISPR detection.** `minced -minNR 2` on the phage FASTA. → `evidence/crispr_phiCDKH01.txt`.
6. **Prophage localization.** Fetch host contig JACSDL010000003.1; BLASTn phiCDKH01 vs contig; extract span, %identity, coverage. → `evidence/prophage_localization.tsv`.
7. **LLM judge.** Feed claim-by-claim comparison table + per-claim evidence to Argo `gpt-5.2`; parse verdict + confidence. → `evidence/llm_judge_verdict.txt`.
8. **Compile REPORT.md** with claim-by-claim table and verdict.

---

## 5. Work Estimate

| Phase | Wall time | Notes |
|---|---|---|
| Data pull (all NCBI accessions) | ~10 min | dominated by NCBI throttling |
| BLASTn all-vs-all (13 genomes, small) | ~5 min | tiny genomes, cheap |
| VIRIDIC-style dedup matrix | <1 min | pure Python |
| CRISPR (minced) | <1 min | single small FASTA |
| Prophage localization (BLASTn vs 410 kb contig) | <1 min | |
| LLM judge | ~30 s | one Argo call |
| Report write-up | ~30 min | human/agent time |
| **Total end-to-end** | **~1 hour** | on a laptop, one analyst |

Rerun cost: ~pennies (only network + one free Argo call). No GPU. No SLURM job.

---

## 6. Provenance & Reproducibility

- All accessions are public and permanent (GenBank/RefSeq).
- No credential-gated data.
- BLAST+ and minced are open-source, packaged in bioconda.
- VIRIDIC-style deduplication script is checked into `work/` (verify `viridic_matrix2.py`).
- Argo LLM judge is optional — the human/expert can inspect the claim-by-claim table directly.

Anyone with `conda install -c bioconda blast minced` + `pip install biopython` can re-run this in an hour and reproduce every numeric result reported.

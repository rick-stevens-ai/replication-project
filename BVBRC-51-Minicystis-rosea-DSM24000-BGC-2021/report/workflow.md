# Workflow: BVBRC-51 Minicystis rosea DSM 24000T Replication

**Paper:** Pal, Sharma & Subramanian (2021), BMC Genomics 22:655 (PMID 34511070, PMC8436480).
**Verdict target:** PARTIAL (achieved).
**Compute footprint:** CherryRd (Python + BLAST+) + uicgpu A100 (antiSMASH 8.0.4). Free endpoints only (Argo LLM judges).

---

## Stage 0 — Paper harvest

- **Input:** DOI 10.1186/s12864-021-07955-x (open access, CC BY 4.0 via BMC).
- **Action:** Pull full-text XML from Europe PMC for PMC8436480.
- **Output:** `work/fulltext.xml`. Extracted the two anchors needed for replication:
  - **Genome accession:** `CP016211.1` (chromosome record)
  - **BioProject:** `PRJNA321464`
  - Methods block for antiSMASH (v5.0) and the *pfa* cluster reference set (Aetherobacter + Sorangium Pfa proteins).

## Stage 1 — Genome + annotation download

- **Input:** BioProject PRJNA321464.
- **Action:** Map BioProject → assembly accession via NCBI `esearch` / `esummary` chain.
  - Resolved to assembly **GCA_001931535.1**.
- **Action:** Download genome package via the **NCBI Datasets REST API** (free, no auth). Bundle contains:
  - Genomic FASTA (chromosome CP016211.1, one circular contig)
  - GFF3 annotation (PGAP)
  - Protein FASTA (proteome)
- **Verification:** MD5 of the downloaded zip recorded in the artifact-harvest log.
- **Output:** `work/GCA_001931535.1/` (FASTA, GFF, faa).

## Stage 2 — C2 / C3: Genome statistics (Table 1 replication)

- **Script:** `genome_stats.py` (CherryRd, pure Python + Biopython).
- **Compute:**
  - Genome size = sum of sequence lengths in genomic FASTA.
  - GC% = base-count over the concatenated chromosome.
  - CDS / strand-split / tRNA / rRNA counts = parse GFF3 feature types.
  - Coding density = sum(CDS-length) / genome-length.
- **Output:** `evidence/genome_stats.json`.
- **Result:** Genome size, total CDS, and strand-split CDS counts reproduce EXACTLY (16,040,666 bp; 14,018 CDS; 6,983 + / 7,035 −). GC and coding density within Δ0.03 / Δ0.28.

## Stage 3 — C5: *pfa* PUFA cluster (homology + synteny)

- **Script:** `pfa_blast.py` (CherryRd).
- **Reference set:** 10 Pfa proteins the paper cites, fetched by `efetch`:
  - Aetherobacter sp. SBSr008: AIJ50375, AIJ50376, AIJ50377
  - Aetherobacter fasciculatus: AIJ50372, AIJ50373, AIJ50374
  - Sorangium cellulosum So ce56: CAN90975, CAN90976, CAN90977, CAN95221
- **Pipeline:**
  1. `makeblastdb -in mrosea_proteome.faa -dbtype prot`
  2. `blastp -query pfa_refs.faa -db mrosea -evalue 1e-10 -outfmt 6`
  3. Per reference: best hit + summed-HSP coverage.
  4. GFF synteny check: pull loci of the top three hits, confirm same strand + adjacency.
- **Output:** `evidence/pfa_blast_summary.json`.
- **Result:** Pfa1/2/3 + PfaE homologs identified (APR86155/56/57 + APR88149); three core hits are consecutive same-strand loci `A7982_11504/05/06` with 27/29 bp intergenic gaps — a contiguous *pfa* operon.

## Stage 4 — C4: antiSMASH BGC survey

- **Compute:** uicgpu A100 host (free tier, no wall clock).
- **Env setup:** fresh conda environment, `antismash 8.0.4` installed from bioconda, all databases pre-downloaded (`download-antismash-databases`).
- **Command:** `antismash --genefinding-tool prodigal --cpus 16 --output-dir mrosea_asmash8/ genome.fna`
- **Parse:** custom Python reads `mrosea.json`, walks region records, tallies product categories.
- **Output:** `evidence/antismash_summary.json`.
- **Result:** 53 total BGC regions (vs paper's 47 under v5.0); category ranking (terpene > NRPS > RiPP > PKS) and singleton set (phosphonate, phenazine, siderophore, thioamitide, arylpolyene) reproduce.

## Stage 5 — Convergent confirmation of the *pfa* cluster

- **Cross-check:** the antiSMASH JSON is queried for regions overlapping the pfa_blast synteny window (chromosome ~13.09–13.15 Mb).
- **Match:** T1PKS/hglE-KS region at 13,095,900–13,151,432 exactly spans the operon → three independent lines of evidence agree (BLAST + GFF synteny + antiSMASH BGC prediction).
- **Independent annotation:** PGAP labels APR86156.1 as "omega-3 polyunsaturated fatty acid synthase subunit, PfaA" — a fourth convergent signal from a completely different pipeline.

## Stage 6 — LLM-judge verdict pass

- **Judges:** two free Argo endpoints, run in series (single-endpoint concurrency rule):
  - `argo:gpt-5.2` → verdict: PARTIAL (weighted 53-vs-47 delta)
  - `argo:claude-opus-4.8` → verdict: REPLICATED (attributed 53-vs-47 to tool version)
- **Reconciliation rule:** follow the more conservative judge; do not inflate.
- **Output:** `evidence/llm_judge_gpt52.txt`, `evidence/llm_judge_opus48.txt`.
- **Final verdict:** PARTIAL (strong).

## Stage 7 — Reporting

- **Report:** `REPORT.md` (canonical) + `REPORT.tex` (LaTeX with genuine-critique section).
- **Artifact index:** `artifacts_summary.md`.
- **Failure log:** `failure_analysis.md`.
- **Open questions:** `open_questions.json`.
- **Chronology:** `attempt_log.md` (per-stage timings + commands).
- **Provenance:** `artifact_harvest.md` (URLs + accessions + checksums).

---

## Data-flow summary

```
Europe PMC ──► fulltext.xml ──► [CP016211.1, PRJNA321464]
                                      │
                                      ▼
                       NCBI Datasets ──► GCA_001931535.1/
                                              │
                    ┌─────────────────────────┼─────────────────────────┐
                    ▼                         ▼                         ▼
             genome_stats.py           pfa_blast.py              antismash 8.0.4
             (CherryRd)                 (CherryRd)               (uicgpu A100)
                    │                         │                         │
                    ▼                         ▼                         ▼
            genome_stats.json      pfa_blast_summary.json     antismash_summary.json
                    │                         │                         │
                    └─────────────────────────┼─────────────────────────┘
                                              ▼
                                    Argo LLM judges (×2)
                                              │
                                              ▼
                                       Verdict: PARTIAL
```

## Free-endpoint discipline

- **Data:** NCBI Datasets REST API + Europe PMC (both free, no auth).
- **Compute:** local CherryRd + uicgpu A100 (both free to Rick).
- **LLM:** Argo proxy (`argo:gpt-5.2`, `argo:claude-opus-4.8`) — free under standing rule.
- **No paid API calls** were made in any stage of this replication.

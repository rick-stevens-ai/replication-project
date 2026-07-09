# Workflow: BVBRC-54 — *S. flexneri* 5a M90T Complete Genome (Cervantes-Rivera 2020) Replication

**Paper:** Cervantes-Rivera R, Tronnet S, Puhar A. *BMC Genomics* 21:285 (2020). PMID 32252626. DOI 10.1186/s12864-020-6565-5.
**Verdict:** PARTIAL REPLICATION (strong).
**Compute:** uicgpu (8×A100 node; CherryRd was under memory pressure). Free tools only.

## Pipeline stages

### Stage 1 — Paper acquisition & claim extraction
- **Query:** Europe PMC by PMID 32252626.
- **Confirmed:** Open access CC BY 4.0, PMC7132871, `hasData=Y`.
- **Actions:** Pulled full-text XML; parsed Tables 1–3 for the paper's exact numbers (chromosome bp, plasmid bp, tRNA/rRNA/CDS/pseudogene/IS counts, TSS counts).
- **Output:** 7 testable claims C1–C7 tabulated (see REPORT §2).

### Stage 2 — Genome identification (assembly selection)
- **Search:** NCBI assembly, *S. flexneri* 5a M90T → 6 candidate assemblies.
- **Selection criteria:** submitter = paper's lab (Umeå University / MIMS); assembly level = Complete Genome; release date consistent with the paper.
- **Selected:** **GCF_004799585.1** (ASM479958v1), submitted 2019-04-18.
- **Decisive identity check:** `contig_n50` = 4,596,714 (paper's chromosome length) and `total − chromosome` = 232,195 (paper's plasmid length) — bp-for-bp identity.
- **Replicons:** chromosome **CP037923.1** (RefSeq NZ_CP037923.1), plasmid pWR100 **CP037924.1** (RefSeq NZ_CP037924.1).
- **BioSample:** SAMN10608416.

### Stage 3 — Data download
- **API:** NCBI Datasets REST v2alpha (free, no auth): `.../genome/accession/GCF_004799585.1/download`.
- **Artifacts pulled:** FASTA (nucleotide), GFF (annotation), protein FASTA, sequence report.

### Stage 4 — Independent genome statistics (C1, C2)
- **Method:** Python parse of the downloaded FASTA.
- **Metrics computed:** replicon count, per-replicon length, per-replicon GC%.
- **Result:** 2 circular replicons; chromosome 4,596,714 bp / plasmid 232,195 bp (bp-for-bp match); GC chrom 50.92%, plasmid 45.68% (NCBI report 51.0% / 45.5%).

### Stage 5 — Independent re-annotation (C4)
- **Tool:** Prokka 1.12 (conda env `bvbrc28`) de novo on the downloaded FASTA.
- **Compared against:** paper's own Prokka + manual curation counts; RefSeq PGAP counts.
- **Output:** `evidence/prokka_stats.txt`.

### Stage 6 — Specialty-gene / BV-BRC-equivalent workflow (C5)
Conda env `bvbrc14`.
- **abricate 1.4.0** vs:
  - **VFDB, Victors, ecoli_vf** — BV-BRC "Specialty Genes: Virulence".
  - **CARD, ResFinder, NCBI** — BV-BRC AMR.
  - **PlasmidFinder** — BV-BRC PlasmidFinder-via-similar-genome.
- **AMRFinderPlus 4.2.7** (`--organism Escherichia --plus`) — the paper's CARD/AMRFinder AMR path.
- **mlst 2.33.1** — Achtman *E. coli*/*Shigella* scheme.
- **Outputs:** `evidence/abricate_*.tsv`, `evidence/amrfinder.tsv`, `evidence/mlst.tsv`, `evidence/virulence_T3SS_summary.txt`.

### Stage 7 — LLM-judge verdict (C1–C7 scoring)
- **Model:** `argo:gpt-5.2` via free Argo proxy at `localhost:44497`.
- **Method:** per-claim scoring from the evidence artifacts; free-text verdict rationale (no regex).
- **Verdict:** **PARTIAL** — "independently confirms the deposited complete-genome structure and exact replicon lengths, and corroborates that the virulence plasmid carries a complete T3SS gene set … however, the raw-read assembly strategy and the dRNA-seq TSS quantifications were not re-executed."
- **Full text:** `report/evidence/judge_verdict.md` (from `work/`).

## What was NOT run (bounds the verdict at PARTIAL)
- **C3 raw-read assembly:** did not fetch PacBio subreads and did not re-run Canu 1.7 + Illumina RNA-seq polish. Only the finished-assembly structure/lengths were verified.
- **C6 dRNA-seq TSS re-processing:** did not fetch the TEX± libraries; did not re-derive 6723 primary / 7328 secondary TSS.
- **IS element re-typing:** did not run ISfinder / ISEScan on CP037923.1; the 402-IS number was corroborated only indirectly via pseudogene load.

## Provenance & reproducibility
- Assembly: `GCF_004799585.1` (GenBank `GCA_004799585.1`).
- Replicons: `CP037923.1` (chromosome), `CP037924.1` (pWR100).
- BioSample: `SAMN10608416`.
- Tools: Prokka 1.12; abricate 1.4.0 (VFDB/Victors/CARD/PlasmidFinder DBs 2026-Apr snapshot); AMRFinderPlus 4.2.7; mlst 2.33.1.
- Compute envs: `bvbrc28` (Prokka), `bvbrc14` (abricate/AMRFinderPlus/mlst) on uicgpu.
- Judge: `argo:gpt-5.2` via free Argo proxy.

# Artifacts Summary: BVBRC-54 — *S. flexneri* 5a M90T Replication

**Paper:** Cervantes-Rivera R, Tronnet S, Puhar A. *BMC Genomics* 21:285 (2020). PMID 32252626.
**Verdict:** PARTIAL.

## Source artifacts (pulled from public repositories)

| Artifact | Identifier | Source | Format | Notes |
|---|---|---|---|---|
| Genome assembly | GCF_004799585.1 (ASM479958v1) | NCBI RefSeq | — | Umeå/MIMS deposit; Complete Genome; 2019-04-18. GenBank alias GCA_004799585.1. |
| Chromosome | CP037923.1 (RefSeq NZ_CP037923.1) | NCBI | FASTA | 4,596,714 bp. GC 50.92% (indep) / 51.0% (NCBI). |
| Plasmid pWR100 | CP037924.1 (RefSeq NZ_CP037924.1) | NCBI | FASTA | 232,195 bp. GC 45.68% (indep) / 45.5% (NCBI). |
| Annotation (RefSeq PGAP) | GFF for GCF_004799585.1 | NCBI Datasets | GFF | 4,053 protein-coding CDS; 102 tRNA; 22 rRNA; 757 pseudogenes. |
| Protein set | GCF_004799585.1 proteins | NCBI Datasets | FASTA | Used for downstream homology if needed. |
| Sequence report | GCF_004799585.1 | NCBI Datasets | JSON/TSV | Provided the `contig_n50=4,596,714` identity check. |
| BioSample | SAMN10608416 | NCBI BioSample | — | Provenance for the Umeå/MIMS deposit. |
| Paper full text | PMC7132871 / PMID 32252626 | Europe PMC | XML | Open access CC BY 4.0; `hasData=Y`; Tables 1–3 parsed. |

## Generated artifacts (under `report/evidence/`)

| Artifact | Tool | Purpose |
|---|---|---|
| `genome_stats_comparison.md` | Python (FASTA parse) | Independent replicon count, per-replicon length, GC vs. paper/NCBI report. Establishes C1 & C2 EXACT match. |
| `prokka_stats.txt` | Prokka 1.12 | Independent re-annotation counts: 5,004 CDS (4720+284); 103 tRNA; 22 rRNA. Cross-pipeline consistency for C4. |
| `virulence_T3SS_summary.txt` | abricate (VFDB/Victors/ecoli_vf) | Effector/apparatus/regulator repertoire on pWR100: mxi/spa apparatus, ipa invasins + ipg chaperones, osp + ipaH effectors, virF/virB regulators, icsA/virG. Establishes C5. |
| `abricate_vfdb.tsv` | abricate | Raw VFDB virulence hits (per-locus). |
| `abricate_victors.tsv` | abricate | Raw Victors virulence hits. |
| `abricate_ecoli_vf.tsv` | abricate | Raw ecoli_vf hits. |
| `abricate_card.tsv` | abricate | AMR (CARD). |
| `abricate_resfinder.tsv` | abricate | AMR (ResFinder). |
| `abricate_ncbi.tsv` | abricate | AMR (NCBI). |
| `abricate_plasmidfinder.tsv` | abricate | PlasmidFinder → IncFII on 232 kb megaplasmid (pWR100). |
| `amrfinder.tsv` | AMRFinderPlus 4.2.7 | Intrinsic-only AMR profile: `blaEC` (chromosomal ampC-type β-lactamase) + `emrE` efflux; no acquired resistance. Clean laboratory-reference-strain signature. |
| `mlst.tsv` | mlst 2.33.1 | Achtman scheme → **ST631**. |
| `judge_verdict.md` (from `work/`) | Argo `argo:gpt-5.2` | Free-text LLM-judge scoring & PARTIAL verdict rationale. |

## Key quantitative results (bp-for-bp match)

| Metric | Paper | Independent (this replication) | Verdict |
|---|---:|---:|---|
| Chromosome length | 4,596,714 bp | 4,596,714 bp | **EXACT** |
| Plasmid pWR100 length | 232,195 bp | 232,195 bp | **EXACT** |
| Total genome | 4,828,909 bp | 4,828,909 bp | **EXACT** |
| # circular replicons | 2 | 2 | **EXACT** |
| tRNA (genome) | 102 (paper) / 102 (PGAP) | 103 (Prokka 1.12) | ≈ Match |
| rRNA (genome) | 22 (paper) / 22 (PGAP) | 22 (Prokka 1.12) | **EXACT** |
| CDS total | 4,949 (paper) / 4,053 (PGAP) | 5,004 (Prokka 1.12) | Consistent within pipeline variance |
| Pseudogenes | 769 (paper) / 757 (PGAP) | — | Paper vs PGAP agree to ~1.5% |
| MLST | (not reported) | ST631 | Adds context |
| AMR | (no claim) | intrinsic only: blaEC + emrE | Consistent with lab reference strain |

## Coverage summary

- **Claims fully reproduced:** C1 (2 circular replicons), C2 (chromosome + plasmid lengths bp-for-bp), C5 (pWR100 T3SS).
- **Claims partially reproduced:** C4 (tRNA/rRNA match; CDS/pseudogene within pipeline-difference tolerance; IS count not directly re-typed).
- **Claim verified as availability:** C7 (public deposit / usable).
- **Claims NOT re-executed:** C3 (raw-read Canu assembly), C6 (dRNA-seq TSS counts 6723/7328).

## What is missing / would be needed for full REPLICATED

1. PacBio raw subreads (SRA / ENA) + Illumina RNA-seq reads → re-run Canu 1.7 + polish for C3.
2. dRNA-seq TEX± libraries → re-derive TSS counts for C6.
3. ISfinder / ISEScan on CP037923.1 → directly re-type the 402 IS elements for C4.
4. Frozen snapshot of VFDB/Victors/PlasmidFinder DB versions used → to make specialty-gene calls exactly reproducible over time.

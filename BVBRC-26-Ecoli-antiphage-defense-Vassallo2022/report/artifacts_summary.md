# Artifacts Summary — BVBRC-26 (Vassallo et al. 2022)

Inventory of every deposited artifact used or produced by this replication, with source, size class, and role. All items live under the replication directory `BVBRC-26-Ecoli-antiphage-defense-Vassallo2022/`.

## Directory layout

```
BVBRC-26-Ecoli-antiphage-defense-Vassallo2022/
├── report/
│   ├── REPORT.md                              # canonical Markdown report
│   ├── REPORT.tex                              # LaTeX rendering + genuine critique
│   ├── open_questions.json                     # 5 truly open follow-up questions
│   ├── workflow.md                             # DAG + runtime characteristics
│   ├── artifacts_summary.md                    # this file
│   ├── failure_analysis.md                     # what did not replicate, causes
│   └── evidence/
│       ├── bvbrc_genome_map.json              # 71/71 GCA → BV-BRC genome_id
│       ├── crispr_rm_survey.json              # per-genome CRISPR-Cas + RM presence
│       └── independent_reproduction/          # 2026-07-03 second-pass evidence
└── work/                                      # execution tree (all scripts + data)
    ├── paper_fulltext.xml                     # Europe PMC PMC9519451 JATS
    ├── SupplementaryTables.xlsx               # Vassallo Tables S1–S8
    ├── paper_S5_source_strains.json           # 71 strains + GCA (Table S5)
    ├── paper_S2_systems.json                  # 21 systems + coords (Table S2)
    ├── defense_representatives.fasta          # 21 system-representative proteins
    ├── defense_proteins.fasta                 # 32 protein components
    ├── map_bvbrc.py                           # Stage 1 script
    ├── fetch_ncbi_proteomes.py                # Stage 2 script
    ├── build_distribution.py                  # Stage 3 script
    ├── mge_context.py                         # Stage 4 script
    ├── crispr_survey.py                       # Stage 5 script
    ├── llm_judge.py                           # Stage 7 script
    ├── ncbi_proteomes/                        # 71 * .faa files
    ├── blast/
    │   ├── all71_proteomes.faa                # concatenated BLAST input (~140 MB)
    │   ├── all71_proteomes.p*                 # BLAST DB files
    │   ├── rep_vs_all71.tsv                   # BLASTP hits (outfmt 6)
    │   └── distribution_summary.json          # per-system tier summary
    ├── mge_context_summary.json               # per-system MGE + hotspot counts
    └── llm_judge_verdict.txt                  # Argo gpt-o3 verdict
```

## Inputs (external, free/public)

| Artifact | Source | Purpose | Size class |
|---|---|---|---|
| `paper_fulltext.xml` | Europe PMC PMC9519451 (JATS full-text API) | paper narrative + method sections | small (~1 MB) |
| `SupplementaryTables.xlsx` | Nature Microbiology supplementary materials | Tables S1–S8 (source strains, per-system provenance, Gao 2020 comparison) | small (~500 KB) |
| 71 assembly proteomes | NCBI Datasets v2alpha REST (per GCA accession) | BLASTP database for provenance / distribution | medium (~140 MB combined, 348,507 proteins) |
| BV-BRC genome + feature records | BV-BRC data API `patricbrc.org/api/{genome,genome_feature}` | corpus mapping (Stage 1) + MGE context (Stage 4) + CRISPR/RM survey (Stage 5) | streamed JSON, not archived |
| Argo `argo:gpt-o3` completions | Argo proxy `http://127.0.0.1:44497/v1` | LLM-judge verdict | prompt + response only |

## Parsed / derived inputs

| Artifact | Provenance | Contents |
|---|---|---|
| `paper_S5_source_strains.json` | openpyxl parse of Table S5 | 71 entries `{strain_id, GCA_accession, notes}` |
| `paper_S2_systems.json` | openpyxl parse of Table S2 | 21 entries `{system_name, source_strain, contig_accession, cds_id, start, stop, strand}` (32 component-level entries when expanded) |
| `defense_representatives.fasta` | assembled from `paper_S2_systems.json` + NCBI protein fetch | 21 protein-representative FASTAs (one per PD-*) |
| `defense_proteins.fasta` | full component set | 32 protein FASTAs (multi-component systems expanded) |

## Stage 1 outputs — corpus mapping

| Artifact | Contents | Contract |
|---|---|---|
| `report/evidence/bvbrc_genome_map.json` | `{GCA_accession: BV-BRC genome_id}` for 71 strains | 71/71 mapped (100% required); ECOR block = `562.333xx/562.334xx`, UMB block = `562.387xx/562.388xx/562.453xx` |

## Stage 2 outputs — proteomes

| Artifact | Contents |
|---|---|
| `work/ncbi_proteomes/<genome_id>.faa` | Per-genome protein FASTA; header `>{original_ncbi_id} …` (filenamed by BV-BRC `genome_id` to preserve group link) |
| Total | 71 files, 348,507 proteins, ~140 MB uncompressed |

## Stage 3 outputs — distribution / provenance

| Artifact | Contents |
|---|---|
| `work/blast/all71_proteomes.faa` | Concatenated proteomes, headers prefixed with genome_id for back-mapping |
| `work/blast/all71_proteomes.p*` | BLAST protein DB (phr/pin/psq/etc.) |
| `work/blast/rep_vs_all71.tsv` | `blastp -outfmt 6` hits: 21 queries × up-to-2000 targets each |
| `work/blast/distribution_summary.json` | Per-system: `n_homolog`, `n_ortholog`, `n_self`, `source_strain_recovered` (bool), `carrier_genome_ids` (list) |

Key numbers from `distribution_summary.json`:
- 21/21 systems have exactly one `self` hit (source recovered)
- Mean homolog count 2.9 / 71; range 1 (many singletons) to 11 (PD-λ-1)
- All source-recovery bools == True

## Stage 4 outputs — MGE / hotspot context

| Artifact | Contents |
|---|---|
| `work/mge_context_summary.json` | Per-system: `contig_accession`, `system_start`, `system_stop`, `neighbours_window` (list of ±20 genes with product strings), `mge_neighbour_count`, `defence_like_neighbour_count`, `hotspot` (bool) |

Key numbers:
- 16/21 systems with ≥1 MGE-signature neighbour in ±20-gene window
- 14/21 systems with hotspot flag (≥2 defence-like neighbours)
- 5/21 with 0 MGE neighbours (PD-T4-1, PD-λ-6, PD-T7-2/4/5) — attributed to short/fragmented source contigs

## Stage 5 outputs — CRISPR / RM known-system survey

| Artifact | Contents |
|---|---|
| `report/evidence/crispr_rm_survey.json` | Per-genome: `crispr_cas_hits` (count of Cas/CRISPR product-string matches), `rm_hits` (count of restriction/methyltransferase matches), `has_crispr` (bool), `has_rm` (bool) |

Key numbers: 71/71 genomes with CRISPR-Cas annotation, 71/71 with RM annotation.

**Caveat:** BV-BRC returns dual RefSeq + PATRIC annotation sets for the same assemblies, so raw CDS counts are roughly 2×. Presence/absence conclusions are unaffected because the deduplication is orthogonal to the presence signal, but exact CDS ratios in this file should not be quoted without rededuplication.

## Stage 6 outputs — novelty (Table S4 re-read)

No file emitted; numbers are cited directly from `SupplementaryTables.xlsx` Table S4:
- 18/32 components without prior Gao et al. 2020 seed-cluster match
- 14/32 components with a match, identity range 26–49%, majority <35%

## Stage 7 outputs — LLM-judge verdict

| Artifact | Contents |
|---|---|
| `work/llm_judge_verdict.txt` | Argo `gpt-o3` verdict block: per-claim verdicts (C1..C6), overall verdict PARTIAL, Coverage 8/10, Agreement 9/10, free-text justification |

## Independent-reproduction outputs (2026-07-03)

Under `report/evidence/independent_reproduction/`:

| Artifact | Contents |
|---|---|
| Re-parsed `SupplementaryTables.xlsx` outputs | Fresh openpyxl parse from scratch, independent of Stage 0 outputs |
| NCBI Datasets v2 assembly summaries | Fresh fetch for 71 GCAs; 70/71 direct + 1 as GCA→GCF consolidation to `GCF_003892355.1` |
| NCBI Entrez eutils protein records | 32/32 defence-system proteins retrieved by accession; DBSOURCE / `/coded_by` field verifies contig == declared contig |
| Coordinate-verification worksheet | 9 proteins across 6 systems: contig FASTA freshly downloaded, 6-frame translation of declared genomic region confirms protein sequence at declared start/stop within 0–500 bp |
| Matched-numbers checklist | 13/13 checkable numbers concur (see REPORT.md § "Independent Reproduction") |

## What is NOT here (deliberately)

- **No SRA-derived data.** Vassallo et al. did not deposit tab-selection raw reads; C6 (functional-defence phenotype) is not computationally reproducible.
- **No re-run of the cross-phyla / NCBI-nr conservation analysis.** That analysis lives in the sibling directory `36123438-Anti-phage-defense-Ecoli/` (BLASTP of the 21 reps against NCBI-nr), which this replication treats as read-only prior work.
- **No PHASTER / geNomad / VirSorter2 prophage-caller output.** MGE calls here are keyword-based over BV-BRC product strings; a proper orthogonal MGE re-annotation is a follow-up (see `failure_analysis.md`).
- **No DefenseFinder / PADLOC re-scan.** The novelty claim (C5) is a re-read of Table S4 against Gao et al. 2020; a modern DefenseFinder/PADLOC audit is a follow-up (see `open_questions.json` OQ2).
- **No wet-lab data.** No fosmid constructs, no phage stocks, no growth curves; those would be de novo experimental work, not replication.

## Provenance chain (audit tag)

Every artifact in `work/` can be regenerated from `paper_fulltext.xml` + `SupplementaryTables.xlsx` + the 6 Python scripts, using only free public endpoints. Every artifact in `report/evidence/` is either (a) a copy of a stable subset of the `work/` outputs promoted to evidence, or (b) an independent second-pass re-derivation (`independent_reproduction/`). The chain is:

```
Europe PMC + Nature suppl → paper_fulltext.xml + SupplementaryTables.xlsx
                        → paper_S5 + paper_S2 (openpyxl)
                        → defense_{representatives,proteins}.fasta
                        → [Stage 1] bvbrc_genome_map.json
                        → [Stage 2] ncbi_proteomes/*.faa
                        → [Stage 3] distribution_summary.json  ← C1, C2, C3-panel
                        → [Stage 4] mge_context_summary.json   ← C4
                        → [Stage 5] crispr_rm_survey.json
                        → [Stage 6] novelty (Table S4 re-read) ← C5
                        → [Stage 7] llm_judge_verdict.txt      ← verdict
```

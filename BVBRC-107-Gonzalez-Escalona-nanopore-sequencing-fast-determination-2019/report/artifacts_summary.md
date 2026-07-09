# Artifacts Summary — BVBRC-107 (González-Escalona et al. 2019, STEC O26:H11)

## Input artifacts (fetched from public sources)

### 1. Deposited PacBio-closed assemblies (NCBI Nucleotide, CC0)
| Accession | Strain | Molecule | Size (bp) | Purpose |
|-----------|--------|----------|-----------|---------|
| CP037943 | CFSAN027343 | chromosome | 5,768,712 | main chr, ST21, Argentina 1999 clinical |
| CP037944 | CFSAN027343 | plasmid | ~90,183 | virulence plasmid (IncFIB + IncB/O/K/Z) |
| CP037945 | CFSAN027346 | chromosome | ~5,672,000 | main chr, ST21, USA 1999 clinical |
| CP037946 | CFSAN027346 | plasmid-1 | ~97,455 | virulence plasmid (shared architecture w/ 343) |
| CP037947 | CFSAN027346 | plasmid-2 | ~74,265 | **AMR plasmid, IncFII, unique to 346** — carries 6 acquired AMR genes |
| CP037941 | CFSAN027350 | chromosome | ~5,513,791 | main chr, ST29, USA 2012 environmental |
| CP037942 | CFSAN027350 | plasmid | ~159,850 | larger virulence plasmid (IncFIB + IncFII) |

Location on disk: `work/ncbi_fasta/CP0379{41..47}.fasta`.
Total input FASTA: ~17 Mb.

### 2. Reference databases
| DB | Version / date | Records | Used for |
|---|---|---|---|
| CGE `plasmidfinder_db` | Bitbucket head | 488 replicons | plasmid Inc typing |
| CGE `virulencefinder_db` | Bitbucket head | 5,102 sequences (used `virulence_ecoli.fsa` + `stx.fsa`) | virulence-gene BLAST cross-check |
| CGE `resfinder_db` | Bitbucket head | 3,212 sequences | AMR-gene reference |
| CGE `serotypefinder_db` | Bitbucket head | ~500 O + H antigens | serotype call |
| NCBI AMRFinderPlus DB | v2024-07-22.1 | (bundled) | primary AMR + virulence caller |
| pubMLST `ecoli_achtman_4` | via `mlst` v2.35.0 | (bundled) | Achtman MLST scheme |

## Output artifacts (this replication)

### 3. Per-strain concatenated FASTA
- `work/strain_343.fasta` (chr + 1 plasmid, ~5.86 Mb)
- `work/strain_346.fasta` (chr + 2 plasmids, ~5.84 Mb)
- `work/strain_350.fasta` (chr + 1 plasmid, ~5.67 Mb)

### 4. Screen results (per strain × per tool)
`report/evidence/*.tsv` (BLAST outfmt-6 or tool-native TSV) + `*.log`:
| File | Strain | Tool | Records |
|------|--------|------|---------|
| `serotype_343.tsv` / `_346.tsv` / `_350.tsv` | 3 | SerotypeFinder BLAST | O + H antigen hits per strain |
| `mlst_343.tsv` / `_346.tsv` / `_350.tsv` | 3 | mlst v2.35.0 | ST call + 7 allele numbers |
| `plasmidfinder_343.tsv` / `_346.tsv` / `_350.tsv` | 3 | PlasmidFinder BLAST | Inc replicon hits by target contig |
| `amrfinder_343.tsv` / `_346.tsv` / `_350.tsv` | 3 | AMRFinderPlus 3.12.8 | AMR + virulence gene calls with %cov, %id, contig, coords |
| `virulence_blast_343.tsv` / `_346.tsv` / `_350.tsv` | 3 | blastn vs `virulence_ecoli.fsa` | independent virulence cross-check |

### 5. Aggregate + verdict
| File | Content |
|------|---------|
| `report/evidence/gene_summary.json` | Per-strain gene-presence matrix; keys `(strain, gene)` → {present, %id, %cov, source_tool} |
| `report/verdict.json` | Argo `argo:gpt-5.2` LLM-judge output: `{verdict: "PARTIAL", coverage_score: 70, agreement_score: 98, justification, one_line_summary}` |
| `report/REPORT.md` | Human-readable replication report (this run's canonical narrative) |
| `report/REPORT.tex` | LaTeX version with dedicated GENUINE CRITIQUE section |
| `report/workflow.md` | Step-by-step reproducibility recipe |
| `report/artifacts_summary.md` | This file |
| `report/failure_analysis.md` | Honest analysis of what did/didn't reproduce and why |
| `report/open_questions.json` | 5 truly open research questions grounded in the paper's methodological gaps |

### 6. Scripts
- `work/run_screens.sh` — driver script for step 4 (per-strain × per-tool loops).
- (Judge prompt + call inline in workflow.md.)

## Artifacts NOT produced (why verdict is PARTIAL)

The paper's C9 (MinION-vs-PacBio de novo congruence) and C10 (MiSeq missed genes)
claims require these additional artifacts, which were **not** generated in this run:

| Missing artifact | Would come from | Cost |
|---|---|---|
| Canu v1.6+ MinION-only assembly (per strain × 3) | SRR8335317, SRR8335318 → Canu on uicgpu | ~2 h + ~10 GB |
| SPAdes MiSeq-only assembly (per strain × 3) | SRR8333590–92 → SPAdes | ~1 h + ~15 GB |
| Per-platform gene-recall diff | rerun step 4 on new assemblies | ~30 min |

Deferred to a follow-up run; see `failure_analysis.md` for details.

## Provenance

- All data fetched from public NCBI + Bitbucket (no auth, no paywall).
- Compute: `ssh uicgpu` (A100), micromamba env `amr` (fully open-source stack).
- LLM judge: Argo `argo:gpt-5.2` (Rick's free Argo endpoint).
- Zero cost to Rick beyond compute time on already-owned uicgpu.
- License chain: paper CC0, GenBank public domain, CGE DBs open (Apache-2.0),
  AMRFinderPlus + mlst open (public-domain / GPL).

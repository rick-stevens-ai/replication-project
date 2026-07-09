# Artifacts Summary — BVBRC-53 (Nakazono 2022)

## Report bundle (`report/`)

| File | Purpose |
|---|---|
| `REPORT.md` | Canonical markdown replication report (primary; verdict PARTIAL) |
| `REPORT.tex` | LaTeX build of the report with a dedicated `GENUINE CRITIQUE` section |
| `open_questions.json` | 5 open scientific questions (biology / translational) grounded in the paper |
| `workflow.md` | Reproducible step-by-step pipeline used for this replication |
| `artifacts_summary.md` | This file — one-stop map of what exists on disk |
| `failure_analysis.md` | Where we fell short, why, and what a fuller replication would need |

## Evidence (`report/evidence/`)

| File | What it holds |
|---|---|
| `genome_stats.txt` | Per-plasmid length, GC%, CDS count; gene-cluster inventory (epi*/nuk*) |
| `blastn_pNuk650_vs_pIVK45.tsv` | Local blastn HSPs (percent identity 80 threshold); source for the 99.6% backbone / 7,781 bp unaligned computation |
| `abricate_plasmidfinder.tsv` | PlasmidFinder rep-typing on all three plasmids (repUS46, repUS23_repA/SAP099B, rep21/pWBG754 in the nukacin lineage; rep39/rep5a-like in pEpi56) |
| `abricate_card.tsv`, `abricate_resfinder.tsv`, `abricate_megares.tsv` | AMR screens — all negative |
| `abricate_vfdb.tsv` | Virulence — no hits |
| `abricate_bacmet2.tsv` | Biocide/metal resistance — only spurious <33% hits |
| `amrfinder_*.tsv` | AMRFinderPlus 4.2.7 per plasmid — no hits |
| `llm_judge_prompt.txt` | Structured judging prompt (claim set C1–C8) |
| `llm_judge_result.json` | LLM judge JSON verdict via Argo `argo:gpt-5.2` |

## Working data (`work/seqs/`)

| File | What it holds |
|---|---|
| `OK031036.fasta` / `OK031036.gb` | pEpi56 (64,386 bp, 81 CDS) |
| `OK031035.fasta` / `OK031035.gb` | pNuk650 (26,160 bp, 29 CDS) |
| `KP702950.fasta` / `KP702950.gb` | pIVK45 reference (21,840 bp, 17 CDS annotated) |

## Key sequence-level numbers (all measured, all matching paper)

| Item | Paper | Measured |
|---|---:|---:|
| pEpi56 length | 64,386 bp | **64,386 bp** ✓ |
| pEpi56 ORFs / CDS | 81 | **81** ✓ |
| pNuk650 length | 26,160 bp | **26,160 bp** ✓ |
| pNuk650 ORFs / CDS | 29 | **29** ✓ |
| pIVK45 length | 21,840 bp | **21,840 bp** ✓ |
| Epidermin KSE56 aa identity vs Tü3298 | 100% | **100% (0 aa mismatches)** ✓ |
| Nukacin KSE650 vs IVK45 prepeptide mismatches | 1 (mature identical) | **1 at leader pos 4 (L↔F); mature identical** ✓ |
| pNuk650 vs pIVK45 backbone identity | shared | **99.6% nt** ✓ |
| pNuk650 insertion vs pIVK45 | ~8 kbp | **5,926 bp block + 1,821 bp block = 7,781 bp unaligned** ✓ |

## Claim × evidence map

| Claim | Verdict | Evidence artifact |
|---|---|---|
| C1 pEpi56 size/ORFs/epi cluster | MATCH | `genome_stats.txt` (pEpi56 block) |
| C2 pNuk650 size/ORFs/nuk cluster | MATCH | `genome_stats.txt` (pNuk650 block) |
| C3 ~8 kbp insertion pNuk650 vs pIVK45 | MATCH (structural) | `blastn_pNuk650_vs_pIVK45.tsv` |
| C4 Epidermin 100% aa identity | MATCH | peptide alignment in `genome_stats.txt` / notebook |
| C5 Nukacin 1-mismatch prepeptide / identical mature | MATCH | peptide alignment in `genome_stats.txt` / notebook |
| C6 Deposits in NCBI | MATCH | fetched FASTA/GB files |
| C7 BV-BRC PlasmidFinder rep-typing applicable | YES | `abricate_plasmidfinder.tsv` |
| C8 Antibacterial activity + ESI-MS mass | OUT OF REACH | wet-lab, not attempted |

## Environment provenance

- Local: Python + BLAST+ + eutils (light).
- uicgpu conda env `bvbrc14` (`/data/stevens/envs/bvbrc14`): abricate 1.4.0
  with DBs dated 2026-Apr-03, AMRFinderPlus 4.2.7.
- Argo proxy `localhost:44497`, model `argo:gpt-5.2` for LLM judge.

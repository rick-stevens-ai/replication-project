# Workflow — BVBRC-87 (Gancz 2021, KpnU95 ST1412)

## Overview

End-to-end replication workflow for a single-isolate *K. pneumoniae* WGS + plasmidology paper. All steps use public, no-auth data + free/OSS tools. Compute host: `uicgpu` (8×A100, proxy internet). Wall time ≤5 minutes (mostly Kleborate).

## Pipeline

```
Paper metadata (DOI, PMID, PMC)
        │
        ▼
┌──────────────────────────────────────────────────────────┐
│ 1. Full-text pull                                        │
│    NCBI eutils efetch db=pmc rettype=xml id=PMC8151138  │
│    → work/paper.xml (169 KB JATS XML)                    │
└──────────────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────────────┐
│ 2. Extract testable claims                               │
│    → 11 claims (C1–C11), 8 genomic + 1 comparative +     │
│      1 provenance + 1 wet-lab                            │
└──────────────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────────────┐
│ 3. Public artifact pull                                  │
│    a. NCBI Datasets REST: assembly GCA_015714665.1       │
│       → work/kpnu95_asm/ (FASTA + protein + GFF)         │
│    b. NCBI eutils efetch db=nuccore MK552109.1           │
│       → work/pKpnU95.fasta + work/pKpnU95.gb             │
│    c. Bitbucket genomicepidemiology/plasmidfinder_db    │
│       → work/plasmidfinder_db/enterobacteriales.fsa      │
└──────────────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────────────┐
│ 4. Genomic replication (parallelizable)                  │
│                                                          │
│   ├─ mlst 2.35.0 --scheme klebsiella kpnu95.fna         │
│   │  → report/evidence/mlst_klebsiella.tsv               │
│   │  (validates C2: ST1412)                              │
│   │                                                      │
│   ├─ Kleborate 3.2.4 --preset kpsc kpnu95.fna           │
│   │  → report/evidence/kleborate_kpsc.tsv                │
│   │  (validates C2 ST, C5 ARGs, C6 chr AMR, C10 K)      │
│   │                                                      │
│   ├─ BLAST+ blastn plasmidfinder_db vs pKpnU95.fasta    │
│   │  -perc_identity 90 -evalue 1e-30                     │
│   │  → report/evidence/plasmidfinder_blast.txt           │
│   │  (validates C4 IncFIB[K] identity)                   │
│   │                                                      │
│   ├─ Biopython assembly stats on kpnu95.fna              │
│   │  → report/evidence/assembly_stats.txt                │
│   │  (validates C3 chromosome bp/GC/ORF)                 │
│   │                                                      │
│   └─ Biopython GenBank feature audit on pKpnU95.gb       │
│      → report/evidence/plasmid_annotation.txt            │
│      (validates C4 CDS count, C5 10-gene resistome,     │
│       C7 persistence operons, C8 non-conjugative)        │
└──────────────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────────────┐
│ 5. Per-claim comparison                                  │
│    For each Cn: paper_value vs tool_output               │
│    → tabulate REPLICATED / PARTIAL / CONTRADICTED /      │
│      UNTESTED / NOT ATTEMPTED                            │
└──────────────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────────────┐
│ 6. LLM-judge aggregate verdict                           │
│    Argo proxy (localhost:44497), argo:gpt-5, T=1        │
│    strict-JSON reply — no regex verdict                  │
│    → report/evidence/llm_judge_verdict.json              │
└──────────────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────────────┐
│ 7. Report generation                                     │
│    → report/REPORT.md (canonical narrative)              │
│    → report/REPORT.tex (LaTeX + genuine-critique)        │
│    → report/open_questions.json (5 comparative openers)  │
│    → report/artifacts_summary.md                         │
│    → report/failure_analysis.md                          │
└──────────────────────────────────────────────────────────┘
```

## Tool inventory

| Tool | Version | Role |
|---|---|---|
| NCBI eutils (efetch) | 2024-era API | JATS + FASTA + GenBank pulls |
| NCBI Datasets REST | v2alpha | assembly download |
| mlst | 2.35.0 (Seemann) | 7-locus MLST, klebsiella scheme |
| Kleborate | 3.2.4 (Holt lab) | species/ST/K/O typing, AMR, virulence, MIC prediction (`kpsc` preset) |
| PlasmidFinder DB | 2024-era, `enterobacteriales.fsa` | 159 replicon references |
| BLAST+ | blastn / makeblastdb | replicon typing |
| Biopython | 1.87 | assembly stats + GenBank feature audit |
| Argo proxy | local :44497 | LLM-judge (`argo:gpt-5`), free per project policy |

## Design choices

- **Real public data only.** No simulation, no substitution. Everything pulled from NCBI + Bitbucket.
- **No regex verdicts.** Aggregate verdict is LLM-judged with strict-JSON reply, not string-matching.
- **Multiple independent methods per claim where possible.** Example: 10-gene resistome (C5) is confirmed by Kleborate (whole-assembly call) AND by direct GenBank feature audit of the plasmid — two independent code paths reach the same 10-ARG count.
- **Byte-for-byte comparison where the paper reports exact numbers.** Chromosome 5,055,295 bp and plasmid 180,286 bp are checked as integers, not ranges.
- **Wet-lab claims explicitly excluded, not silently skipped.** C11 (plasmid curing, *C. elegans* killing, artificial urine, copper) requires the physical strain → labelled `NOT ATTEMPTED` in the claims table so the reader cannot mistake absence for verification.

## Reproducibility

- All commands + tool outputs captured under `report/evidence/`.
- All raw input artifacts under `work/`.
- Assembly + plasmid deposited by original authors (`GCA_015714665.1`, `MK552109.1`), so anyone can re-run this pipeline end-to-end with no auth in ≤5 minutes on a modest workstation.
- Reproducibility rating: **5/5** for the computational claims scoped here.

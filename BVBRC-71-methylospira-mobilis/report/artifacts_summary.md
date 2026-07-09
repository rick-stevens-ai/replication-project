# Artifacts Summary — BVBRC-71

## Directory Layout (expected)

```
BVBRC-71-methylospira-mobilis/
├── report/
│   ├── REPORT.md                    (11 KB — canonical narrative report)
│   ├── REPORT.tex                   (LaTeX version with dedicated GENUINE CRITIQUE section)
│   ├── open_questions.json          (5 open questions grounded in the paper)
│   ├── workflow.md                  (this replication's step-by-step method)
│   ├── artifacts_summary.md         (this file)
│   └── failure_analysis.md          (what didn't fully replicate + why)
├── genomes/
│   ├── CP044205.gb                  (~10.6 MB — Shm1 chromosome, gbwithparts)
│   └── AE017282.gb                  (~7.2 MB  — M. capsulatus Bath, gbwithparts)
├── work/
│   ├── genome_stats.py              (length, GC%, feature counts, marker tallies)
│   ├── gene_products_scan.py        (37 pathway-marker regex over CDS product/gene/note)
│   ├── rrna_ani2.py                 (16S extraction + Biopython global alignment)
│   ├── judge2.py                    (LLM-judge caller, Argo proxy)
│   └── downloads.sha256             (SHA-256 of the two GenBank flatfiles)
└── evidence/
    └── llm_judge_verdict.json       (single-judge verdict: PARTIAL, 100% cov, 86% agr)
```

## Key Numeric Artifacts (from REPORT.md, Section 4.1)

| Artifact | Paper | Independent | Source |
|----------|-------|-------------|--------|
| Shm1 genome length | 4.7 Mbp | 4,703,534 bp | `work/genome_stats.py` on CP044205.gb |
| Shm1 G+C | 54 mol% | 54.05% | `work/genome_stats.py` (from sequence) |
| Shm1 rRNA operons | 3 | 3 (3× 16S+23S+5S) | `work/genome_stats.py` (feature counts) |
| Shm1 tRNA | 49 | 48 | `work/genome_stats.py` (feature counts) |
| Shm1 CDS | 4858 (RAST) | 4214 (PGAP) | `work/genome_stats.py` (CDS feature count) |
| Bath length | 3.3 Mbp | 3,304,561 bp | `work/genome_stats.py` on AE017282.gb |
| Bath G+C | 63.6 mol% | 63.58% | `work/genome_stats.py` |
| Bath rRNA operons | 2 | 2 | `work/genome_stats.py` |
| 16S identity Shm1↔Bath | 94.06% | 93.89% | `work/rrna_ani2.py` |
| Shm1 IS elements | >200 | 194 transposase-CDS | `work/gene_products_scan.py` |

## Key Qualitative Artifacts (REPORT.md, Section 4.2)

- **Chemotaxis expansion:** 52 chemotaxis CDS in Shm1 vs. 2 in Bath (35× more) — `work/gene_products_scan.py`
- **Flagellar apparatus:** 44 CDS in Shm1, complete fli*/flg*/motAB families
- **V-Fe nitrogenase asymmetry:** vnfD=1, vnfK=1 in Shm1; 0 in Bath
- **Mo-Fe nitrogenase:** Shm1 nifH=1, nifD=2, nifK=2; Bath 1/1/1
- **pMMO clusters:** ≥ 2 pmoC subunit sets in Shm1 (F6R98_01470–1480 + paralogs)
- **sMMO cluster:** F6R98_10895–10905 with mmoD (single cluster in Shm1)
- **CRISPR Type I-E cas cassette:** cas1/2/3, casA/B, cas5e, cas6e, cas7e all annotated in Shm1
- **Terminal oxidases:** cydA/B/X = 7 CDS in Shm1 (bd-type, low-affinity); cbb3-type present via cytochrome-oxidase set
- **PEP carboxylase asymmetry:** present in Shm1, absent in Bath — confirmed
- **Transposase load:** 194 vs. 41 (Shm1 4.7× more than Bath)

## LLM-Judge Artifact

**File:** `evidence/llm_judge_verdict.json`

- verdict: `PARTIAL`
- coverage_pct: 100
- agreement_pct: 86
- 17 of 21 claims `agrees=true`
- 4 flagged: **C4** (tRNA 48 vs 49), **C5** (RAST 4858 vs PGAP 4214), **C12** (MxaFI/XoxF substring-match), **C16** (194 vs >200 IS)
- judge model: `argo:gpt-5.2` at temperature 0.1, max_tokens 1800
- judge fallback path: `argo:claude-opus-4.7` reproducibly 502'd at max_tokens ≥ 2500

## Provenance
- All computations from public GenBank records (NCBI E-utils, free tier).
- Two flatfiles hashed at `work/downloads.sha256`.
- Argo proxy free (localhost:44497 on CherryRd).
- Total compute: <5 min on uicgpu (Biopython) + ~30 s LLM judge call.

## Not Present (deliberate)
- **No RAST re-annotation** (would resolve C5).
- **No ISfinder / ISEScan** (would resolve C16).
- **No HMMER / BLAST orthology** (would resolve C12).
- **No multi-judge ensemble** (single Argo judge only).

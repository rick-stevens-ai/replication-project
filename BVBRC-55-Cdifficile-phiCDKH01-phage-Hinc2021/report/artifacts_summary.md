# Artifacts Summary — phiCDKH01 Replication (BVBRC-55, Hinc et al. 2021)

**Directory:** `~/Dropbox/REPLICATE-PROJECT/BVBRC-55-Cdifficile-phiCDKH01-phage-Hinc2021/`
**Verdict:** REPLICATED (LLM-judge 93/100)
**Date:** 2026-07-02

---

## 1. Top-level structure (expected)

```
BVBRC-55-Cdifficile-phiCDKH01-phage-Hinc2021/
├── report/
│   ├── REPORT.md              # canonical human-readable report
│   ├── REPORT.tex             # LaTeX version (this backfill)
│   ├── workflow.md            # replication workflow (this backfill)
│   ├── artifacts_summary.md   # this file
│   ├── failure_analysis.md    # honest failure analysis (this backfill)
│   └── open_questions.json    # 5 open questions (this backfill)
├── extraction/                # (paper text extraction; marker.md not present)
├── evidence/                  # primary evidence artifacts (see §2)
└── work/                      # scripts + intermediate files (see §3)
```

---

## 2. Evidence artifacts (per REPORT.md §3 method)

| File | Produced by | Contents | Supports claim |
|---|---|---|---|
| `evidence/genome_stats.json` | Biopython 1.87 on MN718463 | length, GC%, CDS count, per-CDS strand, tRNA/rRNA count | C1, C2, C3, C4, C5 |
| `evidence/phiCDKH01_vs_phiCD24-1.tsv` | BLASTn 2.17.0 + dedup | pairwise per-position best pident vs phiCD24-1 (LN681534) | C7 |
| `evidence/phiCDKH01_intergenomic_dedup.json` | custom `viridic_matrix2.py` | phiCDKH01 vs each of 12 neighbours (phiCD24-1 + 11 comparators) | C7, C9 |
| `evidence/viridic_matrix_dedup.tsv` | custom `viridic_matrix2.py` | full 13×13 VIRIDIC-style intergenomic identity matrix with per-query-position best-pident deduplication | C9 |
| `evidence/crispr_phiCDKH01.txt` | `minced -minNR 2` on MN718463 | 5 spacers (36/35/35/37/37 bp), 6 repeats, consensus `GTATTATATTAACTAAGTGGTATGTAAAGT`, span 30,200–30,559 | C8 |
| `evidence/prophage_localization.tsv` | BLASTn phage vs host contig | prophage span 288,611–333,698 @ 99.7% identity on JACSDL010000003.1 | C10 |
| `evidence/llm_judge_verdict.txt` | Argo gpt-5.2 (free) | verdict REPLICATED, score 93/100 | overall |

---

## 3. Work / script artifacts

| Path | Role |
|---|---|
| `work/viridic_matrix2.py` | VIRIDIC-style intergenomic-identity computation with per-query-position best-pident deduplication (avoids overlapping-HSP double counting) |
| `work/` (other files) | intermediate BLAST DBs, raw BLAST outputs, per-genome FASTAs — *not* meant to be re-consumed downstream; the `evidence/` files are the canonical deliverables |

**Note:** the task instructions explicitly warned against reading anything in `work/` because raw sequence dumps burn context budget. This summary reflects the structure implied by REPORT.md §3, not a directory listing.

---

## 4. Trace: which claim → which evidence file

| Claim | Paper says | This replication says | Evidence file |
|---|---|---|---|
| C1 length | 45,089 bp | 45,089 bp (exact) | `genome_stats.json` |
| C2 GC | 28.7% | 28.72% (exact) | `genome_stats.json` |
| C3 ORFs | 66 | 66 (exact) | `genome_stats.json` |
| C4 strand | 53(+)/13(−) | 52(+)/14(−) (off by 1) | `genome_stats.json` |
| C5 tRNA/rRNA | 0 | 0 (exact) | `genome_stats.json` |
| C6 functional ORFs | 37 (myRAST) | 9 (GenBank deposit) — partial | `genome_stats.json` + note |
| C7 closest relative | phiCD24-1 @ 89% | phiCD24-1 @ 81.8% VIRIDIC WG (~96% on aligned regions) | `phiCDKH01_vs_phiCD24-1.tsv` |
| C8 CRISPR | 5 spacers, 35–37 bp | 5 spacers, 36/35/35/37/37 bp (exact) | `crispr_phiCDKH01.txt` |
| C9 novelty | novel vs other C. difficile phages | 11 comparators all ≤9.9%; only phiCD24-1 congeneric | `viridic_matrix_dedup.tsv`, `phiCDKH01_intergenomic_dedup.json` |
| C10 integration | contig3 nt 288,650–333,698 | nt 288,611–333,698 @ 99.7% (Δ=39 bp) | `prophage_localization.tsv` |

---

## 5. Report artifacts

| File | Format | Audience |
|---|---|---|
| `report/REPORT.md` | Markdown | canonical human-readable (Rick, reviewers) |
| `report/REPORT.tex` | LaTeX | typeset PDF for archival / distribution |
| `report/workflow.md` | Markdown | reproducibility instructions |
| `report/artifacts_summary.md` | Markdown | this file — index of what exists and why |
| `report/failure_analysis.md` | Markdown | honest failure / partial-success accounting |
| `report/open_questions.json` | JSON | 5 open questions with basis + next steps |

---

## 6. External accessions (permanent, public)

| Accession | Type | Bytes-ish | Role |
|---|---|---|---|
| MN718463 | GenBank (nucleotide) | ~45 kb | primary — phiCDKH01 genome |
| JACSDL010000003.1 | GenBank contig | ~410 kb | host contig containing integrated prophage |
| LN681534 | GenBank | ~50 kb | phiCD24-1 (closest relative) |
| PMC8270841 | Europe PMC XML | small | paper full text |
| 11 comparator accessions | GenBank | small–medium each | novelty panel (phiCD6356, phiCDHM11/13/14/19, phiCD111/146/211/505/506, phiCDIF1296T) |

All resolvable via NCBI E-utilities without authentication.

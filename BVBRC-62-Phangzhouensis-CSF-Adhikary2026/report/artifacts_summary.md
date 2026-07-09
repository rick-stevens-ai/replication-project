# Artifacts Summary — BVBRC-62
## *Providencia hangzhouensis* HL_Adamas-11 replication

**Directory root:** `~/Dropbox/REPLICATE-PROJECT/BVBRC-62-Phangzhouensis-CSF-Adhikary2026/`

---

## 1. Source paper artifacts

| File | Purpose | Provenance |
|---|---|---|
| `work/paper_fulltext.xml` | Full text of Adhikary et al. 2026 (MRA e01372-25) | Pulled from Europe PMC REST `.../PMC13248694/fullTextXML` (Open Access, CC-BY 4.0) |

---

## 2. Deposited genome artifacts (from NCBI)

Assembly identity: **GCA_053592895.1 / GCF_053592895.1** (ASM5359289v1), matched to paper by exact `Coverage = 91.664×` and `ContigN50 = 16,147 bp`.

| File | Purpose |
|---|---|
| `genomes/…/GCA_053592895.1_ASM5359289v1_genomic.fna` | Assembly nucleotide FASTA (493 contigs, 5,024,867 bp) |
| `genomes/…/protein.faa` | Predicted protein sequences (4,935 CDS) |
| `genomes/…/genomic.gff` | GFF3 annotation |
| `genomes/…/assembly_data_report.jsonl` | NCBI assembly report (contigs, coverage, GC, N50, plasmid labels) |

Note: NCBI also holds duplicate deposit **GCF_056140255.1** (same biosample). Not used.

---

## 3. Computed / replication artifacts

| File | Tool | Content |
|---|---|---|
| `work/fastani_ref.txt` | fastANI v1.x | ANI vs *P. hangzhouensis* GCF_029193595.2 → **98.46%** |
| (skani output) | skani | ANI vs same reference → **98.62%** |
| `work/mlst_out.txt` | mlst v2.33.1 | ST call: `-` (unassigned); alleles fusA(17) gyrB(105) ileS(29) lepA(~49) leuS(49) |
| `work/mlst.log` | mlst v2.33.1 | Run log (scheme selected: `providencia`) |
| `work/amrfinder_nuc.tsv` | AMRFinderPlus v4.2.7, DB 2026-05-15.1 | 27 AMR rows (nucleotide `--plus` mode) |
| `work/amrfinder_nuc.log` | AMRFinderPlus v4.2.7 | Run log |
| `work/judge_input.md` | (hand-assembled) | Paper claims vs replication results table + free-text discrepancies |
| `work/judge_output.md` | Argo `gpt-5.2`, temp 0 | Verdict PARTIAL; Coverage 8/10; Agreement 7/10; rationale |

---

## 4. Report artifacts

| File | Purpose |
|---|---|
| `report/REPORT.md` | Human-readable synthesis (10 KB) — canonical source of truth |
| `report/REPORT.tex` | Detailed LaTeX report + GENUINE CRITIQUE section |
| `report/open_questions.json` | 5 truly-open follow-up questions with basis + next steps |
| `report/workflow.md` | End-to-end methodology / commands / non-steps |
| `report/artifacts_summary.md` | This file |
| `report/failure_analysis.md` | What did not replicate and why |

---

## 5. Numeric-claim replication snapshot (from REPORT.md §3)

| Claim | Paper | Replicated | Status |
|---|---|---|---|
| Contigs | 493 | 493 | ✓ exact |
| Total length (bp) | 5,034,782 | 5,024,867 | ~✓ (−0.20%) |
| N50 (bp) | 16,147 | 16,147 | ✓ exact |
| Coverage (×) | 91.664 | 91.664 | ✓ exact |
| GC (%) | **49.5** | **42.35 / 42.5** | ✗ **DISCREPANT** (paper typo) |
| CDS | 4,935 | 4,935 | ✓ exact |
| tRNA | 59 | 59 | ✓ exact |
| rRNA | 4 | 4 | ✓ exact |
| Plasmids | chromosome + 4 | 4 (pAA860, pAB133, pAC129, pnovel_c01a4b) | ✓ |
| ANI vs P. hangzhouensis (%) | 98.75 | 98.46 (fastANI) / 98.62 (skani) | ✓ (within 0.3%) |
| MLST | ST-356 | `-` (unassigned) | ✗ scheme-version mismatch |
| β-lactamases (5 named) | 5/5 | 5/5 + 3 extra | ✓ |
| Aminoglycoside class | 3 genes | class fully confirmed; 1 typo, 1 name correction | ✓ (class); typo (allele) |
| Macrolide/phenicol (5 named) | 5/5 | 5/5 + 3 extra | ✓ |

---

## 6. External references used

- Reference genome: **GCF_029193595.2** (*P. hangzhouensis* strain PR-310)
- PubMLST *Providencia* scheme (as bundled in `mlst` v2.33.1) — version-mismatched with paper
- AMRFinderPlus reference DB version **2026-05-15.1**
- Europe PMC full-text REST API
- NCBI `datasets` CLI for genome retrieval

---

## 7. Judge

- Model: Argo `gpt-5.2` (temp 0, free-tier via Argo proxy at :44497)
- Input: `work/judge_input.md`
- Output: `work/judge_output.md` → **PARTIAL** / Coverage 8/10 / Agreement 7/10

---

## 8. Constraint compliance

- All tools free / open-source. AMRFinderPlus, fastANI, skani, mlst, Biopython, NCBI datasets CLI.
- LLM judge on free Argo endpoint (no paid API).
- No paid PDF services used (Europe PMC XML for full text).

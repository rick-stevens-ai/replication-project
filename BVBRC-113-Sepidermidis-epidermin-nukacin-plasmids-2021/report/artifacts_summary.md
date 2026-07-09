# BVBRC-113 — Artifacts Summary

**Paper:** Nakazono et al. 2022 (PLoS ONE, doi:10.1371/journal.pone.0258283)
**Verdict:** PARTIAL, 74/100
**Generated:** 2026-07-05

---

## Report files (`report/`)

| File | Purpose |
|---|---|
| `REPORT.md` | Canonical Markdown replication report (source of truth for verdict + numbers) |
| `REPORT.tex` | LaTeX mirror with an added dedicated GENUINE CRITIQUE section |
| `open_questions.json` | 5 truly open questions (biosynthetic completeness, immunity co-occurrence, mobilization, CoNS comparative diversity, activity-spectrum gap) |
| `workflow.md` | Numbered, reproducible workflow (Stages 0–7) |
| `artifacts_summary.md` | This file |
| `failure_analysis.md` | Post-hoc analysis of what did not fully replicate and why |

## Evidence files (`report/evidence/`)

| File | Content |
|---|---|
| `plasmid_summary.json` | Length, topology, CDS/gene counts, epi*/nuk* gene inventory for OK031036, OK031035, KP702950, X62386, U77778 |
| `bacteriocin_alignment.json` | Position-by-position mismatch counts for epiA (KSE56 vs Tü3298) and nukA (KSE650 vs IVK45); mature-peptide comparison |
| `pNuk650_vs_pIVK45_blast.json` | BLASTP hit table + no-ortholog count using pident≥30% AND qcov≥50% |
| `llm_judge_verdict.txt` | Structured per-claim MATCH/PARTIAL/MISMATCH + overall verdict + 0–100 score from argo:claude-sonnet-4.6 |

## Working files (`work/`)

| File | Content |
|---|---|
| `paper.xml` | Full PMC XML of the paper (225,843 B, from `efetch db=pmc id=PMC8765612 rettype=xml`) |
| `sequences/OK031036.{gb,fasta}` | pEpi56 GenBank + FASTA |
| `sequences/OK031035.{gb,fasta}` | pNuk650 GenBank + FASTA |
| `sequences/KP702950.{gb,fasta}` | pIVK45 comparator GenBank + FASTA |
| `sequences/X62386.{gb,fasta}`   | Tü3298 epidermin reference |
| `sequences/U77778.{gb,fasta}`   | Nukacin locus reference (context) |
| `analyze_plasmids.py` | Structural parsing (Stage 3) |
| `bacteriocin_align.py` | epiA / nukA identity (Stage 4) |
| `compare_plasmids.py` | pNuk650 vs pIVK45 BLASTP delta (Stage 5) |
| `llm_judge.py` | Argo-hosted LLM judge (Stage 6) |

---

## Key quantitative results (one-line each)

- **pEpi56**: 64,386 bp, circular, 81 CDS → MATCH paper.
- **pNuk650**: 26,160 bp, circular, 29 CDS → MATCH paper.
- **pIVK45**: 21,840 bp → MATCH paper.
- **pNuk650 − pIVK45 size**: +4,320 bp → MATCH paper's "larger" claim.
- **pNuk650 − pIVK45 ORF delta**: +12 raw / +13 no-ortholog vs paper's "+7" → PARTIAL.
- **epiA KSE56 vs Tü3298**: 2 nt mismatches (both synonymous), 0 aa mismatches, 100.0% aa identity → EXACT MATCH.
- **nukA KSE650 vs IVK45**: 1 aa mismatch at prepeptide position 4 (L↔F); mature 27-aa peptide identical → EXACT MATCH.
- **epi cluster on pEpi56**: 11 named epi loci (epiP Q D C B A T′ H F E G); no explicit epiY annotation → PARTIAL (naming ambiguity).
- **nuk cluster on pNuk650**: all 7 canonical nuk genes present (nukA M T F E G H) → MATCH.
- **LLM judge**: PARTIAL, 74/100 (argo:claude-sonnet-4.6; opus-4.7 and opus-4.8 both 502'd on the ~30 kB payload).

## Deposits verified

- NCBI `OK031036` (pEpi56, 64,386 bp) — retrieved and parsed successfully.
- NCBI `OK031035` (pNuk650, 26,160 bp) — retrieved and parsed successfully.

## What is NOT in these artifacts

- No wet-lab data (purification, MS, plasmid curing, MW2 braRS assays, M. luteus co-culture, spectrum panels).
- No Marker-parsed extraction (`extraction/marker.md` not present at write time).
- No re-annotation of pIVK45 with a normalized pipeline (Prokka/Bakta) — the "+7 ORFs" discrepancy is documented but not re-adjudicated.

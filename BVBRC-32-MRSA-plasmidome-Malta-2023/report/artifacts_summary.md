# Artifacts Summary — BVBRC-32

Replication of Al-Trad et al. 2023 MRSA plasmidome (HSNZ, Kuala Terengganu,
Malaysia; DOI 10.3390/antibiotics12040733; BioProject PRJNA722830).
Directory retains legacy `-Malta-2023` tag; paper is Malaysia.

## Report-directory files

| File | Purpose | Source of truth? |
|---|---|---|
| `REPORT.md` | Canonical human-readable replication report; methods, claim table (C1–C11), results, verdict. | ✅ Source of truth |
| `REPORT.tex` | LaTeX rendering of REPORT.md with a dedicated Genuine Critique section. | Derived |
| `open_questions.json` | 5 grounded open research questions, each with `q`, `basis` (rooted in REPORT.md), `next_steps`. | Derived |
| `workflow.md` | 10-stage pipeline from paper ID → data pull → BLAST → judge → report. | Derived |
| `artifacts_summary.md` | This file — artifact inventory. | Derived |
| `failure_analysis.md` | Honest accounting of what did not reproduce and why. | Derived |
| `judge_verdict.md` | Per-claim LLM-judge assessment (`argo:gpt-5.2`). Referenced by REPORT.md §5. | External (judge) |

## Upstream data artifacts (per REPORT.md)

| Item | Value |
|---|---|
| BioProject | PRJNA722830 (study's own submissions) |
| Assemblies pulled | 88 GCA (72.8 MB FASTA-only, genome level) |
| Assemblies cited by paper | 94 total (79 sequenced + 15 previously published) |
| Delta | 6 assemblies not pulled (the 15 external minus overlap) |
| Retrieval tool | NCBI `datasets` v2 |

## Reference databases used

| DB | Purpose | Thresholds |
|---|---|---|
| CGE PlasmidFinder (Gram+) | Replicase superfamily typing | ≥80% id, ≥60% cov |
| CGE ResFinder (`all.fsa`) | AMR gene detection | ≥90% id, ≥60% cov |
| CGE DisinFinder (qac) | Biocide gene detection | ≥80% id, ≥60% cov |
| (heavy-metal operon DB) | **Not used** — C11 not tested | n/a |

## Key numerical outputs (from REPORT.md)

### Plasmid replicon landscape
| Superfamily | Paper (n plasmids) | Replication (loci) | Replication (genomes) |
|---|---|---|---|
| RepL       | 63 (most common) | 67 | 66 |
| RepA_N     | 57  | 60 | 51 |
| Rep_1      | 54  | 57 | 52 |
| Rep_3      | (39 as RepA_N+Rep_3) | 58 | 57 |
| Rep_trans  | —   | 16 | 15 |
| Rep_2      | 2   | —  | 2  |
| PriCT_1    | 1   | 1  | 1  |
| (Inc18)    | not in paper's 7 | 20 | 20 |
| **Total**  | 189 curated plasmids | **279 loci** | — |

### Resistance gene tallies
| Gene | Genomes | Plasmid-borne | Note |
|---|---|---|---|
| mecA | 88 | — | universal MRSA marker (C10 verified exact) |
| blaZ | 87 | 17 | β-lactamase, largely chromosomal/Tn |
| erm(C) | 67 | 66 | MLS_B, RepL small plasmid (C6 verified) |
| tet(K) | 5  | plasmid-borne | rare AMR (C8) |
| tet(L) | 3  | plasmid-borne | rare AMR (C8) |
| cat    | 3  | plasmid-borne | rare AMR (C8) |
| aadD   | 2  | plasmid-borne | rare AMR (C8) |
| mupA   | 1  | plasmid-borne | rare AMR (C8) |
| erm(B) | 1  | plasmid-borne | rare AMR (C8) |
| lnu    | 1  | plasmid-borne | rare AMR (C8) |
| aac(6′)-aph(2″) | 23 | mixed | largely chromosomal/Tn4001 |
| qacA/qacB | 5 | 5 | biocide (C9 verified) |

### Coverage summary
- 85/88 carry ≥1 replicon; **3 plasmid-free** (matches paper's exactly-3).
- All 7 paper replicase superfamilies detected + 1 extra (Inc18).
- Every isolate is genotypically MRSA (mecA 88/88).

## Verdict summary
| Category | Count |
|---|---|
| VERIFIED / VERIFIED (exact) | 8 (C1, C2, C3, C5, C6, C8, C9, C10) |
| PARTIAL | 2 (C4, C7) |
| NOT TESTED | 1 (C11) |
| **Overall** | **PARTIAL–to–STRONG REPLICATION** (judge: PARTIAL) |

## Tooling / infra
- BLAST+ (local, CherryRd).
- NCBI `datasets` v2 CLI.
- LLM judge: `argo:gpt-5.2` via Argo free endpoint (opus-4.8 502).

## Known artifacts flagged in REPORT.md
- Enterobacterales `blaTEM` allele cross-hit in a single genome — excluded
  from plasmid-AMR tally as a raw-allele-DB artifact.
- Extra Inc18 signal — documented as DB-version / threshold sensitivity,
  not a contradiction of the paper's 7-superfamily count.

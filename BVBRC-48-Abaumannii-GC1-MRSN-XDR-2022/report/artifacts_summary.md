# Artifacts Summary — BVBRC-48 (Harmer 2022, MRSN 56 GC1 A. baumannii)

**Dir root:** `~/Dropbox/REPLICATE-PROJECT/BVBRC-48-Abaumannii-GC1-MRSN-XDR-2022/`
**Verdict:** REPLICATED
**Compute:** uicgpu (A100 host); envs `bvbrc28` + `bvbrc14`
**LLM judge:** free Argo `argo:gpt-5.2`, T=0 (coverage 9/10, agreement 9/10)

---

## Report / narrative

| File | Type | Description |
|---|---|---|
| `report/REPORT.md` | Markdown | Primary replication report — paper summary, 8-claim test table, method, results, verdict, limitations, `WAVE_RESULT` footer. |
| `report/REPORT.tex` | LaTeX | Formal typeset sibling of REPORT.md with an additional dedicated **Genuine Critique** section (9 concrete criticisms). |
| `report/open_questions.json` | JSON | 5 open, non-superficial questions grounded in A. baumannii GC1 MRSN XDR clinical genomics, each with basis + concrete next_steps. |
| `report/workflow.md` | Markdown | Step-by-step pipeline: paper acquisition → genome fetch → MLST → 3-caller resistome → localization → variants → IS counting → ampC context → plasmid identity → judge scoring → packaging. |
| `report/artifacts_summary.md` | Markdown | This file — inventory of everything produced. |
| `report/failure_analysis.md` | Markdown | What failed, what partially failed, what was avoided by design; root causes and lessons. |

## Source data (inputs, all public)

| Accession / ID | Kind | Source | Use |
|---|---|---|---|
| PMC9244215 | Paper full text (XML) | Europe PMC REST `fullTextXML` | Claim extraction, accession harvest. |
| PRJNA742487 | BioProject | NCBI | Discovery only — assembly link (GCA_021484925.1/CP090606) rejected as later, different assembly. |
| CP080452.1 | Chromosome (4,033,258 bp) | NCBI eutils `efetch` | Primary genome — all analyses. |
| CP080453.1 | pMRSN56-1 (2,178 bp) | NCBI eutils `efetch` | Replicon size + AMR-absence check. |
| CP080454.1 | pMRSN56-2 (2,725 bp) | NCBI eutils `efetch` | Replicon size + AMR-absence + identity vs pA85-1. |
| CP080455.1 | pMRSN56-3 (6,772 bp) | NCBI eutils `efetch` | Replicon size + AMR-absence check. |
| CP080456.1 | pMRSN56-4 (8,731 bp) | NCBI eutils `efetch` | Replicon size + AMR-absence + identity vs pA1-1. |
| CP021783 | Comparator plasmid pA85-1 | NCBI | BLAST vs pMRSN56-2 (C8). |
| CP010782 | Comparator plasmid pA1-1 | NCBI | BLAST vs pMRSN56-4 (C8). |
| EU029998 | Canonical IS*Aba1* transposase | NCBI | blastn query for IS*Aba1* copy-number count. |
| WP_001988464 | IS*Aba125*-family tnpA (341 aa) | NCBI | tblastn query for IS*Aba125* copy-number count. |

## Tools / dependencies

| Tool | Version | Env | Purpose |
|---|---|---|---|
| NCBI Datasets | 18.32.0 | bvbrc28 | Assembly / genome fetch (also used to interrogate BioProject links). |
| NCBI eutils (efetch) | — | bvbrc28 | Direct-by-accession replicon fetch (the actual method used). |
| mlst | 2.33.1 | bvbrc14 | Pasteur (`abaumannii_2`) + Oxford (`abaumannii`) MLST. |
| AMRFinderPlus | 4.2.7 | bvbrc14 | Resistome + gyrA/parC point mutations (`--organism Acinetobacter_baumannii --plus`). |
| abricate | 1.4.0 | bvbrc14 | 2nd + 3rd resistome callers (CARD, ResFinder databases). |
| BLAST+ | — | bvbrc28 | `makeblastdb`, `blastn`, `tblastn` for IS counting, ampC context, plasmid identity. |
| Argo proxy (gpt-5.2) | — | (cherryrd :44497 tunnel from uicgpu) | Free LLM judge for coverage/agreement scoring, T=0. |

## Key numerical results (all sourced, none fabricated)

| Item | Value | Source |
|---|---|---|
| Chromosome length | 4,033,258 bp | FASTA of CP080452.1 |
| Chromosome GC | 39.19 % | Direct count on CP080452.1 |
| Plasmid sizes | 2178 / 2725 / 6772 / 8731 bp | FASTA of CP080453–56 |
| MLST Pasteur | ST1 (cpn60-1, fusA-1, gltA-1, pyrG-1, recA-5, rplB-1, rpoB-1) | mlst 2.33.1 |
| gyrA point mut | S81L, 99.89 % id vs WP_000116450.1 | AMRFinderPlus 4.2.7 |
| IS*Aba1* chromosome count | 20 | blastn (EU029998, ≥99 % id, transposase region) |
| IS*Aba125* chromosome count | 2 | tblastn (WP_001988464, 100 %/100 %) |
| IS*Aba1* → ampC gap | 10 bp | Coord diff (IS*Aba1* 2,823,501–2,824,068 vs ADC start 2,824,078) |
| pMRSN56-2 vs pA85-1 | 99.89 % over 2726 bp | blastn |
| pMRSN56-4 vs pA1-1 | 100.00 % over 8731 bp | blastn |
| Judge coverage / agreement | 9/10 / 9/10 | free Argo gpt-5.2, T=0 |

## Provenance & reproducibility notes

- All inputs are fetched by explicit accession (not by BioProject auto-select) after we discovered that PRJNA742487 links to a later, different assembly (GCA_021484925.1/CP090606, 4,153,776 bp) that does not match the paper. Pin by replicon accession, not by BioProject.
- All tools are open-source with versions pinned above.
- LLM judge is free-tier Argo; no paid endpoint was used.
- No manual edits to FASTA; no synthetic reads; no cherry-picked callers. Cross-caller agreement is the primary confidence gate.

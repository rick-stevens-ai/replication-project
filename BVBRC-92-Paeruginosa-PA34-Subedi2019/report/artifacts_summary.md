# Artifacts Summary — Subedi et al. (2019) PA34 Replication

**Project:** X-100 replication project, BVBRC set (index 92)
**Working directory (uicgpu):** `/data/stevens/BVBRC-92-PA34/`
**Report directory (Dropbox):** `~/Dropbox/REPLICATE-PROJECT/BVBRC-92-Paeruginosa-PA34-Subedi2019/`

---

## Public artifacts acquired

### Paper
| Artifact | Source | Size | License |
|---|---|---:|---|
| Subedi et al. 2019 PDF | `https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0215038&type=printable` | 3.7 MB | CC-BY 4.0 (PLOS) |
| Rasterized text | `pdftotext -layout` of the above | — | — |

Stored at `work/paper.pdf` + `work/paper.txt`.

### Genome sequences (NCBI Entrez efetch, no auth)
| Accession | Record | Fetched formats | Purpose |
|---|---|---|---|
| CP032552 | PA34 chromosome (6,810,079 bp, 66.1% GC, 6,462 CDS) | FASTA + GenBank | Primary — Table 2 + per-locus verification |
| MH547560 | pMKPA34-1 (95,404 bp, 57.22% GC, 98 CDS) | FASTA + GenBank | Primary — plasmid AMR verification |
| MH547561 | pMKPA34-2 (26,862 bp, 61.00% GC, 32 CDS) | FASTA + GenBank | Primary — plasmid AMR / Tn7 verification |
| AE004091 | PAO1 reference | FASTA + GenBank | Pan-genome reference |
| CP000438 | PA14 reference | FASTA + GenBank | Pan-genome reference |
| CP008739 | VRFPA04 reference (ocular) | FASTA + GenBank | Pan-genome reference |

Total ~26.6 MB. Staged on `uicgpu:/data/stevens/BVBRC-92-PA34/`; file list in `report/evidence/genomes_downloaded.txt`. Easily re-derived from NCBI on demand.

### BV-BRC cross-reference (public REST API)
| Artifact | Source | Size |
|---|---|---:|
| `sp_gene` specialty-gene table for `genome_id` 287.6355 | `https://www.bv-brc.org/api/sp_gene/?eq(genome_id,287.6355)&...` | 295 KB |

Stored at `report/evidence/bvbrc_spgene_pa34.json`. Contains 251 Antibiotic Resistance + 37 Metal Resistance annotations.

---

## Derived artifacts (products of this replication)

### Recomputed / verified numbers
| File | Contents |
|---|---|
| `report/evidence/summary_verification.json` | Machine-readable Table 2 recomputation + per-locus AMR/virulence/mobilome verification (positions + RGP interval checks). |
| `report/evidence/pangenome_result.json` | DIAMOND+MCL clustering output side-by-side with the paper's Roary numbers (pan / core / PA34 accessory / PA34 unique / no-ortho vs each reference). |

### LLM-judge outputs
| File | Contents |
|---|---|
| `report/evidence/llm_judge_verdict.json` | Structured JSON: `{verdict: "PARTIAL", confidence: "high", reasoning: "...", one_line: "..."}` from `argo:gpt-5.2` (T=0.1). |
| `report/evidence/llm_judge_verdict.txt` | Human-readable copy of the above. |

### Code
| File | Purpose |
|---|---|
| `work/pangenome_pa34.py` | Roary-style pan-genome analysis: DIAMOND all-vs-all → 50%/50% filter → weighted graph → MCL (inflation=1.5) → genome-membership tagging. |
| `work/paper.pdf` + `work/paper.txt` | Paper source + full-text search corpus. |

### Reports
| File | Purpose |
|---|---|
| `report/REPORT.md` | Main replication report (this artifact set is derived from it). |
| `report/REPORT.tex` | LaTeX version with dedicated Genuine Critique section. |
| `report/brief.md` | 1-paragraph what/why/verdict. |
| `report/attempt_log.md` | Chronological run log. |
| `report/artifact_harvest.md` | Every public artifact fetched with URL / size / checksum (detailed sibling of this file). |
| `report/workflow.md` | Stage-by-stage methodology. |
| `report/artifacts_summary.md` | This file. |
| `report/failure_analysis.md` | What did not fully replicate and why. |
| `report/open_questions.json` | 5 truly open scientific questions grounded in the paper. |

---

## Reproducibility inventory (what a re-runner needs)

**Hardware / OS:** anything with Python 3.11+ and ~50 GB scratch; the pan-genome step used 32 threads and finished in <30 min on an A100 node but is CPU-bound (DIAMOND) — a laptop works with `-p 4` and ~2 h.

**Software (verified versions):**
- Biopython 1.87
- DIAMOND 2.1.9
- `markov_clustering` (PyPI)
- `pdftotext` (poppler)
- `curl`
- Argo LLM proxy on 127.0.0.1:44497 (only for Stage 6 LLM judge; not required for the numeric replication).

**External data (all open):**
- 6 NCBI GenBank/FASTA records (accessions above).
- 1 BV-BRC REST API call.
- 1 PLoS PDF fetch.

**Not needed:** paid databases, private strain collections, wet-lab equipment. (Fig 5 / Fig 6 phenotypes were explicitly out of scope.)

---

## What is *not* in this artifact set
- Live PA34 isolate / cell culture / MIC data (out of scope — public-data replication only).
- Roary v3 output at canonical 95% ID thresholds (would remove the pan-genome-count caveat; time budget did not permit installing Roary here).
- CRISPRCasFinder positive-negative run for C17 (currently inferred from "no Cas gene in PGAP annotation").
- MAUVE-rerun-derived RGP inventory (we verified stated RGPs at their stated coordinates, not the full RGP call).
- MLST ST1284 confirmation (would need `mlst` tool + PubMLST scheme, out of scope here).

These absences are called out in `failure_analysis.md` and in the Genuine Critique section of `REPORT.tex`.

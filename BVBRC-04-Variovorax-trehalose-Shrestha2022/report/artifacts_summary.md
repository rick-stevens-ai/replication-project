# Artifacts Summary — BVBRC-04 Shrestha 2022 Re-pass

**Paper:** Shrestha et al. 2022, *BMC Genomic Data* 23:4, DOI 10.1186/s12863-021-01020-y.
**Genome:** NZ_CP014517.1 / *Variovorax* sp. PAMC28711.
**Verdict:** PARTIAL (COVERAGE 9/10, AGREEMENT 9/10).
**Re-pass date:** 2026-06-23. Reports generated 2026-07-05.

This document indexes every artifact produced by the re-pass and records its role,
scope, and provenance pointer.

---

## 1. Paper & parser artifacts

| File | Role | Notes |
|---|---|---|
| `paper/shrestha2022.pdf` | Self-sourced PDF (CC BY 4.0) | SHA-256 `f0f7a5addf671072cdab447b7c4b3b42c9bb07472e95305f9aba957a18ffc424`; 1.84 MB |
| `paper/shrestha2022.txt` | `pdftotext -layout` extract | 361 lines; used only for audit / claim enumeration, not numeric extraction |
| `PARSER_PROVENANCE.md` | Source-of-truth for parser pipeline | Records the PDF hash and the blockers (MetaCyc + 2018 snapshots) |

## 2. Genome input

| File | Role | Notes |
|---|---|---|
| `data/CP014517.1.gb` | PGAP GenBank flatfile for *Variovorax* sp. PAMC28711 | Single circular chromosome, 4,316,152 bp; zero `/EC_number` qualifiers (PGAP keys on product names) |

## 3. Code (`code/repass/`)

| File | Purpose | Key output |
|---|---|---|
| `01_genome_features.py` | Direct GenBank feature counter (length, GC%, CDS, pseudo, rRNA, tRNA, host, date) | `results/repass/genome_features.json` |
| `02_trex_and_full_cluster.py` | BioPython + product-name regex over the trehalose target set (now including TreX EC 3.2.1.68); dumps the glycogen cluster region | `results/repass/trex_and_cluster.json` |
| `03_kegg_crosscheck.py` | KEGG REST per-EC → KO → vaa link queries; also counts vaa entries, pathway maps, modules | `results/repass/kegg_crosscheck.json` |
| `04_bvbrc_metadata.py` | BV-BRC genome-metadata fetch (country, host, assembly, biosample, CDS, status) | `results/repass/bvbrc_metadata.json` |

Design: plain Python 3, only BioPython + stdlib `urllib`, no LLM in the numeric path,
laptop-seconds runtime.

## 4. JSON results (`results/repass/`)

| File | Contents |
|---|---|
| `genome_features.json` | 4,316,152 bp / 65.973% GC / 4,104 CDS / 129 pseudogenes / 6 rRNA / 46 tRNA / host *Himantormia* / 2015 |
| `trex_and_cluster.json` | Per-enzyme hits (OtsA, OtsB, TreY [PSEUDO], TreZ, TreS, TreF/H, TreX ×2, glycogen cluster) with coordinates, strand, product, `/pseudo` flag |
| `kegg_crosscheck.json` | Per-KO vaa link queries + inventory: 4,159 entries / 3,975 proteins / 2,351 KO-assigned / 133 maps / 56 modules |
| `bvbrc_metadata.json` | Antarctica / *Himantormia* / GCA_001577265.1 / SAMN04457487 / 4,263 PATRIC CDS / genome status = complete |
| `claims_enumerated.json` | 37 claims machine-readable: `{id, section, claim_text, testable, status}` |
| `parser_provenance.json` | All input hashes, all URL invocations, all timestamps |

## 5. Reports (`report/`)

| File | Format | Role |
|---|---|---|
| `REPORT.md` | Markdown | Canonical re-pass report (2026-06-23). Primary source of truth. |
| `REPORT.pass1.md` | Markdown | Preserved verbatim pass-1 report (2026-05-05) |
| `REPORT.tex` | LaTeX | Formal typeset render of the re-pass report + GENUINE CRITIQUE section (2026-07-05) |
| `open_questions.json` | JSON | 5 truly-open scientific questions with basis and next-steps (2026-07-05) |
| `workflow.md` | Markdown | Executable-order description of the re-pass pipeline (2026-07-05) |
| `artifacts_summary.md` | Markdown | THIS document — indexes all artifacts (2026-07-05) |
| `failure_analysis.md` | Markdown | Explicit inventory of what did not / could not replicate (2026-07-05) |

## 6. What each artifact answers

- **"What did the paper actually claim?"** → `results/repass/claims_enumerated.json` (37 rows).
- **"Is the genome as described?"** → `results/repass/genome_features.json` + `bvbrc_metadata.json`.
- **"Do the trehalose enzymes actually exist at the claimed loci?"** → `results/repass/trex_and_cluster.json`.
- **"Do KEGG's vaa records support the paper's KEGG column?"** → `results/repass/kegg_crosscheck.json`.
- **"What could not be verified and why?"** → `report/failure_analysis.md`, plus `NOT_TESTED` rows in `claims_enumerated.json`.
- **"What are the honest open scientific questions?"** → `report/open_questions.json`.
- **"How would I re-run this end-to-end?"** → `report/workflow.md`.

## 7. Standing rules honoured

- **Free compute only.** All KEGG / BV-BRC access is free public REST; no LLM in numeric path.
- **Reproducibility.** Every quantitative claim carries a JSON provenance pointer.
- **Honesty about blockers.** MetaCyc column (5 cells) and 2018 historical snapshots (6 numbers)
  are recorded as `NOT_TESTED`, not fudged.
- **Single writer per artifact.** Pass-1 report preserved verbatim rather than overwritten.
- **No fabricated numbers.** Every number in `REPORT.md`, `REPORT.tex`, and this file traces
  back to a JSON file under `results/repass/` or to `data/CP014517.1.gb`.

# Artifacts Summary — BVBRC-72 *B. amyloliquefaciens* WS-8

All under `~/Dropbox/REPLICATE-PROJECT/BVBRC-72-bamyloliquefaciens-ws8/`.

## report/

| File | Purpose |
|---|---|
| `REPORT.md` | Canonical human-readable narrative — 21-claim table, method, results vs paper, verdict. Master output of the replication. |
| `REPORT.tex` | LaTeX rendition of REPORT.md + a dedicated GENUINE CRITIQUE section covering what did/didn't replicate, systematic gaps, LLM-judge dependence, and what the exercise says about the paper's real strengths. |
| `open_questions.json` | 5 truly-open scientific questions grounded in WS-8 genome/comparative genomics, each with `q`, `basis`, `next_steps`. Covers: (1) species reassignment vs *B. velezensis*; (2) BGC inventory + antifungal-spectrum comparison to FZB42; (3) PGPR rhizosphere-colonization + VOC signatures; (4) anti-phage defense-system profile + deployment risk; (5) genome/plasmid/BGC stability under industrial fermentation. |
| `workflow.md` | End-to-end recipe (8 stages: paper retrieval → accession → download → stats → BGC scan → antiSMASH v7 web → antiSMASH v8 local → LLM judge). Includes commands, endpoints, compute topology, reproducibility notes. |
| `artifacts_summary.md` | This file. |
| `failure_analysis.md` | What could not be replicated + why, categorized by failure class (data-not-deposited, tool-version drift, scope-of-effort). |
| `artifact_harvest.md` | (pre-existing) Accession bookkeeping. |
| `attempt_log.md` | (pre-existing) Chronological execution log. |
| `evidence/` | `genome_stats.json`, `llm_judge_result.json`, antiSMASH v7 + v8 output archives. |

## paper/

| File | Purpose |
|---|---|
| `PMC9728402_fulltext.xml` | Europe PMC full-text XML (107 KB). |
| `pubmed_31601062.txt` | NCBI PubMed abstract efetch. |
| `s2_metadata.json` | Semantic Scholar v1 metadata (open-access flag, canonical PDF URL). |

## genomes/

| File | Purpose |
|---|---|
| `CP018200.gb` | GenBank flat file for WS-8 chromosome (9.09 MB, downloaded via NCBI E-utils efetch, `rettype=gbwithparts`). Includes full PGAP feature table. |
| `CP018200.fasta` | Assembly FASTA (3.99 MB). Used for direct GC-composition compute and antiSMASH input verification. |

## work/

| File | Purpose |
|---|---|
| `genome_stats.py` | Biopython 1.83 parser → JSON stats (bp length, direct-computed GC, feature-type tallies). |
| `bgc_gene_scan.py` | CDS `product/gene/note` scan for canonical BGC marker genes (dfnJ, mlnH/I, bacA, srfA*, dhbA-F, LanC/M, etc.). |
| `nrps_pks_scan.py` | CDS scan for NRPS/PKS domain descriptors (A, C, PCP, KS, AT, KR, DH, ER, TE). Proximity-clusters into BGC-like regions. |
| `judge.py` | LLM-judge harness — POSTs 21-claim table + paper-fact summary to Argo `argo:gpt-5.2`, parses per-claim + aggregate JSON. |

## Key numerical anchors (all traceable to `REPORT.md`)

- **Genome:** 3,929,787 bp, 1 circular chromosome, 0 plasmids, 46.499 % GC (direct compute).
- **PGAP feature counts:** 3895 genes / 3777 CDS / 107 pseudo / 86 tRNA / 27 rRNA (9× 5S+16S+23S) / 4 ncRNA + 1 tmRNA / 25 regulatory.
- **antiSMASH:** 13 regions (v8.0.4 local) / 12 regions (v7.1.0 web) vs paper's 19 (v3.0) — tool-version delta.
- **Named BGCs reconfirmed:** 7/7 (difficidin, fengycin, bacillaene, macrolactin, surfactin, bacilysin, bacillibactin) + 1 class-II lanthipeptide confirmed present + novel (no MIBiG hit).
- **BGC per-gene identity:** 6 of 7 at 95–100 %; bacillibactin at 57–81 % (*B. subtilis* dhbA-F variant).
- **LLM-judge:** verdict PARTIAL, coverage 90 %, agreement 83.6 % (`argo:gpt-5.2`, temp 0.1).

## Endpoints used (all FREE)

NCBI E-utils · Europe PMC · Semantic Scholar Graph v1 · antiSMASH web api/v1.0 · antiSMASH v8.0.4 local (uicgpu) · Argo proxy (localhost:44497, `argo:gpt-5.2`).

No paid LLM APIs; no OpenAI / Anthropic / OpenRouter direct calls.

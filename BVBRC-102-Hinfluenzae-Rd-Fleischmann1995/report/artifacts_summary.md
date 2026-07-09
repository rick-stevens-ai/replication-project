# Artifacts Summary — Fleischmann1995 (H. influenzae Rd KW20) replication

Inventory of every artifact produced or pulled by this replication + backfill, with sizes,
checksums, and provenance traces.

## Directory tree
```
BVBRC-102-Hinfluenzae-Rd-Fleischmann1995/
├── paper.pdf.MISSING.md              # provenance note — no OA copy exists
├── extraction/
│   ├── marker.md                     # pending stub
│   └── nougat.mmd                    # pending stub
├── report/
│   ├── REPORT.md                     # original markdown report (2026-07-04)
│   ├── REPORT.tex                    # detailed LaTeX report (backfill 2026-07-05)
│   ├── brief.md                      # one-paragraph what/why
│   ├── attempt_log.md                # timestamped attempt log
│   ├── artifact_harvest.md           # original harvest table
│   ├── workflow.md                   # comprehensive workflow narrative (backfill)
│   ├── artifacts_summary.md          # THIS FILE (backfill)
│   ├── open_questions.json           # 5 open questions (backfill)
│   ├── failure_analysis.md           # honest failure analysis (backfill)
│   └── evidence/
│       ├── computed.json             # deterministic numeric results
│       ├── feature_counts.csv        # feature-type histogram
│       ├── genbank_head.txt          # head of the GenBank record (provenance)
│       ├── genbank_tail.txt          # tail of the GenBank record (provenance)
│       ├── llm_judge.json            # parsed LLM-judge verdict
│       └── llm_judge_raw_response.json  # raw Argo response
└── work/
    ├── Hinf_Rd_NC_000907.1.gb        # source GenBank flatfile (4.4 MiB)
    ├── analyze.py                    # numeric analysis
    ├── judge.py                      # LLM-judge harness
    └── computed.json                 # (same as evidence/computed.json)
```

## Primary data artifact (input)

| Artifact | Source URL | Size | Checksum | Notes |
|---|---|---:|---|---|
| `work/Hinf_Rd_NC_000907.1.gb` | `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=NC_000907.1&rettype=gbwithparts&retmode=text` | 4,604,072 B (4.4 MiB) | MD5 `f13c8a0011a13f610fa9556dd11b5057` | GenBank flatfile w/ features. Annotation date 2020-04-04. RefSeq derived from L42023 (1995 Fleischmann submission). BioProject PRJNA224116, Assembly GCF_000027305.1. |

## Derived numeric artifacts (outputs)

| Artifact | Size | Content |
|---|---:|---|
| `report/evidence/computed.json` | ~1.5 KiB | All numeric results: length_bp=1830138, gc_pct=38.1503, cds_total=1721 (1604 non-pseudo + 117 pseudo), tRNA=57, rRNA=19 (6×16S, 6×23S, 7×5S), coding_density_pct=82.5326, mean_cds_length_nt=942.95, mean_cds_length_aa=313.32, strand split 851/870. |
| `report/evidence/feature_counts.csv` | 123 B | Feature-type histogram: gene=1801, CDS=1721, tRNA=57, rRNA=19, regulatory=7, misc_feature=3, ncRNA=3, source=1, tmRNA=1, repeat_region=1. |
| `report/evidence/genbank_head.txt` | (small) | Head of the GenBank record for provenance snapshot. |
| `report/evidence/genbank_tail.txt` | (small) | Tail of the GenBank record for provenance snapshot. |

## LLM-judge artifacts

| Artifact | Content |
|---|---|
| `report/evidence/llm_judge.json` | Parsed verdict JSON: verdict=REPLICATED, coverage_pct=100, agreement_pct=100, per-claim breakdown (length drift 1 bp, gc drift 0.15 pp, CDS drift −1.3%, tRNA drift +5.6%, rRNA operons exact match, topology exact match). |
| `report/evidence/llm_judge_raw_response.json` | Raw Argo `argo:gpt-5` chat-completion response, verbatim. |

## Code artifacts

| Artifact | Size | Purpose |
|---|---:|---|
| `work/analyze.py` | 4,486 B / ~110 LOC | Deterministic Biopython analysis of the GenBank record. |
| `work/judge.py` | 4,293 B / ~110 LOC | HTTPS POST to Argo `argo:gpt-5`, JSON verdict parse. |

## Report artifacts

| Artifact | Purpose |
|---|---|
| `report/REPORT.md` | Original narrative report with §1 Paper summary, §2 Claims table (C1–C15), §3 Method, §4 Results-vs-paper table, §5 Verdict. |
| `report/REPORT.tex` | Detailed LaTeX report (this backfill): same structure plus explicit Critique section, per-claim what-worked / what-didn't, Verdict + justification, Open Questions Q1–Q5. |
| `report/brief.md` | One-paragraph what/why. |
| `report/attempt_log.md` | Timestamped attempt log with things-that-worked / things-explicitly-not-done. |
| `report/artifact_harvest.md` | Original artifact table (subset of this file). |
| `report/workflow.md` | Comprehensive workflow narrative + tools/versions + effort estimate. |
| `report/open_questions.json` | Five open questions with basis + next steps. |
| `report/failure_analysis.md` | Honest failure analysis and critique of evidence strength. |

## External references / accessions (consulted, not stored locally)

| Reference | ID / URL | Role |
|---|---|---|
| Fleischmann et al. 1995 | doi:10.1126/science.7542800, PMID 7542800 | Source paper. No OA copy per Unpaywall 2026-07-05. |
| GenBank L42023 | (retired accession) | Original 1995 TIGR submission. |
| RefSeq NC_000907.1 | https://www.ncbi.nlm.nih.gov/nuccore/NC_000907.1 | Current reference record for this genome; source of all numeric measurements. |
| BioProject | PRJNA224116 | RefSeq re-annotation project. |
| Assembly | GCF_000027305.1 | Reference assembly of H. influenzae Rd KW20. |
| BV-BRC genome | 71421.1 | BV-BRC's H. influenzae Rd KW20 reference genome entry (not fetched, cross-referenced). |
| Argo LLM proxy | http://127.0.0.1:44497 | Free localhost proxy (model `argo:gpt-5`) for LLM-judge only. |

## Backfill provenance

| Backfill file | Origin |
|---|---|
| `paper.pdf.MISSING.md` | Unpaywall API lookup 2026-07-05: `is_oa: false, oa_status: closed, best_oa_location: null`. Cannot obtain from free endpoints per policy. |
| `extraction/marker.md` | Stub — depends on paper.pdf. |
| `extraction/nougat.mmd` | Stub — depends on paper.pdf + GPU. |
| `report/REPORT.tex` | Composed from existing REPORT.md + computed.json + llm_judge.json + explicit critique. |
| `report/open_questions.json` | Grounded re-reading of the paper's claims via REPORT.md + evidence deltas. Five heavy-duty open questions with concrete next steps. |
| `report/workflow.md` | Composed from attempt_log.md + analyze.py inspection. |
| `report/artifacts_summary.md` | This file — direct filesystem inventory. |
| `report/failure_analysis.md` | Honest failure & critique — includes items the original replication glossed over. |

# Artifacts Summary — BVBRC-98 · Stover 2000 PAO1 Replication

**Target dir:** `~/Dropbox/REPLICATE-PROJECT/BVBRC-98-Paeruginosa-PAO1-Stover2000/`
**Date:** 2026-07-04 · **Host:** CherryRd · **Verdict:** PARTIAL

---

## Inputs (downloaded, real bytes)

| Path (under `work/genome/ncbi_dataset/data/GCF_000006765.1/`) | Size | Role |
|---|---|---|
| `GCF_000006765.1_ASM676v1_genomic.fna` | ~6.3 MB | Genome FASTA (single contig, `NC_002516.2`) |
| `genomic.gff` | ~3.2 MB | RefSeq PGAP annotation (features: gene/CDS/rRNA/tRNA/ncRNA/tmRNA) |
| `protein.faa` | ~2.3 MB | Predicted protein FASTA (5,572 headers) |

Fetched via `datasets download genome accession GCF_000006765.1 --include genome,gff3,protein`. Per-file MD5s are captured in `report/artifact_harvest.md` (see that file for the exact hex digests).

## Scripts

| Path | Language | Purpose |
|---|---|---|
| `work/analyze.py` | Python 3.13, stdlib only | Parse FASTA + GFF3 + protein FASTA; emit `report/evidence/genome_stats.json` with per-contig lengths, base counts, feature counts, MD5s, and per-claim comparison table |
| `work/llm_judge.py` | Python 3.13, stdlib only | Call Argo local proxy (`127.0.0.1:44497`, `argo:gpt-4o`, `T=0`) with the paper claims + observed numbers; emit `report/evidence/llm_judge.json` with per-claim `reproduced / agreement / notes` and an overall verdict from the canonical vocabulary |

Combined footprint ~150 lines of Python, no third-party dependencies.

## Report artefacts (this directory)

| File | Purpose |
|---|---|
| `REPORT.md` | Primary human-readable replication report (paper summary, claims table, method, results, verdict, evidence pointers, constraints). |
| `REPORT.tex` | LaTeX version of the report with a dedicated **Genuine critique** section (what did/didn't replicate, honest limitations). |
| `workflow.md` | Step-by-step reproduction recipe and data-flow diagram. |
| `artifacts_summary.md` | This file — inventory of inputs, scripts, evidence, and outputs. |
| `failure_analysis.md` | What did not fully replicate, why the verdict is PARTIAL rather than REPLICATED, known limitations. |
| `open_questions.json` | Five truly open scientific/technical questions raised by (but not answered by) this replication. |
| `evidence/genome_stats.json` | Full numeric output of `analyze.py`. |
| `evidence/llm_judge.json` | Cached LLM-judge prompt + JSON response. |
| `artifact_harvest.md` | MD5s + provenance of the downloaded NCBI files. |

## Key numeric outputs (headline)

| Claim | Paper | Replication | Δ | Reproduced? |
|---|---|---|---|---|
| C1 genome size (bp) | 6,264,403 | **6,264,404** | +1 bp (+1.6 × 10⁻⁵ %) | ✅ effectively exact |
| C2 G+C content | 66.6 % | **66.556 %** | −0.044 pp | ✅ within rounding |
| C3 predicted ORFs | 5,570 | **5,573** CDS (unique protein IDs = 5,572; `protein.faa` = 5,572) | +3 (+0.054 %) | ✅ within annotation drift |
| tRNA count | ~63 | **63** | — | ✅ consistent |
| rRNA operons | 4 | 13 rRNA features / 3 = **4** | — | ✅ consistent |
| Topology | single circular | 1 contig, 0 ambiguous bases | — | ✅ consistent |
| Coding density | ~89 % | **89.3 %** | — | ✅ consistent |
| C4 largest bacterial genome at publication | true | not re-derivable from FASTA | — | context-only |
| C5 exceptional regulatory / two-component gene richness | true | not re-derivable from single FASTA | — | context-only |

## External endpoints touched

- `https://api.ncbi.nlm.nih.gov/datasets/…` (via `datasets` CLI, no auth) — one-shot pull of `GCF_000006765.1`.
- `http://127.0.0.1:44497/v1/chat/completions` (Argo local proxy, model `argo:gpt-4o`, free) — one LLM-judge call with `temperature=0.0`, response cached to `evidence/llm_judge.json`.

No Anthropic / OpenAI / OpenRouter / paid endpoints touched.

## Storage footprint (approximate)

- Downloaded assembly bytes: ~12 MB uncompressed.
- Scripts + evidence + report: <100 kB combined.
- Total target-dir footprint: ~12 MB.

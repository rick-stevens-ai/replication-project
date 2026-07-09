# Artifacts summary — Kunst 1997 B. subtilis 168 replication

Inventory of every artifact produced or pulled by this replication (original 2026-07-04 run + backfill 2026-07-05).

## Master inventory

| # | Artifact | Path | Bytes | SHA-256 | Origin |
|---|---|---|---:|---|---|
| 1 | Paper PDF | `paper.pdf` | 2,435,413 | `5ce7199b85c06828c656ed12bfa50dcbb4eeb015d620b8db9ef349e18aa2cb6f` | https://www.nature.com/articles/36786.pdf (backfill 2026-07-05) |
| 2 | Marker text extraction (fallback) | `extraction/marker.md` | 911,032 | `ccef5af192ca85b54065252cd1baf6a07ed75d7f1f69414409001e5bbe5916ff` | `pdftotext -layout paper.pdf` (backfill) |
| 3 | Nougat text extraction | `extraction/nougat.mmd` | 854 | `ccf7d4cc7d9d73b8c7fc1ab348a74f6bea784c6d8d68886b79ccaa26ca6b623b` | Placeholder — pending central Eagle Nougat sweep |
| 4 | B. subtilis 168 FASTA | `work/data/Bsub168_NC_000964.3.fasta` | 4,275,902 | `a334e891ffc0e307f23f48842775d3383177a9d9cb5d5075b552a2cccddfe139` | NCBI E-utilities, RefSeq NC_000964.3 |
| 5 | B. subtilis 168 GenBank-with-parts | `work/data/Bsub168_NC_000964.3.gb` | 13,415,984 | `ab0ea7ab52d59e3212fca7677b9e0c0df8c0ae2aa0efe659a9d0c7cd9bfd5d94` | NCBI E-utilities, RefSeq NC_000964.3 |
| 6 | Reproduction script | `work/analyze.py` | 6,918 | `522dcbfea5c476e9ec3ccc1117967132a7d5489c55c3d78e50cafbeb6bca4353` | Written 2026-07-04 |
| 7 | Judge #1 script | `work/judge.py` | 3,523 | `08ebe99a874bf203113e872931b514278727c1f083acfb1833cbfbf6880e68e5` | Written 2026-07-04 |
| 8 | Judge #2 script | `work/judge2.py` | 4,047 | `b48f2205ceb38bfa3dd682b5c5950062040c5776932a3e0280202be033d3cc15` | Written 2026-07-04 |
| 9 | Analyze stdout | `report/evidence/analyze_stdout.txt` | 1,428 | `c503cb9cd9aff6ca67181aa6b1c2a577373b36b431ff031c92e5d7174f9fbbdf` | `python work/analyze.py` |
| 10 | Measured metrics (machine-readable) | `report/evidence/metrics.json` | 1,570 | `6c6347e7d5f4ffedc20ca78ce842f0b4a731f6848606316bca4cc4f0df1f4b2b` | Same run |
| 11 | Judge #1 output | `report/evidence/judge.json` | 3,224 | `7cd6af0d63bb8f1a699fa236117b4c03976ad49682bb1310c38f27ba229a71a6` | Argo `argo:gpt-5` |
| 12 | Judge #2 output | `report/evidence/judge2.json` | 3,881 | `ccee62e5ecd76d4cf777c8e98598160cc644b2e64a0050f64331560f669935b5` | Argo `argo:gpt-5.2` |
| 13 | Original REPORT | `report/REPORT.md` | ~12 KB | (existing) | Written 2026-07-04 |
| 14 | Original brief | `report/brief.md` | ~1.5 KB | (existing) | Written 2026-07-04 |
| 15 | Original attempt log | `report/attempt_log.md` | ~4.8 KB | (existing) | Written 2026-07-04 |
| 16 | Original artifact harvest | `report/artifact_harvest.md` | ~2 KB | (existing) | Written 2026-07-04 |
| 17 | LaTeX detailed report | `report/REPORT.tex` | see file | — | Backfill 2026-07-05 |
| 18 | Open questions (5) | `report/open_questions.json` | see file | — | Backfill 2026-07-05 |
| 19 | Workflow | `report/workflow.md` | see file | — | Backfill 2026-07-05 |
| 20 | Failure analysis | `report/failure_analysis.md` | see file | — | Backfill 2026-07-05 |
| 21 | This inventory | `report/artifacts_summary.md` | this file | — | Backfill 2026-07-05 |

## Accessions & external references

| Accession / DOI | What | URL |
|---|---|---|
| doi:10.1038/36786 | Paper (Kunst et al. 1997) | https://doi.org/10.1038/36786 |
| PMID 9384377 | Paper (PubMed) | https://pubmed.ncbi.nlm.nih.gov/9384377/ |
| NC_000964.3 | RefSeq unified B. subtilis 168 chromosome (2009, curated 2018) | https://www.ncbi.nlm.nih.gov/nuccore/NC_000964.3 |
| AL009126.1 → 3 | Original 1997 EMBL deposit → current update | https://www.ebi.ac.uk/ena/browser/view/AL009126 |
| Barbe et al. 2009 | 2009 unified re-annotation paper | doi:10.1099/mic.0.027839-0 |
| Borriss et al. 2018 | 2018 curation update paper | doi:10.1111/1751-7915.13043 |

## Traces / logs

- `report/evidence/analyze_stdout.txt` — full stdout of `work/analyze.py`.
- `report/evidence/metrics.json` — full machine-readable measured metrics + paper claims side-by-side.
- `report/evidence/judge.json` — full prompt + raw response + parsed verdict for judge #1 (`argo:gpt-5`, PARTIAL/100/87).
- `report/evidence/judge2.json` — full prompt + raw response + parsed verdict for judge #2 (`argo:gpt-5.2`, REPLICATED/100/93).
- `report/attempt_log.md` — timestamped narrative of the original 2026-07-04 run (what worked / what failed / what was NOT tested).

## What is NOT present

- **Nougat parse (`extraction/nougat.mmd`)** — placeholder only. Requires GPU; will be pulled from the central Eagle Nougat manifest on next sweep (resolve by paper.pdf sha256 `5ce7199b…`).
- **Compiled `report/REPORT.pdf`** — LaTeX source is present but not compiled here (no `pdflatex` invocation required for the backfill). Compile with `pdflatex report/REPORT.tex` if a rendered version is needed.
- **No re-run of genomic analysis** — backfill pass was report-only per the brief. Original evidence/ was preserved verbatim.
- **No fresh LLM judging on the current evidence** — the original judge.json / judge2.json outputs were preserved; a fresh triangulation was not run because it would just re-consume Argo tokens on unchanged inputs.

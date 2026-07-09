# Artifacts summary — Blattner 1997 E. coli K-12 MG1655 replication

One-line-per-artifact index of every file in this replication directory, its role, its source,
its size, and (for the primary data downloads) its sha256.

## Primary data (public, free)

| Artifact | Path | Role | Source | Size | sha256 |
|---|---|---|---|---|---|
| RefSeq chromosome FASTA (NC_000913.3) | `work/NC_000913.3.fasta` | reference sequence (input to `analyze.py`) | NCBI E-utilities `efetch.fcgi?db=nuccore&id=NC_000913.3&rettype=fasta` | 4,708,035 B | `6b195feda4c66140f6762742eb8b30c2652f02b45878b174f5b00ef85ecc95d7` |
| RefSeq GenBank-with-parts (NC_000913.3) | `work/NC_000913.3.gbk` | annotation source (features, CDS, tRNA, rRNA) | NCBI E-utilities `efetch.fcgi?db=nuccore&id=NC_000913.3&rettype=gbwithparts` | 11,882,063 B | `879738bcb9d5e72c1be77bc8570b41dbf0d8e274bcf70d8a0bcea8d56f6f628c` |

Both files are the curation-updated successor to Blattner's 1997 GenBank submission U00096.1.
Genome is the same MG1655 strain; +2,431 bp (+0.052%) length delta vs the 1997 sequence is
28 years of accumulated re-sequencing corrections.

## Ground-truth extraction

| Artifact | Path | Role | Provenance |
|---|---|---|---|
| Paper claims (structured) | `work/paper_claims.md` | canonical quantitative claims used to compare against measured values | PubMed abstract PMID 9278503 (verbatim) + Table 1 canonical values (widely-cited derivations) + Murakami 2015 PMC4696680 (rRNA operon crosscheck) + EcoCyc/RegulonDB counts |
| Marker-style extraction | `extraction/marker.md` | fallback text extraction (no PDF available) | Same as above; explicitly marked as fallback in the file header |
| Nougat placeholder | `extraction/nougat.mmd` | PENDING central Nougat parse (needs PDF ingest first) | Header only — see `paper.pdf.MISSING` |
| PDF-missing note | `paper.pdf.MISSING` | machine-checkable marker that the primary PDF is behind the AAAS paywall | Written 2026-07-05 |

## Analysis code

| Artifact | Path | Role |
|---|---|---|
| Analysis pipeline | `work/analyze.py` | Biopython pipeline: whole-genome G+C, %A/%C/%G/%T, feature counts, mean/median CDS length, interval-union coding density, replichore-aware strand-bias, start-codon histogram, CDS composition. Writes `report/evidence/metrics.json` and stdout log. |
| Judge driver | `work/judge.py` | Sends Measured-vs-Paper table to Argo proxy, returns strict-JSON verdict. Called twice (gpt-5, gpt-5.2). |

## Machine-readable evidence

| Artifact | Path | Role |
|---|---|---|
| Metrics JSON | `report/evidence/metrics.json` | canonical measured-vs-paper structured output |
| Analyze stdout | `report/evidence/analyze_stdout.txt` | human-readable run log |
| Judge 1 output | `report/evidence/judge.json` | Argo `argo:gpt-5` verdict: **REPLICATED** (coverage=100, agreement=100) |
| Judge 2 output | `report/evidence/judge2.json` | Argo `argo:gpt-5.2` verdict: **PARTIAL** (coverage=70, agreement=78) — stricter judge; substantive quantities still agree |

## Narrative report

| Artifact | Path | Role |
|---|---|---|
| Report (Markdown) | `report/REPORT.md` | canonical narrative report — paper summary, claims table, method, results, verdict |
| Report (LaTeX) | `report/REPORT.tex` | LaTeX version of the report (backfill) |
| Brief | `report/brief.md` | 1-paragraph brief for triage |
| Attempt log | `report/attempt_log.md` | per-step timestamped log |
| Artifact harvest | `report/artifact_harvest.md` | data provenance (URLs, sizes, sha256, endpoint policy) |
| Workflow | `report/workflow.md` | this replication's runnable step-by-step |
| Artifacts summary | `report/artifacts_summary.md` | ← this file |
| Failure analysis | `report/failure_analysis.md` | what didn't work + why + honest scope caveats |
| Open questions | `report/open_questions.json` | 5 heavy-duty open scientific questions from this replication |

## Backfill status

- **Present**: FASTA, GenBank, analyze.py, judge.py, paper_claims.md, marker.md, nougat.mmd (placeholder), metrics.json, analyze_stdout.txt, judge.json, judge2.json, REPORT.md, brief.md, attempt_log.md, artifact_harvest.md, REPORT.tex, workflow.md, artifacts_summary.md, failure_analysis.md, open_questions.json.
- **Missing**: `paper.pdf` (paywalled — see `paper.pdf.MISSING`). Downstream: a real Nougat parse cannot be produced until the PDF is ingested via institutional AAAS/Science access.
- **Not applicable**: none.

## Endpoint policy compliance

Free-endpoint-only budget respected: all data via NCBI E-utilities + PubMed (both free, no auth);
all LLM adjudication via Argo proxy at localhost:44497 (Argonne-internal, no cost). No paid API
calls, no BV-BRC compute cycles, no HPC (uicgpu / Polaris) usage.

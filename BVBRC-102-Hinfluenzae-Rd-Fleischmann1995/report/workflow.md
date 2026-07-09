# Workflow — Fleischmann1995 (H. influenzae Rd KW20) replication

## Narrative

This replication targets the quantitative, sequence-derivable claims in
Fleischmann et al. 1995 (*Science* 269:496–512) — the first complete genome sequence of a
free-living organism. The workflow deliberately did NOT attempt a de-novo re-assembly of the
original ~19,687 Sanger reads (unavailable in a publicly reusable form), and instead performs
an *evidence-based* replication: pull the modern RefSeq record derived from the paper's
GenBank submission L42023 (now NC_000907.1), compute the paper's headline numbers directly from
that flatfile with Biopython, and diff.

The workflow has three stages: (1) **fetch**, (2) **compute**, (3) **judge**.

### 1. Fetch (network, ~1 request, ~5 s wall-clock)

Single NCBI E-utilities call with `rettype=gbwithparts` to pull the full GenBank flatfile for
`NC_000907.1` (features + sequence). The record is 4,604,072 bytes, MD5
`f13c8a0011a13f610fa9556dd11b5057`, annotated 2020-04-04, and is written to
`work/Hinf_Rd_NC_000907.1.gb`. No auth, no API key, free tier only.

### 2. Compute (local CPU, single Python invocation, ~2 s wall-clock)

`work/analyze.py` (Biopython 1.87, ~110 lines) parses the GenBank record with
`SeqIO.read(GB, "genbank")` and computes:
- Chromosome length from `len(rec.seq)`.
- Per-base counts (A, T, G, C, N, other-IUPAC) from `Counter(str(seq).upper())`.
- G+C% and A+T% from those counts.
- Feature-type histogram from `Counter(f.type for f in rec.features)`.
- CDS breakdown: total, non-pseudo, pseudo (via `"pseudo" in f.qualifiers or "pseudogene" in f.qualifiers`).
- Mean CDS length (nt and aa) over non-pseudo CDSs, computed as sum of per-part
  `location.end − location.start` divided by count.
- Coding density: **interval-union** of all non-pseudo CDS parts (merged after sort-by-start)
  divided by chromosome length. This is more honest than sum-of-lengths because it correctly
  handles overlapping ORFs.
- tRNA/rRNA feature counts.
- rRNA product breakdown (16S / 23S / 5S loci) from `qualifiers["product"]`.
- CDS strand distribution.

All outputs are numeric and go to `work/computed.json` (also copied to
`report/evidence/computed.json`) plus `report/evidence/feature_counts.csv`. No LLM in the
number-computation path.

### 3. Judge (LLM, Argo proxy, one prompt, ~5 s wall-clock)

`work/judge.py` posts the paper's target numbers + this replication's computed numbers + the
claims table to the Argo proxy at `127.0.0.1:44497/v1/chat/completions` using model
`argo:gpt-5`, asking for a strict JSON verdict with per-claim match/drift/mismatch classification
plus coverage% and agreement%. The response is saved verbatim to
`report/evidence/llm_judge_raw_response.json` and the parsed JSON to
`report/evidence/llm_judge.json`. The LLM is **not** in the numeric-truth path — it is only a
structured scorer.

## Tools and codes (enumerated)

| Tool / library | Version | Role |
|---|---|---|
| Python | 3.14 | Runtime |
| Biopython | 1.87 | GenBank parsing + feature/location handling |
| curl | 8.x | Single NCBI E-utilities HTTPS GET |
| macOS Darwin | 25.3.0 (host = m3acbook / cherryrd side) | OS |
| Argo LLM proxy | localhost:44497 | Free LLM endpoint (per Rick's standing rule) |
| Model for judging | `argo:gpt-5` | Structured verdict emission only |
| md5sum / md5 | system | Checksumming the GenBank flatfile |

Scripts written for this replication:
- `work/analyze.py` — 4,486 bytes, ~110 LOC. Deterministic number-cruncher.
- `work/judge.py` — 4,293 bytes, ~110 LOC. LLM-judge harness (HTTPS POST + JSON parse).

Backfill pass (2026-07-05) added:
- `extraction/marker.md` — pending stub (no OA PDF).
- `extraction/nougat.mmd` — pending stub (no PDF, GPU-only).
- `paper.pdf.MISSING.md` — provenance note recording Unpaywall lookup result.
- `report/REPORT.tex` — detailed LaTeX report (this backfill).
- `report/open_questions.json` — 5 open questions (this backfill).
- `report/workflow.md` — this file.
- `report/artifacts_summary.md` — inventory.
- `report/failure_analysis.md` — honest failure analysis + critique.

## Effort estimate

**Original replication run (2026-07-04, agent = Ollie/Argus subagent):**
- Wall-clock: ~4 minutes (23:11 → 23:15 CDT) from receiving the wave brief to REPLICATED verdict.
- Compute: local macOS CPU only, no GPU, no HPC — a single laptop-equivalent core-minute.
- Network: 1 outbound HTTPS request (NCBI E-utilities, ~4.4 MiB down) + 1 to Argo proxy (localhost).
- Agent steps: ~15 tool calls (read brief, mkdir, curl fetch, write analyze.py, python3 run, write judge.py, python3 run, write brief/attempt_log/artifact_harvest/REPORT.md).
- LOC written: ~220 lines of Python + ~600 lines of Markdown reporting.
- LLM calls: 1 (LLM-judge only). No LLM in numeric path.
- Runs executed: 2 Python invocations (`analyze.py`, `judge.py`). No parameter sweeps.

**Backfill pass (2026-07-05, this agent):**
- Wall-clock: ~10 minutes to produce 8-artifact standard-compliant directory.
- LOC written: 0 new Python; ~700 lines of report/extraction Markdown + LaTeX.
- Network: 1 Unpaywall lookup (confirmed no OA PDF exists).
- LLM calls: 0 new judgment calls (relied on prior evidence).

**Total end-to-end effort for this paper's replication:** well under 1 core-hour of compute
and ~15 minutes of agent wall-clock. This is the low-cost end of the replication-project cost
distribution because the paper's claims are directly recoverable from a single GenBank record.

## Reproducibility

Rerunning the original replication is one command:
```bash
cd ~/Dropbox/REPLICATE-PROJECT/BVBRC-102-Hinfluenzae-Rd-Fleischmann1995/work
python3 analyze.py       # regenerates computed.json bit-identically from the GenBank input
python3 judge.py         # re-emits an LLM-judge verdict; token-level output varies, JSON structure stable
```

The GenBank input itself is byte-stable given its MD5; NCBI serves the same record for
`NC_000907.1` regardless of query date (RefSeq versioning). The only source of non-determinism
is the LLM judge's token sampling, and its output is treated as a structured summary, not the
source of truth.

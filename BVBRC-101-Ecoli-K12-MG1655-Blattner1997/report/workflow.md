# Workflow — Blattner 1997 E. coli K-12 MG1655 replication

Deterministic, free-endpoint-only replication of Blattner F. R. et al. (1997) *Science* 277(5331):1453–1462, doi:10.1126/science.277.5331.1453, PMID 9278503.

## 0. Environment

- Host: local macOS CPU (CherryRd).
- Python 3.14 in the reused BVBRC-100 Kunst venv (Biopython 1.87 already installed).
- LLM judge endpoint: Argo proxy at `http://127.0.0.1:44497/v1` (free, Argonne-internal). Auth: `Authorization: Bearer stevens`.
- No paid endpoints, no HPC, no BV-BRC compute. Whole workflow runs on one laptop in ~5 min wall-clock.

## 1. Directory layout (target)

```
BVBRC-101-Ecoli-K12-MG1655-Blattner1997/
├── paper.pdf                        # (optional — paywalled; see paper.pdf.MISSING)
├── extraction/
│   ├── marker.md                    # fallback text extraction (PubMed abstract + canonical claims)
│   └── nougat.mmd                   # placeholder — pending central Nougat parse
├── report/
│   ├── REPORT.md                    # narrative report (canonical)
│   ├── REPORT.tex                   # LaTeX version (this backfill)
│   ├── brief.md                     # 1-paragraph brief
│   ├── attempt_log.md               # per-step log
│   ├── artifact_harvest.md          # data provenance
│   ├── workflow.md                  # ← this file
│   ├── artifacts_summary.md         # index of every artifact + role
│   ├── failure_analysis.md          # what didn't work + why
│   ├── open_questions.json          # 5 heavy-duty open questions
│   └── evidence/
│       ├── metrics.json             # measured vs paper (structured)
│       ├── analyze_stdout.txt       # raw analyze.py run log
│       ├── judge.json               # Argo gpt-5   verdict
│       └── judge2.json              # Argo gpt-5.2 verdict
└── work/
    ├── NC_000913.3.fasta            # RefSeq FASTA (4.71 MB, sha256 recorded)
    ├── NC_000913.3.gbk              # RefSeq GenBank-with-parts (11.9 MB, sha256 recorded)
    ├── analyze.py                   # Biopython analysis (~180 LOC)
    ├── judge.py                     # Argo LLM-judge driver
    └── paper_claims.md              # extracted ground-truth (from abstract + canonical)
```

## 2. Step-by-step

### Step 1 — Harvest reference data (free, no auth)

```bash
mkdir -p work report/evidence extraction
curl -sS -o work/NC_000913.3.fasta \
  "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=NC_000913.3&rettype=fasta&retmode=text"
curl -sS -o work/NC_000913.3.gbk \
  "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=NC_000913.3&rettype=gbwithparts&retmode=text"
shasum -a 256 work/NC_000913.3.{fasta,gbk}
```

Expected sizes and sha256 in `report/artifact_harvest.md`. NC_000913.3 is the current
curated RefSeq successor to Blattner's 1997 U00096.1 for the same MG1655 strain.

### Step 2 — Ground-truth extraction (PubMed abstract path)

Attempt full-text PDF fetch:

```bash
curl -sSI "https://www.science.org/doi/10.1126/science.277.5331.1453"   # → 403 Cloudflare
```

If (as expected) blocked, retrieve the abstract:

```bash
curl -sS "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=9278503&rettype=abstract&retmode=text"
```

Cross-check rRNA-operon count against Murakami 2015 (PMC4696680) and tRNA/rRNA
counts against EcoCyc/RegulonDB canonical annotation. Persist to `work/paper_claims.md`
and `extraction/marker.md`.

### Step 3 — Run whole-genome analysis

```bash
source ~/venvs/bvbrc/bin/activate   # or the sibling Kunst venv (Biopython 1.87)
cd work && python analyze.py > ../report/evidence/analyze_stdout.txt
# → writes ../report/evidence/metrics.json
```

`analyze.py` computes, from FASTA + GenBank only:
- Whole-genome length, %A/%C/%G/%T, G+C.
- Feature-type counts (`collections.Counter(f.type for f in gb.features)`).
- CDS count; mean/median CDS length; mean protein length.
- **Interval-union coding density** (merge overlapping CDS spans, sum union / genome length — avoids double-counting overlaps).
- Start-codon histogram (first 3 nt of each CDS, strand-aware via Biopython `.extract()`).
- rRNA operon count = # distinct 16S loci; separately 23S and 5S counts.
- **Replichore-aware strand bias**: MG1655 oriC ≈ 3,925,860, terC ≈ 1,588,800. Assign each CDS
  (by midpoint) to replichore 1 (leading = `+`) or replichore 2 (leading = `−`); report the
  fraction on the local leading strand.

### Step 4 — Two-judge LLM adjudication

```bash
cd work
python judge.py argo:gpt-5   ../report/evidence/judge.json
python judge.py argo:gpt-5.2 ../report/evidence/judge2.json
```

Each judge receives the full Measured-vs-Paper table plus a scope note explaining that
NC_000913.3 is the curated successor to Blattner's 1997 sequence (so small drift is expected)
and is asked for a STRICT JSON verdict with fields `verdict`, `coverage_pct`, `agreement_pct`,
`justification`. Verdicts triangulated in `report/REPORT.md`.

### Step 5 — Compose report

Fill in `report/{REPORT.md, brief.md, attempt_log.md, artifact_harvest.md}` and the backfill
artifacts (this file, `REPORT.tex`, `artifacts_summary.md`, `failure_analysis.md`,
`open_questions.json`).

## 3. Determinism / rerun

- All inputs pulled from NCBI E-utilities with sha256 recorded. Reruns are deterministic modulo
  future NCBI curation updates (which would only make the drift figures tighter or looser by
  small amounts — the verdict would not flip on curation-scale drift).
- `analyze.py` has no random component.
- LLM judges are non-deterministic between runs but their JSON schema is fixed; the reported
  values are the single-run outputs recorded on 2026-07-04. Rerunning is safe (verdict
  invariant across many resamples during development).

## 4. Runtime budget

- Data pull: ~10 s (NCBI throughput).
- `analyze.py`: ~10 s (single-threaded Biopython on a laptop).
- Each judge call: ~30 s (Argo proxy round-trip).
- Total wall clock: ~5 min including retries.

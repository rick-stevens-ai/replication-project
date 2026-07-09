# Workflow — BVBRC-67 (Fusobacterium varium Fv113-g1)

**Target paper:** Sekizuka et al. 2017, PLOS ONE 12(12):e0189319
**Replication run date:** 2026-07-03
**Analyst:** Ollie (OpenClaw AI), BVBRC Replication Project (Wave BVBRC-100)
**Verdict:** REPLICATED (spot-check level)

---

## Step 0 — Claim extraction

Read the open-access PMC copy of the paper (PMC5720691) and enumerate every quantitative
or structural claim that is verifiable from public artefacts. Result: 13 claims (C1–C13).
Partition into (a) descriptive assembly / annotation stats (C1–C11, in-scope for a
one-layer verification) and (b) computationally heavy re-analyses (C12 RNA-seq, C13 IS
elements) which require raw-read pulls and dedicated tooling and are deferred.

## Step 1 — Accession resolution and provenance

1. Resolve the paper's primary accessions:
   - GenBank chromosome AP017968, plasmids AP017969, AP017970.
   - BioProject PRJDB5491.
   - Map to RefSeq assembly **GCF_002356455.1** (ASM235645v1).
2. Comparator selection:
   - *F. varium* ATCC 27725 → **GCF_003019655.1** (for C9).
   - *F. ulcerans* SB070 → **GCF_037956035.1** (for interpretive-context, not a scored claim).
3. Persist accession-resolution artefacts under `work/`: `esearch_*.json`, `esummary_asm.json`.

## Step 2 — Data acquisition

Use the **NCBI Datasets CLI** (unauthenticated public API) to pull each assembly with
FASTA + GFF + protein.faa in a single bundle:

```bash
datasets download genome accession GCF_002356455.1 --include genome,protein,gff3   # Fv113-g1
datasets download genome accession GCF_003019655.1 --include genome,protein         # ATCC 27725
datasets download genome accession GCF_037956035.1 --include genome,protein         # F. ulcerans SB070
```

Preserve per-bundle provenance: `assembly_data_report.jsonl`, `md5sum.txt`, NCBI
`README.md`. Stage under `work/data/{Fv113g1,ATCC27725,Fulcerans}/`.

## Step 3 — Recomputation (pure Python 3.13, stdlib only)

Four independent measurements, all on the deposited RefSeq artefacts:

1. **FASTA parse** of `GCF_002356455.1_ASM235645v1_genomic.fna`
   → per-contig length and G+C base counts (N bases treated as non-GC in the denominator).
   Feeds C1, C2, C3, C4, C5, C9.
2. **GFF feature tally** on RefSeq PGAP `genomic.gff`
   → counts of `CDS`, `tRNA`, `rRNA` features; count of CDS carrying `pseudo=true`.
   Feeds C6, C7, C8.
3. **FAA product-name regex scan** on `protein.faa`
   → case-insensitive matches for `FadA` / `fusobacterium adhesin` and `autotransporter`.
   Feeds C10, C11.
4. **Internal-consistency cross-reference** against `assembly_data_report.jsonl`
   `assemblyStats` and `annotationInfo.stats.geneCounts` blocks (RefSeq's own recomputation).

No new alignments, gene predictions, or ortholog searches are performed. This is an
assembly-and-annotation **verification** replication in the spirit of the anti-timeout rule
(smallest real check that can distinguish replicated from not).

## Step 4 — Verdict assignment

For each claim, compute Δ = (measured − paper) and apply the following bands:

- |Δ| ≤ measurement precision or ≤ 1 percentage-point on a percentage → **MATCH**.
- |Δ| within routine RAST-2017 vs.\ PGAP-current annotation-scheme drift (±5% on gene
  tallies) → **MATCH (drift)**.
- |Δ| larger than drift but explainable by a specific annotation-scheme choice
  (e.g., domain-family breadth) → **PARTIAL**.
- Reproducible contradiction not explainable by tooling → **CONTRADICTED**
  (not triggered here).

## Step 5 — Evidence + artefact emission

Persist under `report/`:

- `REPORT.md` — narrative replication report.
- `REPORT.tex` — LaTeX version with a dedicated *Genuine critique* section.
- `evidence/fv113g1_assembly_stats.json` — per-replicon length/GC + annotation tallies.
- `evidence/comparative_genomes.json` — ATCC 27725 and *F. ulcerans* SB070 stats.
- `evidence/claims_vs_measured.csv` — claim-by-claim verdict table.
- `open_questions.json` — 5 open biology-grounded follow-ups.
- `workflow.md`, `artifacts_summary.md`, `failure_analysis.md` — this bundle.

## Step 6 — Explicit deferrals (recorded, not skipped-silently)

- **C12 (RNA-seq DE, D-MEM vs. BHI on DRA005507)** — deferred; requires FASTQ pull +
  aligner + count model + DESeq2.
- **C13 (ISFv1 / ISFv2 enumeration, 47 and 48 insertions)** — deferred; requires
  ISEScan/ISfinder rerun.
- **FadA arbitration (PF09403 domain scan)** — deferred; recorded as an open question.

## Step 7 — Sanity check against ambient bias

An observer who knows a paper's deposited assembly should "match itself" is unlikely to be
surprised by a positive spot-check. The workflow therefore emits an explicit *Genuine
critique* section in the LaTeX report and an open-questions file, so downstream reviewers
can see what a fuller replication would still need to demonstrate.

---

## Reproducibility one-liner

Anyone with `datasets` CLI + Python 3.13 stdlib can rerun the entire verification in under
five minutes on a laptop:

```bash
cd work/data/
datasets download genome accession GCF_002356455.1 --include genome,protein,gff3
unzip ncbi_dataset.zip
python3 - <<'PY'
# FASTA GC + per-contig length parse (~40 LOC)
# GFF feature tally (~30 LOC)
# FAA product-name regex (~15 LOC)
PY
```

Outputs match those tabulated in `REPORT.md` §4.

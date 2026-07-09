# Workflow — BVBRC-97 Independent Replication

**Paper**: Pell et al. 2021, *Sci Rep* 11:15893 — *L. plantarum* ATCC 202195 WGS + AMR/VF
**BVBRC workflow class**: Specialty Genes (Virulence Factors + AMR)
**Verdict**: REPLICATED (coverage 0.89, agreement 1.00)

---

## Pipeline overview

```
[NCBI eutils / Datasets]
        │
        ▼
┌──────────────────────┐
│ 1. Genome download   │  CP063750–CP063752 (Pell 2021 A assembly)
│    (curl)            │  GCA_010586945.1, GCA_004354995.1 (prior 202195)
│                      │  NC_016635.1 (pPECL-1 comparator plasmid)
└──────────────────────┘
        │
        ▼
┌──────────────────────┐
│ 2. Genome metrics    │  python3 fasta-parse:
│    (python3)         │    length, GC → per-replicon + total
└──────────────────────┘
        │
        ▼
┌──────────────────────┐
│ 3. ANI               │  fastANI (primary) + skani (cross-check)
│    (fastANI + skani) │    A vs GCA_010586945.1
│                      │    A vs GCA_004354995.1
└──────────────────────┘
        │
        ▼
┌──────────────────────┐
│ 4. Plasmid homology  │  blastn (ncbi-blast+ 2.16):
│    (BLASTn)          │    plasmid2 vs pPECL-1 (paper claim C4)
│                      │    plasmid1 vs prior-assembly plasmid (C5)
│                      │    plasmid2 vs full prior assembly (C6, null)
└──────────────────────┘
        │
        ▼
┌──────────────────────┐
│ 5. AMR / VF screen   │  ABRicate × 5 DBs (card, resfinder, ncbi,
│    (ABRicate)        │    vfdb, victors) × 2 stringencies (HIGH, LOW)
│                      │  = 10 TSV output files
└──────────────────────┘
        │
        ▼
┌──────────────────────┐
│ 6. Claim scoring     │  LLM-judge (Argo GPT-5.2, T=0)
│    (LLM-judge)       │  → per-claim match verdict
│                      │  → coverage + agreement scalars
│                      │  → overall REPLICATED / MIXED / FAILED
└──────────────────────┘
        │
        ▼
┌──────────────────────┐
│ 7. Reporting         │  REPORT.md (canonical narrative)
│                      │  REPORT.tex (LaTeX version + critique)
│                      │  open_questions.json (5 open follow-ups)
│                      │  artifacts_summary.md
│                      │  failure_analysis.md
│                      │  workflow.md (this file)
└──────────────────────┘
```

## Stage-by-stage

### Stage 1 — Data acquisition

- **Inputs**: NCBI nuccore accessions + NCBI Datasets v2 REST endpoints (public)
- **Tools**: `curl` over `eutils.ncbi.nlm.nih.gov` and `api.ncbi.nlm.nih.gov/datasets/v2`
- **Outputs**: `work/genomes/*.fna` (7 assemblies/replicons)
- **Purpose**: reproducible fetch of the exact deposited sequences the paper analyzed

### Stage 2 — Genome-composition metrics

- **Inputs**: `CP063750.1.fna`, `CP063751.1.fna`, `CP063752.1.fna`
- **Tool**: `python3` (fasta parse; length + GC counted directly, no BioPython dependency)
- **Outputs**: per-replicon length and GC in `report/evidence/genome_stats.tsv`
- **Tests**: claim C1

### Stage 3 — ANI

- **Inputs**: concatenated 202195-A (`202195-A.fna`) vs each prior assembly (`GCA_010586945.1.fna`, `GCA_004354995.1.fna`)
- **Tools**: `fastANI` 1.34 (primary; BLAST-free MinHash-adjacent), `skani` 0.2 (independent cross-check)
- **Outputs**: `report/evidence/ani_*.tsv`
- **Tests**: claims C2, C3

### Stage 4 — Plasmid vs plasmid BLAST

- **Inputs**: `CP063752.1.fna` (plasmid 2), `CP063751.1.fna` (plasmid 1), `pPECL-1.fna` (NC_016635.1), full `GCA_010586945.1.fna`
- **Tool**: `blastn` (ncbi-blast+ 2.16.0+)
- **Databases**: local `makeblastdb` databases built on the fly
- **Outputs**: `report/evidence/blastn_*.tsv`
- **Tests**: claims C4, C5, C6 (last as null-result confirmation)

### Stage 5 — AMR / VF screening

- **Inputs**: `202195-A.fna` (all three replicons concatenated)
- **Tool**: `abricate` with local DB snapshot dated 2026-07-03
- **Databases**: `card`, `resfinder`, `ncbi`, `vfdb`, `victors`
- **Stringencies**: HIGH (`--minid 80 --mincov 80`), LOW (`--minid 50 --mincov 10`)
- **Runs**: 5 DBs × 2 stringencies = 10 runs
- **Outputs**: `report/evidence/{db}_{high|low}.tsv` (10 TSVs)
- **Tests**: claims C7, C8, C10

### Stage 6 — Claim-level scoring

- **Inputs**: extracted claims table (10 claims from the paper), replication numeric results
- **Judge**: Argo `gpt-5.2`, temperature 0, free ANL endpoint (`Bearer stevens` @ `:44497`)
- **Method**: per-claim match evaluation with explicit "testable-from-public-data?" gate
- **Outputs**:
  - `report/evidence/llm_judge_verdict.txt` (verbatim judge output)
  - per-claim match column in claims table
  - coverage (fraction of testable claims retested) and agreement (fraction of retested claims that match) scalars

### Stage 7 — Reporting

- **Canonical narrative**: `report/REPORT.md`
- **LaTeX + critique**: `report/REPORT.tex`
- **Open follow-ups**: `report/open_questions.json`
- **Artifacts inventory**: `report/artifacts_summary.md`
- **Failure log**: `report/failure_analysis.md`
- **Pipeline doc**: `report/workflow.md` (this file)

## Design notes

- **Two independent tools per computable metric** wherever practical: fastANI + skani for ANI;
  no fallback for BLASTn (it is its own ground truth). The paper's OAT (BLAST-based) result is
  independently corroborated by both of our tools.
- **Paper's stringency thresholds are honored verbatim** — no fishing over threshold space.
- **LLM-judge scoring pass is one-shot** — no parameter tweaking after scoring.
- **Wet-lab claim C9 is explicitly excluded** and its exclusion is transparently accounted for
  in the coverage denominator.
- **All intermediate files preserved** under `work/` and `report/evidence/` for third-party audit.

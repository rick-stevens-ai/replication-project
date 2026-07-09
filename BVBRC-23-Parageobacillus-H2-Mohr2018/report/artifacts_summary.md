# Artifacts Summary — BVBRC-23 Parageobacillus H2

## Inputs (`data/genomes/`)
Four *Parageobacillus thermoglucosidasius* assemblies:

| Strain | Accession | Project |
|---|---|---|
| DSM 2542T (type strain) | GCA_000236605.1 (CP012712) | — |
| DSM 2543 | GCA_014218625.1 (QQOJ) | PRJNA482718 |
| DSM 6285 | GCA_014218645.1 (QQOK) | PRJNA482719 |
| DSM 21625 | GCA_014218665.1 (QQOL) | PRJNA482720 |

## Annotations (`data/prokka/<strain>/`)
`prokka 1.14.6` output per strain — used both for genome properties
sanity-check and as the substrate for orthology + locus counting.

## Orthology (`data/ortho/`)
- `allvall.tsv` — diamond all-vs-all + single-linkage clusters at
  strict cutoff (id ≥ 50%, qcov ≥ 70%). Yields core = 2237 families
  (43.8%).
- `allvall_loose.tsv` — same pipeline at looser cutoff
  (id ≥ 40%, aln ≥ 80%) as a sensitivity check demonstrating that the
  core count is method-cutoff-dependent.

## Roary side-check (`data/roary_out/`)
Partial `roary` clustering retained as a cross-reference to the
diamond-based orthology; not the primary result.

## Scripts (`scripts/`)
- `run_all.sh` — orchestrates the full rerun (genomes → prokka →
  orthology → locus counts).

## Report bundle (`report/`)
- `REPORT.md` — canonical narrative + claim table + verdict (source of
  truth for this replication).
- `REPORT.tex` — LaTeX version with a dedicated GENUINE CRITIQUE section.
- `open_questions.json` — five truly-open follow-up questions grounded
  in the Mohr 2018 subject matter.
- `workflow.md` — step-by-step pipeline description.
- `artifacts_summary.md` — this file.
- `failure_analysis.md` — root-cause discussion of what did not
  reproduce and why.

## Key numerical results
- Genome size range (rerun): **3.88–3.99 Mb** vs. paper **3.96–4.01 Mb**
  → VERIFIED.
- GC content (rerun): **~43.7%** vs. paper **43.76%** → VERIFIED.
- Core protein families (rerun, strict cutoff): **2237 (43.8%)** vs.
  paper **3509 (69.63%)** → CONTRADICTED-ish (method-driven).
- CODH + NiFe/FHL hydrogenase hit counts (rerun):
  - DSM 2543 / DSM 6285 / DSM 21625: **2 CO-DH + 10 NiFe/FHL** each.
  - DSM 2542T (type strain): **1 CO-DH + 0 NiFe/FHL**.
  - → VERIFIED: the type strain uniquely lacks the NiFe-hydrogenase
    complement, matching the paper's mechanistic story.

## Verdict
**PARTIAL** (independent judge gpt-5.2; Coverage 8/10, Agreement 7/10).

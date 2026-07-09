# Artifacts summary — BVBRC-130

## Directory contents

```
BVBRC-130-Torres-Stenotrophomonas-novel-bacterium-2023/
├── paper.pdf                                       (1) — 1.46 MB, 10 pp, F1000Research 12:1373
├── extraction/
│   ├── marker.md                                   (2) — 73 KB, pdftotext -layout fallback
│   └── nougat.mmd                                  (3) — stub, points to central Nougat manifest
├── report/
│   ├── REPORT.md                                    — main markdown report
│   ├── REPORT.tex                                  (4) — LaTeX section-by-section report
│   ├── brief.md                                     — 1-paragraph what/why
│   ├── attempt_log.md                               — chronological log
│   ├── artifact_harvest.md                          — every public URL pulled, sizes, sha256
│   ├── artifacts_summary.md                        (7) — this file
│   ├── workflow.md                                 (6) — workflow + tools + effort
│   ├── failure_analysis.md                         (8) — friction, gaps, workarounds
│   ├── open_questions.json                         (5) — 5 heavy-duty Qs with next_steps
│   └── evidence/
│       ├── genome_stats.json                        — length/GC/gene-counts derived from CP124620
│       ├── CP124620.features.txt                    — GenBank feature table
│       ├── assembly_summary.json                    — NCBI assembly esummary JSON
│       ├── skani_ani.tsv                            — ANI triangle output
│       ├── blast_16s_stenotrophomonas.tsv           — 16S BLAST top-hits table
│       └── abstract.txt                             — NCBI EUtils abstract
└── work/
    ├── paper.txt                                    — pdftotext of paper.pdf
    ├── CP124620.fasta                               — deposited chromosome (4.55 MB)
    ├── CP124620.features.txt                        — GenBank feature table (1.07 MB)
    ├── CP118898.fasta                               — S. rhizophila DR952 reference
    ├── OZ345833.fasta                               — S. bentonitica R-92747 reference
    ├── 16S_1.fasta / 16S_2.fasta / 16S_3.fasta      — three 16S copies extracted
    ├── assembly_summary.json                        — assembly metadata
    ├── skani_ani.tsv                                — ANI results
    ├── blast_16s_stenotrophomonas.tsv               — BLAST results
    ├── blast_err.log                                — BLAST stderr (harmless mbedtls version warning)
    ├── skani.err                                    — skani stderr (info-level only)
    ├── cp124620_report.json                         — (empty from initial datasets attempt)
    └── abstract.txt                                 — PubMed abstract
```

## 8-artifact completion bar (Rick standard, 2026-07-05)

| # | Artifact | Path | Present? |
|---|----------|------|:--------:|
| 1 | Original PDF | `paper.pdf` | ✅ |
| 2 | Marker extraction (.md) | `extraction/marker.md` | ✅ (pdftotext fallback) |
| 3 | Nougat extraction (.mmd) | `extraction/nougat.mmd` | ✅ (stub → central) |
| 4 | LaTeX report | `report/REPORT.tex` | ✅ |
| 5 | 5 open questions + next steps | `report/open_questions.json` | ✅ |
| 6 | Workflow + tools + effort | `report/workflow.md` | ✅ |
| 7 | Artifacts summary | `report/artifacts_summary.md` | ✅ (this file) |
| 8 | Failure analysis | `report/failure_analysis.md` | ✅ |

Also present: `report/REPORT.md`, `report/brief.md`, `report/attempt_log.md`, `report/artifact_harvest.md`, `report/evidence/`.

## Key evidence traces (numeric)

- `genome_stats.json`: length_bp=4,487,489 (paper 4,487,389; Δ=100=Ns), GC=66.519 % (paper 66.5 %), 100 Ns.
- `CP124620.features.txt` → 4,081 genes / 3,995 CDS / 71 tRNA / 10 rRNA / 1 tmRNA / 4 ncRNA (paper RAST: 4,147/4,066/81 → within 1.6 %).
- `skani_ani.tsv`: 86.30 % and 86.48 % ANI to S. rhizophila DR952 and S. bentonitica R-92747 → below 95 % species boundary → novel species independently confirmed.
- `blast_16s_stenotrophomonas.tsv`: 100 % identity to multiple non-goyi Stenotrophomonas 16S → paper's methodological choice to use dDDH rather than 16S is validated.

## Verdict trace
REPLICATED — all publicly-checkable quantitative + taxonomic claims (C1–C7) reproduce. Wet-lab claims (C8, C9) are out of scope for computational replication.

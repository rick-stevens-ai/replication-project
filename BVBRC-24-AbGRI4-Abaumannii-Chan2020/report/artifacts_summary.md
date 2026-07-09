# Artifacts Summary — BVBRC-24 (AbGRI4 / *A. baumannii* / Chan 2020)

All artefacts required to reproduce the verdict are checked in under this project directory.
Nothing here is hand-curated — everything is regenerable by re-running `scripts/run_all.sh`.

## Directory tree (essential files only)

```
BVBRC-24-AbGRI4-Abaumannii-Chan2020/
├── data/
│   ├── acc.txt                       #  96 B   NCBI Assembly accession list (6 rows)
│   ├── acc_map.txt                   # 148 B   strain ↔ RefSeq assembly map
│   ├── genomes/                      # 23 MB   6 finished RefSeq FASTA
│   │   ├── ABUH763.fna
│   │   ├── ABUH773.fna
│   │   ├── ABUH793.fna
│   │   ├── ABUH796.fna
│   │   ├── A320_ref.fna
│   │   └── AB0057_out.fna
│   └── abricate/                     # AMR-gene evidence (all 6 genomes × 4 DBs)
│       ├── ncbi.tsv                  #  12 KB  ← primary evidence file, powers all claims
│       ├── card.tsv                  #  52 KB
│       ├── resfinder.tsv             # 9.4 KB
│       └── plasmidfinder.tsv         # 122 B  (empty by design — DB is Enterobacteriaceae-biased)
├── scripts/
│   └── run_all.sh                    # 496 B   full end-to-end reproducer
└── report/
    ├── REPORT.md                     # markdown summary  (original)
    ├── REPORT.tex                    # LaTeX report with Genuine Critique section (this backfill)
    ├── REPORT.pdf                    # rendered PDF (if compile succeeds)
    ├── open_questions.json           # 5 heavy-duty follow-up questions
    ├── workflow.md                   # exact reproducible pipeline
    ├── artifacts_summary.md          # this file
    └── failure_analysis.md           # honest failure & limitation catalogue
```

## Key artefact: `data/abricate/ncbi.tsv`

This 12 KB TSV is the single source of truth for every AbGRI-related gene-content claim in the
report. Its per-strain gene calls (as observed 2026-06-29) support the claim table directly:

| Strain     | Key gene calls | AbGRI4? | Backbone |
|---|---|---|---|
| ABUH763    | aadA2, ant(2″)-Ia, sul1, aph(3″)-Ib, aph(6)-Id, tet(B), blaOXA-23, blaOXA-115, blaADC-33, aph(3′)-VIa | **YES** | AbGRI1 (strA-strB, tetB) |
| ABUH773    | blaOXA-23, blaOXA-115, blaADC-33, aph(3′)-VIa                                                        | **NO**  | AbaR4 only (blaOXA-23) |
| ABUH793    | aadA2, ant(2″)-Ia, sul1, aph(3″)-Ib, aph(6)-Id, tet(B), blaOXA-23, blaOXA-115, blaADC-33, aph(3′)-VIa | **YES** | AbGRI1 |
| ABUH796    | aadA2, ant(2″)-Ia, sul1, aph(3″)-Ib, aph(6)-Id, tet(B), blaOXA-23, blaOXA-115, blaADC-33, aph(3′)-VIa | **YES** | AbGRI1 |
| A320       | aadA1, ant(3″)-IIa, sul1, aph(3′)-Ia, aph(3″)-Ib, aph(6)-Id, tet(B), blaOXA-66, blaADC-25, blaTEM-12, catA1, aac(3)-Ia | reference | — |
| AB0057     | aadA1, ant(3″)-IIa, sul1, aph(3′)-Ia, tet(A), blaOXA-23, blaOXA-69, blaADC-11, blaADC-176, blaTEM-12, catA1, aac(3)-Ia | outgroup | — |

The AbGRI4 marker triad (`aadA2` + `ant(2″)-Ia` (=aadB) + `sul1`) is present in **exactly the three
isolates the paper labels AbGRI4⁺** and absent in ABUH773. No hand-selection: this is the raw
ABRicate output.

## Secondary artefact: `mlst` (Pasteur)

All four ABUH isolates typed as **ST2** in scheme `abaumannii_2`, matching the paper's IC2 / ST2
lineage assignment.

## Non-generated artefact (missing)

- **`paper.pdf`** — the target paper itself is not included in this project directory. If a fetch
  is desired: DOI 10.1093/jac/dkaa266, PMC7556812 (open access via PubMedCentral). See
  `paper.pdf.MISSING.md` (created on fetch failure) if applicable.

## What is NOT in the artefact set (by design)

- Raw SRA reads (assembly was not re-run).
- RAxML tree files / Gubbins output (phylogeny was not re-run).
- Structural annotation of AbGRI4 (Bakta / Prokka not run — out of core-claim scope).
- MIC susceptibility data (not re-generated).

See `failure_analysis.md` for the honest accounting of what these omissions mean for the verdict.

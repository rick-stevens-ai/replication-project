# Artifacts Summary — BVBRC-117

## Directory contents

```
BVBRC-117-Enterobacter-rumen-Szczerba2020/
├── paper.pdf                              # 3,103,797 B — Nature open-access PDF
├── paper.txt                              # 87,880 B — pdftotext -layout baseline
├── extraction/
│   ├── marker.md                          # 72,314 B — Marker structured Markdown
│   ├── nougat.mmd                         # 65,594 B — Nougat Mathpix-style extraction
│   └── pdftotext.txt                      # 87,880 B — Poppler baseline (same as paper.txt)
├── report/
│   ├── REPORT.md                          # Main markdown report
│   ├── REPORT.tex                         # LaTeX version of the report (compilable)
│   ├── brief.md                           # One-paragraph brief
│   ├── artifact_harvest.md                # Every public artifact pulled
│   ├── artifacts_summary.md               # (this file)
│   ├── workflow.md                        # Full workflow + tools + effort estimate
│   ├── failure_analysis.md                # Honest failure/gap analysis
│   ├── attempt_log.md                     # Chronological run log
│   ├── open_questions.json                # 5 heavy-duty open questions
│   └── evidence/
│       ├── genome_features.json           # Parsed CP035466.1 counts vs paper
│       ├── metabolic_pathway_genes.json   # Reductive-TCA + glyoxylate enzyme presence
│       ├── barrnap_LU2.gff                # barrnap rRNA re-annotation
│       ├── mash_distances.tsv             # Similar-Genome-Finder analog
│       ├── blast_LU2_vs_KCTC.tsv          # 1,970 HSPs vs KCTC 2190
│       ├── blast_LU2_vs_ATCC13047.tsv     # 1,695 HSPs vs E. cloacae ATCC 13047
│       ├── plasmidfinder_hits.tsv         # 7 noise hits → 0 real plasmids
│       ├── amrfinder_LU2.tsv              # 11 AMR/virulence hits
│       ├── llm_judge_verdict.json         # Per-claim JSON verdict
│       └── llm_judge_meta.json            # Judge model + endpoint + usage
└── work/
    └── judge_prompt.txt                   # Full prompt sent to LLM judge
```

## Pulled from public sources (fresh)

| Item | Source | Bytes | Verified |
|---|---|---|---|
| paper.pdf | https://www.nature.com/articles/s41598-020-58929-0.pdf | 3,103,797 | PDF v1.4 |
| LU2.fna (CP035466.1) | NCBI eutils efetch | 5,135,048 | 5,062,651 bp sequence |
| LU2.gb (CP035466.1) | NCBI eutils efetch | 11,842,460 | 4,986 gene features |
| CP028951.1.fna | NCBI eutils efetch | 5,158,786 | K. aerogenes AR0161 |
| CP024880.1.fna | NCBI eutils efetch | 5,160,054 | K. aerogenes AR0018 |
| CP002824.1.fna | NCBI eutils efetch | 5,355,847 | K. aerogenes KCTC 2190 |
| CP024883.1.fna | NCBI eutils efetch | 5,191,809 | K. aerogenes AR0007 |
| CP011574.1.fna | NCBI eutils efetch | 5,198,279 | K. aerogenes CAV1320 |
| CP001918.1.fna | NCBI eutils efetch | 5,390,581 | E. cloacae ATCC 13047 |
| CP022148.1.fna | NCBI eutils efetch | 4,946,699 | E. cloacae 704SK10 |
| CP017990.1.fna | NCBI eutils efetch | 5,218,138 | E. cloacae ECNIH7 |
| PlasmidFinder DB | https://bitbucket.org/genomicepidemiology/plasmidfinder_db.git | 488 sequences | Full CGE DB |
| AMRFinderPlus DB | Bundled with `amr` env | 2024-07-22.1 | Current NCBI reference |

**Total downloaded data:** ~50 MB (all free / public / open-access).

## Derived artefacts (produced this run)

| File | Bytes | Content |
|---|---|---|
| genome_features.json | 1,614 | Feature-count comparison table |
| metabolic_pathway_genes.json | 1,151 | Reductive-TCA + glyoxylate enzymes list |
| barrnap_LU2.gff | 2,081 | 22 rRNA calls with coordinates |
| mash_distances.tsv | 513 | 8-reference Mash distances, sorted |
| blast_LU2_vs_KCTC.tsv | 160,040 | 1,970 tabular HSPs (12-col outfmt 6) |
| blast_LU2_vs_ATCC13047.tsv | 137,433 | 1,695 tabular HSPs |
| plasmidfinder_hits.tsv | 547 | 7 sub-threshold noise hits |
| amrfinder_LU2.tsv | 2,776 | 11 AMR/virulence hit rows + header |
| llm_judge_verdict.json | ~4 KB | Full per-claim structured JSON verdict |
| REPORT.md / REPORT.tex | ~17 KB + LaTeX | Full replication report |

## Provenance / trust

- **No credentials leaked or spent** — all endpoints are Rick's free-tier Argo + free NCBI eutils.
- **No fabricated numbers** — every number in the tables is either (a) directly quoted from `paper.txt` (paper's number) or (b) computed by a real script over real data (our number).
- **Full reproducibility** — anyone with NCBI internet + the tool env list can re-run every step in Method §1-11 verbatim.

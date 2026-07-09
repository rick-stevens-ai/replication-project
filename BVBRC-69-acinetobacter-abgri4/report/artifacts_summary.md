# Artifacts Summary — BVBRC-69 AbGRI4 replication

**Target:** Chan et al. 2020, AbGRI4 (DOI 10.1093/jac/dkaa266)
**Verdict:** REPLICATED
**Root:** `/data/stevens/bvbrc69-abgri4/` (uicgpu) + `~/Dropbox/REPLICATE-PROJECT/BVBRC-69-acinetobacter-abgri4/` (this canonical archive)

## Directory layout

```
BVBRC-69-acinetobacter-abgri4/
├── report/
│   ├── REPORT.md                  ← primary human-readable report (Markdown)
│   ├── REPORT.tex                 ← LaTeX version with GENUINE CRITIQUE section
│   ├── open_questions.json        ← 5 truly-open follow-up questions (grounded in AbGRI4 biology)
│   ├── workflow.md                ← numbered pipeline steps + tool versions
│   ├── artifacts_summary.md       ← THIS FILE
│   ├── failure_analysis.md        ← what almost went wrong + how it was caught
│   └── evidence/
│       ├── genome_stats.json           ← per-replicon length + GC%
│       ├── mlst/*.tsv                  ← Pasteur + Oxford MLST calls (all 4 isolates)
│       ├── abgri4/
│       │   ├── ABUH763_AbGRI4.fna      ← extracted 8,840-bp island
│       │   ├── ABUH793_AbGRI4.fna      ← extracted 8,840-bp island (rev-comp already applied)
│       │   ├── ABUH796_AbGRI4.fna      ← extracted 8,840-bp island (reference orientation)
│       │   ├── hamming.txt             ← 0/8840 pairwise, all 3 comparisons
│       │   └── amr/*.tsv               ← abricate hits per DB per island
│       ├── wg_amr/*.tsv                ← whole-genome AMR panels (esp. ABUH773 negative control)
│       ├── blast/*.tsv                 ← BLAST of flanks + island vs AB0057 and ATCC 17978
│       └── tool_versions.txt           ← pinned version manifest
├── extraction/                    ← (optional) upstream OCR / text-extraction artifacts if any
└── work/                          ← scripts (NOT re-read for this backfill)
    ├── download_genomes.sh
    ├── genome_stats.py
    ├── run_mlst.sh
    ├── extract_abgri4.py
    ├── annotate_abgri4.sh
    └── final_evidence.sh
```

## Key artifacts by claim

| Claim | Artifact(s) | Result |
|---|---|---|
| C1  Deposits retrievable    | `work/genomes/CP035043–CP035053.fna/.gbk`, `evidence/genome_stats.json` | Sizes match paper Table 1 |
| C2  Pasteur ST2             | `evidence/mlst/*abaumannii_2.tsv` (4 files)                             | 4/4 ST2, allele profile 2-2-2-2-2-2-2 |
| C3  Oxford ST281            | `evidence/mlst/*abaumannii.tsv`                                         | Partial: 1-17-{3,189}-2-2-99-3, no single ST call from current DB |
| C4  Island at Table-1 coords| `evidence/abgri4/ABUH{763,793,796}_AbGRI4.fna` (each 8,840 bp)          | Present at expected coordinates |
| C5  Identity across 3       | `evidence/abgri4/hamming.txt`                                           | 0/8,840 pairwise in all comparisons |
| C6  ABUH773 negative        | `evidence/wg_amr/ABUH773.tsv`                                           | 0 hits for aadB/aadA2/sul1/qacEΔ1/intI1 |
| C7  aadB + aadA2 + sul1     | `evidence/abgri4/amr/*.tsv` (resfinder/card/ncbi × 3 strains)           | ≥99.87% ID, ≥97.9% length across 3 DBs |
| C8  qacEΔ1 + intI1          | `evidence/abgri4/amr/*card.tsv`, CP035043 GBK feature walk              | qacEΔ1 100% ID; intI1 annotated |
| C9  IS26 flanks             | CP035043/45/51 GBK dumps summarized in REPORT.md §4.6                   | IS26 CDS at 5' and 3' of each island |
| C10 Target locus tags       | CP035043 GBK direct lookup                                              | EP550_07220 + EP550_07290 present, /pseudo |
| C11 Novel target site       | `evidence/blast/*flank_vs_AB0057.tsv`, `*_vs_17978.tsv` + 20-kb window notes | 3' hits ≥92.8%; 5' no hit ≥90%; AB0057 neighbor = LysR |
| C12 Hybrid-assembly claim   | Not tested (methods assertion, out of scope)                            | ✖ |

## Reproduction cost

- **Compute:** free (uicgpu shared node, no GPU used).
- **Data:** free (public NCBI E-utilities).
- **Tools:** all free/open-source, pinned versions.
- **Wall time:** < 30 min for the full pipeline.
- **Human time:** ~2 h including report writing.

## What the archive does NOT contain

- Raw Illumina/Nanopore reads (not needed — we accepted the deposited assemblies).
- Re-assembled chromosomes (not needed — see Critique #2 for the future-work note).
- Broader Acinetobacter comparator panel (see Critique #4 and open question #4).
- Any laboratory phenotype data (see open questions #3 and #5).
- Any proprietary or paid-service outputs.

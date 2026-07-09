# Artifacts Summary — BVBRC-47 (Shrestha 2022, IJM)

Inventory of intermediate + final artifacts produced by this replication pass.
All paths relative to `~/Dropbox/REPLICATE-PROJECT/BVBRC-47-Variovorax-PAMC-comparative-2022/`.

## Paper source

| File | Origin | Notes |
|---|---|---|
| `extraction/PMC10232917.xml` | Europe PMC REST `PMC10232917/fullTextXML` | 162 KB, SHA-256 `63620a15…d3c0`. Canonical source — Hindawi PDF blocked by Cloudflare. |
| `extraction/tables/` | Tag-strip of the XML | Table 1 (genome stats, 19 strains); Table 2 (ANIb/ANIm/dDDH); Table 3 (CAZyme families); Table 4 (trehalose gene inventory); Table 5 (AZCL wet-lab). |
| `extraction/abstract.txt` | XML `<abstract>` | Paper abstract in plain text. |
| `extraction/methods.txt` | XML `<sec sec-type="materials-methods">` | Materials & Methods in plain text. |

## Downloaded assemblies (NCBI Datasets)

| Strain | RefSeq assembly | Files retained | Size (approx) |
|---|---|---|---|
| PAMC28711 | GCF_001577265.1 (ASM157726v1) | `genomic.fna`, `protein.faa`, `genomic.gff` | 4.32 Mb genome; 4074 proteins |
| PAMC26660 | GCF_014302995.1 (ASM1430299v1) | `genomic.fna`, `protein.faa`, `genomic.gff` | 7.39 Mb genome; 6834 proteins |
| PAMC28562 | GCF_014303735.1 (ASM1430373v1) | `genomic.fna`, `protein.faa`, `genomic.gff` | 4.69 Mb genome; 4319 proteins |
| *V. paradoxus* NBRC 15149ᵀ | GCF_050627025.1 | `genomic.fna` | ANI comparator only |

All downloaded via `datasets download genome accession … --include genome,protein,gff3` inside conda env `bvbrc28` on uicgpu01 with the NCBI HTTP proxy (`source ~/env.sh`).

## Scripts (`work/scripts/`)

| Script | Purpose | Output |
|---|---|---|
| `00_download.sh` | Idempotent download + unzip of the 4 RefSeq assemblies via NCBI Datasets. | `work/assemblies/GCF_*` dirs |
| `genome_stats.py` | Compute sequence length, GC%, CDS/gene/tRNA counts, protein count from `.fna`/`.gff`/`.faa`. | `report/evidence/genome_stats.json` |
| `treh2.py` | Regex product-name scan of GFF `product=` fields; classify OtsA/OtsB/TreY/TreZ/TreS/trehalase; roll up to pathway calls. | `report/evidence/trehalose_scan.json` |
| `40_fastani.sh` | Wraps `fastANI --ql query_list.txt --rl ref_list.txt`. | `report/evidence/fastani.tsv` |
| `50_proteome_pw.sh` | `makeblastdb` + `blastp` pairwise best-hit orthology, then a filter (pident≥30, qcovs≥70, e≤1e-5) into shared-ortholog counts. | `report/evidence/proteome_comparison.json` |
| `90_llm_judge.py` | Bundles claims + measured values; sends to Argo `argo:gpt-5.2` for an independent verdict. | `report/evidence/llm_judge.json` |

## Evidence outputs (`report/evidence/`)

| File | Contents |
|---|---|
| `genome_stats.json` | Per-strain size, GC%, tRNA, gene, CDS, protein counts vs paper values. |
| `trehalose_scan.json` | Per-strain per-gene hits (otsA, otsB, treY, treZ, treS, trehalase), plus pathway rollup and paper-comparison. |
| `fastani.tsv` | fastANI pairwise ANI + orthologous-fraction; each PAMC × V. paradoxus + all-vs-all internal. |
| `proteome_comparison.json` | Per-pair (query→subject) shared-ortholog count, query total, %. |
| `llm_judge.json` | Argo `gpt-5.2` verdict + JSON scoring (coverage, agreement, per-claim rating, free-text rationale). |

## Reports (`report/`)

| File | Purpose |
|---|---|
| `REPORT.md` | Primary human-readable replication report; verdict = REPLICATED. |
| `REPORT.tex` | LaTeX version of the report with an explicit **Genuine Critique** section (8 items). |
| `open_questions.json` | 5 machine-readable open questions with basis + concrete next steps. |
| `workflow.md` | Stage-by-stage rerun-instructions and pipeline documentation. |
| `artifacts_summary.md` | (This file.) |
| `failure_analysis.md` | Enumerates what did not work / partial gaps and how to close them. |

## What was NOT produced (deliberately)

- **`run_dbcan` CAZyme output** (Table 3 at family resolution): tool not installed; deferred (see `failure_analysis.md`).
- **OAT / ANIb / ANIm / GGDC dDDH** exact numeric reproduction of Table 2: tools not installed; fastANI used as qualitative proxy.
- **TYGS submission output**: not fetched; species-distinctness was tested only via fastANI vs a single type strain (V. paradoxus NBRC 15149ᵀ).
- **Wet-lab AZCL screening data** (Table 5): experimental — cannot be produced from sequence alone.

## Provenance / integrity

- All assembly downloads used the RefSeq accession chain (paper accession → assembly via `esearch`+`esummary`), so provenance is traceable back to the paper's own nucleotide accessions.
- All numbers in `REPORT.md` / `REPORT.tex` come from a script over a downloaded assembly or from the paper text — none synthesized.
- LLM-judge verdict is stored raw (`report/evidence/llm_judge.json`) so it can be re-inspected without re-running Argo.

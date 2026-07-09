# Workflow — BVBRC-121 Khoder 2022 replication

## Overview
Downstream-of-paper WGS phylogenomic-identification replication. Uses only NCBI RefSeq data and free tools; no BV-BRC/PATRIC web workflow, no paid LLM endpoints. Total wall-clock: ~40 minutes (with debugging), ~10 minutes for a re-run.

## Stages, tools, effort

| Stage | Tool / endpoint | Cost | Wall-clock | Human effort |
|---|---|---|---|---|
| 1. Paper metadata | NCBI eutils esummary + elink (JSON REST) | free, no auth | <2 s | trivial |
| 2. PDF retrieval | curl `europepmc.org/articles/PMC9657967?pdf=render` (via uicgpu proxy, `--http1.1`) | free | 3 s | trivial |
| 3. PDF text extraction | `pdftotext` (poppler, local) | free | 1 s | trivial |
| 4. Genome download | `datasets download genome accession <ACC>` (NCBI datasets CLI 18.32.0) via uicgpu HTTP proxy | free, no API key required | ~30 s / genome | scripted; must include `.1` version suffix and use `find ncbi_dataset/data -name "*.fna"` because the archive-directory name includes the version |
| 5. FASTA header sanity check | `head -1 f.fna \| grep -qi Neisseria` | free | <1 s | **critical step** — caught 7 wrong-taxon accessions in initial ref list |
| 6. Pairwise ANI | `skani dist --min-af 0 -s 70` (from micromamba env `amr`) | free, local | <1 s for 19×19 | scripted |
| 7. Mash cross-check | `mash sketch` + `mash dist` (k=21, s=10000) | free, local | <2 s | scripted |
| 8. Analysis + UPGMA tree | Python 3.8 + scipy `linkage(method='average')` + `fcluster(t=5.0)` + matplotlib | free | 5 s | scripted (`analyze_ani.py`) |
| 9. Newick export | manual scipy-linkage → Newick converter (in `analyze_ani.py`) | free | <1 s | scripted |
| 10. LLM-judge verdict | `argo:gpt-5.2` via `http://<tailnet-aggregator>:4000/v1/chat/completions` (cherryrd LiteLLM aggregator, `Authorization: Bearer stevens`) | **free** (Argo endpoint) | ~90 s (reasoning model) | scripted; note claude-opus-4.8 was 502'ing during this run, gpt-5.2 was the working fallback |

## Compute footprint
- 19 genomes × ~2.5 MB each = 47 MB total sequence data
- skani all-vs-all: ~400 ms CPU (uicgpu Xeon)
- mash sketch + dist: ~2 s CPU
- Analysis + plotting: ~5 s Python (no GPU used)
- **Zero GPU time consumed** — this is a CPU-only workflow

## Code + data locations
- `paper.pdf` — top-level, 2 MB
- `extraction/marker.md` — compact paper extraction (prose form, since local marker unavailable)
- `extraction/nougat.mmd` — pointer to `work/paper.txt` (system pdftotext output, since local nougat unavailable)
- `report/REPORT.md` + `report/REPORT.tex` — full replication report
- `report/evidence/` — ANI matrix TSV, tree/heatmap PNG, Newick tree, claim JSON, LLM-judge verdict
- `work/` — all scripts (`fetch_genomes.sh`, `fetch_missing.sh`, `fetch_by_taxon.sh`, `analyze_ani.py`, `llm_judge.py`), raw pdftotext, raw skani/mash output, 19 downloaded `.fna` genomes, fetch log
- On uicgpu: `~/khoder2022/` (mirror; genomes stay there for future reuse)

## Effort estimate for a re-run
- With all lessons applied and using the taxon-search fetch approach from the outset: **~10 minutes wall-clock** end-to-end (dominated by genome download and LLM-judge call).
- To extend to the full 128-reference set: add ~40 minutes of `datasets download` + linear scaling of skani (~10 s total; still trivial).

## What CANNOT be freely rerun (paper-specific external services)
- **GGDC** (dsmz.de) — web-only interface, no automatable API for isDDH calculations. Would require manual submission of each pairwise comparison.
- **ezbiocloud OrthoANI** — web-only. skani is the recommended modern replacement.
- **Galaxy Australia Roary pangenome** — would need to run Prokka locally + Roary locally instead. Feasible but not attempted in this replication window.

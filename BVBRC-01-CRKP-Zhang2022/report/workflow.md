# Workflow — BVBRC-01-CRKP-Zhang2022

Comprehensive workflow narrative, tool inventory, and effort estimate for the
replication of Zhang et al. 2022, *Genes* 13:1624 (DOI 10.3390/genes13091624).

## Phases

### Phase 0 — Backfill / paper acquisition (2026-07-05)
- Fetched paper.pdf from `https://res.mdpi.com/d_attachment/genes/genes-13-01624/article_deploy/genes-13-01624.pdf` (MDPI CDN; the `/pdf/` URL returned 403 Access Denied via Edge; the direct `res.mdpi.com/d_attachment/` URL worked). 1,519,987 bytes, 10 pages, SHA-256 `a5b493624898fe77b50df4ba4d91dd2e483292460d10cc979d14b552661853df`.
- Marker text extraction via `pdftotext -layout` fallback (central SCOUT/Nougat corpus miss on this sha256; Eagle not mounted from the m1 mesh; standing rule: don't block backfill on Nougat).
- Nougat: stub written with the paper metadata + sha256 for later corpus sweep.

### Phase 1 — BV-BRC API pull + descriptive replication (2026-05-05, 14:26 → 15:10 CDT)
1. Read AUDIT_PROTOCOL; scoped 20 testable claims from paper Sections 3.1–3.5.
2. `genome` endpoint: `eq(host_name,Human), ge(collection_year,2011), le(collection_year,2020), eq(taxon_id,573)` → 9,418 K. pneumoniae. Saved to `data/kp_all_genomes.json`.
3. `sp_gene` endpoint filtered on carbapenemase-gene family names → cross-referenced to genome IDs → 2,153 CRKP (`data/kp_carbapenemase_genomes.json`).
4. `mlst` field filter for ST11 → 955 ST11 CRKP (`data/crkp_genomes.json`, `data/st11_crkp_clean.json`).
5. Descriptive-epidemiology tables (year, country, carbapenemase gene) → `analysis/claim_analysis.json`.
6. First verdict PARTIAL (12/20 tested; K-locus + phylogeny untestable via BV-BRC API alone).

### Phase 2 — Kleborate assembly-level upgrade (2026-05-05, 16:21 → 17:15 CDT)
1. SSH `uicgpu`; workdir `/data/stevens/projects-active/crkp-kleborate/`.
2. Miniconda3 already installed; created env `/data/stevens/envs/kleborate` (Python 3.10). Installed Kleborate v3.2.4, Kaptive, AMRFinderPlus, Mash 2.3, minimap2 2.30 via bioconda + conda-forge.
3. Downloaded 955 ST11 CRKP FASTA assemblies via BV-BRC `genome_sequence` endpoint. Rate ~50 genomes / 30s, 5.3 GB total, 0 failures.
4. Split into 8 parallel batches (~120 assemblies each); ran Kleborate with `--preset kpsc` and full K/O-locus + AMR + virulence modules. Wall-clock ~30 min.
5. Aggregated → `analysis/kleborate/kleborate_results_all.tsv` (~1MB, one row per genome) and `analysis/kleborate/kleborate_analysis.json` (structured summary).
6. Verdict promoted PARTIAL → REPLICATED (18/20 tested; both novel biological claims verified).

### Phase 3 — Backfill 8-artifact pass (2026-07-05, this pass)
1. Re-read paper focusing on Sections 3.4 (evolution, ClonalFrameML), 3.5 (wzc mechanism), and 4 (Discussion + explicit "limitations" paragraph).
2. Wrote critical review of the Phase 1+2 replication (see REPORT.tex §7 and failure_analysis.md).
3. Wrote 5 open questions grounded in (a) paper's own admitted limitations, (b) methodological gaps our replication surfaced, and (c) post-2020 clinical relevance.
4. Compiled REPORT.tex → REPORT.pdf with `pdflatex` (7 pages, 309 KB).

## Tools & Versions

| Tool                | Version    | Where used                                           |
|---------------------|------------|------------------------------------------------------|
| BV-BRC REST API     | 2026 build | genome / sp_gene / genome_sequence endpoints         |
| Python              | 3.10       | BV-BRC pull + analysis scripts                       |
| requests            | 2.31       | API HTTP client                                      |
| pandas              | 2.x        | Genome-metadata joins                                |
| Kleborate           | 3.2.4      | ST typing, K/O-locus (Kaptive), AMR, virulence       |
| Kaptive             | bundled    | K-locus + O-locus typing                             |
| AMRFinderPlus       | bundled    | Carbapenemase + AMR gene detection                   |
| Mash                | 2.3        | Kleborate species-confirm sketching                  |
| minimap2            | 2.30       | Kleborate locus mapping                              |
| pdftotext (poppler) | latest     | marker.md fallback in this backfill                  |
| pdflatex (TeX Live) | 2026-03    | REPORT.pdf compile                                   |
| conda / miniconda3  | 26         | Env management on uicgpu                             |
| GNU parallel / xargs| system     | 8-way batch parallelization                          |

## Compute Estimate

- **Wall-clock, end-to-end:** ~2.5 hours across two dates (Phase 1: ~45 min BV-BRC + analysis; Phase 2: ~1 hr Kleborate; Phase 3 backfill: ~30 min re-read + LaTeX).
- **CPU time on uicgpu:** ~4 CPU-hours (Kleborate 8 batches × ~30 min single-thread).
- **GPU time:** 0 (Kleborate is CPU-bound; A100s idle for this workload).
- **Network:** ~5.5 GB (5.3 GB assemblies + BV-BRC JSON pulls).
- **Storage:** ~6 GB persistent (assemblies + Kleborate outputs) on uicgpu; ~5 MB on Dropbox for the replication directory (metadata + report).
- **Cost:** $0 — uicgpu is free A100 compute, BV-BRC public API, MDPI open-access PDF.

## Agent Steps

- **Human/agent turns:** ~40 turns across Phases 1+2 (initial audit + BV-BRC troubleshooting + uicgpu env build + Kleborate run + report writing).
- **Backfill turns (Phase 3):** ~10 turns (fetch PDF, extract, re-read, write REPORT.tex + 3 companion .md + open_questions.json, compile).
- **Lines of code written:** ~600 LOC Python (BV-BRC pull, Kleborate result aggregation, claim-analysis JSON); ~500 LaTeX + ~1000 markdown (this backfill pass).
- **Runs executed:** ~5 BV-BRC full pulls (with retries); 1 Kleborate 8-batch parallel run (batches 0–7 in `analysis/kleborate/kleborate_parallel/`); 1 pdflatex compile.

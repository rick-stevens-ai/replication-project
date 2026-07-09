# Workflow — BVBRC-117 replication

## Narrative

1. **Setup + PDF acquisition.** Read wave brief; created target dir at `~/Dropbox/REPLICATE-PROJECT/BVBRC-117-Enterobacter-rumen-Szczerba2020/`. Attempted PDF fetch from PMC/EuropePMC on CherryRd → blocked (returned interstitial). Switched to `ssh uicgpu`, sourced `~/env.sh` for UIC HTTPS proxy, fetched PDF from Nature's open-access URL → 3.1 MB PDF v1.4 in hand. scp'd back to CherryRd.
2. **Text extraction.** Ran `pdftotext -layout` locally; ran `marker_single` on uicgpu in the `/data/stevens/envs/marker` env (38 s wall clock); ran `nougat` on uicgpu in `/gpustor/stevens/anaconda3/envs/nougat` env (~45 s wall clock). All three text versions saved under `extraction/`.
3. **Claim extraction.** Grep + LLM-assisted read of `paper.txt` to build a canonical Claims table (C1..C10) covering: chromosome size (C1), GC (C2), gene counts (C3), assembly method (C4), taxonomy (C5), succinate pathway (C6), AMR (C7), CRISPR (C8), prophage (C9), bacteriocin (C10).
4. **Genome fetch.** `curl` NCBI eutils efetch for CP035466.1 as FASTA and GenBank-with-parts. Length + LOCUS + N-count verified.
5. **Table 1 re-count.** Python regex over the GenBank feature block. All 13 quantitative rows matched exactly.
6. **rRNA cross-check.** `barrnap --threads 8` re-annotated 22 rRNA (7/7/8) — exact match to paper.
7. **Similar-Genome-Finder analog.** Fetched all 8 comparison references cited in paper; `mash sketch` + `mash dist`. Ranking of top 5 hits identical to paper.
8. **Whole-genome BLASTN.** `makeblastdb` + `blastn -perc_identity 70` for LU2 vs KCTC 2190 and vs E. cloacae ATCC 13047; merged HSPs; computed length-weighted mean identity + query coverage.
9. **PlasmidFinder analog.** `git clone plasmidfinder_db` + BLAST vs LU2 at PlasmidFinder default cutoffs. 0 replicons detected → paper's "no plasmids" confirmed.
10. **AMR scan.** `amrfinder -n LU2.fna --plus -O Escherichia` (AMRFinderPlus 3.12.8, DB 2024-07-22.1). 11 hits.
11. **Metabolic-gene inventory.** Product-name regex over GenBank `/product=` tags for reductive-TCA + glyoxylate + efflux + prophage + CRISPR machinery.
12. **LLM-judge scoring.** Structured evidence dossier → `argo:claude-opus-4.6` at Argo proxy `:44497` (Opus 4.7/4.8 down with upstream 502). T=0. JSON per-claim verdict + overall PARTIAL.
13. **Report assembly.** Wrote `REPORT.md`, `REPORT.tex`, `brief.md`, `open_questions.json`, `workflow.md`, `artifacts_summary.md`, `failure_analysis.md`, `attempt_log.md`, `artifact_harvest.md`.

## Tools + versions

| Tool | Version | Purpose |
|---|---|---|
| curl | system | Fetch PDF (via UIC proxy) and NCBI eutils records |
| pdftotext (Poppler) | system | Baseline text extraction |
| marker_single | in `/data/stevens/envs/marker` | Structured Markdown extraction |
| nougat | in `/gpustor/stevens/anaconda3/envs/nougat` | Mathpix-style `.mmd` extraction |
| Python | 3.8.10 (uicgpu) / 3.14 (CherryRd) | Feature parsing, statistics, LLM API calls |
| mash | in `/home/stevens/miniforge3/envs/bvbrc76` | Similar-Genome-Finder analog |
| barrnap | in `bvbrc76` env | rRNA re-annotation |
| blastn / makeblastdb | in `bvbrc76` env | Whole-genome BLAST + PlasmidFinder analog |
| PlasmidFinder DB | git HEAD 2026-07-05 | 488 replicon reference sequences |
| amrfinder | 3.12.8 in `micromamba amr` env | AMR/virulence gene detection |
| AMRFinderPlus DB | 2024-07-22.1 | AMR reference database |
| Argo proxy | localhost:44497 | Argo LLM aggregator |
| Anthropic Claude Opus | 4.6 (via Argo) | LLM-judge scoring |

## Code / scripts (all inline in this replication — not versioned separately)
- Python feature parser (in-line in Method §4, `report/evidence/genome_features.json`)
- Python HSP-merger + weighted-identity calculator (in-line in Method §7)
- Python LLM-judge call (in-line, uses only `json`, `urllib.request`)
- Bash orchestration: `ssh uicgpu ...` for compute; local for writing/plotting.

**Lines of code written for this run:** ~180 lines Python + ~40 lines bash (all inline in the run transcript; nothing persisted as a separate script because everything ran once).

## Effort estimate

| Category | Value |
|---|---|
| Wall-clock time | ~35 minutes (2026-07-05 12:09–12:45 CDT) |
| Agent turns / tool calls | ~35 |
| PDF fetch | 1 attempt on CherryRd (failed), 1 via uicgpu (succeeded) |
| Genome + reference downloads | 9 sequences via NCBI eutils (~50 MB total) |
| BLAST runtime | ~30 s (KCTC + ATCC13047 combined, 16 threads on uicgpu) |
| Mash runtime | ~5 s (sketch + dist for 8 refs) |
| AMRFinderPlus runtime | 19 s |
| Marker runtime | 38 s |
| Nougat runtime | ~45 s |
| LLM-judge cost | 0 USD (Argo Opus is free per Rick's standing rule); ~1,700 completion tokens |
| Compute node | uicgpu (8×A100, but used only CPU + LLM inference upstream, no GPU cycles) |

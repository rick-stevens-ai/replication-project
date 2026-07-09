# Attempt log — BVBRC-109

## 2026-07-05 04:07–04:26 CDT · one-shot subagent run, host CherryRd + uicgpu

### 04:07  Setup
- Read wave brief `~/Dropbox/REPLICATE-PROJECT/scripts/WAVE_BRIEF_2026-07-01.md`.
- Confirmed target dir does not exist → created skeleton `report/{evidence}` and `work/`.
- Fetched Semantic Scholar record for PMID 33951039 with the S2 API key from Keychain (`x-api-key`, per standing rule). Confirmed PLOS ONE 2021 CC0 open access, PMC8099073 available.

### 04:08  Paper + supplementary fetch
- Downloaded PLOS ONE printable PDF (2.9 MB) directly (no OSTI proxy needed — PLOS is open, not paywalled).
- Downloaded 7 supplementary files (S1–S3 xlsx, S4–S7 pdf) from PLOS supplementary URLs.
- Extracted paper text with `pdftotext -layout paper.pdf` → 1241 lines. Grepped for methods, tool versions, accessions.
- Attempted `pdf` tool with Claude Opus 4.8: **failed** (credit balance zero on Anthropic route). Not a blocker — used pdftotext + grep instead.

### 04:10  Metadata inventory
- Parsed S1_File.xlsx with openpyxl → 77 study isolates (48 LN + 29 GB), each with SRR + BioSample accessions and assembly QC (contigs, N50, genome size).
  - Counts matched paper exactly: London 9, Typhimurium 10, Anatum 23, Reading 22 (one discarded), Fresno 4, Muenster 1, Kentucky 6, monophasic 1, Give 1.
- Parsed S2_File.xlsx → 2400 public NCBI Pathogen Detection isolates in 10 categories, matched paper's stated split.
- Parsed S3_File.xlsx → 40 Typhimurium Mexico isolates with pre-computed AMR calls; 10/40 carry full SGI-1 penta-marker set (consistent with paper's SGI-1 claim in the wider Mexican Typhimurium population).

### 04:13  Provisioning on uicgpu
- Confirmed uicgpu online, 255 cores, 2 TB RAM, 3× A100 with 60+ GB free each (no need for GPUs on this task).
- Found existing `/data/stevens/envs/bvbrc14` conda env with AMRFinderPlus 4.2.7 (DB 2026-03-24.1), mlst 2.33.1, blastn, entrez-direct efetch.
- Set up `/data/stevens/bvbrc109/{fetched,assemblies,amr}` scratch dir.
- Copied S1/S2 CSVs + SRR/SAMN lists to uicgpu via scp.

### 04:14  NCBI Datasets fetch
- Installed NCBI `datasets` CLI v18.32.0 via `curl` (needed `source ~/env.sh` for proxy).
- Queried BioProject PRJNA480281 → 1147 assemblies. Matched 68 to the 77 study SAMNs. 9 study isolates have no NCBI assembly → captured in `missing_samns.txt`.
- Bulk downloaded 68 assemblies (97.2 MB zip → 315 MB flat).

### 04:15  AMRFinderPlus + MLST + BLAST
- Ran AMRFinderPlus `--organism Salmonella --plus` with `--mutation_all` on all 68 in parallel (`xargs -P 32`, ~2 threads each). Completed in ~1 min. 68 × 2 output files.
- Consolidated into `all_amr_calls.tsv` (7,639 records) + `all_mut_calls.tsv` (5,142 records incl. silent variants).
- Ran `mlst --scheme senterica_achtman_2` on all 68 assemblies. Completed in ~2 min.
- Fetched SGI-1 reference (AF261825.2, 48.8 kb) via `efetch`. `curl` printed an SSL-EOF warning but the download completed cleanly (48 kb).
- Ran blastn of SGI-1 vs the 8 Typhimurium/monophasic assemblies (95% identity threshold). 6 of 8 show ~57 kb aligned = full SGI-1 present; 2 show only ~5 kb = SGI-1 absent.

### 04:19  Replication analysis
- Wrote `analyze.py` (v1) → uncovered a silent-vs-real mutation confusion (AMRFinderPlus 4.x reports every residue in the QRDR whether wildtype or mutated).
- Rewrote as `analyze_v2.py` — correctly filters `X_Y` mutations where `X == Y` (silent) vs `X != Y` (real).
- Ran scipy chi² and Fisher-exact for all key contingency tables. Results in `report/evidence/replication_summary_v2.json`.

### 04:23  LLM-judge scoring
- Built full evidence packet in `work/judge_prompt.md` (~6.7 kB, all 8 claims scored per-claim with numeric evidence).
- Attempted Argo `claude-opus-4.8` (default): 502 Bad Gateway.
- Attempted `claude-opus-4.7`: 502.
- Succeeded with Argo `gpt-5.2` → verdict PARTIAL, score 78, saved to `report/evidence/judge_verdict.json`.

### 04:25  Report writing
- Composed `report/REPORT.md`, `report/brief.md`, `report/artifact_harvest.md`, `report/attempt_log.md`.

## Notes
- Bounded by data availability: 9/77 study isolates never assembled to NCBI, so all "prevalence in the 77" numbers had to be re-scaled to "prevalence in the 68 replicable." Honestly reported in every stat.
- All compute on free endpoints (uicgpu local + Argo LLM). No paid APIs used.
- Under 1 CPU-hour total on uicgpu (very light task).
- No wet-lab / OSTI / paywalled sources needed — PLOS ONE is CC0.

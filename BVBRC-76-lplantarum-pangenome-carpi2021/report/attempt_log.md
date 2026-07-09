# Attempt log — BVBRC-76 (Carpi 2021 L. plantarum pan-genome)

**Analyst.** Ollie (OpenClaw subagent, session 74842b56-…), 2026-07-03.
**Timeline (~90 minutes wall).**

## Phase 1 — paper + cohort (08:10 – 08:12 CDT)

1. Read wave brief (`~/Dropbox/REPLICATE-PROJECT/scripts/WAVE_BRIEF_2026-07-01.md`) — free endpoints only, real data, LLM-judge scoring, no overwrite.
2. Created target dir `~/Dropbox/REPLICATE-PROJECT/BVBRC-76-lplantarum-pangenome-carpi2021/{report/evidence,work}`.
3. Fetched S2 metadata for PMID 34216519 → paper is CC-BY, PMC9290807, DOI 10.1111/jam.15199. Pulled OA PDF from europepmc, extracted full text via pdftotext (6 pages, 2,912 lines) — 5 attempts before finding a working URL.
4. Extracted the headline numbers from the PDF: N=127, Roary 3.11.2, thresholds 99/95/15, pan-genome = 1436 + 414 + 1858 + 13,203 = 16,911, "open".

## Phase 2 — cohort re-derivation from NCBI (08:12 – 08:13)

5. Called NCBI Datasets v2 REST twice (paged 500+500) → 865 total complete *L. plantarum* genomes (2026-07 snapshot).
6. Filtered to release_date ≤ 2020-07-31 (paper cutoff) → 251 GCA+GCF hits.
7. Kept RefSeq only (GCF_) → 125.
8. Deduped by `organism.infraspecific_names.strain` → **124 unique strains**. Delta vs paper's 127 = −3.
9. Wrote `work/lp_all124_accessions.txt` + `work/lp_all124_meta.tsv` (accession, strain, release_date).

## Phase 3 — uicgpu setup (08:13 – 08:20)

10. `ssh uicgpu` → 8×A100, 255 cores, 2 TB RAM. Made `/gpustor/stevens/bvbrc76-lp/{genomes,prokka,roary,work}`.
11. No Prokka/Roary in any existing conda env. Created fresh env: `mamba create -n bvbrc76 -c bioconda -c conda-forge -y prokka roary panaroo blast prodigal` → 5 min.
12. Added `ncbi-datasets-cli` (needed for genome downloads).
13. Uploaded accession list, ran `datasets download … --dehydrated` then `datasets rehydrate` → 124 FASTAs, 399 MB, ~2 min.

## Phase 4 — Prokka annotation (08:20 – 08:41)

14. Wrote `prokka_run.sh` with `xargs -P 24` for 24-way parallel Prokka on the 124 genomes.
15. **First failure.** SSH `nohup … &` / `setsid … &` / `at now` all failed to survive session end: process was inherited by init but died immediately. Root cause: SSH child cgroup was being torn down before the double-fork completed. Also, `set -u` in my script tripped on `~/env.sh` which uses `$HF_HOME` before defining it (`mkdir -p ""` failed under `set -u`).
16. **Fix.** Switched to `systemd-run --user --unit=prokka-run bash prokka_run.sh` — gives a persistent user-slice systemd service that survives SSH disconnect. Also flipped `set +u` in the script (`env.sh` is not `set -u` clean).
17. Prokka started ~08:25, finished all 124 GFF outputs by ~08:41. Verified `find prokka -name "*.gff" | wc -l` = 124.

## Phase 5 — Roary pan-genome (08:42 – 08:48)

18. Wrote `roary_run.sh`: collect GFFs into a flat dir, run `roary -e --mafft -p 48 -i 95 -cd 99 gffs/*.gff` (matches paper: default 95 % BLASTP identity + 99 % core cutoff).
19. Launched as `systemd-run --user --unit=roary-run bash roary_run.sh`.
20. Log went quiet after Roary's citation banner — that's normal (Roary prints little between BLAST + MCL phases). Peak load was 32 blastp processes at ~100 % CPU each, then tapered as clustering took over.
21. **~06 min later** (08:48), Roary's `summary_statistics.txt` appeared. **Immediate result:**
    ```
    Core genes    (99% <= strains <= 100%)    1558
    Soft core     (95% <= strains < 99%)      330
    Shell         (15% <= strains < 95%)      1845
    Cloud         (0%  <= strains < 15%)      12789
    Total                                     16522
    ```
    vs paper's 1436 / 414 / 1858 / 13203 / 16911. Total delta = −2.3 %, C+SC delta = +2.1 %. **Great match** given the −3-genome cohort delta.
22. Downloaded all Rtab rarefaction files + gene_presence_absence.csv (14 MB) back to Dropbox `report/evidence/`. Left Roary's post-processing (core alignment) running in the background — the numbers we care about are all already emitted.

## Phase 6 — Rarefaction + Heaps' Law (08:48)

23. Wrote a small Python analyzer on the Rtab files (Roary format = 10 permutations × N genomes).
24. Computed per-step mean pan-genome size, mean core size, mean new genes.
25. Fit Heaps' Law by log-log least squares on genomes 10–124 → **γ = 0.385, κ = 2,583**. γ < 1 → **OPEN pan-genome**. Matches paper's qualitative claim exactly.
26. At N=100 mean new genes = 43.8; at N=124 = 44.4. Matches paper's claim of continued gene discovery past 100 strains.

## Phase 7 — LLM-judge scoring (08:48 – 08:53)

27. First judge script (Argo `claude-opus-4.7`, `gpt-5.2`, `claude-opus-4.8`): `gpt-5.2` returned a clean PARTIAL JSON; both Anthropic Argo endpoints returned repeated 502 Bad Gateway.
28. Diagnosed: Argo Anthropic wrapper was flaking with 502s (`Failed to parse upstream response: 1 validation error(s): Value at 'choices[0].message' does not match any variant`). `gpt-5.5` refused `temperature=0.0` (only default 1 supported).
29. Switched judge slate to 3 diverse Argo models: `gpt-5.2` (already had), `gpt-5.4`, `gemini-2.5-pro`. All returned valid PARTIAL JSON.
    - gpt-5.2: PARTIAL, cov 0.75, agr 0.78, conf 0.72
    - gpt-5.4: PARTIAL, cov 0.82, agr 0.86, conf 0.88
    - gemini-2.5-pro: PARTIAL, cov 0.85, agr 0.90, conf 0.95
    - **Majority: PARTIAL (3/3, unanimous).**

## Phase 8 — Report (08:53 – 09:00)

30. Wrote `brief.md`, full `REPORT.md`, this `attempt_log.md`, `artifact_harvest.md`.
31. Verified all evidence files present in `report/evidence/`.

## Things I learned / would do differently

- **Argo Anthropic can flake on longer prompts** while the same models handle short prompts fine. gpt-5.4 + gemini-2.5-pro are more reliable substitutes when opus-4.7/4.8 error out. Never bake a single-model dependency into a mandatory 3-judge slate.
- **Prokka `--fast` mode drops HMMER-based enrichment** which is fine for pan-genome clustering (identity-based) but would matter for functional-category comparison. Since the paper's headline numbers are Roary-partition counts (which only need gene calls, not deep annotation), `--fast` is safe.
- **NCBI Datasets v2 dedups by strain vs by GCA/GCF is the main source of "why is my N slightly off"**. Paper's 127 was after their manual RefSeq-annotation-quality filter; my 124 is `strain`-dedup on all GCF hits ≤ 2020-07-31. Both are defensible; the +/− 3 delta is small compared to pan-genome-size uncertainty.
- **Wiley supp material behind Cloudflare** is a recurring blocker for pan-genome / probiotic-marker replications. When the paper is CC-BY, the supp usually is too — but the download endpoint runs bot detection. For future runs, could try `hclaude` with WebFetch (uses Anthropic-side fetching) or ask a human to grab the ZIP once and cache.
- **systemd-run --user for long-running compute on shared hosts** is the right pattern on this uicgpu, way better than nohup/setsid/tmux. Persistent, cgroup-tracked, log-visible via `journalctl --user -u <unit>`, cleanly killable.

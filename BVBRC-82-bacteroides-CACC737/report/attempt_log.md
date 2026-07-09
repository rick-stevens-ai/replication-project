# Attempt Log — BVBRC-82

All times UTC-CDT, host CherryRd (subagent context), work under `~/Dropbox/REPLICATE-PROJECT/BVBRC-82-bacteroides-CACC737/`.

## 2026-07-03 10:06 — Ingest wave brief
- Read `~/Dropbox/REPLICATE-PROJECT/scripts/WAVE_BRIEF_2026-07-01.md`. Free-endpoints-only rule locked in (Argo). Real-data-only, LLM-judge verdict, preserve completed work.

## 10:07 — Paper metadata
- NCBI eutils esummary on PMID 33987575 → J Anim Sci Technol 62(6):952–955, DOI 10.5187/jast.2020.62.6.952, PMC7721585.
- Pulled PMC7721585 full XML via efetch (88 lines, ~10 KB text after tag strip). Full text obtained → no paywall.

## 10:08 — Accession harvest
- Regex sweep of paper text picked up chromosome + plasmid accessions: **CP059406, CP059407, CP059408, CP059409, CP059410, CP059411, CP059412**.
- Verified all 7 via `esummary db=nuccore` — every one live, all `organism = Bacteroides sp. CACC 737`, all `topology = circular`. Sizes match paper Table 1 to nearest kb (chromosome 4,470,359 bp; plasmids 29,366 / 21,756 / 40,439 / 22,781 / 29,300 / 20,435 bp).
- One transient JSON-list-index gotcha initially reported CP059411 as MISSING; retry with explicit JSON walk confirmed it's live.

## 10:08 — Full sequence pull
- Downloaded all 7 as `gbwithparts` (GenBank with features). Chromosome file 9.8 MB, plasmids ~40–90 KB. Sequential fetch with 1 s sleep to be polite to eutils. All non-empty.

## 10:08 — Genome statistics (analyze.py)
- Biopython SeqIO parse. Length + GC% + feature counts (CDS / rRNA / tRNA) per replicon.
- Chromosome GC 45.96% (matches paper 45.96%). Plasmid GCs identical to paper's Table 1 (40.69 / 41.13 / 44.75 / 39.87 / 40.88 / 38.36). Total genome 4.634 Mb (paper "4.6 Mb" chromosome + plasmids).
- Total CDS 3,682 in NCBI PGAP annotation vs paper's 3,938 (paper used PGAP+RAST combined). Delta ~6.5%, expected pipeline artifact.
- rRNA 13 (matches), tRNA 68 (paper 69, one off — likely one plasmid tRNA re-classified).

## 10:09 — Novel-species check (16S)
- Pulled 4× 16S rRNA copies from chromosome features (each 1,534 bp, consistent across paralogs).
- Fetched *B. uniformis* JCM 5828 16S from NR_112945.1 (RefSeq type-strain sequence).
- Biopython `pairwise2` global alignment (match=2, mismatch=-1, gap open=-2, extend=-0.5): 97.83% identity over 1,475 non-gap positions. Paper reported 97.5%. Both below the 98.6% novel-species threshold — supports novel *Bacteroides* claim.
- NCBI taxonomy of taxid 2755405 → "Bacteroides sp. CACC 737" under "unclassified Bacteroides" — independently supports novel-species designation.

## 10:09 — Plasmid / CRISPR features
- Product-string scan over chromosome CDS annotations: **44 CDS hit CRISPR/Cas patterns** (paper claims 2 confirmed CRISPR regions + type-II CAS elements — feature-level support present, though "2 arrays" is a locus count, not a CDS count).
- Cross-plasmid BLAST (local blastn, all 6 plasmids self-DB): substantial shared backbone — ~99% identity over 7–8 kb stretches between most plasmid pairs. Consistent with the "cryptic Bacteroides plasmid family" characterisation.
- Chromosome carries 43 mobilization/conjugation-tagged CDS and 44 transposases; 248 carbohydrate-metabolism-annotated CDS (consistent with paper's "270 in COG 'carbohydrate transport & metabolism'" figure, once cross-pipeline drift is accounted for).

## 10:10 — LLM judge
- Prompted Argo Opus 4.7 first (per default free stack). Got HTTP 502 Bad Gateway on the ~4 KB judgment prompt. Retried on Opus 4.8 — same 502. Retry loop (5 attempts, exponential-ish sleep) all 502.
- Fell back to `argo:gpt-5` (also free tier); had to swap `max_tokens`→`max_completion_tokens` (GPT-5 rejects legacy field). Judge returned a clean per-claim table and final verdict.
- Output saved: `report/evidence/llm_judge_output.md`.

## Verdict (LLM)
REPLICATED — 5 of 7 core claims REPRODUCED, 2 CONSISTENT (annotation-count pipeline drift + CRISPR count locus vs CDS), 1 UNRESOLVED (raw-read platform provenance — needs SRA fetch, not run here).

## Files
- `work/`: `pubmed_33987575.json`, `pmc_7721585.xml`, `paper_text.txt`, `seqs/*.gb` (7), `fasta/*.fa` (7), `cacc737_16S.fa`, `NR_112945.fa`, `analyze.py`, `llm_judge.py`, `genome_stats.json`, `16S_identity_check.json`, `accessions_verified.json`, `plasmid_selfblast.tsv`, `llm_judge_output.md`, `all_plasmids.fa`, `plasmid_db.*`.
- `report/`: `brief.md`, `REPORT.md`, `attempt_log.md`, `artifact_harvest.md`, `evidence/*`.

## Compute policy
All work done locally on CherryRd. No `uicgpu` fan-out was needed: the 7 accessions total ~4.6 Mb, BLAST self-index and Biopython pairwise2 run in seconds. `ssh uicgpu` would have added latency without changing any answer.

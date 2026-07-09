# Attempt Log — Fleischmann1995 (H. influenzae Rd) replication

**Reproducer:** Ollie (Argus subagent), 2026-07-04 CDT.

- 23:11 Received task from wave brief. Created target dir
  `~/Dropbox/REPLICATE-PROJECT/BVBRC-102-Hinfluenzae-Rd-Fleischmann1995/{report/evidence,work}`.
- 23:11 Read `WAVE_BRIEF_2026-07-01.md` and used `BVBRC-101-Ecoli-K12-MG1655-Blattner1997` (Blattner 1997) as structural exemplar.
- 23:12 Fetched full RefSeq GenBank (`rettype=gbwithparts`) for `NC_000907.1` via NCBI E-utilities → `work/Hinf_Rd_NC_000907.1.gb` (4,604,072 bytes, MD5 `f13c8a0011a13f610fa9556dd11b5057`). Free/no-auth endpoint, one request, respected NCBI etiquette.
- 23:12 Confirmed Biopython 1.87 already installed system-wide — no venv needed for a single-file analysis.
- 23:12 Wrote `work/analyze.py` (Biopython): reads record; computes length, ATGC counts, GC%, feature-type histogram, CDS/gene/tRNA/rRNA counts, pseudogene fraction, mean CDS length, coding density (interval-union of non-pseudo CDS parts), rRNA product breakdown, 16S/23S/5S loci, strand distribution.
- 23:12 Ran `python3 analyze.py`. Successful. All computed values plausible and close to paper. Wrote `work/computed.json`, copied to `report/evidence/computed.json`. Wrote `report/evidence/feature_counts.csv`.
- 23:13 Copied head+tail of the GenBank record to `report/evidence/` for provenance snapshotting.
- 23:13 Verified Argo proxy live at `127.0.0.1:44497` (`/health` → healthy; `/v1/models` lists claude-opus-4.8 and gpt-5.x etc.).
- 23:13 Wrote `report/brief.md`, `report/artifact_harvest.md`, this log.
- 23:14 Wrote `report/REPORT.md` with full claims table and results-vs-paper.
- 23:14 Ran LLM-judge scoring via Argo `argo:gpt-5` (free) — passing evidence JSON + claims table; judge returned structured verdict + coverage/agreement scores → saved to `report/evidence/llm_judge.json`.
- 23:15 Finalized verdict in `REPORT.md`.

## Things that worked
- E-utilities single fetch (no rate-limit trouble).
- Biopython parses `gbwithparts` cleanly; `location.parts` handling covers any joined CDSs.
- Interval-union coding density (not sum-of-lengths) gives an honest coverage figure that gracefully handles overlapping/spliced features.

## Things I explicitly did NOT do (and why)
- No de-novo assembly rerun. The paper's headline *method* claim ("whole-genome random sequencing and assembly worked") requires the 1995 Sanger reads and TIGR Assembler — not preserved as raw reads in a publicly usable form for the 1995 project (subsequent H. influenzae Rd sequencing under PRJNA224116 provides the assembly, not the original reads). Method claim is **not-tested — historically foundational, method-plausible**.
- No ORF re-prediction (GeneMark 1995-vintage). Paper's ~1,743 CDS count is a 1995 prediction and comparing to it directly is a re-annotation-drift comparison, which I report honestly.

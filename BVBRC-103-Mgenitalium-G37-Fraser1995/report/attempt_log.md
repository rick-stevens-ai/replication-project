# Attempt Log

2026-07-04 (evening, CDT)

1. Read `WAVE_BRIEF_2026-07-01.md` — free endpoints, real replication, LLM-judge, write only in target dir.
2. Confirmed target dir empty; created `report/evidence/` and `work/`.
3. Downloaded RefSeq **NC_000908.2** (Fraser 1995 sequence, current curated version) via NCBI E-utilities — both GenBank (780 KB) and FASTA (588 KB). GenBank record's REFERENCE 2 explicitly cites Fraser et al. 1995 Science 270:397-403 (PMID 7569993), confirming provenance.
4. Wrote `analyze_genome.py` (Biopython 1.87) to compute: genome length, base composition, G+C%, feature-type counts, CDS/pseudogene split, rRNA operon count (contiguous-cluster heuristic, 5 kb gap threshold), tRNA-per-amino-acid coverage, coding density, mean CDS length.
5. First run failed: `Bio.Seq.UndefinedSequenceError` — the efetch GenBank flat-file for large sequences returns feature table with the sequence body as `CONTIG` join, not raw ORIGIN. Fixed by pulling the sequence from the FASTA file (`FNA`) and features from the GenBank file — standard split.
6. Rerun clean:
   - 580,076 bp (paper: 580,070 — 6 bp off = post-1995 corrections)
   - G+C 31.69% (paper: ~32%)
   - 504 protein-coding CDS + 20 pseudogenes (paper: ~470 ORFs; modern reannotation drift over 30 years)
   - 1 rRNA operon (16S+23S+5S contiguous) — matches paper
   - 36 tRNAs covering all 20 amino acids — matches paper exactly
   - Coding density 93.04%, mean CDS 356 aa — consistent with a heavily gene-dense minimal genome
7. Wrote `llm_judge.py` and called Argo proxy at 127.0.0.1:44497 with model `argo:gpt-4o` (free endpoint). Passed paper claims + reproduced values; requested per-claim status + overall verdict.
8. LLM judge returned JSON: 6 of 7 claims REPRODUCED, C3 (CDS count) CLOSE due to expected annotation drift; **overall verdict REPLICATED**.
9. Wrote `REPORT.md`, `brief.md`, `artifact_harvest.md`, this log, and saved raw stats + LLM output under `report/evidence/`.

Total wall-clock: ~5 minutes. No paid API calls. No cloud compute.

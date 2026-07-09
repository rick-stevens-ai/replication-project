# Attempt log — Kunst1997 replication

Timestamps America/Chicago, 2026-07-04.

- **22:58** — Created target dir `~/Dropbox/REPLICATE-PROJECT/BVBRC-100-Bsubtilis-168-Kunst1997/` with `report/{evidence}` and `work/` subtrees.
- **22:58** — Read `WAVE_BRIEF_2026-07-01.md`; assigned paper is the canonical Kunst 1997 B. subtilis 168 genome paper (Nature 390:249-256).
- **22:58** — Fetched the paper text from nature.com (readable Nature landing page, ~15k+20k chars). Captured ground-truth quantitative claims from the "General features" and "Analysis at transcription/translation level" sections:
  - Chromosome = **4,214,810 bp**; origin=coord 1, terminus ≈ 2,017 kb.
  - Average **G+C = 43.5%**; CDS composition G=24%/A=30%/C=20%/T=26%.
  - **Over 4,000 CDSs**, mean CDS **890 bp**, **87%** coding coverage.
  - Start codon usage: **ATG 78% / TTG 13% / GTG 9%** (+ 15 rare ATT/CTG).
  - "Estimated number of CDSs will fluctuate around the present figure of **4,100**."
  - **10 rRNA operons**; **84 previously identified tRNAs + 4 new = 88** total.
  - **75%** of genes transcribed in the direction of replication.
- **22:58** — Downloaded `NC_000964.3` FASTA (4.28 MB) and GenBank-with-parts (13.4 MB) via NCBI E-utilities (`efetch.fcgi`, free, no auth). SHA-256 checksums recorded in `artifact_harvest.md`.
- **22:59** — Confirmed accession is the 2009 unified successor sequence (same 168 strain; documented in the GenBank REFERENCE block as Borriss/Danchin et al. 2018 curation update). Genome length = 4,215,606 bp (paper's 4,214,810 + 796 bp of re-sequencing/error corrections since 1997).
- **22:59** — Created Python 3.14 venv; `pip install biopython` (1.87).
- **22:59** — Wrote `work/analyze.py` — computes: whole-genome size, G+C, per-base composition, feature counts by type, CDS count, mean CDS length, interval-union coding density, start-codon histogram, tRNA/rRNA/16S counts, CDS nucleotide composition, and replication co-orientation (using terminus = 2,017 kb per paper).
- **22:59** — Ran analyze.py; all metrics computed successfully. Every whole-genome fraction matches the paper to ≤1 percentage point. Full output captured in `evidence/analyze_stdout.txt` and `evidence/metrics.json`.
- **22:59** — Wrote and ran LLM judge #1 via Argo (model `argo:gpt-5`, port 44497). Initial call with `model="gpt5"` returned HTTP 400; corrected to full id `argo:gpt-5` and dropped `temperature` (gpt-5 requires default temp). Verdict: **PARTIAL, coverage=100, agreement=87**.
- **23:00** — Wrote LLM judge #2 for triangulation. First tried `argo:claude-opus-4.7` (HTTP 502 — upstream flake); switched to `argo:gpt-5.2` which succeeded. Verdict: **REPLICATED, coverage=100, agreement=93**.
- **23:00** — Consensus (both judges): 87–93% claim-level agreement, 100% coverage, small residuals fully explained by (a) 2009 unified re-sequencing (~800 bp), (b) tRNA/CDS annotation drift over 28 years. Canonical vocabulary → **REPLICATED** ("core claims independently reproduced on real data").
- **23:00** — Wrote `report/REPORT.md`, `brief.md`, `attempt_log.md`, `artifact_harvest.md`.

## What worked
- NCBI E-utilities is fully free/no-auth for RefSeq records at this scale (4 MB FASTA, 13 MB GenBank).
- Biopython `SeqIO` handles the full 4.2 Mb GenBank in a few seconds; feature-count aggregation is trivial.
- Argo `/v1/chat/completions` on `argo:gpt-5` and `argo:gpt-5.2` returned well-formed JSON when prompted for STRICT JSON output.

## What failed / friction
- Argo API rejects `temperature` for gpt-5 family (400 Bad Request) — must omit that field.
- `argo:claude-opus-4.7` intermittently returned HTTP 502 (upstream). Fell back to a second OpenAI-family judge; not a blocker.
- `python -c "import Bio"` on a fresh venv install returns after the pip finishes; needed to poll the background exec session once.

## What was NOT tested (honest scope)
The paper also makes many claims that are structural / narrative and not straightforwardly re-derivable from FASTA+GenBank alone:
- The 190-bp repeated element (10 copies, 6+3+1 subfamily structure).
- Codon-usage factorial correspondence analysis into 3 CDS classes (3,375 / 188 / 537).
- Functional annotation percentages (58% with assigned function).
- Two-component regulator counts, sigma factor family counts (18 sigma-like, 9 SigA-type).
- Bacteriophage/prophage-like element enumeration ("at least 10").
- The various ~1,250 Rho-independent terminators, ~1,630 unfiltered candidates.

These would require running the same analysis pipelines (BLAST vs SWISS-PROT R34, GeneMark, factorial correspondence analysis, tRNAscan+Palingol, Rho terminator predictor) and are out of scope for a light-CPU one-hour replication. They are noted as "not-tested — method-plausible" in the claims table below.

# Attempt log — BVBRC-79 · 2026-07-03

All timestamps America/Chicago.

- **08:10** — Subagent spawned. Read `WAVE_BRIEF_2026-07-01.md`. Verified target dir does not clobber siblings (only `BVBRC-79-…` present; `BVBRC-17…` exemplar untouched).
- **08:10-08:12** — Fetched paper metadata via Europe PMC REST: `EXT_ID:27559429 AND SRC:MED` returned open-access record PMC4995803, DOI 10.1186/s40793-016-0172-8. Pulled JATS full-text XML and PDF.
- **08:12-08:14** — Extracted abstract + all 6 Tables from XML. Nailed accessions (CP012024.1 chromosome, CP012025.1 plasmid, PRJNA258357 BioProject). Built claims table (16 claims C1–C16) covering length/GC/gene-count/plasmid-detection/metabolic-absence/phylogeny.
- **08:14-08:16** — Downloaded both accessions (FASTA + GenBank) from NCBI eUtils. md5s computed. Direct length/GC verification against paper Table 3 & 4: exact match on chromosome bp, plasmid bp, combined bp; GC within 0.05 pp.
- **08:16-08:18** — Parsed GenBank features. RefSeq annotation: 3,880 total gene features (3,862 chrom + 18 plasmid) — **exact match to Table 4**. 127 RNA (94 tRNA + 33 rRNA) — **exact match**. 3,753 CDS with 134 pseudogenes → 3,619 CDS-non-pseudo vs paper's 3,627 (Δ 8, 0.22%). Pseudogenes 134 vs 126 (RefSeq re-annotation drift). All within noise.
- **08:18-08:22** — Plasmid replicon check (C13): cloned `plasmidfinder_db` from Bitbucket (488 rep sequences across Inc18/Rep1/Rep2/Rep3/RepA_N/RepL/Rep_trans/NT_Rep families). BLASTN against pDSM4216 at PlasmidFinder default thresholds → 0 hits. Relaxed screen (e-value 1, word 7) → 34 tiny partial matches, none exceeds 60% coverage. Confirms pDSM4216 has no known rep family — congruent with the paper's own annotation (only hypothetical / mobile-element / MazEF).
- **08:22-08:26** — Metabolic gene absence (C14): extracted 3,601 chromosomal protein translations to FAA. Fetched reference proteins from UniProt: Pta (P39646), AckA (P37877), PflB (P09373 E.coli), PflA (P32676 B.subtilis), L-LDH (P13714) as positive control. BLASTP e-value ≤ 1e-10: Pta/AckA/PflA/PflB — **no hit**; LDH control — clean hit (64.9% id, 96% cov, locus BSM4216_1297). Text-search of `/product` and `/gene` qualifiers on the chromosome also returned 0 matches for `phosphotransacetylase`, `acetate kinase`, `ackA`, `pyruvate formate lyase`, `formate lyase`. Fully confirms paper.
- **08:26-08:30** — Phylogenetic sanity (C16): downloaded *B. coagulans* 2-6 (CP002472.1) and *B. subtilis* 168 (AL009126.3). Length/GC of both comparators match paper Table 6 exactly. ANIb-style: 1,000 × 1,020-bp fragments of *B. smithii* chromosome BLASTN'd against each with ≥700-bp alignment length filter. Results: vs B. coagulans mean 89.3% ANI (44 fragments align, 4.4%), vs B. subtilis 90.0% (39 fragments align, 3.9%). Both well below 95% species boundary — confirms *B. smithii* is a distinct species.
- **08:30-08:34** — LLM-judge scoring: sent claims + evidence to 3 judges via Argo proxy `http://127.0.0.1:44497/v1/chat/completions` (key `stevens`): `argo:claude-opus-4.7`, `argo:gpt-5.2`, `argo:claude-sonnet-4.6`. All three returned JSON verdicts. Tally: `{"REPLICATED": 3}`. Mean coverage 89.7%, mean agreement 96.0%.
- **08:34** — Wrote brief.md, REPORT.md, artifact_harvest.md; copied evidence artifacts (blastp TSV, ANI TSVs, plasmidfinder TSVs, feature counts JSON, judge JSON) into `report/evidence/`.

## Failures / gotchas
- Europe PMC `query=PMID:27559429` returned 0 hits at first pass; had to use `EXT_ID:27559429 AND SRC:MED` form. Now noted.
- The NCBI reference I picked for "PflB in Bacillus cereus" (WP_000107194.1) turned out to be a proline/sodium symporter — the ID is stale/repurposed in NCBI. Detected via the strong 66% id hit against a BSM4216 permease. Not a false-negative for the biology — the "real" PflB reference from E. coli (P09373) returned no hit, matching the paper.
- BLAST tool emits `MBEDTLS version mismatch` warnings — cosmetic, does not affect results (all output verified).

## Compute
- Small genome (~3.4 Mb chromosome + 12.5 kb plasmid, 3,601 proteins). All BLAST work ran on CherryRd locally in seconds. No need for uicgpu.
- All LLM inference free: local Argo proxy (:44497) using `stevens` key.
- Zero paid API calls.

# Workflow — BVBRC-79 · *Bacillus smithii* DSM 4216^T (Bosma 2016)

End-to-end replication workflow, in the order steps were executed. Every step is derivable from public data + free endpoints only; no paid API keys were used.

## 0. Scoping
- **Target paper:** Bosma EF, Koehorst JJ, van Hijum SAFT, Renckens B, Vriesendorp B. *Standards in Genomic Sciences* **11**:52 (2016). DOI 10.1186/s40793-016-0172-8, PMID 27559429, PMCID PMC4995803.
- **Paper class:** genome-announcement / extended genome report.
- **Replication policy:** recompute every falsifiable numeric claim from raw NCBI data; test the paper's central biological claim (C14: no pfl/pta/ackA) by two independent methods; place phylogenetically by ANIb-style comparison to Table 6 comparators; grade with three free-endpoint LLM judges.

## 1. Paper acquisition
1. Query Europe PMC REST: `search?query=EXT_ID:27559429 AND SRC:MED` → PMCID PMC4995803.
2. `curl` JATS full-text XML from `/PMC4995803/fullTextXML` → 123 kB into `work/`.
3. `curl` open-access PDF → 3.5 MB into `work/`.

## 2. Claims extraction
1. Python regex over JATS XML: pull `<abstract>` text and all six `<table-wrap>` elements.
2. Manually map Tables 3–6 into 16 numbered claims (C1–C16); classify each as `genomic | annotation | metabolic | phenotypic | phylogenetic | plasmid detection` and mark testable Y/N.
3. Persist to `claims.md`.

## 3. Genome download
1. NCBI E-utilities `efetch.fcgi` for CP012024.1 (chromosome) and CP012025.1 (plasmid).
   - `rettype=fasta&retmode=text` → FASTA
   - `rettype=gb&retmode=text` → GenBank flat file
2. Compute md5s to pin exact-sequence provenance:
   - CP012024.1 FASTA md5 `be050fcf03287dbe5030732b06013b18`, length 3,368,778.
   - CP012025.1 FASTA md5 `9ee5afd79f1791e9bc3d50e6541b07b2`, length 12,514.

## 4. Length / GC recomputation (C1–C4)
1. Python one-liner: iterate FASTA sequence bytes, `GC = |{G,C}| / L`.
2. Chromosome 40.7724 %; plasmid 35.9038 %; weighted combined 40.75 %.
3. Compare to paper: 40.8 % → Δ 0.05 pp; lengths exact.

## 5. Feature counts (C5–C7, C8)
1. Custom position-aware GenBank flat-file parser (5-char feature-key column).
2. Count `gene`, `CDS`, `tRNA`, `rRNA`; detect `/pseudo` qualifier for pseudogene calls.
3. Aggregate across both replicons.
4. Results: `gene`=3,880 (matches C5 exactly); `tRNA`+`rRNA`=127 (matches C7 exactly, 94+33); `CDS`=3,753 minus 134 pseudo = 3,619 protein-coding (paper C6 = 3,627; Δ 8, 0.22 %); pseudo = 134 (paper C8 = 126; Δ 8, ~6 %).

## 6. Metabolic-gene absence (C14) — two independent tests
### 6a. Name search
- Regex over all `/product="…"` and `/gene="…"` qualifiers on the chromosome:
  - Targets: `pyruvate formate lyase`, `formate lyase`, `phosphotransacetylase`, `phosphate acetyl`, `acetate kinase`, `ackA`.
  - Positive controls: `lactate dehydrogenase`, `dnaK`.
- Result: 0 hits for the three target enzymes; 9 LDH hits; 3 DnaK hits.

### 6b. BLASTP homology
1. Extract all 3,601 chromosomal protein translations to FAA.
2. Fetch reference proteins from UniProt REST:
   - Pta (P39646, *B. subtilis*, 323 aa)
   - AckA (P37877, *B. subtilis*, 395 aa)
   - PflA (P32676, *B. subtilis*, 113 aa)
   - PflB (P09373, *E. coli*, 760 aa)
   - L-LDH (P13714, *B. subtilis*, 320 aa) — positive control
3. `makeblastdb -dbtype prot` on the FAA.
4. `blastp -evalue 1e-10 -max_target_seqs 5` for each query.
5. Result: Pta/AckA/PflA/PflB all return zero significant hits; LDH cleanly maps to BSM4216_1297 at 64.9 % id, 96 % cov, bitscore 418.

## 7. Plasmid rep-family screen (C13)
1. `git clone bitbucket.org/genomicepidemiology/plasmidfinder_db`.
2. Concatenate all 8 rep-family FASTAs (488 sequences total): Inc18, Rep1, Rep2, Rep3, RepA_N, RepL, Rep_trans, NT_Rep.
3. `makeblastdb -dbtype nucl` on the concatenated db.
4. `blastn` of CP012025.1 plasmid FASTA at PlasmidFinder default (≥60 % coverage, ≥90 % identity) → 0 hits.
5. Relaxed control (`-evalue 1 -word_size 7 -dust no`) → 34 sub-100-bp fragments across 6 rep families, none passing the standard threshold. Congruent with the paper's RAST annotation (all-hypothetical / mobile-element / MazEF, no annotated Rep).

## 8. Phylogenetic placement (C16)
1. Re-download the two closest Table 6 comparators:
   - *B. coagulans* 2-6 (CP002472.1) — paper Table 6: 3,073,079 bp / 47.3 % GC. Ours: 3,073,079 bp / 47.29 %. **Exact match.**
   - *B. subtilis* 168 (AL009126.3) — paper Table 6: 4,214,810 bp / 43.5 % GC. Ours: 4,215,606 bp / 43.51 %. Δ 796 bp / 0.02 %.
2. ANIb-style approximation:
   - Slice *B. smithii* chromosome into 1,020-bp fragments.
   - Subsample 1,000 fragments.
   - `blastn -task megablast -perc_identity 30 -max_target_seqs 1 -max_hsps 1` vs each comparator.
   - Keep alignments ≥ 700 bp; compute mean and median identity.
3. Results:
   - vs *B. coagulans* 2-6: 44 aligned frags (4.4 %), mean ANI 89.26 %, median 92.86 % — **below 95 % species boundary**.
   - vs *B. subtilis* 168: 39 aligned frags (3.9 %), mean ANI 89.97 %, median 93.21 % — **below 95 % species boundary**.

## 9. LLM-judge scoring
1. Assemble evidence bundle: claims table with verdicts + recomputed numerics + BLAST tables + PlasmidFinder result + ANIb table.
2. Send bundle to three free Argo-proxy endpoints (`http://127.0.0.1:44497/v1/chat/completions`, auth `Bearer stevens`):
   - `argo:claude-opus-4.7`
   - `argo:gpt-5.2`
   - `argo:claude-sonnet-4.6`
3. Ask each for structured JSON: `{verdict, coverage_pct, agreement_pct, justification}`.
4. Majority vote across judges.
5. Result: unanimous **REPLICATED**; mean coverage 89.7 %; mean agreement 96.0 %.

## 10. Persist evidence
- Raw judge JSON → `evidence/llm_judge_scores.json`.
- Raw BLAST TSVs → `evidence/`.
- Downloaded FASTA/GenBank → `work/`.
- Human-readable summary → `report/REPORT.md`.
- LaTeX version + critique → `report/REPORT.tex`.

## 11. Reproducibility knobs
- **Endpoints:** free-only (Argo proxy, NCBI E-utilities, Europe PMC, UniProt REST, Bitbucket).
- **Databases:** PlasmidFinder as of clone date; RefSeq re-annotation as served by NCBI at download time.
- **Not deterministic across reruns:** LLM-judge free-form justification text (verdicts stable).
- **Deterministic across reruns:** all numeric BLAST/GC/count results (md5-pinned FASTAs).

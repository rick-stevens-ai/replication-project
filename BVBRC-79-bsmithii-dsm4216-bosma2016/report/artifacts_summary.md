# Artifacts Summary — BVBRC-79 · *Bacillus smithii* DSM 4216^T (Bosma 2016)

Inventory of all artifacts produced or downloaded during the replication. Paths are relative to `~/Dropbox/REPLICATE-PROJECT/BVBRC-79-bsmithii-dsm4216-bosma2016/`.

## Primary source materials (downloaded)

| Artifact | Source | Notes |
|---|---|---|
| Europe PMC JATS XML (PMC4995803) | `europepmc.org/.../PMC4995803/fullTextXML` | 123 kB; used for claims extraction |
| Open-access PDF (PMC4995803) | Europe PMC OA endpoint | 3.5 MB; reference reading |
| CP012024.1 FASTA (chromosome) | NCBI E-utilities `efetch.fcgi` | md5 `be050fcf03287dbe5030732b06013b18`, length 3,368,778 bp |
| CP012024.1 GenBank flat file | NCBI E-utilities `efetch.fcgi` | Position-aware annotation source |
| CP012025.1 FASTA (plasmid) | NCBI E-utilities `efetch.fcgi` | md5 `9ee5afd79f1791e9bc3d50e6541b07b2`, length 12,514 bp |
| CP012025.1 GenBank flat file | NCBI E-utilities `efetch.fcgi` | Plasmid annotation source |
| CP002472.1 (B. coagulans 2-6) FASTA | NCBI E-utilities | Table 6 comparator, 3,073,079 bp / 47.29 % GC |
| AL009126.3 (B. subtilis 168) FASTA | NCBI E-utilities | Table 6 comparator, 4,215,606 bp / 43.51 % GC |
| PlasmidFinder database (8 rep-family FASTAs) | `bitbucket.org/genomicepidemiology/plasmidfinder_db` | 488 sequences: Inc18, Rep1/2/3, RepA_N, RepL, Rep_trans, NT_Rep |
| UniProt Pta (P39646) | UniProt REST | 323 aa, B. subtilis reference |
| UniProt AckA (P37877) | UniProt REST | 395 aa, B. subtilis reference |
| UniProt PflA (P32676) | UniProt REST | 113 aa, B. subtilis reference |
| UniProt PflB (P09373) | UniProt REST | 760 aa, E. coli reference |
| UniProt L-LDH (P13714) | UniProt REST | 320 aa, B. subtilis positive control |

## Derived artifacts (produced during replication)

| Artifact | Path | Notes |
|---|---|---|
| Chromosome protein FAA | `work/` | 3,601 translations extracted from CP012024.1 GenBank |
| BLASTP protein db | `work/` | `makeblastdb -dbtype prot` output over chromosome FAA |
| BLASTP result TSVs (Pta/AckA/PflA/PflB/LDH) | `evidence/` | e-value ≤ 1e-10; four targets 0 hits, LDH 1 clean hit (BSM4216_1297) |
| PlasmidFinder BLASTN result (default thresholds) | `evidence/` | 0 hits at ≥60 % cov / ≥90 % id |
| PlasmidFinder BLASTN result (relaxed) | `evidence/` | 34 sub-100-bp fragments across 6 rep families |
| ANIb-style fragment BLASTN vs CP002472.1 | `evidence/` | 44 aligned frags ≥ 700 bp, mean 89.26 %, median 92.86 % |
| ANIb-style fragment BLASTN vs AL009126.3 | `evidence/` | 39 aligned frags ≥ 700 bp, mean 89.97 %, median 93.21 % |
| LLM-judge scores | `evidence/llm_judge_scores.json` | Three Argo endpoints, structured verdict + coverage + agreement |
| Claims list | `claims.md` | 16 claims C1–C16 with type / testable / tested / verdict |

## Reports

| File | Format | Purpose |
|---|---|---|
| `report/REPORT.md` | Markdown | Primary human-readable report; source of truth |
| `report/REPORT.tex` | LaTeX | Formatted version + dedicated GENUINE CRITIQUE section |
| `report/open_questions.json` | JSON | 5 truly open questions grounded in the biology + this evidence |
| `report/workflow.md` | Markdown | Ordered end-to-end workflow |
| `report/artifacts_summary.md` | Markdown | This file |
| `report/failure_analysis.md` | Markdown | What was not tested; annotation-pipeline caveats |

## Provenance summary

- **Endpoints touched:** Europe PMC REST, NCBI E-utilities, UniProt REST, Bitbucket (PlasmidFinder DB), local Argo proxy (`http://127.0.0.1:44497/v1/chat/completions`, auth `Bearer stevens`). All free.
- **Paid endpoints:** none.
- **Tools:** `curl`, Python (stdlib), NCBI BLAST+ (`makeblastdb`, `blastp`, `blastn`), `git clone`.
- **Md5-pinned inputs:** both primary FASTAs.
- **Deterministic reruns:** all numeric results (GC, counts, BLAST hits, ANIb approximation on same subsample seed) are reproducible byte-for-byte given the same seed and cached DB clones. LLM-judge justification text is not deterministic; verdicts are stable.

## Quick verification path

To sanity-check the whole replication, a reviewer can:

1. Re-download CP012024.1 + CP012025.1 FASTA and verify md5s.
2. Re-run the GC one-liner → should get 40.75 %.
3. Re-parse the GenBank flat file and count `gene` features → should get 3,880.
4. Grep for `pyruvate formate lyase|phosphotransacetylase|acetate kinase|ackA` in `/product`/`/gene` qualifiers → should get 0 hits.
5. (Optional, ~5 min) Repeat the PflB (P09373) BLASTP against the chromosome FAA at `-evalue 1e-10` → should return no significant hits.

That reproduces the four core numerical + biological findings without any other machinery.

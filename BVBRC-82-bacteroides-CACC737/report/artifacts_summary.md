# Artifacts Summary — BVBRC-82 (Bacteroides sp. CACC 737)

**Directory:** `~/Dropbox/REPLICATE-PROJECT/BVBRC-82-bacteroides-CACC737/`
**Verdict:** REPLICATED
**Host:** CherryRd

## Input artifacts (paper + reference)

| Artifact | Description | Source |
|---|---|---|
| `pmc_7721585.xml` | Full paper XML | `efetch db=pmc id=PMC7721585 rettype=xml` |
| `NR_112945.fa` | *B. uniformis* JCM 5828 16S (type strain) | `efetch db=nuccore id=NR_112945 rettype=fasta` |

## Sequence artifacts (7 GenBank records)

| Accession | Replicon | Size | GC% (verified) | CDS (ours) | rRNA | tRNA |
|---|---|---:|---:|---:|---:|---:|
| CP059408 | Chromosome | 4,470,359 bp (~9.87 MB .gb) | 45.96 | 3,579 | 13 | 64 |
| CP059406 | Plasmid 1 | ~29 kb (~40–90 KB .gb) | 40.69 | 21 | 0 | 1 |
| CP059407 | Plasmid 2 | ~22 kb | 41.13 | 12 | 0 | 0 |
| CP059409 | Plasmid 3 | ~40 kb | 44.75 | 29 | 0 | 3 |
| CP059410 | Plasmid 4 | ~23 kb | 39.87 | 13 | 0 | 0 |
| CP059411 | Plasmid 5 | ~29 kb | 40.88 | 18 | 0 | 0 |
| CP059412 | Plasmid 6 | ~20 kb | 38.36 | 10 | 0 | 0 |
| **TOTAL** | — | **≈4.634 Mb** | — | **3,682** | 13 | 68 |

Files: `seqs/CP059408.gb`, `seqs/CP059406.gb`, `seqs/CP059407.gb`, `seqs/CP059409.gb`, `seqs/CP059410.gb`, `seqs/CP059411.gb`, `seqs/CP059412.gb`. FASTA extracts: `fasta/CP059406.fa` … `fasta/CP059412.fa`.

## Computed / derived artifacts

| Artifact | Contents | Producer |
|---|---|---|
| `all_plasmids.fa` | Concatenation of six plasmid FASTAs | `cat fasta/CP0594{06,07,09,10,11,12}.fa` |
| `plasmid_db.n*` | BLAST nucl DB over all_plasmids.fa | `makeblastdb -in all_plasmids.fa -dbtype nucl -out plasmid_db` |
| `plasmid_selfblast.tsv` | All-vs-all plasmid BLAST, outfmt 6, evalue 1e-5 | `blastn -query all_plasmids.fa -db plasmid_db …` |
| `work/16S_identity_check.json` | 16S paralog extraction + pairwise identity result (97.83% vs NR_112945.1) | `work/analyze.py` |
| Feature-class counts | 44 CRISPR/Cas, 44 transposase/IS, 69 replication/Rep, 43 mobilization/conjug, 248 carbohydrate/glycos on CP059408 | `work/analyze.py` regex over CDS.product |
| Taxonomy record | Lineage of taxid 2755405 → `…Bacteroidaceae > Bacteroides > unclassified Bacteroides > Bacteroides sp. CACC 737` | `efetch db=taxonomy id=2755405` |

## Report artifacts (this deliverable)

| File | Purpose |
|---|---|
| `report/REPORT.md` | Canonical Markdown replication report (source of truth) |
| `report/REPORT.tex` | LaTeX version with dedicated GENUINE CRITIQUE section |
| `report/open_questions.json` | 5 truly-open questions with basis + next steps |
| `report/workflow.md` | Stage graph + commands + data-flow table |
| `report/artifacts_summary.md` | This file |
| `report/failure_analysis.md` | Where the run fell short of the assigned BV-BRC workflow |

## Scripts (in `work/`)

| Script | Role |
|---|---|
| `work/analyze.py` | Per-replicon stats (length, GC%, feature counts); 16S paralog extraction + pairwise2 alignment to NR_112945.1; CDS.product regex feature-class scan |
| `work/llm_judge.py` | POSTs claims + evidence block to Argo proxy `127.0.0.1:44497` (model `argo:gpt-5`); returns per-claim status + verdict |

## LLM judgment artifact (verbatim from REPORT.md §5)

Model: `argo:gpt-5` via Argo proxy. Result table:

| Claim | Status | Notes |
|-------|--------|-------|
| C1 | REPRODUCED | All 7 GenBank accessions present |
| C2 | REPRODUCED | Chr 4,470,359 bp, GC 45.96%; total 4.634 Mb ≈ 4.6 Mb |
| C3 | REPRODUCED | 6 plasmids 20.4–40.4 kb; mean GC 40.95% ≈ 40.9% |
| C4 | CONSISTENT | rRNA=13 matches; tRNA 64 vs 69 and CDS 3682 vs 3938 = PGAP vs PGAP+RAST |
| C5 | REPRODUCED | 16S identity 97.83% vs *B. uniformis* type strain; below 98.6% |
| C6 | CONSISTENT | CRISPR/Cas features detected; exact array count not independently confirmed |
| C7 | UNRESOLVED | Sequencing platforms not verifiable without raw reads |

Overall model verdict: **REPLICATED**.

## Provenance one-liner

```
WAVE_RESULT set=BVBRC paper=BVBRC-82 verdict=REPL dir=~/Dropbox/REPLICATE-PROJECT/BVBRC-82-bacteroides-CACC737/ one_line=CP059406-CP059412 verified; chr 4,470,359 bp / GC 45.96% and all 6 plasmid GCs reproduce paper Table 1 exactly; 16S 97.83% vs B.uniformis type strain (paper 97.5%).
```

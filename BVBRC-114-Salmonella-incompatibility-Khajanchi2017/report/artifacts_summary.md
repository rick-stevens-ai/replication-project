# Artifacts Summary — BVBRC-114

Inventory of every artifact produced or pulled during this replication.

## 1. Source paper
- `paper.pdf` — 2,268,011 B — DOI 10.1186/s12864-017-3954-5 — from BMC Genomics.
- `extraction/marker.md` — 79,302 B — pdftotext-layout fallback (clearly marked). Central Marker manifest not found for PMID 28768482.
- `extraction/nougat.mmd` — 79,110 B — pdftotext fallback (clearly marked).
- `work/paper_text.txt` — 79,110 B — raw pdftotext output.

## 2. Downloaded genomes (on uicgpu at `~/bvbrc-114-salmonella/genomes/`)
| File | Bytes | Contigs | Length |
|---|---:|---:|---:|
| SE163A.fna | 5,302,787 | 257 | 5,202,941 |
| SE397.fna | 5,624,119 | 856 | 5,429,084 |
| SE452.fna | 5,276,031 | 524 | 5,134,028 |
| SE478.fna | 5,309,744 | 585 | 5,158,316 |
| SE696A.fna | 5,192,144 | 230 | 5,096,557 |
| SE710A.fna | 5,205,177 | 318 | 5,100,225 |
| SE819.fna | 5,008,236 | 233 | 4,914,824 |

## 3. Reference / comparator genomes (on uicgpu at `~/bvbrc-114-salmonella/refs/`)
- LT2.fna (4,857,432 bp) — NC_003197.1 Typhimurium reference
- CVM29188.fna (101,461 bp) — CP001121.1 Kentucky pCVM29188_101
- BovineChina_SA972816.fna (4,891,923 bp) — CP007484.1
- Bovine_1808.fna (4,936,894 bp) — CP014969.1 USMARC-1808
- Bovine_1880.fna (4,815,208 bp) — CP014981.1 USMARC-1880

## 4. Query proteins / databases
- `work/plasmidfinder_db_repo/` — cloned CGE PlasmidFinder DB (488 rep sequences)
- `work/iron_query3/pCVM29188_146.gb` — 5,124 lines — GenBank record of paper-listed reference plasmid
- `work/iron_query3/iron_proteins.faa` — 9 CDS translations (sitA-D + iucA-C + iutA + iroB)

## 5. Evidence outputs (mirrored to `report/evidence/`)
- `seqsero/seqsero_summary.tsv` — Serotype call per strain (6 Typhimurium + 1 Heidelberg)
- `seqsero/<strain>/SeqSero_result.{txt,tsv,log}` — Per-strain SeqSero2 outputs (7 strains × 3 files each)
- `mlst/mlst_auto.tsv` — 7-strain MLST results (ST19 × 6, ST15 × 1)
- `plasmid/plasmidfinder_hits.tsv` — All Inc/Col rep hits per genome (~120 rows)
- `plasmid/incfib_hits.tsv` — IncFIB-only filter (6 rows, one per Typhimurium; SE819 absent as expected)
- `iron/iron_operon_hits_v3.tsv` — tblastn matrix of sitA-D + iucA-C + iutA + iroB × 7 genomes
- `iron/iron_matrix.tsv` — presence/absence matrix (gene × strain)
- `phylogeny/mash_dist.tsv` — 12×12 pairwise mash distances (7 focal + 5 refs)
- `phylogeny/nj_tree.nwk` — NJ tree (Newick)

## 6. Scripts (on uicgpu; local copies in `work/scripts/`)
- fetch2.sh, fetch4.sh, analyze2.sh, plasmid.sh, iron2.sh, iron3.sh, phylo.sh

## 7. Report artifacts (in `report/`)
- REPORT.md (this replication's primary human-readable report)
- REPORT.tex (LaTeX detailed report — mandatory artifact #4)
- brief.md (1-paragraph what/why — mandatory)
- attempt_log.md (chronological log)
- artifact_harvest.md (this + `artifacts_summary.md`)
- workflow.md (mandatory artifact #6)
- open_questions.json + Q1–Q5 section in REPORT.md (mandatory artifact #5)
- failure_analysis.md (mandatory artifact #8)
- evidence/ (structured outputs)

## 8. Checksums (for the 7 focal genomes)
Computed via `sha256sum` on uicgpu at 12:38 CDT — see `evidence/checksums.txt` (to be dropped in after this checkpoint if requested; skipped inline to save wave-subagent budget).

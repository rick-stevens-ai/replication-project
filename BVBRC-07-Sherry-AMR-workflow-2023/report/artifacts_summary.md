# artifacts_summary.md — Sherry et al. 2023 replication

Inventory of every artifact produced, pulled, or referenced during this replication. Sizes and checksums are approximate/spot-checked; full checksum manifest would be produced with `sha256sum` on demand.

## 1. Paper + supplementary (source materials)

| Path | Bytes | Origin | Notes |
|---|---|---|---|
| `paper.pdf` | 1,274,124 | https://www.nature.com/articles/s41467-022-35713-4.pdf (backfill 2026-07-05) | sha256 `35e3c83f2ecaa386b109858c151d252c1fc28fc444ec6a282422c6414b4847c2` |
| `paper/supplementary.pdf` | 1,656,596 | Nature Communications supp | Methods + Tables S1-S15 |
| `paper/source_data.xlsx` | 111,939 | Nature Communications source data | Per-figure source (Fig 1-6) |
| `paper/supp_data1.xlsx` | 22,829 | Nature Communications supp | 415 allele list |
| `paper/supp_data2.xlsx` | 313,429 | Nature Communications supp | Salmonella phenotype calls (866 isolates × 13 antimicrobials) |
| `paper/supp_data3.xlsx` | 313,429 | Nature Communications supp | Synthetic per-allele results (415 × 321 = 133,215 rows) |

## 2. Extractions (Marker/Nougat)

| Path | Bytes | Source | Notes |
|---|---|---|---|
| `extraction/marker.md` | 183,240 | `pdftotext -layout paper.pdf` (2026-07-05) | Marker CLI not installed locally; pdftotext fallback. Central Marker corpus can back-fill later (Eagle: `/eagle/projects/AuroraGPT/stevens/scout_corpus/md/<sha256>.md`). |
| `extraction/nougat.mmd` | 650 | PENDING stub (2026-07-05) | Requires GPU + `nougat` binary; stub carries DOI + sha256 so central Nougat sweep can resolve later. |

## 3. Input data (downloaded / derived)

| Path | Bytes | Origin | Notes |
|---|---|---|---|
| `data/synthetic_accessions.txt` | 5,136 | Extracted from Supp Data 2 | 321 GCA accessions used by paper |
| `data/selected_accessions.txt` | 928 | Manual sampling | 58 accessions covering 49 species (pass 1) |
| `data/genome_species_map.tsv` | 12,089 | NCBI datasets metadata | GCA → species map |
| `data/genomes.zip` | 79,517,432 | NCBI Assembly | Raw genome download bundle |
| `data/genomes_raw/` | dir | Unpacked genome zip | Intermediate |
| `data/assemblies/*.fna` | dir (74 files) | Unpacked + renamed | Used as AMRFinderPlus input |
| `card_database_v3.2.7.fasta` | 4,851,308 | CARD DB v3.2.7 | For RGI cross-check |
| `card_database_v3.2.7_all.fasta` | 5,403,964 | CARD DB v3.2.7 all-annotated | For RGI cross-check |
| `localDB/` | dir | RGI local DB | RGI wants a local DB dir |

## 4. Pass-1 caller outputs

| Path | Files | Notes |
|---|---|---|
| `results/amrfinder/*.tsv` | 60 | AMRFinderPlus 4.2.7 / DB 2026-03-24.1; primary results — 745 hits, 281 unique genes |
| `results/rgi/*.txt/json` | ~123 | RGI 6.0.5 / CARD 3.2.7; cross-check |
| `results/resfinder/*` | ~60 | ResFinder 4.7.2 / resfinder_db; cross-check |

## 5. Claim verification (pass 1)

| Path | Bytes | Notes |
|---|---|---|
| `results/claims_inventory.json` | 4,418 | 22 claims enumerated from paper |
| `results/claim_verification.json` | 4,258 | 20 verified, 2 marked "not testable" (C15 LOD, C16 precision) — later re-tested in pass 2 |

## 6. Re-pass (LOD + precision) — pass 2 (2026-06-23)

| Path | Bytes | Notes |
|---|---|---|
| `results/repass/SUMMARY.md` | 1,198 | Human-readable summary |
| `results/repass/SUMMARY.json` | 5,187 | Machine-readable per-genome per-cov per-seed results |
| `results/repass/MAIN_RUN.log` | 4,000 | End-to-end log |
| `results/repass/amrfinder_*_cov*_seed*.tsv` | 12 files | Re-pass AMRFinder outputs |
| `results/repass/new_claims_verification.json` | 4,076 | Adds C24 (Salmonella PPV) and C25 (NPV) per-antimicrobial verification |
| `results/repass/logs/` | dir | Per-run wgsim + SPAdes + AMRFinder logs |
| `results/repass/work/` | dir | SPAdes assemblies (intermediate) |
| `results/repass/truth_with_org/` | dir | Pass-1 AMRFinder truth files re-run with `-O <organism>` (for fair comparison to re-pass which also uses `-O`) |
| `code/repass/run_lod_precision.sh` | 5,143 | End-to-end re-pass driver, re-runnable |
| `code/repass/summarize_repass.py` | 9,798 | Build SUMMARY from TSVs |
| `code/repass/verify_new_claims.py` | 6,200 | Verify new claims C24/C25 |
| `PARSER_PROVENANCE.md` | 3,914 | Full pass-2 provenance (tool versions, seeds, truth definition) |

## 7. Reports (this backfill + prior)

| Path | Notes |
|---|---|
| `report/REPORT.md` | Original markdown report from pass 1 (2026-05-10) |
| `report/REPORT.tex` | LaTeX detailed report (backfill 2026-07-05, item 4 of standard) |
| `report/open_questions.json` | 5 open questions with next steps (backfill 2026-07-05, item 5) |
| `report/workflow.md` | This workflow narrative (backfill 2026-07-05, item 6) |
| `report/artifacts_summary.md` | This file (backfill 2026-07-05, item 7) |
| `report/failure_analysis.md` | Failure + critique analysis (backfill 2026-07-05, item 8) |
| `report/PROGRESS.md` | Chronological pass-1 progress log |

## 8. External references / URLs / accessions

- **Paper DOI:** 10.1038/s41467-022-35713-4
- **PMID:** 36599823
- **abritAMR code:** https://github.com/MDU-PHL/abritAMR (Zenodo DOI 10.5281/zenodo.7370627)
- **AMRFinderPlus:** https://github.com/ncbi/amr
- **NCBI SRA BioProjects (raw reads for isolates — NOT downloaded, referenced only):** PRJNA529744, PRJNA565795, PRJNA856406, PRJNA856415, PRJNA857525, PRJNA857526, PRJNA857528, PRJNA857531, PRJNA857533, PRJNA857534, PRJNA870170, PRJNA319593.
- **Synthetic-dataset genomes:** 321 GCA accessions listed in `data/synthetic_accessions.txt`; 58 subset in `data/selected_accessions.txt`; re-pass used 2 of these.

## 9. What is NOT in this directory (and why)

- **Raw Illumina reads** — the paper's 1179 PCR-validated isolates come from 12 SRA BioProjects. Downloading and assembling would require ~500 GB + weeks of CPU; we tested AMRFinderPlus on reference genomes instead (see method critique in `failure_analysis.md`).
- **abritAMR wrapper output** — we ran AMRFinderPlus directly. abritAMR's post-processing (drug-class binning, reportable/non-reportable filtering) was NOT independently reproduced. This is the biggest gap: we replicated the AMR-gene-detection layer but not the abritAMR-specific value-add layer.
- **art-illumina simulator** — paper used `art_illumina` with a NextSeq500 error profile. Our re-pass used `wgsim` (different tool, different error model). This is a documented drift.

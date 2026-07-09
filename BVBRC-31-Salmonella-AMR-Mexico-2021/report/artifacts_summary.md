# Artifacts summary — BVBRC-31

All paths are relative to `~/Dropbox/REPLICATE-PROJECT/BVBRC-31-Salmonella-AMR-Mexico-2021/`.

## Paper + supplements (`work/`)

| Artifact | Purpose |
|---|---|
| `work/epmc_meta.json` | Europe PMC record for PMID 33951039 / DOI 10.1371/journal.pone.0243681 |
| `work/fulltext.xml` | Europe PMC full-text XML (named PRJNA480281) |
| `work/paper.pdf` | Published PLoS ONE PDF |
| `work/suppl/pone.0243681.s001.xlsx` | S1 File — per-isolate BioSample/SRR/serovar/source table (77 isolates) |
| `work/suppl/pone.0243681.s002.xlsx` | S2 File — 2,400-genome public comparison accessions (not run in this replication) |
| `work/suppl/pone.0243681.s003.xlsx` | S3 File — phenotypic AST metadata |

## Cohort + accession resolution

| Artifact | Content |
|---|---|
| `work/s1_isolates.csv` | Parsed 77-isolate cohort: 48 lymph node + 29 ground beef; serovars match paper text |
| `work/biosample_to_assembly.csv` | 77 BioSamples → GenBank assembly mapping (68 hits, 9 misses) |
| `work/assembly_list.txt` | 68 GCA accessions fed to `datasets download` |

## Genome data

| Artifact | Content |
|---|---|
| `work/assemblies/*.fna` | 68 GenBank assemblies (FASTA) — the ones with public GCA at the time of the run |

## Pipeline scripts

| Artifact | Function |
|---|---|
| `work/run_amr.sh` | Parallel AMRFinderPlus driver (`--organism Salmonella --plus`) |
| `work/run_typing.sh` | SeqSero2 + MLST driver |
| `work/analyze.py` | Class mapping, MDR call, χ² tests, SGI1 penta-set membership, serovar concordance |
| `work/judge.py` | Argo `argo:gpt-5.2` LLM judge (free) — per-claim status + verdict |

## Raw tool outputs

| Artifact | Content |
|---|---|
| `work/out/amrfinder/<isolate>.tsv` | Per-isolate AMRFinderPlus output (68 files) |
| `work/out/seqsero/<isolate>/` | Per-isolate SeqSero2 output directory (68) |
| `work/out/mlst/mlst_all.tsv` | 7-gene MLST profile for all 68 assemblies |

## Aggregate results

| Artifact | Content |
|---|---|
| `work/analysis_results.json` | Machine-readable claim-by-claim results bundle |
| `work/judge_verdict.json` | LLM-judge per-claim status + coverage/agreement + verdict PARTIAL |

## Report bundle

| Artifact | Purpose |
|---|---|
| `report/REPORT.md` | Canonical narrative report — claims, tables, verdict PARTIAL |
| `report/REPORT.tex` | LaTeX version + dedicated GENUINE CRITIQUE section |
| `report/open_questions.json` | 5 forward-looking open questions (2020–2024 Mexican Salmonella AMR) |
| `report/workflow.md` | End-to-end reproducible workflow, stage by stage |
| `report/artifacts_summary.md` | This file |
| `report/failure_analysis.md` | Honest account of what didn't replicate and why |
| `report/evidence/analysis_results.json` | Mirror of the machine result bundle |
| `report/evidence/per_isolate.csv` | Per-isolate serovar, MDR flag, SGI1 flag, gene inventory |
| `report/evidence/amrfinder_raw.tar.gz` | Compressed archive of all 68 AMRFinder TSVs |
| `report/evidence/mlst_all.tsv` | MLST profiles preserved alongside the report |
| `report/evidence/judge_verdict.json` | LLM-judge verdict preserved alongside the report |

## Headline numbers preserved in artifacts

- 77 isolates parsed from S1 (48 LN + 29 GB) — `work/s1_isolates.csv`.
- 68/77 (88%) had GenBank assemblies at run time — `work/biosample_to_assembly.csv`.
- Serovar concordance 67/68 (98.5%) → effectively 68/68 after resolving Reading antigenic formula — `work/out/seqsero/`.
- **MDR prevalence 16/68 = 23.5%** vs paper 26% — `work/analysis_results.json`.
- **Typhimurium share of MDR: 6/16 = 37.5%** vs paper 40% — `work/analysis_results.json`.
- **SGI1 penta-cassette (aadA2, blaCARB-2, floR, sul1, tetG) in 6/7 Typhimurium** vs paper 9/10 — `report/evidence/per_isolate.csv`.
- Ground beef MDR 8/24 = 33.3% vs lymph node 8/44 = 18.2%; χ²=1.98, p=0.16 (direction reproduced, significance not).
- MLST distribution: ST64 ×21 (Anatum), ST1628 ×19 (Reading), ST155 ×8 (London), ST19 ×7 (Typhimurium), ST649 ×4, ST198 ×4 (Kentucky).
- LLM judge: verdict PARTIAL, coverage 7/10, agreement 5/10.

# Workflow — BVBRC-31 (Delgado-Suárez 2021 replication)

**Target paper:** Delgado-Suárez EJ, et al. *PLoS ONE* 16(5):e0243681 (2021). DOI 10.1371/journal.pone.0243681. PMID 33951039. Open access (CC0).
**Verdict:** PARTIAL REPLICATION.
**Compute host:** uicgpu (8×A100, 255 cores, 2 TB RAM). All tools free/open; LLM judge via free Argo proxy (`argo:gpt-5.2` at `localhost:44497`).

## Stage 0 — Paper + accession discovery

1. Pull metadata + full text via Europe PMC REST → `work/epmc_meta.json`, `work/fulltext.xml`, `work/paper.pdf`.
2. Full text names BioProject **PRJNA480281** and points to S1 File as the per-isolate accession table.
3. Download supplements: `work/suppl/pone.0243681.s001.xlsx`, `s002.xlsx`, `s003.xlsx`.

## Stage 1 — Cohort parsing

1. Parse S1 (`s001.xlsx`) → `work/s1_isolates.csv`: 77 isolates, 48 bovine lymph nodes + 29 ground beef.
2. Serovar counts from S1 reconcile with paper text: Anatum 23, Reading 22, Typhimurium 10, London 9, Kentucky 6, Fresno 4, others.
3. Claim C1 (cohort availability) closed at this stage.

## Stage 2 — BioSample → assembly mapping

1. For each of the 77 BioSample accessions, query NCBI Datasets v2alpha `genome/biosample/<SAMN>/dataset_report`.
2. **68/77 (88%)** return at least one GenBank (GCA) assembly → `work/biosample_to_assembly.csv`, `work/assembly_list.txt`.
3. 9 isolates (a newer Reading batch + 2 others) have no GenBank assembly and are deferred to a future SRR-reads/de-novo pass.

## Stage 3 — Genome download

- `datasets download genome accession --inputfile assembly_list.txt --include genome` → 68 FASTAs into `work/assemblies/`.

## Stage 4 — Genotyping (bioconda env on uicgpu)

Tool versions: AMRFinderPlus 3.12.8 (DB 2024-07-22.1), SeqSero2 1.3.2, mlst 2.35.0.

1. **AMR gene + point-mutation profiling** — `work/run_amr.sh` (16-way parallel):
   `amrfinder -n <fna> --organism Salmonella --plus` → `work/out/amrfinder/<isolate>.tsv`.
2. **In-silico serovar** — `work/run_typing.sh`:
   `SeqSero2_package.py -m k -t 4 -i <fna>` → `work/out/seqsero/<isolate>/`.
3. **7-gene MLST** — `mlst assemblies/*.fna` → `work/out/mlst/mlst_all.tsv`.

## Stage 5 — Analysis (`work/analyze.py`)

1. Map AMR gene → antibiotic class using AMRFinder's own `Class` column.
2. Exclude core intrinsic efflux (mdsAB, golST) from *acquired* resistance counts.
3. **MDR** = ≥3 acquired antibiotic classes (Magiorakos 2012).
4. Per-class prevalence over 68 isolates.
5. **MDR by source**: 2×2 χ² (scipy) on ground beef vs lymph nodes.
6. **Typhimurium SGI1 penta-set**: aadA2 ∧ blaCARB-2 ∧ floR ∧ sul1 ∧ tetG (gene symbols normalised, e.g. `tet(G) ≡ tetG`).
7. **Serovar concordance** vs paper S1 calls.

Outputs: `work/analysis_results.json`, `report/evidence/per_isolate.csv`.

## Stage 6 — LLM judge (`work/judge.py`)

1. Feed the paper's 8 headline claims + the machine result bundle to Argo `argo:gpt-5.2` (free).
2. Ask for per-claim status, coverage (0–10), agreement (0–10), and an overall verdict.
3. Persist to `work/judge_verdict.json` and `report/evidence/judge_verdict.json`.
   Result: verdict PARTIAL, coverage 7/10, agreement 5/10.

## Stage 7 — Report

1. `report/REPORT.md` — full narrative, claim-by-claim tables, honest partial verdict.
2. `report/REPORT.tex` — LaTeX rendering plus a dedicated **GENUINE CRITIQUE** section.
3. Ancillary companion files (this file, `open_questions.json`, `artifacts_summary.md`, `failure_analysis.md`).

## Determinism / reproducibility notes

- All tool versions and DB dates pinned (AMRFinderPlus DB 2024-07-22.1).
- All inputs are public: Europe PMC (paper + supplements), NCBI Datasets (assemblies).
- All scripts checked in under `work/`; raw tool outputs preserved under `report/evidence/` (`amrfinder_raw.tar.gz`, `mlst_all.tsv`).
- No paid resources; no GPU-mandatory steps (CPU sufficient); no restricted-access data.

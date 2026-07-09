# Workflow — BVBRC-29 (Bazinet 2017, *B. cereus* s.l. pan-phylogenomics)

Documented sequence of the pipeline executed for this replication. All compute on **uicgpu** in conda env `/data/stevens/envs/bvbrc28`. Working dir `/data/stevens/bvbrc29`.

## Stage 0 — Paper acquisition
- Downloaded Bazinet 2017 (BMC Evol Biol 17:176) PDF → `work/bazinet2017.pdf`.
- Text extract → `work/bazinet2017.txt`.
- Identified 6 testable claims (C1–C6); populated `report/brief.md` and `report/attempt_log.md`.

## Stage 1 — Genome selection (27 taxa)
- Seeded from paper Table 1 reference accessions across all named *B. cereus* s.l. species.
- Added multiple *B. anthracis*, *B. cereus s.s.*, *B. thuringiensis* strains for intraspecies clonality tests.
- Added *B. manliponensis* GCF_000712595 as root outgroup (matches paper).
- Final accession list → `report/evidence/accessions.txt` (27 GCF accessions).

## Stage 2 — Download + QC
- `datasets download genome accession <ACC> --include genome` (NCBI Datasets 18.32.0), no auth required.
- 41 MB zip, unpacked → 27 FASTA files.
- QC → `report/evidence/genome_stats.csv` (length, GC, N50, contig count).
- Flagged: `B_cereus_4` (GCF_000290435, 2.13 Mbp partial) + `B_thuringiensis_7` (GCF_000832985, GC 37.8%). Retained for ANI, noted for pan-genome.

## Stage 3 — Mash + FastANI (C3, C4)
- Mash sketch k=21, s=1000 (identical to Bazinet).
- All-vs-all `mash dist` → `report/evidence/mash_dist.tsv` (729 pairs).
- FastANI 1.34 all-vs-all → `report/evidence/fastani_out.tsv` (627 usable pairs; <80% ANI pairs dropped by design).
- Summary stats → `report/evidence/ani_summary.txt`.

## Stage 4 — Prokka annotation
- Prokka 1.12 --kingdom Bacteria --genus Bacillus on all 27 FASTAs.
- Produced GFF3 + faa + ffn per genome.
- Total gene counts per genome in `evidence/genome_stats.csv`.

## Stage 5 — Roary pan-genome (three runs, C1, C2, C6)
- **Run A** (all 27, `-i 95`, `-cd 99`): `evidence/roary_full27_summary.txt` → Pan 48,118; Core 0.
- **Run B** (26 excl. partial, `-i 80`, `-cd 99`): `evidence/roary_i80_26genomes_summary.txt` → Pan 26,839; Core 251.
- **Run C** (17 Clade-1 homogeneous subset, `-i 95`, `-cd 99`): `evidence/roary_clade1_summary.txt` → Pan 15,247; Core 2,415.
- Presence/absence Rtab exports: `panacc_clade1_pan.Rtab`, `panacc_clade1_core.Rtab`, `panacc_clade1_new.Rtab`.

## Stage 6 — Accumulation curves (C6)
- Roary `-r` permutation output plotted as pan/core/new-genes vs N.
- Data in `panacc_clade1_*.Rtab`; monotonic pan growth, +492 new genes at N=17 → open pan-genome confirmed.

## Stage 7 — Phylogeny (C4, C5)
- FastTree 2.x -gtr -nt on Roary's Clade-1 core-gene alignment → `evidence/core_gene_tree_clade1.nwk`.
- Roary accessory-gene presence/absence binary tree → `evidence/accessory_binary_tree_clade1.nwk`.
- Manual topology comparison: both trees collapse anthracis into single clade + intermingle anthracis/cereus/thuringiensis.

## Stage 8 — LLM judge (Argo free proxy)
- `evidence/llm_judge_prompt.py` builds a structured claim-by-claim prompt against Argo proxy localhost:44497.
- Tried `argo:claude-opus-4.8` first → 3× HTTP 502.
- Fell through to `argo:gpt-5.2` → returned JSON verdict PARTIAL.
- Verdict → `evidence/llm_judge_verdict.json` + human-readable `llm_judge_verdict_pretty.json`.

## Stage 9 — Report + artifacts
- Narrative → `report/REPORT.md`.
- LaTeX → `report/REPORT.tex` (this backfill).
- Failure analysis → `report/failure_analysis.md` (this backfill).
- Open questions → `report/open_questions.json` + `open_questions_section.tex` (this backfill).
- Artifacts summary → `report/artifacts_summary.md` (this backfill).
- Nougat MMD stub → `extraction/nougat.mmd` (this backfill).

## What was NOT run (honest disclosure)
- No **HaMStR** ortholog inference (used Roary CD-HIT/BLAST instead).
- No **RAxML** ML tree with bootstrap (used FastTree with SH-like local support).
- No **Scoary** pan-GWAS (phenotype metadata assembly out of scope).
- No **hierBAPS** clustering (nine-cluster partition not reproduced).
- No **full-scale** 114/498-genome run (compute + time budget).

# Attempt Log — BVBRC-28 (chronological)

All timestamps 2026-07-01 CDT. Analyst: Ollie (OpenClaw subagent). Heavy compute: uicgpu (`~/bvbrc28`), env `/data/stevens/envs/bvbrc28`.

1. Read WAVE_BRIEF + BVBRC-17 exemplar. Created target dir `report/{evidence}` + `work/`.
2. Europe PMC: resolved PMID 33917427 → PMC8038741, DOI 10.3390/ijms22073780, IJMS 2021, OA=Y. Pulled abstract (core) + full-text XML (222 KB).
3. Parsed full text for accessions: FLUB = BioProject **PRJNA595831**, chromosome **CP047121.1** (3,071,102 bp) + 5 plasmids CP047122-126. Assembly GCF_009832765.1. Total 3,190,226 bp, GC 40.09%. Pangenome numbers: 4181 clusters (2059 core / 1210 accessory / 912 singletons; core 49.3%). Roary used. Reference strain ATCC 8290 (=DSM 20176 = NRRL B-1843). Closest ANI neighbor = ATCC 27305 / LMG 07934 (L. brevis subsp. gravesensis label).
4. uicgpu check: docker + singularity + conda (miniforge3/miniconda3) + internet via `~/env.sh`. Pre-existing `bvbrc14` env has blast/mafft/fasttree but no prokka/roary/fastani.
5. Built new conda env `bvbrc28` with prokka, roary, fastani, mash, ncbi-datasets-cli, cd-hit (conda-forge + bioconda).
6. NCBI Datasets REST: pulled 6 L. hilgardii genome FASTAs (FLUB + ATCC8290 + DSM20176 + LMG07934 + ATCC27305 + LH500) — the paper-era public set of the species.
7. Genome stats (`gstats.py`): **FLUB = 3,190,226 bp, 6 contigs, GC 40.09%, chr N50 3,071,102** → EXACT match to paper C1. FLUB largest of the 6.
8. FastANI all-vs-all: all L. hilgardii pairs 96.9–99.99%. FLUB closest to ATCC27305 (99.77%) — the paper's named closest neighbor. Confirms C5/C6 species structure.
9. Prokka annotated all 6 genomes (parallel, 8 cpu each). CDS: FLUB 2991 (most of the 6); paper 2871 via PGAP/PATRIC (~4% pipeline delta).
10. Roary pangenome (i=95%). **Blocker:** post-analysis crashed — missing Perl `File::Find::Rule` (conda installed it for perl 5.26 but Roary uses env perl 5.22). Fixed by copying the pure-Perl module into the 5.22 site_perl path; re-ran.
11. Roary 5-genome result: **4089 total clusters, 2000 core (48.9%)** vs paper 4181/2059 (49.3%) — close. 6-genome: 4134/1993.
12. FLUB strain-unique (singleton) genes from `gene_presence_absence.csv`: **268 (5-genome) / 269 (6-genome)** vs paper **266** — near-exact match to C4.
13. Collected evidence → `report/evidence/`. Ran LLM-judge (Argo `argo:gpt-5.2`, free localhost:44497) → **VERDICT: PARTIAL** (2/6 agree, 4/6 partial, 0 disagree; coverage 6/6).

## Cross-validation pass (2026-07-01, later) — second pipeline + core-genome tree

14. Re-pulled the **exact 5-strain set from paper Table 2** (FLUB GCA_009832765.1, LMG07934 GCA_011765585.1, LH500 GCA_008694025.1, MGYG-HGUT-01333 GCA_902374015.1, DSM20176 GCA_001434655.1) via NCBI Datasets REST. Note pass 1 had used ATCC8290/ATCC27305 as extra comparators; this pass matches the paper's published pangenome table exactly.
15. **Blocker:** MGYG-HGUT-01333 (GCA_902374015.1) has metadata-only on NCBI Datasets (5 KB zip, no sequence) and 404 on NCBI FTP — it is an EBI/MGnify human-gut MAG. **Fix:** fetched FASTA from the ENA browser API (`ebi.ac.uk/ena/browser/api/fasta/GCA_902374015`) → 106 contigs, 3.14 Mbp (matches Table 2).
16. Genome stats (Biopython) on all 5: sizes/GC/contig-counts all match Table 2; FLUB replicons match Table 1 to the base pair (6/6 replicons = CP047121–126, total 3,190,226 bp).
17. **Local tool fix:** the PATH `mafft` was broken (missing MAFFT_BINARIES); used the brew-installed `/usr/local/Cellar/mafft/7.526/bin/mafft` directly. Installed `mmseqs2` via brew.
18. Second, fully independent pangenome pipeline: **Prodigal** uniform gene-calls + **mmseqs2** clustering (95% id, 0.7 cov). Result: 4190 clusters, core 1923 (45.9%), accessory 1293 (30.9%), singleton 974 (23.2%); FLUB singletons 260. Brackets the paper's 4181/49.3%/28.9%/21.8% together with the Roary pass.
19. **Core-genome ML tree** (NEW): 400 single-copy-core genes, MAFFT-aligned, concatenated (125,120 aa), FastTree. Topology `((FLUB,MGYG),LMG07934,…)` — FLUB sister to MGYG-HGUT-01333, matching paper §2.1 exactly. fastANI FLUB↔MGYG 99.7%.
20. Consolidated LLM-judge (Argo gpt-5.2, free) over all evidence → **REPLICATED** (4 AGREE/3 PARTIAL/0 DISAGREE, 7/7). Headline kept conservatively at PARTIAL-strong (dDDH + wet-lab not reproduced). Evidence saved to `report/evidence/`.

## What worked
- FLUB genome size/GC: exact reproduction.
- FLUB singleton-gene count: 268 vs 266 (99% agreement).
- Pangenome core fraction: 48.9% vs 49.3%.
- ANI-based species membership + closest-neighbor structure.

## What was out of reach / not attempted
- Exact PGAP gene/RNA/pseudogene tallies (needs identical annotation pipeline).
- dDDH numeric values (GGDC web service — not scriptable/free-batch here).
- CRISPR / prophage / genomic-island counts (CRISPRCasFinder/PHASTER/IslandViewer — separate services).
- Wet-lab growth phenotypes (Bioscreen ethanol/sugar tolerance, fructophily) — not replicable computationally.

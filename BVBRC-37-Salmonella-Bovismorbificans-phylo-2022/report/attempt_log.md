# Attempt Log — BVBRC-37 (2026-07-01, night wave)

1. **Dedup:** `ls REPLICATE-PROJECT | grep -iE bovismorbificans|salmonella` → only `BVBRC-31-Salmonella-AMR-Mexico-2021` (different paper). No conflict. Created target dir.
2. **Read** WAVE_BRIEF + BVBRC-17 exemplar REPORT.md (structure model: claims table, method, results-vs-paper, verdict).
3. **Located paper** via S2 API: PMC9228720, DOI 10.3390/microorganisms10061199. MDPI/PMC PDF endpoints returned HTML (bot block) — used `web_fetch` on the PMC HTML full text instead. Extracted abstract, methods, Table 1 (per-strain source/country/year/ST/BioSample/accession), BioProject **PRJNA378379**.
4. **Identified dataset:** queried NCBI Datasets REST for PRJNA378379 → 425 genomes (broad GenomeTrakr). Filtered organism == Bovismorbificans → **82 genomes**. BioSample IDs match paper Table 1 (e.g. SAMN12657228 = N14_0646). Confirmed = paper's genomes.
5. **uicgpu setup:** no tools on PATH initially; found existing micromamba env `amr` with SeqSero2 1.3.2, mlst 2.35, AMRFinderPlus 3.12.8, datasets 18.32, BLAST. Installed `mash`+`skani` into it. Proxy internet via `~/env.sh` (200 OK).
6. **Downloaded** all 82 assemblies (datasets CLI, 117 MB zip, validated 82/82), flattened to `genomes/fna/*.fna`.
7. **MLST** — first run 0 rows: mlst couldn't find `blastn` (needs env bin on PATH; also needed env `perl` due to shebang). Fixed with `export PATH=$env/bin:$PATH` + `perl mlst`. Result: ST142=49, ST377=14, ST1499=11, ST2640=5, ST150=2, ST8700=1.
8. **mash** sketch + all-vs-all distance (82×82 = 6724 rows).
9. **SeqSero2** on all 82 (kmer mode, `-t 4` assembly) → 82/82 = Bovismorbificans, 8:r:1,5.
10. **Clustering:** scipy average-linkage on mash matrix, 2-cluster cut → Cluster1 = {2×ST150}, Cluster2 = {80: the four backbone STs}. Reproduces the two-polyphyletic-cluster claim. Dendrogram rendered.
11. **Source metadata:** NCBI BioSample per accession → 70 clinical, 8 food, + animal/env/feed; CH/CA/US. Clinical+food co-occur within STs.
12. **AMRFinderPlus** — first run failed: hard-coded `/opt/conda` DB path unwritable, no DB. Fixed: `amrfinder_update -d ~/bvbrc37/amrdb` (got 2024-07-22.1), reran with `-d`. 82/82, 1203 hits (799 VIRULENCE, 199 AMR, 205 STRESS). mdsA/mdsB universal; acquired AMR sparse; spvD in 56/82.
13. **LLM judge:** argo:claude-opus-4.8 → 502 (known proxy bug) → fell back to **free** argo:gpt-5.2. Verdict REPLICATED, per-claim C1-C5 reproduced, C6 partial, coverage ~0.92.
14. Wrote report package. All raw outputs copied to `report/evidence/`. Nothing overwritten outside target dir.

## What worked
- Existing `amr` micromamba env saved a full toolchain install.
- BioSample IDs gave an unambiguous link between NCBI assemblies and paper Table 1.
- mash distance is a fast, independent proxy for the core-genome phylogeny and gives the identical 2-cluster topology.

## What was out of reach (honest)
- Paper's bespoke 2690-locus core-genome schema (built from 150 complete genomes), the k-mer-binning >260-strain extended survey, and the digital DNA microarray/tiling-array near-neighbor mining were not reconstructed. Clustering used mash as a proxy.
- Detailed prophage/plasmid cataloguing not done (AMRFinder gives feature classes, not full mobile-element maps).

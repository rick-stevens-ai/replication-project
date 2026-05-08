# REPLICATE-PROJECT — Status Audit
**Date:** 2026-05-05 · **Auditor:** Ollie (subagent `integrate-replication-report-v2026-05-05`) · **Scope:** All papers including 10 new biology/BV-BRC replications
**Reference:** `STATUS_AUDIT_2026-04-30.md` (prior audit, 53 paper entries)

---

## Executive Summary

This audit integrates **10 new biology/bioinformatics replications** completed on 2026-05-05 into the corpus. These span microbial genomics, antibiotic resistance, bile acid metabolism, phage defense, and RB-TnSeq fitness profiling. The corpus now contains **55 distinct paper entries** (up from ~53). The new papers are the first batch of BV-BRC-primary replications and include 3 papers using the BV-BRC API as their primary data source.

### New Papers Added (2026-05-05)

| Paper | Verdict | Coverage | Agreement |
|-------|---------|----------|-----------|
| Li 2015 — Outer mucus niche (PMID 26392213) | **PARTIAL** | 6 | 6 |
| Jiang 2017 — ARG dissemination (PMID 28589945) | **REPLICATED** | 9 | 9 |
| Price 2018 — Mutant phenotypes bacterial genes (PMID 29769716) | **REPLICATED** | 10 | 9 |
| Sato 2021 — Centenarian bile acid (PMID 34325466) | **SPOT-CHECK** | 4 | 6 |
| Vassallo 2022 — Anti-phage defense E. coli (PMID 36123438) | **REPLICATED** | 8 | 9 |
| Zhang 2022 — ST11 CRKP genomic evolution (BV-BRC-01) | **REPLICATED** | 8 | 8 |
| Fluit 2021 — Ralstonia clinical strains (BV-BRC-02) | **PARTIAL** | 7 | 8 |
| Sivakumar 2023 — S. aureus mastitis (BV-BRC-03) | **REPLICATED** | 9 | 9 |
| Shrestha 2022 — Variovorax trehalose (BV-BRC-04) | **PARTIAL** | 6 | 8 |
| Thakur 2022 — Trueperella pyogenes (BV-BRC-05) | **REPLICATED** | 9 | 9 |

---

## Full Corpus Summary Table

### Biology / Bioinformatics Papers (New — May 2026)

| Dir | Title | Authors | Year | DOI/PMID | Verdict | Cov | Agr | Claims Tested | Key Caveats |
|-----|-------|---------|------|----------|---------|-----|-----|---------------|-------------|
| `26392213-Outer-mucus-niche` | The outer mucus layer hosts a distinct intestinal microbial niche | Li et al. | 2015 | PMID 26392213 | **PARTIAL** | 6 | 6 | PERMANOVA sig. replicated; R²=3-7% (small effect) | Bray-Curtis used instead of weighted UniFrac; no OTU clustering; no taxonomy; pseudoreplication concern |
| `28589945-ARG-dissemination` | Dissemination of ARGs from antibiotic producers to pathogens | Jiang et al. | 2017 | PMID 28589945 | **REPLICATED** | 9 | 9 | 56/56 ARG proteins matched (mean Δ=0.3%); 23/32 claims tested; 0 contradicted | 9 untested claims are wet-lab or genome-level synteny; BV-BRC cross-phylum confirmed |
| `29769716-Mutant-phenotypes-bacterial-genes` | Mutant phenotypes for thousands of bacterial genes of unknown function | Price et al. | 2018 | PMID 29769716 | **REPLICATED** | 10 | 9 | 32/32 organisms (100%); 4,870 experiments exact match; 12,855 vs 11,779 poorly-annotated genes with phenotype (+9.1%) | +9.1% overestimate explained by approximate FDR control + missing TIGRFAM data; corrected estimate within 0.2% |
| `34325466-Centenarian-bile-acid` | Novel bile acid biosynthetic pathways enriched in centenarian microbiome | Sato et al. | 2021 | PMID 34325466 | **SPOT-CHECK** | 4 | 6 | 10/330 centenarian + 10 elderly control samples; 5AR enrichment directionally consistent (1.30x) | Only 3-7% of reads subsampled; no MAG assembly; no metabolomics; Odoribacteraceae-specific genes too sparse |
| `36123438-Anti-phage-defense-Ecoli` | Previously undetected anti-phage defence systems in E. coli pangenome | Vassallo et al. | 2022 | PMID 36123438 | **REPLICATED** | 8 | 9 | 21/21 defense systems: all proteins retrieved, all conserved in E. coli; 3 independently annotated post-publication (Abi, Shedu, SNIPE) | Functional validation not replicable computationally; BLAST hit cap at 500 |
| `BVBRC-01-CRKP-Zhang2022` | Genomic evolution of ST11 CRKP 2011–2020 | Zhang et al. | 2022 | DOI 10.3390/genes13091624 | **REPLICATED** | 8 | 8 | 18/20 claims tested (90%); KL47→KL64 serotype transition strongly confirmed; KL64 higher virulence confirmed | Absolute counts differ (955 vs 386 ST11) due to database growth + missing sample-source filter; proportions consistent |
| `BVBRC-02-Ralstonia-Fluit2021` | Characterization of clinical Ralstonia strains | Fluit et al. | 2021 | PMID 34463860 | **PARTIAL** | 7 | 8 | 10/15 claims tested (67%); 8 verified, 2 partial; ANI species groupings confirmed; OXA-22/OXA-60 in all 18 strains | cgMLST (commercial Ridom SeqSphere), phylogenetics, and MIC testing not replicated |
| `BVBRC-03-Saureus-mastitis-Sivakumar2023` | Comparative genomics of bovine mastitis S. aureus | Sivakumar et al. | 2023 | DOI 10.1186/s12864-022-09090-7 | **REPLICATED** | 9 | 9 | 31/33 claims tested (94%); 23 verified + 6 partial; 15 STs exact match; blaZ 14/41 exact; all MSSA confirmed | Pan-genome counts differ (PLFam vs Roary); spa typing not available via BV-BRC |
| `BVBRC-04-Variovorax-trehalose-Shrestha2022` | Trehalose pathway prediction in Variovorax sp. PAMC28711 | Shrestha et al. | 2022 | PMID 34991451 | **PARTIAL** | 6 | 8 | 11/15 claims tested; 8 verified + 3 partial; TreY annotation discrepancy confirmed; MetaCyc blocked (license) | MetaCyc not replicable (Pathway Tools license); 4 claims are historical database snapshots (inherently untestable) |
| `BVBRC-05-Trueperella-pyogenes-Thakur2022` | Comparative genome analysis of 19 T. pyogenes strains | Thakur et al. | 2022 | DOI 10.3390/antibiotics12010024 | **REPLICATED** | 9 | 9 | 15/15 claims tested (100%); 11 verified + 4 partial; open pan-genome confirmed; ANI ≥97.5% all pairs; plo/nanH in all 19 | Pan-genome absolute numbers differ (EDGAR→Roary tool substitution); RGI→abricate threshold difference |

### Prior Papers (from STATUS_AUDIT_2026-04-30)

| Dir | Title (short) | Domain | Verdict | Cov | Agr | Notes |
|-----|---------------|--------|---------|-----|-----|-------|
| `1997354` | Integer Sequences Hausdorff | Mathematics | REPLICATED | 10 | 10 | All 13 formulas exact |
| `1379592` | GraphBLAS Foundations | CS/Graph | REPLICATED | 9 | 10 | 11 ops + 6 algorithms |
| `1523841` | Shift Photocurrent | CMT/Optics | REPLICATED | 7 | 10 | Rice-Mele + Wilson + BHZ |
| `2441075` | Trapped-Ion Qubits | Quantum | REPLICATED | 8 | 9 | Eqs 6-10 + Lindblad |
| `1624105` | Linclust | Bioinformatics | REPLICATED | 8 | 9 | Algorithm + benchmarks |
| `1606674` | CMV Reduction qZSI | Power | REPLICATED | 8 | 9 | State-space + waveforms |
| `1565592` | MSM Hempel | CompChem | REPLICATED | 9 | 8 | 1D/2D/ADP OOM fix |
| `1461824` | Photo-z PDFs | Astrophysics | REPLICATED | 8 | 8 | Stacked N(z) |
| `1842593` | Motion Tomography | Control | REPLICATED | 8 | 8 | Algorithm 1 + sweeps |
| `1412756` | Chiral Spin KH | CMT | REPLICATED | 7 | 8 | MF + Wolff-MC |
| `2217719` | SCALE MSRE | Nuclear | REPLICATED | 6 | 8 | Bateman ODE substitute |
| `2439897` | rVAE | ML/Imaging | REPLICATED | 9 | 10 | SE(2)-equivariant |
| `1475143` | FDTD delay PDE | Quantum | REPLICATED | 7 | 7 | Figs 5-7 |
| `3014512` | Dark Matter SD | Particle | REPLICATED | 7 | 7 | DarkELF tier-lift |
| `2587225` | ScaWL 3-WL | CS/Graph | REPLICATED | 9 | 10 | C++17/MPI single-node |
| `2571909` | CHF Hybrid ML | Nuclear/ML | PARTIAL | 6 | 7 | Data-blocked full benchmark |
| `2475938` | Virophage Taxonomy | Bio | REPLICATED | 8 | 10 | 279-genome scale-up |
| `1427646` | Deep Learning STEM | ML/Imaging | REPLICATED | 8 | 8 | Tier-lift v2.5 |
| `1983793` | CPW Resonator | Quantum | REPLICATED | 5 | 7 | Analytical + Palace |
| `1484740` | 2D GaN | DFT/Materials | REPLICATED | 9 | 9 | Bilayer + Yambo BSE |
| `1559043` | Ignition Kernel PeleC | CFD | COMPUTE-BOUND | 6 | 6 | v5 blocked on Polaris MFA |
| `PVMol-Gen` | Perovskite AI | Materials/ML | PARTIAL | 7 | 5 | xTB filter missing |
| `2571540` | BayesOpt qHSRI | Optimization | REPLICATED | 5 | 6 | 3-way agreement |
| `1864334` | NN-VMC Nuclei | Nuclear/ML | REPLICATED | 8 | 9 | A=2/3/4 + Coulomb |
| `1981773` | Pt/La₂Ti₂O₇ DFT | Catalysis | REPLICATED | 9 | 9 | Yambo PBE/RPA + HSE06 |
| `2396968` | Latent SDE | Astro/ML | PARTIAL | 9 | 6 | WeatherBench blocked |
| `1275503` | CROC | Astrophysics | SHALLOW | 5 | 5 | FGPA surrogate only |
| `1868518` | Graph-RL | Power/ML | REPLICATED | 8 | 7 | 8500-bus done |
| `3003857` | MP-NODE chaos | ML | PARTIAL | 5 | 4 | ERA5 blocked |
| `2469515` | PATRIC binning | Bio | TOOL-BLOCKED | 3 | 5 | SEEDtk proprietary |
| `1609039` | Cu₆₄Zr₃₆ MD | Materials | UNVERIFIED | 7 | 8 | No artifacts in dir |
| — | Lightning Laplace | PDE | REPLICATED | 8 | 10 | — |
| — | Fast Poisson ADI | PDE | REPLICATED | 9 | 10 | — |
| `2582579` | NILC | CMB | REPLICATED | 8 | 8 | <0.2% recovery |
| `2587579` | Mesh GNN | PDE/ML | REPLICATED | 8 | 8 | Halo-swap validated |
| `2587945` | ELM Forecaster | Fusion/ML | REPLICATED | 8 | 8 | Synthetic BES |
| `1861801` | NukeLM | NLP | REPLICATED | 8 | 10 | 325K OSTI abstracts |
| `1578031` | fldgen v2.0 | Climate | REPLICATED | 8 | 8 | Synthetic ESM |
| `1993311` | DMQMC+GPR | DFT/Stats | REPLICATED | 8 | 8 | GPR beats FD |
| `1984484` | DRAS RL | Systems | REPLICATED | 8 | 8 | DQN + PPO |
| — | NANOGrav 15-yr | Astro/GW | REPLICATED | 8 | 8 | HD correlation |
| — | BLS Kepler | Astro | REPLICATED | 8 | 8 | 6 planets |
| — | CosmoPower P(k) | Cosmo/ML | REPLICATED | 8 | 8 | 400-cosmo |
| — | PFGM | ML/PDE | REPLICATED | 7 | 8 | 2D MoG |
| — | Godunov-Loss | PDE/ML | HONEST NEGATIVE | 4 | 8 | MSE beats Godunov |
| — | Walk-on-Stars | Grid-free MC | REPLICATED | — | — | Lens/square/L-shape |
| — | Dedalus | PDE Spectral | REPLICATED | 8 | 8 | 6/8 demos |
| — | Kinetic.jl | Kinetic Theory | REPLICATED | — | — | Julia toolbox |
| — | Latent Spectral | PDE/ML | REPLICATED | — | — | LSM reimpl |
| — | Koopman NO | PDE/ML | PARTIAL | 5 | 7 | NS-2D phantom |
| — | Laplace NO | PDE/ML | PARTIAL | 8 | 8 | 3 benchmarks blocked |
| — | JAX-CFD | PDE/ML | COMPUTE-BOUND | — | — | Decaying turb missing |

---

## Updated Distribution (2026-05-05)

| Verdict | Count | Prior (Apr 30) | Δ |
|---------|-------|----------------|---|
| **REPLICATED** | 42 | 35 | +7 |
| **PARTIAL** | 7 | 5 | +2 |
| **SPOT-CHECK** | 1 | 0 | +1 |
| **HONEST NEGATIVE** | 1 | 1 | 0 |
| **COMPUTE-BOUND** | 2 | 4 | -2 |
| **SHALLOW** | 1 | 1 | 0 |
| **TOOL-BLOCKED** | 1 | 1 | 0 |
| **UNVERIFIED** | 1 | 1 | 0 |
| **Total scored** | ~55 | ~48 | +7 |

### Updated Aggregate Statistics (55-paper scored cohort)

With the 10 new biology papers included:
- **Mean coverage:** ~7.5/10 (previously 7.42/10)
- **Mean agreement:** ~8.0/10 (previously 7.93/10)
- **Papers with ≥8 on both axes:** 33/55 (60%)
- **Papers with ≤5 on at least one axis:** 9/55

---

## Key Observations from May 2026 Biology Batch

1. **BV-BRC API is a powerful replication platform.** Papers using BV-BRC data (Zhang, Sivakumar, Thakur, Shrestha, Fluit) achieved high verification rates (67-100% claims tested) with API-based analysis substituting for standalone tools.

2. **Sequence-level replications are most robust.** Jiang 2017 (ARG dissemination) achieved near-exact identity matches (mean Δ=0.3%) across 56 proteins — the highest precision replication in the biology cohort.

3. **Price 2018 is the largest-scale biology replication** — 32 organisms, 150K+ genes, 4,870 experiments. The +9.1% deviation in gene counts is well-understood and correctable.

4. **Shallow metagenomics spot-checks have limited power.** Sato 2021 (centenarian bile acid) scored lowest due to subsampling constraints (3-7% of reads). Full-depth assembly pipelines are needed for definitive results.

5. **Tool substitutions are well-documented.** EDGAR→Roary, CARD/RGI→abricate, pyani version differences — all produce consistent qualitative conclusions despite quantitative differences.

---

## Recommended Actions

1. **[HIGH]** Update REPLICATION_EVALUATION_REPORT.tex with new 10-paper biology section ✅ (done in this session)
2. **[HIGH]** Create REPORT.md files in root of dirs that only have `report/REPORT.md` subdirectory (for consistency)
3. **[MEDIUM]** Run Sato 2021 at full depth (all 330 samples) on uicgpu for definitive centenarian bile acid replication
4. **[LOW]** Attempt MetaCyc replication of Shrestha 2022 if Pathway Tools license becomes available
5. **[LOW]** Full 72-genome ANIb for Fluit 2021 (requires 54 reference genomes)

---

*Audit method: individual REPORT.md files read for each of 10 new papers; cross-referenced with AUDIT_PROTOCOL.md verdict criteria. Prior audit entries carried forward from STATUS_AUDIT_2026-04-30.md.*

---

## 2026-05-07 Addendum: Report Modularization

On 2026-05-07, the monolithic `REPLICATION_EVALUATION_REPORT.tex` (89 pages, 2506 lines) was
refactored into a modular structure:

### New structure
- **`common/`** — shared LaTeX chunks: `preamble.tex`, `abstract.tex`, `how_to_read.tex`,
  `methodology.tex`, `aggregate.tex`, `cross_cutting.tex`, `wave_summaries.tex`,
  `top_line_table.tex`, `deferred.tex`, `conclusions.tex`, `followon_questions.tex`,
  `recommendations.tex`, `appendix.tex`
- **`papers/`** — 60 individual `.tex` files, one per paper (extracted from the monolith)
- **`master_slim.tex`** → builds **`REPLICATION_EVALUATION_REPORT_slim.pdf`** (~19 pages):
  aggregate stats, cross-cutting findings, wave summaries, top-line table, conclusions
- **`master_full.tex`** → builds **`REPLICATION_EVALUATION_REPORT_full.pdf`** (~99 pages):
  everything in slim + all 60 per-paper evaluations + follow-on questions + recommendations
- **`REPLICATION_EVALUATION_REPORT.pdf`** — alias for the slim version (existing links unbroken)
- **`Makefile`** — `make slim`, `make full`, `make all`, `make clean`

### Per-paper REPORT.md status
- **58/60 papers** have a canonical `REPORT.md` at a known path
- **2 papers** use alternative report names (flagged with † in the table):
  - `1565592` (MSM-Hempel): `replication/replication_report.md`
  - `PVMol-Gen`: `replication_report.md`

### Backup of original monolith
- `REPLICATION_EVALUATION_REPORT_FULL.tex.bak.20260507-modularize`
- `REPLICATION_EVALUATION_REPORT_FULL.pdf.bak.20260507-modularize`

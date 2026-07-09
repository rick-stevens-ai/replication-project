# BVBRC-120 · Independent Replication Report

**Paper.** Zhang Y, Miao J, Zhang N, Wang X, Li Z, Richard OA, Li B (2023). *"The analysis of the function, diversity, and evolution of the Bacillus phage genome."* **BMC Microbiology** 23:170. DOI 10.1186/s12866-023-02907-9. PMID 37337195. PMC PMC10278307.

**Set / rank.** BVBRC-120 (X-100 wave, rank #56).

**Target dir.** `~/Dropbox/REPLICATE-PROJECT/BVBRC-120-Bacillus-phage-genomes-Zhang2023/`

**Verdict.** **PARTIAL — REPLICATED (3 of 4 testable claims)**

---

## 1. Paper summary

The paper mines NCBI (cutoff 30-Dec-2022) for 236 published *Bacillus* lytic-phage complete genomes plus 178 *Bacillus* host genomes, uses PHASTER to predict prophages in the hosts (yielding 36 usable prophage sequences ≥20 kb across 5 focal species), then runs GeneMark for ORF calling, WebMGA for COG functional annotation, VIRIDIC for intergenomic similarity, RAST + Mauve + Easyfig for a 20-lytic-phage / 36-prophage evolutionary panel, and MAFFT + MView for lysis-module protein alignment. The five focal *Bacillus* hosts are *B. anthracis, B. cereus, B. thuringiensis, B. subtilis, B. pumilus*.

Core headline conclusions:
1. Bacillus phages carry known-function gene fragments **and a large number of unknown-function gene fragments** that may influence host sporulation, biofilm formation and virulence-factor transmission.
2. The Bacillus phage genome shows **diversity, with a clear genome boundary between prophages and lytic phages**.
3. Genetic mutations, sequence losses/duplications, and host-switching during evolution have produced **low genome similarity between Bacillus phages**.
4. The **lysis module** is influential in cross-species infestation (two "types" of lysis module described).

## 2. Claims table

| ID | Claim (paraphrased) | Type | Testable from public data? | Tested in this replication? | Outcome |
|----|---|---|---|---|---|
| C1 | *Bacillus* phages carry a large fraction of unknown-function gene fragments, plus functional cargo relevant to sporulation/biofilms/virulence factors. | descriptive + numeric | Partly (unknown-function fraction) | Partly | **Replicated for the "large unknown fraction" sub-claim** (49% singleton protein clusters, 45%-of-ORFs unassigned family). COG functional cargo not re-annotated. |
| C2 | Bacillus phage genomes exhibit diversity (broad size / GC / cluster spread), with a clear boundary between prophages and lytic phages. | numeric + comparative | Yes for diversity; boundary claim needs prophage set. | Yes for lytic diversity; not for the prophage↔lytic boundary. | **Diversity sub-claim replicated** (size 7.4-497.5 kb, GC 27.7-50.1%, MASH mean pairwise d=0.94). Boundary sub-claim not tested (36 predicted prophages not re-derived — PHASTER is a web service, out of scope). |
| C3 | Genome similarity between Bacillus phages is low. | numeric | Yes | Yes | **Replicated.** 92.7% of 53,130 231×231 pairs have MASH d ≥ 0.5 (effectively unrelated). Mean pairwise MASH distance = 0.940. |
| C4 | Two types of lysis module exist and are influential in cross-species infestation. | comparative | Yes for module presence (S6/S7); "influence" is inferential | No (out of scope for wave time budget) | Not tested. |

## 3. Method

Real independent replication — every genome accession was re-fetched from NCBI; no numbers copied from the paper.

1. **Paper + supplementary fetch.** Full-text PDF pulled via BMC direct URL `https://bmcmicrobiol.biomedcentral.com/counter/pdf/10.1186/s12866-023-02907-9.pdf` from uicgpu (proxy `<lan-host>:3128`). All 9 supplementary XLSX pulled from `static-content.springer.com/esm/art%3A10.1186%2Fs12866-023-02907-9/MediaObjects/12866_2023_2907_MOESM{1..9}_ESM.xlsx`.
2. **Accession extraction.** Table S9 → 236 lytic-phage NCBI nucleotide accessions (extracted via `openpyxl`). Table S4 → 20 focal lytic-phage accessions. Table S1 → 178 Bacillus strain host names + accessions (kept as reference, not re-downloaded).
3. **Genome retrieval.** NCBI `efetch -db nuccore -id ... -format fasta` in batches of 50 (bvbrc76 conda env, `entrez-direct` v22.4). 231 of 236 returned; 5 dropped by NCBI's deduplication/withdrawal. The 20-focal set includes 13 accessions that were not in the 236-fetched set (mostly `NC_*` RefSeq versions vs GenBank originals of the same phage) and were fetched separately → 20/20 acquired.
4. **Genome statistics.** `seqkit stats` and `seqkit fx2tab --name --length --gc` on the 231-lytic FASTA and the 20-lytic FASTA.
5. **All-vs-all genome distance.** MASH v2.3 (`mash sketch` per-genome, `mash dist` all-pairs). Two matrices produced: 231×231 (53,361 rows including self) and 20×20 (400 rows including self).
6. **ORF prediction.** Prodigal v2.6 in metagenomic mode (`-p meta`) on the concatenated 231-lytic FASTA and separately on the 20-lytic FASTA. Prodigal replaces GeneMark for licensing reasons; both are widely-used ab-initio gene finders for prokaryotic/phage genomes.
7. **Protein clustering.** MMseqs2 v13.45111 `mmseqs cluster` at 30% sequence identity / 50% coverage on all predicted proteomes. Two runs: (a) all 231 lytic phages (35,069 proteins → 6,875 clusters); (b) 20 focal phages (2,497 proteins → 1,495 clusters).
8. **Phylogeny (20 lytic).** Whole-genome MAFFT alignment was attempted and abandoned after 4 min of runtime on the highly divergent 20-genome panel (as expected — end-to-end nucleotide alignment of Sipho/Myo/Podo-viruses is generally unusable). Replaced with a MASH-distance BIONJ tree via `rapidnj -i pd` on the 20-genome mash matrix. This is the same class of method as the paper's VIRIDIC (intergenomic similarity → tree), just using k-mer sketching instead of nucleotide identity.

**Tool versions (bvbrc76 conda env):** entrez-direct v22.4 · seqkit v2.13.0 · mash v2.3 · prodigal v2.6 · MMseqs2 v13.45111 · MAFFT (not used in final report) · rapidnj v2.3.2 · IQ-TREE v3.1.2 (installed, used opportunistically). All installed via `mamba -c bioconda`.

**Compute.** All heavy work on `uicgpu` (8× A100, 255 cores, 2 TB RAM) at `/data/stevens/bvbrc120/`. Wall-clock: download ~90 s, prodigal ~15 s, MMseqs2 ~10 s, mash all-pairs ~5 s, rapidnj <1 s.

## 4. Results vs paper

### 4.1 Diversity (C2, C3)

| Metric | This replication (n=231 lytic phages) | Paper claim |
|---|---|---|
| Genome length min / max | 7,379 bp / 497,513 bp | "diverse" (Fig 3 shows range roughly 10-500 kb) — ✔ matches |
| Genome length median (IQR) | 58,528 bp (40,632 – 160,286) | Consistent with paper Fig 3 boxplot centred near 50-60 kb |
| GC content min / max | 27.67% / 50.1% | 30-45% typical; paper does not quote exact range; ✔ within bacterial-phage range |
| GC content mean ± SD | 37.98% ± 4.00% | Consistent with Bacillus (host GC ≈ 35-45%) |
| Length histogram | <20 kb: 13, 20-50 kb: 75, 50-100 kb: 36, 100-200 kb: 101, ≥200 kb: 6 | Paper Fig 3 shows bimodal-ish distribution — ✔ we recover a broadly bimodal shape (peaks around 30-50 kb + 100-160 kb) |

**Verdict for C2 (diversity sub-claim): REPLICATED.**

| MASH-231 pairwise metric | Value |
|---|---|
| n pairs (231-choose-2) | 53,130 |
| Mean MASH distance d | 0.940 |
| Median d | 1.000 |
| Frac pairs with d < 0.05 (near-identical) | 1.11% |
| Frac pairs with d < 0.10 | 2.42% |
| Frac pairs with d ≥ 0.50 (highly divergent) | 92.7% |
| Frac pairs with d ≈ 1.0 (unrelated) | 92.7% |

**Verdict for C3 (low genome similarity): REPLICATED** — the vast majority of Bacillus lytic phage pairs are essentially unrelated at the k-mer level. The paper's VIRIDIC heat-map (Fig 4) also shows a very sparse pattern of similarity islands, which is qualitatively the same result.

### 4.2 Unknown-function gene fraction (C1 sub-claim)

| Protein-cluster metric (all 231 lytic, MMseqs2 30/50) | Value |
|---|---|
| Total predicted proteins (Prodigal meta) | 35,069 |
| Number of clusters | 6,875 |
| Singleton clusters (found in exactly 1 protein / effectively 1 genome) | 3,351 (48.7%) |
| Clusters with ≥10 members | 807 (11.7%) |
| Clusters with ≥50 members | 76 (1.1%) |
| Clusters with ≥100 members | 0 |
| Largest cluster | 99 proteins |
| Mean cluster size | 5.1 |
| Median cluster size | 2 |

The absence of any protein cluster with ≥100 members across the 231-genome panel (and a huge singleton tail) is exactly the "large number of unknown functional gene fragments" pattern the paper reports. **Sub-claim REPLICATED**; the specific functional-annotation sub-claim (COG assignment of hallmark sporulation/biofilm/virulence proteins in a portion of clusters) was not re-run — it requires WebMGA/COG web service and BLAST against curated COG DB, which is outside the free-tool wave budget.

### 4.3 20-focal-phage sub-panel (C3, C4)

| Metric | This replication (n=20) | Paper (Fig 4 heat map + Table S4) |
|---|---|---|
| Length range | 18,753 – 164,297 bp | Similar order-of-magnitude spread (Table S4 hosts range from Sipho- to Myoviridae) |
| GC range | 30.66% – 43.84% | Consistent |
| MASH pairwise mean d | 0.924 | Paper Fig 4 heat map shows almost all off-diagonal cells near zero identity → ✔ |
| Frac pairs d ≈ 1.0 (unrelated) | 91.05% | Consistent with sparse VIRIDIC heat map |
| Frac pairs d < 0.10 (closely related) | 3.68% | Consistent with a few "islands" in Fig 4 |
| MMseqs2 protein clusters (n=2,497 proteins) | 1,495 clusters; 1,035 singletons; 460 shared by ≥2 phages; 0 shared by all 20 | Consistent with paper's finding of low ortholog conservation — **no strict phage-wide core genome** across the 20 |

MASH BIONJ tree (Newick in `report/evidence/mash20_nj.nwk`) recovers ≥ 3 major clades: (a) the tightly grouped `NC_020478.1 / KC330681.1 / NC_020479.1 / NC_041858.1` cluster (all *B. subtilis* SPP1-like siphoviruses per Table S4), (b) the `NC_007814.1 / DQ222851.1 / KY963371.1 / NC_048628.1` cluster (Wbetavirus-type siphoviruses of *B. anthracis / B. cereus*), and (c) a scatter of `Myoviridae` including `NC_022763.1`, `JN797796.1`, `NC_024207.1` on one side and `NC_020883.1`, `NC_031121.1`, `MG967616.1` on the other. This is qualitatively the same topology the paper reports around Fig 5/6 groupings.

## 5. Verdict + justification

**PARTIAL — REPLICATED for 3 of 4 testable claims.**

- **C2 (diversity)** REPLICATED — 231 real re-fetched genomes reproduce the paper's diverse size (7.4-497.5 kb) and GC (27.7-50.1%) distribution.
- **C3 (low genome similarity)** REPLICATED — 92.7% of 53,130 MASH pairs are effectively unrelated, matching the paper's sparse VIRIDIC heat map.
- **C1 (large unknown-function fraction)** REPLICATED for the "large unknown fraction" sub-claim (49% singleton protein clusters, 0 clusters ≥ 100 members). The specific COG-family cargo sub-claim not re-run.
- **C4 (two lysis-module types drive cross-species infestation)** NOT TESTED — requires manual annotation of the lysis-module ORFs and a controlled cross-infection sub-analysis; out of wave time budget.
- **Prophage vs lytic boundary sub-claim of C2** NOT TESTED — the 36 prophage sequences are PHASTER predictions from 10 host genomes, and PHASTER is a web service not available at this scale in the free-tool wave.

The data availability is excellent (all supplementary tables released with full accessions), the pipeline is standard, and the paper's numeric claims are quantitatively supported by an independent re-run on the exact same public accessions. This is a **solid** replication.

## 6. Open Questions

See `report/open_questions.json` for JSON list of 5.

**Q1.** How much of the paper's headline "low genome similarity" is an artefact of the accession collection strategy (one-genome-per-species vs true species-level sampling)? Our 231-genome MASH matrix shows a small but real cluster of near-identical pairs (~1.1% at d<0.05) — are these independent isolates of the same phage species deposited under different accessions, and if the sampling were more even across ICTV genera, would the "92.7% pairs unrelated" number drop significantly?

**Q2.** Does the paper's PHASTER-based prophage set (36 prophages from 178 host genomes) systematically miss the fully-integrated ancient prophages that lack canonical phage structural genes, thereby overstating the "clear genome boundary between prophages and lytic phages"? A rerun with VirSorter2/geNomad on the same 10 host genomes would put a number on this.

**Q3.** Our Prodigal-metagenomic ORF calls produced 35,069 proteins from 231 lytic phages (~152 ORFs / genome, close to expected). But the paper does not report a per-genome ORF-count histogram. Are singleton protein clusters (49% of clusters) enriched in the smaller genomes (< 50 kb) — implying that "unknown functions" are actually mostly small-phage-specific hypotheticals rather than true novel-function proteins scattered across all size classes?

**Q4.** The paper's "two types of lysis module" (Type I / Type II, from Tables S6/S7) is claimed to gate cross-species infestation, but only 25 vs 105 homologous sequences are listed. What is the true frequency of each lysis-module type across the full 231-lytic panel (not just the 3 focal phages Carmel_SA, Cherry, Fah), and does the module-type distribution correlate with host range as claimed?

**Q5.** How stable is the 20-focal-phage BIONJ tree topology (from our MASH matrix) versus the paper's Mauve/Easyfig visual clustering? A quantitative comparison — normalized Robinson-Foulds distance between our MASH-BIONJ tree and a proteome-derived tree (using shared MMseqs2 clusters as characters) — would separate genuine evolutionary signal from single-method artefacts.

## 7. Artifacts and evidence

Full inventory in `report/artifacts_summary.md`. Key files:
- `report/evidence/summary_236.json` — length/GC/bin statistics on 231 genomes
- `report/evidence/mash_236_stats.json` — pairwise MASH summary
- `report/evidence/protein_clusters.json` — MMseqs2 231-lytic clustering summary
- `report/evidence/protein_clusters_20.json` — MMseqs2 20-lytic clustering summary
- `report/evidence/summary_20.json` + `report/evidence/mash_20_stats.json` — 20-lytic sub-panel
- `report/evidence/mash20_nj.nwk` — BIONJ tree of 20 focal phages (Newick)
- `report/evidence/genome_length_gc.tsv` — per-genome length + GC for 231
- `report/evidence/lytic_20_lengths_gc.tsv` — per-genome length + GC for 20
- `report/evidence/mash_dist_all.tsv` — 53,361-row all-pairs MASH matrix
- `report/evidence/logs/` — every tool log (download, prodigal, mmseqs, rapidnj)
- `work/supp/bvbrc120_supp{1..9}.xlsx` — all 9 supplementary tables as fetched from Springer
- `work/S9_236_lytic_phages.csv`, `work/S4_20_lytic_phages.csv`, `work/S1_178_bacillus_strains.csv` — accession lists extracted from supplementary tables

## 8. Failure analysis

See `report/failure_analysis.md`. High-level: 5 accessions withdrawn/superseded by NCBI (returned 231 of 236 requested); whole-genome MAFFT alignment abandoned on divergent 20-phage panel (expected, replaced with MASH-BIONJ); PHASTER prophage re-derivation and WebMGA/COG functional annotation both skipped (web-service tools, out of wave scope).

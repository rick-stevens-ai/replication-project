# REPORT — Supervised Extraction of Near-Complete Genomes from Metagenomic Samples: A New Service in PATRIC

**OSTI ID:** 2469515 · **Authors:** Parrello B, Butler R, Chlenski P, Pusch GD, Overbeek R · **Year:** 2021  
**Journal:** PLoS ONE 16(4): e0250092 · **DOI:** [10.1371/journal.pone.0250092](https://doi.org/10.1371/journal.pone.0250092)

---

## Paper claim

The paper presents PATRIC's **supervised metagenome binning service**, which uses a reference-guided approach to extract near-complete draft genomes from metagenomic assemblies. Assembled contigs are anchored to reference genomes via *pheS* (phenylalanyl-tRNA synthetase α) markers BLASTed against PATRIC's 193,980-genome database; contigs are then assigned to bins using discriminating protein 12-mers shared with the reference. Quality is scored by EvalG (completeness/contamination via universal markers) and EvalCon (annotation consistency via random-forest classifiers over ~1,300 reliably predictable gene roles). On 23 human-gut metagenomes from Pasolli et al. (2019), the supervised pipeline produces **205 high-quality bins** (8.91 HQ/sample) versus MetaBAT2's **180 HQ bins** (7.83/sample) with multi-sample coverage, or **122 HQ bins** (5.30/sample) from contigs alone — demonstrating that reference-guided binning outperforms unsupervised methods, particularly on complex real-world communities.

## What we replicated

We reproduced the **MetaBAT2 baseline comparator arm** — the unsupervised binning pipeline the paper uses as its benchmark — on a controlled **synthetic 5-species community**:

| Step | Method | Status |
|------|--------|--------|
| Read simulation | InSilicoSeq 2.0.1 (HiSeq model), 2 samples × 1M read pairs, opposite abundance vectors | ✅ Done |
| Co-assembly | metaSPAdes 4.2.0 (`--meta --only-assembler`) | ✅ Done |
| Per-sample mapping | minimap2 2.30 (`-ax sr`) + samtools 1.23.1 | ✅ Done |
| Coverage profiling | `jgi_summarize_bam_contig_depths` | ✅ Done |
| Binning | MetaBAT2 2.18 (`-m 1500 --seed 42`) | ✅ Done |
| Quality scoring | Ground-truth alignment (minimap2 `asm5`) against source reference genomes | ✅ Done |
| **PATRIC supervised pipeline** | SEEDtk + 193k-genome BV-BRC reference + pheS anchoring + EvalG/EvalCon | ❌ **Not attempted** — proprietary/platform-bound |
| Real human-gut benchmark (23 Pasolli samples) | 23 SRR/ERR accessions | ❌ Substituted with synthetic community |
| CheckM/CheckM2 | Not needed — ground truth available | ⏭️ Skipped |

## Key results (paper vs ours)

### Binning performance comparison

| Metric | Paper: PATRIC supervised | Paper: MetaBAT2 + Bowtie2 | Paper: MetaBAT2 contigs-only | **Ours: MetaBAT2 synthetic** |
|--------|--------------------------|---------------------------|-------------------------------|------------------------------|
| Samples | 23 (real human gut) | 23 | 23 | 1 (5-species synthetic) |
| Total bins | 370 | 840 | 553 | **5** |
| HQ bins | 205 | 180 | 122 | **5** |
| HQ/sample | 8.91 | 7.83 | 5.30 | **5.00** |
| HQ rate | 55.4% | 21.4% | 22.1% | **100%** |

### Per-bin quality (our synthetic community)

| Bin | Species | Purity | Completeness | Bin size (bp) | MIMAG HQ? |
|-----|---------|--------|--------------|---------------|-----------|
| bin.1 | *P. gingivalis* | 100.00% | 85.64% | 2,021,268 | ✅ |
| bin.2 | *E. coli* | 100.00% | 97.19% | 4,513,831 | ✅ |
| bin.3 | *S. aureus* | 100.00% | 98.30% | 2,775,039 | ✅ |
| bin.4 | *L. gasseri* | 100.00% | 95.51% | 1,809,639 | ✅ |
| bin.5 | *B. subtilis* | 100.00% | 96.93% | 4,090,423 | ✅ |

**Summary:** 5/5 genomes recovered, 0% contamination across all bins, mean completeness 94.7%, all pass MIMAG high-quality threshold (≥80% complete, ≤10% contamination).

### Qualitative agreement

- ✅ MetaBAT2 **does** produce high-quality bins when differential coverage across samples is informative — consistent with the paper's findings
- ✅ The read→assemble→map→depth→bin recipe works end-to-end on commodity hardware (macOS iMac, 20 CPU / 128 GB RAM)
- ⚠️ Our 100% HQ rate vs. paper's 21% reflects the trivial difficulty of a 5-species synthetic community vs. complex real gut metagenomes — not a disagreement with the paper

## Honest gaps

**This replication is TOOL-BLOCKED.** The paper's actual scientific contribution — that supervised binning with a 193k-genome reference database outperforms unsupervised methods — was **not tested**. Specifically:

1. **SEEDtk / PATRIC supervised pipeline not implemented.** The supervised binning engine requires the SEEDtk framework (distributed as binary RAST modules, not packaged on conda/PyPI), the full PATRIC/BV-BRC genome corpus, and BV-BRC API access for reference lookups. A BV-BRC access request was submitted ~2 weeks prior; still pending as of 2026-04-27.

2. **EvalG/EvalCon quality scoring not available.** The paper's quality metrics rely on proprietary annotation-consistency classifiers that cannot be run outside BV-BRC. We used direct ground-truth alignment instead, which is actually *stronger* for our synthetic case but cannot replicate the paper's scoring methodology.

3. **Real benchmark data not used.** The paper's 23 human-gut Pasolli metagenomes were substituted with a 5-species synthetic community to fit compute and time constraints. This means the head-to-head comparison (205 vs 180 HQ bins) was never tested.

4. **Key claims untestable:**
   - pheS–genome similarity Pearson r = 0.97 (requires pheS database + BLAST against PATRIC)
   - Postprocessing boost from 1.7 → 8.17 HQ bins/sample (requires EvalCon role filtering)
   - Supervised pipeline's advantage on complex, species-rich real samples

5. **megahit segfault on macOS.** megahit 1.2.9 (bioconda) crashed with SIGSEGV on this Intel iMac; metaSPAdes was used instead. This is an environment issue, not a paper issue.

**Bottom line:** We verified the comparator works correctly on easy data. We did not — and currently cannot — verify the paper's headline contribution.

## Score

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| **Coverage** | **3/10** | Only the MetaBAT2 baseline comparator was reproduced. The paper's core supervised pipeline (pheS anchoring, discriminating 12-mers, EvalG/EvalCon, 193k-genome reference) was not attempted. Real benchmark dataset not used. |
| **Agreement** | **5/10** | The comparator arm works correctly and our results are consistent with the paper's observations about MetaBAT2 performance. But we're comparing synthetic-easy vs. real-hard data, and the headline claim (supervised > unsupervised) is untested. |

**Could improve to 7–8/10** if BV-BRC platform access is granted and the supervised pipeline can be run against the original 23 Pasolli samples.

## Deliverables

| Artifact | Path |
|----------|------|
| Paper PDF | `2469515.pdf` |
| Replication plan | `replication_plan_2469515.pdf` / `.tex` |
| Reference genomes (5 spp.) | `replication/data/*.fna` |
| Abundance profiles | `replication/data/abund_s{1,2}.txt` |
| metaSPAdes assembly | `replication/assembly/spades/` |
| Per-sample BAMs + index | `replication/bins/sample{1,2}.bam` |
| Coverage depths | `replication/bins/depth.txt` |
| MetaBAT2 bins (5 MAGs) | `replication/bins/metabat/bin.{1..5}.fa` |
| Ground-truth evaluation | `replication/checkm/bin_eval.tsv` |
| Detailed LaTeX report | `replication/report/report.tex` / `.pdf` |
| Template report (stub) | `report/2469515_replication_report.tex` / `.pdf` |
| Tier-lift notes | `.openclaw/workspace/24h-progress/tier-lift-v2/2469515.md` |
| **This report** | `REPORT.md` |

**Environment:** conda env `metabin` — metaSPAdes 4.2.0, minimap2 2.30, samtools 1.23.1, MetaBAT2 2.18, seqkit, InSilicoSeq 2.0.1, BioPython 1.87, Python 3.13 · Host: CherryRd (macOS, Intel, 20 CPU / 128 GB RAM)

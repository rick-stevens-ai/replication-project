# Genome Statistics: Paper (Table 3) vs Independent Recompute

Source data: NCBI Datasets REST — GCA_900094135.1 (author-submitted GenBank, = ENA LT604076.1)
and GCF_900094135.1 (RefSeq re-annotation, = NZ_LT604076.1). Recompute via `work/genome_stats.py` (pure stdlib) + Prokka 1.12 de-novo re-annotation on uicgpu.

## Core assembly metrics (paper Table 3 vs GCA author assembly)

| Attribute | Paper Table 3 | GCA_900094135.1 (author) | Match |
|---|---:|---:|:--:|
| Genome size (bp) | 1,731,838 | 1,731,838 | ✅ EXACT |
| DNA G+C (bp) | 679,104 | 679,104 | ✅ EXACT |
| G+C % | 39.21 (39.2%) | 39.21 | ✅ EXACT |
| DNA scaffolds | 1 | 1 (1 circular chromosome) | ✅ |
| Protein-coding genes | 1,556 | 1,556 | ✅ EXACT |
| RNA genes | 70 | 70 (56 tRNA + 14 rRNA) | ✅ EXACT |
| tRNAs | 56 | 56 | ✅ EXACT |
| rRNAs | 14 | 14 | ✅ EXACT |
| Pseudogenes | 224 | 224 | ✅ EXACT |
| Total genes | 1,850 | 1,626 (gene features) + 224 pseudo = 1,850* | ✅ |

\* The GFF lists 1,626 `gene` features (1,556 CDS + 56 tRNA + 14 rRNA) plus 224 `pseudogene`
features = **1,850 total genes**, exactly the paper's "Total genes 1,850".

**The author-submitted assembly reproduces every quantitative value in the paper's Table 3 to the digit.**
This is expected — the submitted assembly IS the paper's assembly — and confirms the deposited
public record is faithful to the published Table 3 (no silent post-publication edits).

## RefSeq re-annotation (GCF) — independent NCBI pipeline (PGAP)

| Attribute | Paper | GCF_900094135.1 (RefSeq/PGAP) |
|---|---:|---:|
| Genome size (bp) | 1,731,838 | 1,731,838 (identical sequence) |
| G+C % | 39.21 | 39.21 |
| Protein-coding | 1,556 | 1,490 |
| Pseudogenes | 224 | 226 |
| tRNAs | 56 | 56 |
| rRNAs | 14 | 15 |
| Other ncRNA (tmRNA, RNase_P, SRP, riboswitch) | not tabulated | 1 tmRNA, 1 RNase_P, 1 SRP, 4 riboswitch, 1 ncRNA |

RefSeq/PGAP is an independent re-annotation of the same sequence. CDS count (1,490 vs 1,556),
pseudogene (226 vs 224), rRNA (15 vs 14), tRNA (56, exact) all fall within the expected
pipeline-to-pipeline variance for a 1.73 Mb genome. Same underlying sequence, near-identical stats.

## Prokka 1.12 de-novo re-annotation (RASTtk-analog, independent tool)

Ran on uicgpu (bvbrc28 conda env) with `--kingdom Bacteria --genus Streptococcus`:

| Feature | Paper (RAST+curation) | Prokka 1.12 (de-novo) |
|---|---:|---:|
| CDS | 1,556 (curated) | 1,818 (uncurated ORF calls) |
| tRNA | 56 | 56 (EXACT) |
| rRNA | 14 | 15 |
| tmRNA | (not tabulated) | 1 |
| Function assigned | 1,182 (63.89%) | 653 (35.9%) |

Prokka's higher CDS count (1,818 vs 1,556) is the classic de-novo-vs-curated gap: Prokka retains
short/dubious ORFs and calls the paper's 224 manually-flagged pseudogenes as CDS (1,556 + 224 = 1,780,
close to 1,818; the residual ~38 are additional small-ORF calls). tRNA count is an **exact match**.
The lower function-assignment fraction reflects Prokka's default single-DB search vs the paper's
RAST + WebMGA + EggNOG + Pfam + manual-curation stack — a methodological difference, not a data conflict.

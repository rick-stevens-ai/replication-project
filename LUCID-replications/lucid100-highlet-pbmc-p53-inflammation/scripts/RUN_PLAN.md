# RUN_PLAN — full replication of LUCID Slot 53 (Wave 6)

Heavy compute. **Do not run on CherryRd.** Target host: **uicgpu** (2 TB RAM, R + Bioconductor available).

## 0. Set up

```bash
ssh uicgpu
source ~/env.sh                          # proxy for outbound HTTPS
mkdir -p /data/stevens/scratch/lucid53/{cels,results,logs}
cd /data/stevens/scratch/lucid53
```

## 1. Pull all 76 CEL files

```bash
# Copy cel_urls.txt from CherryRd (in artifacts/) or regenerate from SDRFs.
xargs -n1 -P4 -I{} bash -c 'f=$(basename {}); [ -s cels/$f ] || curl -sSL -o cels/$f {}' < cel_urls.txt
ls cels/ | wc -l   # expect 76
du -sh cels/       # expect ~830 MB
```

## 2. RMA + limma (R 4.x + Bioconductor)

```r
# Install once:
# BiocManager::install(c("oligo", "limma", "pd.hugene.1.0.st.v1",
#                        "annotate", "hugene10sttranscriptcluster.db",
#                        "enrichR"))

library(oligo); library(limma); library(annotate)
library(hugene10sttranscriptcluster.db)

cel_files <- list.files("cels", pattern="\\.CEL$", full.names=TRUE)
raw <- read.celfiles(cel_files)
eset <- oligo::rma(raw)                  # background-correct + quantile-norm + log2 + summarise

# Map probe IDs to gene symbols
fData(eset)$symbol <- mapIds(hugene10sttranscriptcluster.db,
                             keys=featureNames(eset),
                             column="SYMBOL", keytype="PROBEID", multiVals="first")

# --- Build phenoData from SDRFs ---
# X-ray (E-MTAB-3463): donor, dose ∈ {0, 0.1, 1.0 Gy}, time = 8h
# Heavy ion (E-MTAB-5761): donor, ion ∈ {C, Fe}, dose ∈ {0, 1.0 Gy}, time = 8h
# Joint factor: condition ∈ {sham_X, X_0.1, X_1, sham_C, C_1, sham_Fe, Fe_1}
# Use donor as a blocking factor where possible. Heavy-ion donors are
# distinct from X-ray donors -- treat as independent batches in the joint
# model (block on study with duplicateCorrelation, or fit per-study and
# meta-combine).

# Per-study design then meta:
#   X-ray:   ~0 + dose + donor    (limma + topTable for 1 Gy vs sham)
#   Carbon:  ~0 + dose + donor    (1 Gy vs sham)
#   Iron:    ~0 + dose + donor    (1 Gy vs sham)
#
# Then compare DE sets (X / C / Fe at 1 Gy) with Venn + RRHO.

# Save:
#   results/{xray,carbon,iron}_DE.tsv           -- limma topTable, all genes
#   results/{xray,carbon,iron}_up_sig.tsv       -- adj.P < 0.05, logFC >= 1
#   results/venn_up.png                         -- 3-way Venn of up-regulated
#   results/rrho_{X_vs_C, X_vs_Fe, C_vs_Fe}.tsv -- RRHO matrices
```

## 3. Cross-check with paper

Paper key claims to verify:

| Claim | Where to verify |
|---|---|
| All DE genes (any radiation type) are up-regulated | Sign of `logFC` in each topTable |
| p53 enrichment dominant | enrichR `TRRUST_Transcription_Factors_2019` or `ChEA_2016`; expect TP53 top hit |
| Heavy ions enrich immune/inflammatory GO terms not seen with X-rays | enrichR `GO_Biological_Process_2021` on C-only and Fe-only sets vs X-only |
| RRHO shows strong concordance X vs C/Fe in upper-right | RRHO heatmap |
| Distinct DNA-repair donor in iron arm | Per-donor heatmap of DNA-repair GO genes in Fe set |
| qPCR validation genes: PCNA, GADD45A, RPS27L, ASTN2, NDUFAF6, FDXR, MAMDC4 | Check these are in DE up-sets with consistent logFC ordering Fe ≥ C ≥ X |

## 4. Resource estimate

| Step | RAM | CPU | Wall |
|---|---|---|---|
| `read.celfiles(76)` | ~10 GB | 1 | ~3 min |
| `oligo::rma` | ~15 GB | 1 | ~5 min |
| `lmFit` + `eBayes` per study | <2 GB | 1 | <1 min |
| enrichR | network | 1 | ~30 s |

Easy single-node job. No GPU needed. CherryRd would survive but uicgpu is the policy choice for "heavy" Bioconductor RMA over 76 arrays.

## 5. Optional supplementary harvest

Paper references Supplementary Table 1 (primer list), Supplementary Table 5 (full up-gene lists per radiation), Supplementary Table 6 (full GO enrichment results). They live behind the Frontiers `#supplementary-material` anchor. To pull them deterministically without a browser:

```bash
# Inspect the JSON-LD or article metadata API:
curl -sL "https://www.frontiersin.org/articles/10.3389/fonc.2021.768493/full" \
  | python3 -c 'import sys,re; html=sys.stdin.read(); print(*set(re.findall(r"/articles/[^\"\s]*supplementary[^\"\s]*", html)),sep="\n")'

# If JSON metadata yields a `supplementary_material` array, fetch each `download_url`.
# Otherwise use the bundled browser-automation skill to click the "Download All"
# button on the supplementary-material section.
```

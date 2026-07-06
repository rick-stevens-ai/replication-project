# Job plan — Tier 2 16S re-run from FASTQ (SRP098151)

**Do NOT run on CherryRd.** Data fetch is fine here (2 GB), but the QIIME / DESeq2 / PICRUSt pipeline should run elsewhere.

## Recommended target
**uicgpu** (`ssh uicgpu`). 8× A100 are unnecessary here (CPU-only pipeline), but the 2 TB RAM and fast `/data` NVMe are convenient. Use `/data/stevens/projects-active/lucid100-microbiome-casero2017/`.

Alternative: any Linux box with conda + 16 GB RAM + ~20 GB scratch.

## Sketch (bash + conda)

```bash
# on uicgpu
source ~/env.sh                       # NB: proxy for internet from compute
WORK=/data/stevens/projects-active/lucid100-microbiome-casero2017
mkdir -p $WORK && cd $WORK

# 1. Sync slot artifacts from CherryRd (~/Dropbox is rclone'd or just copy via scp)
rsync -avh cherryrd:'~/Dropbox/REPLICATE-PROJECT/LUCID-replications/_LUCID100_WAVE1_LAUNCH_QA/lucid100-space-type-radiation-induces-multimodal-responses-in-the-mouse-gut-microbi/' ./slot/

# 2. Conda env (QIIME2 2024.5 is the modern, reproducible replacement for QIIME1).
mamba env create -n qiime2-2024.5 -f https://data.qiime2.org/2024.5/environments/qiime2-amplicon-2024.5-py310-linux-conda.yml
conda activate qiime2-2024.5

# 3. Fetch FASTQs
bash slot/scripts/fetch_all_fastq.sh ./fastq    # ~2 GB, md5-verified

# 4. Manifest for QIIME2 import
python3 - <<'PY'
import csv, pathlib
out = open('manifest.csv','w'); out.write('sample-id,forward-absolute-filepath,reverse-absolute-filepath\n')
fq = pathlib.Path('fastq').resolve()
with open('slot/data/metadata.tsv') as f:
    for row in csv.DictReader(f, delimiter='\t'):
        sid = row['sample-id']
        out.write(f"{sid},{fq}/{sid}_1.fastq.gz,{fq}/{sid}_2.fastq.gz\n")
out.close()
PY

# 5. QIIME2 import + DADA2 (or alternative: closed-ref OTU picking against GG 13_8 to match paper)
qiime tools import \
  --type 'SampleData[PairedEndSequencesWithQuality]' \
  --input-path manifest.csv \
  --input-format PairedEndFastqManifestPhred33V2 \
  --output-path demux.qza

qiime dada2 denoise-paired \
  --i-demultiplexed-seqs demux.qza \
  --p-trim-left-f 0 --p-trim-left-r 0 \
  --p-trunc-len-f 150 --p-trunc-len-r 150 \
  --p-n-threads 16 \
  --o-table table.qza --o-representative-sequences rep-seqs.qza --o-denoising-stats stats.qza

# 6. Closed-ref classification against GreenGenes 13_8 99% (to match paper)
qiime feature-classifier classify-sklearn \
  --i-classifier gg-13-8-99-515-806-nb-classifier.qza \
  --i-reads rep-seqs.qza \
  --o-classification taxonomy.qza

# 7. α/β diversity at rarefaction depth 60000
qiime diversity core-metrics-phylogenetic \
  --i-phylogeny tree.qza \
  --i-table table.qza \
  --p-sampling-depth 60000 \
  --m-metadata-file slot/data/metadata.tsv \
  --output-dir core-metrics

# 8. PERMANOVA on Dose, Time, Dose:Time → compare to MOESM1 (Table S1)
for col in dose_gy time_days group; do
  qiime diversity beta-group-significance \
    --i-distance-matrix core-metrics/unweighted_unifrac_distance_matrix.qza \
    --m-metadata-file slot/data/metadata.tsv \
    --m-metadata-column $col --p-pairwise \
    --o-visualization core-metrics/unweighted_unifrac_${col}.qzv
done
```

## Resources
- Walltime: ~3-6 h on 16 CPU
- RAM: ~16 GB peak (DADA2)
- Disk: ~10 GB
- Network: 2 GB pull from ENA

## Tier 1 (CherryRd-safe) digital re-replication
Recompute headline numbers directly from `supplements/*.xls`:
- α-diversity nonparametric t-test (Time / Dose) → compare to MOESM1
- β-diversity ANOSIM / PERMANOVA on Dose, Time, Time:Dose → compare to MOESM1
- Kruskal–Wallis taxa-level ranking → compare to MOESM2
- Metabolite regression FDR counts at 0.1 Gy → compare to MOESM8

Time budget: minutes, pure Python (pandas + scipy).

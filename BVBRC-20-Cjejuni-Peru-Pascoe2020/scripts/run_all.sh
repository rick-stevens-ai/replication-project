#!/usr/bin/env bash
# BVBRC-20 C. jejuni Peru (Pascoe 2020) replication pipeline
set -euo pipefail
source /usr/local/Caskroom/miniforge/base/etc/profile.d/conda.sh
cd "$(dirname "$0")/.."
# 1. data: figshare 10352375 Peru.assemblies.tar -> data/peru_assemblies/*.fas (62)
# 2. MLST
conda activate mlst-env
mlst --scheme campylobacter data/peru_assemblies/*.fas > data/mlst_results.tsv
# 3. AMR/resistome
conda activate vrefm-replication
mkdir -p data/abricate
for db in ncbi card resfinder vfdb plasmidfinder; do abricate --db $db data/peru_assemblies/*.fas > data/abricate/$db.tsv; done
# 4. phylogeny / divergence
conda activate tpyo
mash sketch -s 10000 -o data/phylo/peru data/peru_assemblies/*.fas
mash dist data/phylo/peru.msh data/phylo/peru.msh > data/phylo/mash_dist.tsv
# NJ tree + group-divergence stats: see analysis in REPORT.md

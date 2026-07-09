#!/usr/bin/env bash
set -euo pipefail
source /usr/local/Caskroom/miniforge/base/etc/profile.d/conda.sh
cd "$(dirname "$0")/.."
conda activate amrfinder
datasets download genome accession --inputfile data/acc_list.txt --include genome --filename data/ecoli_genomes.zip
conda activate mlst-env
mlst --scheme ecoli_achtman_4 data/genomes/*.fna > data/mlst_results.tsv
conda activate vrefm-replication
mkdir -p data/abricate
for db in ncbi resfinder plasmidfinder vfdb; do abricate --db $db data/genomes/*.fna > data/abricate/$db.tsv; done

#!/usr/bin/env bash
set -euo pipefail
source /usr/local/Caskroom/miniforge/base/etc/profile.d/conda.sh
cd "$(dirname "$0")/.."
conda activate amrfinder
datasets download genome accession --inputfile data/acc.txt --include genome --filename data/g.zip
conda activate vrefm-replication
mkdir -p data/abricate
for db in ncbi card resfinder plasmidfinder; do abricate --db $db data/genomes/*.fna > data/abricate/$db.tsv; done
conda activate mlst-env
mlst --scheme abaumannii_2 data/genomes/ABUH*.fna

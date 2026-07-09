#!/usr/bin/env bash
set -euo pipefail
source /usr/local/Caskroom/miniforge/base/etc/profile.d/conda.sh
cd "$(dirname "$0")/.."
conda activate vrefm-replication
for g in DSM2542T DSM2543 DSM6285 DSM21625; do prokka --outdir data/prokka/$g --prefix $g --genus Parageobacillus --cpus 2 --force data/genomes/$g.fna; done
conda activate rgi
mkdir -p data/ortho
for g in DSM2542T DSM2543 DSM6285 DSM21625; do cp data/prokka/$g/$g.faa data/ortho/; done
cat data/ortho/*.faa > data/ortho/all.faa
diamond makedb --in data/ortho/all.faa -d data/ortho/alldb
diamond blastp -q data/ortho/all.faa -d data/ortho/alldb -o data/ortho/allvall.tsv -e 1e-5 -k 5 --id 50 --query-cover 70
# core/accessory: union-find on hits (see REPORT.md); CODH/hydrogenase: grep prokka gff products

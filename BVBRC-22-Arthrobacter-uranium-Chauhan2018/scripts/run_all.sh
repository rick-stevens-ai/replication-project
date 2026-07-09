#!/usr/bin/env bash
set -euo pipefail
source /usr/local/Caskroom/miniforge/base/etc/profile.d/conda.sh
cd "$(dirname "$0")/.."
conda activate rgi
prodigal -i data/genomes/SRS-W-1-2016.fna -a data/SRS_proteins.faa -o /dev/null -q
for g in P_aurescens_TC1 A_cupressi_DSM24664 A_globiformis_CNM05; do prodigal -i data/genomes/$g.fna -a data/$g.faa -o /dev/null -q; done
cat data/P_aurescens_TC1.faa data/A_cupressi_DSM24664.faa data/A_globiformis_CNM05.faa > data/comparators.faa
diamond makedb --in data/comparators.faa -d data/compdb_dmnd
diamond blastp -q data/SRS_proteins.faa -d data/compdb_dmnd -o data/srs_vs_comp.tsv -e 1e-5 -k 1 --id 30 --query-cover 50
conda activate vrefm-replication
mkdir -p data/abricate
fastani -q data/genomes/SRS-W-1-2016.fna --rl data/genome_list.txt -o data/ani_srs_vs_all.tsv
for db in bacmet2 ncbi card; do abricate --db $db data/genomes/SRS-W-1-2016.fna > data/abricate/${db}_SRS.tsv; done

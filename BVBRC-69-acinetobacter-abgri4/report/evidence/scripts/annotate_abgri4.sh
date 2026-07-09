#!/usr/bin/env bash
# AMR (CARD, ResFinder, NCBI) + IS26 detection on AbGRI4 regions
set -eo pipefail
set +u; source ~/env.sh || true; set -u
export PATH=/data/stevens/envs/bvbrc14/bin:$PATH

BASE=/data/stevens/bvbrc69-abgri4
cd $BASE
mkdir -p results/abgri4/amr results/abgri4/is

for s in ABUH763 ABUH793 ABUH796; do
  echo "=== $s AbGRI4 region ==="
  fa=results/abgri4/${s}_AbGRI4.fna
  # ResFinder for AMR
  abricate --db resfinder --minid 90 --mincov 80 $fa 2>/dev/null > results/abgri4/amr/${s}_resfinder.tsv
  echo "-- resfinder --"; cat results/abgri4/amr/${s}_resfinder.tsv
  # CARD for AMR
  abricate --db card --minid 90 --mincov 80 $fa 2>/dev/null > results/abgri4/amr/${s}_card.tsv
  echo "-- card --"; cat results/abgri4/amr/${s}_card.tsv
  # NCBI AMRFinderPlus curated
  abricate --db ncbi --minid 90 --mincov 80 $fa 2>/dev/null > results/abgri4/amr/${s}_ncbi.tsv
  echo "-- ncbi --"; cat results/abgri4/amr/${s}_ncbi.tsv
  # PlasmidFinder replicons
  abricate --db plasmidfinder --minid 90 --mincov 80 $fa 2>/dev/null > results/abgri4/amr/${s}_plasmidfinder.tsv
  echo "-- plasmidfinder --"; cat results/abgri4/amr/${s}_plasmidfinder.tsv
done

# Also run resfinder + plasmidfinder on the full chromosome + plasmids per strain
echo ""
echo "=== Whole-genome AMR (all 4 strains including ABUH773 control) ==="
mkdir -p results/wg_amr
for s in ABUH763 ABUH773 ABUH793 ABUH796; do
  fa=genomes/$s/${s}_all.fna
  abricate --db resfinder --minid 90 --mincov 80 $fa 2>/dev/null > results/wg_amr/${s}_resfinder.tsv
  abricate --db plasmidfinder --minid 90 --mincov 80 $fa 2>/dev/null > results/wg_amr/${s}_plasmidfinder.tsv
  echo "-- $s resfinder --"
  cut -f1,2,3,4,5,6,10,14,15 results/wg_amr/${s}_resfinder.tsv
  echo ""
done

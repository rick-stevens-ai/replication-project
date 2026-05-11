#!/bin/bash
# Run Roary pangenome analysis
# Paper used Roary to get core genome (>90% presence) and pan-genome
set -e

eval "$(conda shell.bash hook)"
conda activate vrefm-replication

BASEDIR=~/Dropbox/REPLICATE-PROJECT/BVBRC-11-VREfm-LatAm-Rios2020
ANNDIR=$BASEDIR/data/annotations
OUTDIR=$BASEDIR/data/pangenome

# Collect all GFF files
echo "=== Collecting GFF files ==="
GFF_FILES=""
count=0
for gff in $ANNDIR/*/*.gff; do
    GFF_FILES="$GFF_FILES $gff"
    count=$((count + 1))
done
echo "Found $count GFF files"

# Run Roary
# Paper: core genome = genes present in ≥90% of genomes
# -p = cpus, -e = create multiFASTA, -n = fast core gene alignment with MAFFT
echo "=== Running Roary ==="
cd $OUTDIR
roary -p 8 -e -n -cd 90 -f roary_output $GFF_FILES 2>&1

echo "=== Roary complete ==="
echo "Gene presence/absence matrix:"
head -1 roary_output/gene_presence_absence.csv | tr ',' '\n' | tail -5
echo ""
echo "Summary stats:"
cat roary_output/summary_statistics.txt

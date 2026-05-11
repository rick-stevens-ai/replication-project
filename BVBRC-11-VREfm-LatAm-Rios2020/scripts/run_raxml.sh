#!/bin/bash
# Run RAxML phylogenetic analysis on core genome alignment from Roary
set -e

eval "$(conda shell.bash hook)"
conda activate vrefm-replication

BASEDIR=~/Dropbox/REPLICATE-PROJECT/BVBRC-11-VREfm-LatAm-Rios2020
PANDIR=$BASEDIR/data/pangenome/roary_output
OUTDIR=$BASEDIR/data/phylogeny

# Use core gene alignment from Roary
ALIGNMENT=$PANDIR/core_gene_alignment.aln

if [ ! -f "$ALIGNMENT" ]; then
    echo "ERROR: Core gene alignment not found at $ALIGNMENT"
    exit 1
fi

echo "=== Running RAxML ==="
echo "Input alignment: $ALIGNMENT"
echo "Alignment size: $(wc -c < "$ALIGNMENT") bytes"

cd $OUTDIR

# Paper used GTR + Γ model
# -m GTRGAMMA -p random seed -f a = rapid bootstrap + ML search
# -N 100 = 100 bootstrap replicates (paper used 1000 but we use fewer for speed)
raxmlHPC -m GTRGAMMA -p 12345 -f a -x 12345 -N 100 \
    -s "$ALIGNMENT" -n ERV55_tree -T 4 2>&1

echo "=== RAxML complete ==="
echo "Output files:"
ls -la RAxML_*ERV55_tree*

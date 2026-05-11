#!/bin/bash
set -e
GENOMES=data/genomes
OUTDIR=analysis/prokka
CONDA_ENV=vrefm-replication

for fna in $GENOMES/*.fna; do
    strain=$(basename "$fna" .fna)
    if [ -f "$OUTDIR/$strain/$strain.gff" ]; then
        echo "SKIP $strain (already done)"
        continue
    fi
    echo "Annotating $strain..."
    conda run --no-banner -n $CONDA_ENV prokka \
        --outdir "$OUTDIR/$strain" \
        --prefix "$strain" \
        --genus Enterococcus \
        --species faecium \
        --strain "$strain" \
        --cpus 4 \
        --force \
        --quiet \
        "$fna" 2>&1
done
echo "=== Prokka complete ==="
ls $OUTDIR/*/?.gff 2>/dev/null | wc -l
echo "GFF files generated"

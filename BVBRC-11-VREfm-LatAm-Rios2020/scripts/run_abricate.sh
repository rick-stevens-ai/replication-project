#!/bin/bash
set -e
GENOMES=data/genomes
OUTDIR=analysis/abricate

# Run against multiple databases
for db in resfinder card vfdb; do
    echo "=== Running Abricate with $db ==="
    outfile="$OUTDIR/abricate_${db}.tsv"
    conda run --no-banner -n vrefm-replication abricate \
        --db $db \
        --minid 80 \
        --mincov 80 \
        $GENOMES/*.fna > "$outfile" 2>/dev/null
    echo "$db: $(wc -l < "$outfile") hits"
    
    # Summary
    conda run --no-banner -n vrefm-replication abricate --summary "$outfile" > "${OUTDIR}/summary_${db}.tsv" 2>/dev/null
done
echo "=== Abricate complete ==="

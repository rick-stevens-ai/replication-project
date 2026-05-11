#!/bin/bash
set -e
BASEDIR="$(cd "$(dirname "$0")/.." && pwd)"
RESULTS_DIR="$BASEDIR/results/amrfinder"
DB="/usr/local/Caskroom/miniforge/base/envs/amrfinder/bin/data/2026-03-24.1"
AMRFINDER="/usr/local/Caskroom/miniforge/base/envs/amrfinder/bin/amrfinder"

mkdir -p "$RESULTS_DIR"

count=0
total=0
for fna in "$BASEDIR/data/assemblies/"*.fna; do
    acc=$(basename "$fna" .fna)
    total=$((total + 1))
    if [ -f "$RESULTS_DIR/${acc}.tsv" ]; then
        continue
    fi
    count=$((count + 1))
    echo "[$count] Running AMRFinderPlus on $acc"
    $AMRFINDER --nucleotide "$fna" --plus --threads 4 --database "$DB" \
        --output "$RESULTS_DIR/${acc}.tsv" 2>> "$RESULTS_DIR/amrfinder2.log" || echo "FAILED: $acc"
done

echo "Completed $count new genomes (total $total)"

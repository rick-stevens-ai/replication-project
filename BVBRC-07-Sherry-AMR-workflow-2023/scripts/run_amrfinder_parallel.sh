#!/bin/bash
set -e
BASEDIR="$(cd "$(dirname "$0")/.." && pwd)"
RESULTS_DIR="$BASEDIR/results/amrfinder"
AMRFINDER="/usr/local/Caskroom/miniforge/base/envs/amrfinder/bin/amrfinder"
DB="/usr/local/Caskroom/miniforge/base/envs/amrfinder/share/amrfinderplus/data/latest"

mkdir -p "$RESULTS_DIR"

run_one() {
    local fna="$1"
    local acc=$(basename "$fna" .fna)
    if [ -f "$RESULTS_DIR/${acc}.tsv" ]; then
        return 0
    fi
    echo "Running AMRFinder on $acc"
    $AMRFINDER --nucleotide "$fna" --plus --threads 2 --database "$DB" \
        --output "$RESULTS_DIR/${acc}.tsv" 2>> "$RESULTS_DIR/amrfinder_par.log" || echo "FAILED: $acc"
    echo "Done: $acc"
}

export -f run_one
export RESULTS_DIR AMRFINDER DB

# Run 4 in parallel
ls "$BASEDIR/data/assemblies/"*.fna | xargs -P 4 -I{} bash -c 'run_one "$@"' _ {}

echo "ALL AMRFINDER COMPLETE"

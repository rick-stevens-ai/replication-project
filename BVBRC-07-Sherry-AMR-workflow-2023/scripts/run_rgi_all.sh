#!/bin/bash
set -e
BASEDIR="$(cd "$(dirname "$0")/.." && pwd)"
RESULTS_DIR="$BASEDIR/results/rgi"
mkdir -p "$RESULTS_DIR"

run_one() {
    local fna="$1"
    local acc=$(basename "$fna" .fna)
    if [ -f "$RESULTS_DIR/${acc}.txt" ]; then
        return 0
    fi
    echo "Running RGI on $acc"
    cd "$BASEDIR"
    rgi main -i "$fna" -o "$RESULTS_DIR/${acc}" -t contig --local --clean 2>> "$RESULTS_DIR/rgi.log" < /dev/null || echo "FAILED: $acc"
    echo "Done RGI: $acc"
}

export -f run_one
export RESULTS_DIR BASEDIR

# Run 2 in parallel (RGI is heavier)
ls "$BASEDIR/data/assemblies/"*.fna | xargs -P 2 -I{} bash -c 'run_one "$@"' _ {}

echo "ALL RGI COMPLETE"

#!/bin/bash
set -e
BASEDIR="$(cd "$(dirname "$0")/.." && pwd)"
RESULTS_DIR="$BASEDIR/results/resfinder"
mkdir -p "$RESULTS_DIR"

run_one() {
    local fna="$1"
    local acc=$(basename "$fna" .fna)
    if [ -f "$RESULTS_DIR/${acc}/ResFinder_results_tab.txt" ]; then
        return 0
    fi
    echo "Running ResFinder on $acc"
    mkdir -p "$RESULTS_DIR/${acc}"
    run_resfinder.py -ifa "$fna" -o "$RESULTS_DIR/${acc}" --acquired 2>> "$RESULTS_DIR/resfinder.log" < /dev/null || echo "FAILED: $acc"
    echo "Done ResFinder: $acc"
}

export -f run_one
export RESULTS_DIR

# Run 4 in parallel (ResFinder is lighter)
ls "$BASEDIR/data/assemblies/"*.fna | xargs -P 4 -I{} bash -c 'run_one "$@"' _ {}

echo "ALL RESFINDER COMPLETE"

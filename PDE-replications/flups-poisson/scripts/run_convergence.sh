#!/bin/bash
# FLUPS convergence study — sweep cube resolution N for several BC/kernel combos
# Each run writes its error report into outdir/data/

set -uo pipefail

FLUPS_BIN="${FLUPS_BIN:-/tmp/flups/samples/validation/flups_validation_a2a}"
OUTROOT="${OUTROOT:-/Users/stevens/Dropbox/REPLICATE-PROJECT/PDE-replications/flups-poisson/results}"
LOGDIR="${LOGDIR:-/Users/stevens/Dropbox/REPLICATE-PROJECT/PDE-replications/flups-poisson/logs}"

mkdir -p "$LOGDIR"

# Kernel labels: 0=CHAT2, 1=LGF2, 2=HEJ2, 3=HEJ4, 4=HEJ6
# BC labels: 4=unbounded, 3=periodic, 0=even, 1=odd
# We focus on three scenarios:
#   A) Fully unbounded with CHAT2 (kernel=0)   — Caprace baseline (2nd order)
#   B) Fully unbounded with HEJ4 (kernel=3)    — Hejlesen 4th-order regularized
#   C) Fully periodic  with CHAT2 (kernel=0)   — sanity: spectral / machine-precision

declare -a SCENARIOS=(
  "unb_chat2:0:4 4 4 4 4 4"
  "unb_hej4:3:4 4 4 4 4 4"
  "per_chat2:0:3 3 3 3 3 3"
)

RES_LIST=(16 24 32 48 64 96)

for s in "${SCENARIOS[@]}"; do
  IFS=':' read -r label kernel bc <<<"$s"
  outdir="$OUTROOT/$label"
  mkdir -p "$outdir/data"
  echo "===== Scenario $label  (kernel=$kernel  bc=$bc) ====="
  : >"$outdir/run.log"
  for N in "${RES_LIST[@]}"; do
    echo "  [N=$N]"
    /usr/bin/time -l "$FLUPS_BIN" \
        --kernel="$kernel" \
        --bc=${bc// /,} \
        --res="$N,$N,$N" \
        --nres=1 \
        --outdir="$outdir/" \
      >>"$outdir/run.log" 2>&1
    if [[ $? -ne 0 ]]; then
      echo "    FAILED — see $outdir/run.log"
    fi
  done
  echo "  -> wrote $(ls "$outdir/data/" 2>/dev/null | wc -l) data files"
done

echo "DONE"

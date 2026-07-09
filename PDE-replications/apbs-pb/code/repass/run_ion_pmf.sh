#!/usr/bin/env bash
# ion-pmf: reproduce the Im et al. 1998 ion-ion force decomposition test.
# Reference (APBS 3.0 README at fixed configuration with mol 0 at x=-3, mol 1
# at various x). We reproduce x=-3.0 (origin: bundled ion-pmf.pdb shows this
# as the canonical baseline shipping in the repo).
set -uo pipefail
ROOT="/Users/stevens/Dropbox/REPLICATE-PROJECT/PDE-replications/apbs-pb"
SRC="$ROOT/apbs-src/examples/ion-pmf"
LOG="$ROOT/logs/repass"
RES="$ROOT/results/repass"
mkdir -p "$LOG" "$RES"

source /Users/stevens/opt/anaconda3/etc/profile.d/conda.sh
conda activate apbs
APBS="$(which apbs)"

# Reproduce three runme.sh positions: x = -3, -2, 0 to spot-check the README table
PRNA_LOG="$RES/ion-pmf-forces.tsv"
echo -e "x_mol1\tcomponent\tion0_kJmolA\tion1_kJmolA" > "$PRNA_LOG"

for X in -3.000 -2.000 0.000 2.000; do
  WORK="$(mktemp -d -t apbs-ionpmf-${X}-XXXXXX)"
  cp -r "$SRC"/. "$WORK/"
  # Create complex.pdb with mol 0 at -3, mol 1 at X (same as runme.sh)
  cat > "$WORK/complex.pdb" <<EOF
ATOM      1  ION   ION     1      -3.000   0.000   0.000  1.00 2.00
ATOM      1  ION   ION     1      ${X}    0.000   0.000  1.00 2.00
EOF
  # ion-pmf.in expects "ion-pmf.pdb"; symlink complex into that name
  cp "$WORK/complex.pdb" "$WORK/ion-pmf.pdb"
  outfile="$LOG/ion-pmf__x${X}.stdout.log"
  (cd "$WORK" && "$APBS" ion-pmf.in > "$outfile" 2>&1)
  # Look for the four force components for each ion
  # APBS prints: "  qf  0  <fx> <fy> <fz>", etc.
  for comp in qf db ib sasa; do
    line0=$(grep -E "^[[:space:]]+${comp}[[:space:]]+0[[:space:]]" "$outfile" | head -1)
    line1=$(grep -E "^[[:space:]]+${comp}[[:space:]]+1[[:space:]]" "$outfile" | head -1)
    f0=$(echo "$line0" | awk '{print $3}')
    f1=$(echo "$line1" | awk '{print $3}')
    echo -e "${X}\t${comp}\t${f0:--}\t${f1:--}" >> "$PRNA_LOG"
  done
done

echo "ion-pmf forces:"
column -ts $'\t' "$PRNA_LOG"

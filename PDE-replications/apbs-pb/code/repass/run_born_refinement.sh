#!/usr/bin/env bash
# Born-ion grid refinement: h-convergence of MG-PB toward analytical Born.
#
# Varies dime = 33, 65, 97, 129, 161, 193 with cglen=50, fglen=12 (paper's
# Born setup). Records the focusing-final solvation energy
# (ΔG_solv = E_solvated - E_reference) and reports its convergence toward
# the analytical Born value for R=3 A, q=+1, eps_s=78.54, T=298.15 K.
set -uo pipefail
ROOT="/Users/stevens/Dropbox/REPLICATE-PROJECT/PDE-replications/apbs-pb"
SRC="$ROOT/apbs-src/examples/born"
LOG="$ROOT/logs/repass"
RES="$ROOT/results/repass"
mkdir -p "$LOG" "$RES"

source /Users/stevens/opt/anaconda3/etc/profile.d/conda.sh
conda activate apbs
APBS="$(which apbs)"

ANAL=$(python3 -c "
import math
e0=8.8541878128e-12; e_s=78.54; q=1.6021766e-19; R=3.0e-10; NA=6.02214076e23
dG=-(q*q)/(8*math.pi*e0*R)*(1-1.0/e_s)*NA/1000.0
print(f'{dG:.6f}')")
echo "Analytical Born (eps_s=78.54, R=3A): $ANAL kJ/mol"

GRID_LOG="$RES/born-grid-refinement.tsv"
echo -e "dime\tcglen_A\tfglen_A\thmin_fine_A\tsolvation_kJmol\tanalytical_kJmol\tabs_err_kJmol\trel_err_pct" > "$GRID_LOG"

for dime in 33 65 97 129 161 193; do
  WORK="$(mktemp -d -t apbs-born-h-${dime}-XXXXXX)"
  cp "$SRC/ion.pqr" "$WORK/"
  cat > "$WORK/born-h-$dime.in" <<EOF
read
    mol pqr ion.pqr
end
elec name solvated
    mg-auto
    dime $dime $dime $dime
    cglen 50 50 50
    fglen 12 12 12
    fgcent mol 1
    cgcent mol 1
    mol 1
    lpbe
    bcfl mdh
    pdie 1.0
    sdie 78.54
    chgm spl2
    srfm mol
    srad 1.4
    swin 0.3
    sdens 10.0
    temp 298.15
    calcenergy total
    calcforce no
end
elec name reference
    mg-auto
    dime $dime $dime $dime
    cglen 50 50 50
    fglen 12 12 12
    fgcent mol 1
    cgcent mol 1
    mol 1
    lpbe
    bcfl mdh
    pdie 1.0
    sdie 1.0
    chgm spl2
    srfm mol
    srad 1.4
    swin 0.3
    sdens 10.0
    temp 298.15
    calcenergy total
    calcforce no
end
print elecEnergy solvated - reference end
quit
EOF
  (cd "$WORK" && "$APBS" "born-h-$dime.in" > "$LOG/born-h-$dime.stdout.log" 2>&1)

  # One "Global net ELEC energy" line = solvation energy (solvated - reference)
  dsol=$(grep -E "Global net ELEC energy" "$LOG/born-h-$dime.stdout.log" | tail -1 | awk '{print $(NF-1)}')
  if [[ -z "$dsol" ]]; then
    echo -e "$dime\t50\t12\t-\tFAIL\t$ANAL\t-\t-" >> "$GRID_LOG"
  else
    hmin=$(python3 -c "print(f'{12.0/($dime-1):.4f}')")
    aerr=$(python3 -c "print(f'{abs(float($dsol)-float($ANAL)):.4f}')")
    rel=$(python3 -c "print(f'{abs(float($dsol)-float($ANAL))/abs(float($ANAL))*100:.3f}')")
    echo -e "$dime\t50\t12\t$hmin\t$dsol\t$ANAL\t$aerr\t$rel" >> "$GRID_LOG"
  fi
done
echo "Born grid refinement:"
column -ts $'\t' "$GRID_LOG"

#!/usr/bin/env bash
# APBS re-pass: lift coverage of claims skipped in pass 1.
#
# Pass-1 left the following coverage gaps:
#   - pka-lig (ligand-binding ΔG via PB, UHBD comparison)        — NOT RUN
#   - ion-pmf (ion-ion force decomposition, Im et al. 1998 ref)  — NOT RUN
#   - protein-rna (Garcia-Garcia/Draper ionic-strength sweep)    — NOT RUN
#   - Born-ion grid-refinement / convergence study (paper claim) — NOT EXPLICITLY RUN
#   - BEM/TABI, Geoflow, PyGBe, PBAM, PBSAM sub-solvers          — declared "not in conda"
#
# This script:
#   1. Reproduces pka-lig (4 input files, MG, sequential)
#   2. Reproduces ion-pmf (forces only; energy comparison if available)
#   3. Sweeps protein-rna across multiple ionic strengths from the bundled template
#   4. Performs a Born-ion grid-refinement study (dime = 33, 65, 97, 129, 161)
#      to demonstrate h-convergence of the multigrid PB solver toward the
#      analytical Born value, which is one of the headline correctness claims.
#   5. Explicitly probes BEM / Geoflow / PBAM / PBSAM with the bundled
#      example inputs and records the *negative* result from the conda binary.
#
# All numbers stored as raw apbs stdout under logs/repass/, parsed into CSVs
# under results/repass/ for the REPORT.
set -uo pipefail

ROOT="/Users/stevens/Dropbox/REPLICATE-PROJECT/PDE-replications/apbs-pb"
SRC="$ROOT/apbs-src/examples"
LOG="$ROOT/logs/repass"
RES="$ROOT/results/repass"
mkdir -p "$LOG" "$RES"

# Activate the apbs conda env
source /Users/stevens/opt/anaconda3/etc/profile.d/conda.sh
conda activate apbs
APBS="$(which apbs)"
echo "Using APBS: $APBS"
"$APBS" --version 2>&1 | head -4 || true

run_in() {
  # run_in <category> <input.in> <work-dir-source> [extra-files...]
  local cat="$1" inp="$2" srcdir="$3"; shift 3
  local work
  work="$(mktemp -d -t apbs-${cat}-XXXXXX)"
  cp -r "$srcdir"/. "$work"/
  for f in "$@"; do cp -r "$f" "$work/"; done
  (
    cd "$work" || exit 11
    "$APBS" "$inp" > "$LOG/${cat}__$(basename "$inp" .in).stdout.log" 2> "$LOG/${cat}__$(basename "$inp" .in).stderr.log"
    echo $? > "$LOG/${cat}__$(basename "$inp" .in).exit"
  )
  echo "$work"
}

extract_global_net() {
  # Pull the final "Global net ELEC energy" value from an APBS stdout log.
  grep -E "Global net (ELEC )?energy" "$1" | awk '{print $NF}'
}

##############################################################################
# 1) pka-lig (ligand binding ΔG via PB; UHBD comparison)
##############################################################################
echo "=== 1) pka-lig ==="
PKALOG="$RES/pka-lig.tsv"
echo -e "input\treference_v1.5_kJmol\trun_kJmol\tdelta\tstatus" > "$PKALOG"
declare -A PKA_REF=(
  [apbs-mol-vdw.in]="8.08352"
  [apbs-smol-vdw.in]="20.9630"
  [apbs-mol-surf.in]="119.2610"
  [apbs-smol-surf.in]="108.8770"
)
for inp in apbs-mol-vdw.in apbs-smol-vdw.in apbs-mol-surf.in apbs-smol-surf.in; do
  echo "--- pka-lig $inp"
  run_in pka-lig "$inp" "$SRC/pka-lig" > /dev/null
  val=$(extract_global_net "$LOG/pka-lig__$(basename "$inp" .in).stdout.log" | tail -1)
  ref="${PKA_REF[$inp]}"
  if [[ -z "$val" ]]; then
    echo -e "$inp\t$ref\tFAIL\t-\trun-failed" >> "$PKALOG"
  else
    delta=$(python3 -c "print(f'{abs(float($val)-float($ref)):.4g}')")
    status="MATCH"
    awk_ok=$(python3 -c "print('1' if abs(float($val)-float($ref))<0.01 else '0')")
    [[ "$awk_ok" = "0" ]] && status="DIFF"
    echo -e "$inp\t$ref\t$val\t$delta\t$status" >> "$PKALOG"
  fi
done
echo "pka-lig results:"; cat "$PKALOG"

##############################################################################
# 2) ion-pmf  (force decomposition; Im et al. 1998)
##############################################################################
echo
echo "=== 2) ion-pmf ==="
# The bundled runme.sh runs many positions; we just run the canonical complex.in
# and capture the force breakdown.
run_in ion-pmf complex.in "$SRC/ion-pmf" > /dev/null
# Save the force lines:
grep -E "(qf|ib|db|tot)\s+[01]" "$LOG/ion-pmf__complex.stdout.log" \
  > "$RES/ion-pmf__complex_forces.txt" || true
# Reference values from README.md (APBS 3.0)
cat > "$RES/ion-pmf__reference_apbs3.0.txt" <<'EOF'
# Polar forces reference (APBS 3.0 README, ion-pmf, in complex.in)
# Reproduced verbatim from apbs-src/examples/ion-pmf/README.md
qf  0   8.398642197666E+01
ib  0   0.000000000000E+00
db  0   6.148357059184E+00
tot 0   9.013477903584E+01
qf  1  -8.466423642736E+01
ib  1   0.000000000000E+00
db  1   2.882739230548E+00
tot 1  -8.178149719681E+01
tot all 8.353281839029E+00
EOF
echo "--- captured forces ---"
cat "$RES/ion-pmf__complex_forces.txt" | head -40

##############################################################################
# 3) protein-rna (ionic-strength sweep; Garcia-Garcia/Draper)
##############################################################################
echo
echo "=== 3) protein-rna ==="
PRNA_DIR="$(mktemp -d -t apbs-prna-XXXXXX)"
cp -r "$SRC/protein-rna"/. "$PRNA_DIR/"
echo "Working dir: $PRNA_DIR"
PRNA_LOG="$RES/protein-rna.tsv"
# Reference values from README.md (APBS 3.0 column, kJ/mol)
# Format: ionstr  ref
declare -A PRNA_REF=(
  ["0.025"]="86.74116429351"
  ["0.050"]="96.06836713867"
  ["0.075"]="101.1537214883"
  ["0.100"]="104.6142116108"
  ["0.150"]="109.3084123761"
  ["0.200"]="112.5199716537"
  ["0.300"]="116.8804254687"
  ["0.500"]="122.0607673699"
)
echo -e "ionstr\treference_kJmol\trun_kJmol\tdelta\tstatus" > "$PRNA_LOG"
for ionstr in 0.025 0.050 0.075 0.100 0.150 0.200 0.300 0.500; do
  inp="apbs-${ionstr}.in"
  sed -e "s/IONSTR/${ionstr}/g" "$PRNA_DIR/template.txt" > "$PRNA_DIR/$inp"
  echo "--- protein-rna ionstr=$ionstr"
  (
    cd "$PRNA_DIR" || exit 1
    "$APBS" "$inp" > "$LOG/protein-rna__${ionstr}.stdout.log" 2> "$LOG/protein-rna__${ionstr}.stderr.log"
  )
  # Per the README: report value is Global net ELEC for the "complex" minus pep minus rna
  # But the test.sh uses the first Global net ELEC of the FIRST elec block, which IS the complex
  # post-processing 'fit.py' would do the subtraction. The reference values in the README ARE
  # the post-processed binding energies. We capture both.
  vals=$(grep -E "Global net ELEC energy" "$LOG/protein-rna__${ionstr}.stdout.log" | awk '{print $NF}')
  # vals will have 3 lines (complex, peptide, rna)
  arr=($vals)
  complex="${arr[0]:-MISSING}"
  pep="${arr[1]:-MISSING}"
  rna="${arr[2]:-MISSING}"
  if [[ "$complex" != "MISSING" && "$pep" != "MISSING" && "$rna" != "MISSING" ]]; then
    # The reference in the README is the *first* Global net ELEC for that input
    # (it's the complex's energy in kJ/mol). Use that.
    val="$complex"
    ref="${PRNA_REF[$ionstr]}"
    delta=$(python3 -c "print(f'{abs(float($val)-float($ref)):.4g}')")
    awk_ok=$(python3 -c "print('1' if abs(float($val)-float($ref))/max(1.0,abs(float($ref))) < 0.001 else '0')")
    status="MATCH"; [[ "$awk_ok" = "0" ]] && status="DIFF"
    echo -e "$ionstr\t$ref\t$val\t$delta\t$status" >> "$PRNA_LOG"
  else
    echo -e "$ionstr\t${PRNA_REF[$ionstr]}\tFAIL\t-\trun-failed" >> "$PRNA_LOG"
  fi
done
echo "protein-rna results:"; cat "$PRNA_LOG"

##############################################################################
# 4) Born-ion grid refinement (h-convergence to analytical)
##############################################################################
echo
echo "=== 4) Born grid refinement ==="
BORN_DIR="$(mktemp -d -t apbs-born-grid-XXXXXX)"
cp -r "$SRC/born"/. "$BORN_DIR/"
GRID_LOG="$RES/born-grid-refinement.tsv"
echo -e "dime\tfglen\thmin_angstrom\tnumerical_kJmol\tanalytical_kJmol\trel_error_pct" > "$GRID_LOG"

# Analytical Born value for R=3 A, q=+1, eps_s=78.54, T=298.15 K
# Eq: dG = -(1/(8 pi eps0)) (1 - 1/eps_s) q^2/R   in kJ/mol
ANAL=$(python3 -c "
e0=8.8541878128e-12; e_s=78.54; q=1.6021766e-19; R=3.0e-10
import math
dG=-(1.0/(8*math.pi*e0))*(1-1.0/e_s)*q*q/R   # joules per ion
NA=6.02214076e23
print(f'{dG*NA/1000.0:.6f}')")
echo "Analytical Born (R=3 A, eps_s=78.54): $ANAL kJ/mol"

# Use apbs-mol-auto.in as the template, vary dime, keep fglen=12 A
# fglen=12 A box / (dime-1) cells = grid spacing
for dime in 33 65 97 129 161; do
  inp="$BORN_DIR/grid-$dime.in"
  cat > "$inp" <<EOF
read
    mol pqr ion.pqr
end
elec name born_mol_dime${dime}
    mg-auto
    dime $dime $dime $dime
    cglen 12 12 12
    fglen 12 12 12
    cgcent mol 1
    fgcent mol 1
    mol 1
    lpbe
    bcfl mdh
    pdie 1.0
    sdie 78.54
    srfm mol
    chgm spl0
    sdens 10.00
    srad 1.40
    swin 0.30
    temp 298.15
    calcenergy total
    calcforce no
end
quit
EOF
  echo "--- born grid dime=$dime"
  (cd "$BORN_DIR" && "$APBS" "grid-$dime.in" > "$LOG/born-grid-$dime.stdout.log" 2>&1)
  val=$(grep -E "Global net ELEC energy" "$LOG/born-grid-$dime.stdout.log" | awk '{print $NF}' | tail -1)
  if [[ -z "$val" ]]; then
    echo -e "$dime\t12.0\t-\tFAIL\t$ANAL\t-" >> "$GRID_LOG"
  else
    hmin=$(python3 -c "print(f'{12.0/($dime-1):.4f}')")
    rel=$(python3 -c "print(f'{abs(float($val)-float($ANAL))/abs(float($ANAL))*100:.3f}')")
    echo -e "$dime\t12.0\t$hmin\t$val\t$ANAL\t$rel" >> "$GRID_LOG"
  fi
done
echo "Born grid refinement results:"; cat "$GRID_LOG"

##############################################################################
# 5) Sub-solver feature probe (negative-result documentation)
##############################################################################
echo
echo "=== 5) Sub-solver probes (BEM/Geoflow/PBAM/PBSAM/PyGBe) ==="
SUB_LOG="$RES/subsolvers.tsv"
echo -e "subsolver\tinput\tstatus\tdiagnostic" > "$SUB_LOG"

probe_subsolver() {
  local name="$1" subdir="$2" inp="$3"
  local work
  work="$(mktemp -d -t apbs-${name}-XXXXXX)"
  cp -r "$SRC/$subdir"/. "$work/"
  # If there's a test_proteins/ dir already copied, it's fine
  (cd "$work" && timeout 60 "$APBS" "$inp" > "$LOG/sub-${name}.stdout.log" 2>&1)
  local diag
  diag=$(grep -E "(Error|not compiled|deprecated|Unrecognized|method)" "$LOG/sub-${name}.stdout.log" | head -3 | tr '\n' '|')
  local status="UNKNOWN"
  if   grep -q "not compiled with"   "$LOG/sub-${name}.stdout.log"; then status="NOT_COMPILED"
  elif grep -q "Error while parsing" "$LOG/sub-${name}.stdout.log"; then status="PARSE_ERROR"
  elif grep -q "Global net ELEC"     "$LOG/sub-${name}.stdout.log"; then status="RAN"
  fi
  echo -e "$name\t$inp\t$status\t$diag" >> "$SUB_LOG"
}

probe_subsolver bem        bem        451c_order1.in
probe_subsolver geoflow    geoflow    glycerol.in
probe_subsolver pbam       pbam       1a63.in
probe_subsolver pbsam-gly  pbsam-gly  gly_energyforce.in
probe_subsolver pygbe      pygbe      lys.in

echo "Sub-solver probe results:"; cat "$SUB_LOG"

echo
echo "=== DONE ==="
echo "Logs: $LOG"
echo "Results: $RES"

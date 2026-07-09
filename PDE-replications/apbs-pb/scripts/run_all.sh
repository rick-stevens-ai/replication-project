#!/usr/bin/env bash
# Reproduce the apbs-pb replication end-to-end.
# Requires: conda (any flavor), git, ~3 min, ~200 MB disk.
set -euo pipefail

HERE="$(cd "$(dirname "$0")/.." && pwd)"
cd "$HERE"

# 1. Install APBS via conda-forge if not already present
if ! command -v apbs >/dev/null 2>&1; then
  conda create -n apbs -c conda-forge "apbs=3.4.1" -y
  # shellcheck disable=SC1091
  source "$(conda info --base)/etc/profile.d/conda.sh"
  conda activate apbs
fi
apbs --version | head -3

# 2. Clone source for examples + reference numerics
if [ ! -d apbs-src ]; then
  git clone --depth 1 https://github.com/Electrostatics/apbs.git apbs-src
fi

# 3. Run the formal multigrid/FEM/apolar test categories
mkdir -p logs
cd apbs-src/tests
for t in born actin-dimer-auto alkanes FKBP solv ionize hca-bind \
         ion-protein point-pmf; do
  echo "===== $t ====="
  python apbs_tester.py -e "$(which apbs)" -t "$t" \
    -l "$HERE/logs/tester-$t.log" 2>&1 | \
    grep -E "(PASSED|FAILED|Test failed|Time:|Some tests)" | tail -50
done

# 4. Spot-check Born ion against analytical
cd "$HERE/apbs-src/examples/born"
echo
echo "===== Born ion: numerical vs analytical -230.62 kJ/mol ====="
for inp in apbs-mol-auto.in apbs-smol-auto.in apbs-mol-fem.in apbs-smol-fem.in; do
  result=$(apbs "$inp" 2>&1 | grep -E "Global net ELEC energy" | tail -1)
  printf "%-25s  %s\n" "$inp" "$result"
done

#!/bin/bash
# Run per-L sweeps with parameters tuned so that measurement-record enumeration is tractable.
# Total meas ~ L * t_bulk * p; frontier size ~ 2^N_meas.  We want N_meas <~ 22 for feasibility.
set -euo pipefail
cd "$(dirname "$0")"

PY=../.venv/bin/python
OUT=../report/evidence

mkdir -p "$OUT"

# L=4 : t_bulk=4, so max meas = 16 at p=1.0.  Use full range.
echo "=== L=4 sweep ==="
$PY -u xeb_mipt.py --L 4 --p 0.00 0.05 0.10 0.14 0.20 0.30 0.45 0.60 --n-circuits 60 --seed 20260703 --out $OUT/sweep_L4.json

# L=6 : t_bulk=6, so max meas = 36 at p=1.0.  Cap p at 0.35.
echo "=== L=6 sweep ==="
$PY -u xeb_mipt.py --L 6 --p 0.00 0.05 0.10 0.14 0.20 0.30 0.45 --n-circuits 40 --seed 20260803 --out $OUT/sweep_L6.json

# L=8 : t_bulk=8, expected meas at p=0.3 ~ 19.2, tight but OK; cap p at 0.30.
echo "=== L=8 sweep ==="
$PY -u xeb_mipt.py --L 8 --p 0.00 0.05 0.10 0.14 0.20 0.30 --n-circuits 20 --seed 20260903 --out $OUT/sweep_L8.json

echo "=== all sweeps done ==="
ls -la $OUT/

#!/usr/bin/env bash
# One-shot reproduction script for arXiv:2009.11482 replication.
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -d .venv ]; then
    python3 -m venv .venv
fi
source .venv/bin/activate
pip install --quiet --upgrade pip
pip install --quiet stim pymatching numpy matplotlib

mkdir -p data logs report/evidence
python code/bacon_shor_sim.py --rounds 3 --shots 200000 \
    --out data/results.json 2>&1 | tee logs/main_run.log
python code/make_plot.py
cp data/results.json report/evidence/results.json

echo
echo "Reproduction complete."
echo "See report/REPORT.md and report/evidence/logical_error_curve.png"

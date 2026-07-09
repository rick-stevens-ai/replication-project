#!/bin/bash
# Run VDGN pretrained checkpoint eval + heuristic baselines on linear-advection AMR env.
set -e
set -o pipefail

PROJDIR=/data/stevens/projects-active/marl-amr
LOG=$PROJDIR/eval.log
exec > >(tee -a "$LOG") 2>&1
echo "=== $(date -Is) eval start ==="

source ~/env.sh 2>/dev/null || true
source ~/miniconda3/etc/profile.d/conda.sh
conda activate marlamr
cd "$PROJDIR/marl-amr/marl_amr/alg"

# Force CPU only (avoid GPU init issues; checkpoint eval is tiny anyway)
export CUDA_VISIBLE_DEVICES=""

# (1) VDGN checkpoint eval — uses advection_test config which points to dir_restore=nx16_..._pretrained
echo ""
echo "----- (1) VDGN pretrained checkpoint eval (single Gaussian, single episode) -----"
# The script writes error_vs_time.csv to <cwd>/<dir_restore>/, so make sure dir exists.
mkdir -p nx16_ny16_depth1_tstep0p25_vdgn_pretrained
python test.py tf --config_name=advection_test --verbose --save_err_time 2>&1 | tee $PROJDIR/eval_vdgn_single.log | tail -80

# Now copy the error_vs_time CSV to results
RESTORE_DIR=../results/nx16_ny16_depth1_tstep0p25_vdgn_pretrained
if [ -f "$RESTORE_DIR/error_vs_time.csv" ]; then
  cp "$RESTORE_DIR/error_vs_time.csv" $PROJDIR/results_vdgn_error_vs_time.csv
  echo "Saved VDGN error_vs_time"
fi
ls -la ../results/advection/ 2>/dev/null || true

# (2) Heuristic baseline: DoubleThresholdPolicy at several refine thresholds
echo ""
echo "----- (2) Heuristic baseline: DoubleThresholdPolicy sweep -----"
cd "$PROJDIR/marl-amr/marl_amr/scripts"
mkdir -p $PROJDIR/heuristic_out
# Sweep over a few refine thresholds and one deref threshold
python evaluate_custom_strategies.py advection_href dt \
    --low_array=1e-5 \
    --high_array=1e-4,5e-4,1e-3,5e-3 \
    --n_episodes=1 \
    --save_dir=$PROJDIR/heuristic_out \
    --name=heuristic 2>&1 | tee $PROJDIR/eval_heuristic.log | tail -30

# (3) Error-vs-time for one threshold setting (matches paper Fig style)
echo ""
echo "----- (3) Heuristic err_vs_time at thres_high=5e-4 -----"
python evaluate_custom_strategies.py advection_href err_vs_time \
    --thres_low=1e-5 --thres_high=5e-4 \
    --multipliers=125 \
    --save_dir=$PROJDIR/heuristic_out 2>&1 | tee -a $PROJDIR/eval_heuristic.log | tail -10

# (4) Fixed mesh baselines: coarse and fine
echo ""
echo "----- (4) Fixed mesh baselines (coarse, fine) -----"
python evaluate_custom_strategies.py advection_href coarse \
    --n_episodes=1 --write_csv --save_dir=$PROJDIR/heuristic_out --name=fixed 2>&1 | tail -10
python evaluate_custom_strategies.py advection_href fine \
    --n_episodes=1 --write_csv --save_dir=$PROJDIR/heuristic_out --name=fixed 2>&1 | tail -10

echo "=== $(date -Is) eval done ==="
ls -la $PROJDIR/heuristic_out/ 2>/dev/null

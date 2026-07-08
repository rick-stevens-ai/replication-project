#!/bin/bash
export PATH="$HOME/.local/bin:$PATH"
source ~/env.sh 2>/dev/null
set -e
cd /data/stevens/sowfa_windfarm/windfarm-gnn/graph_farms
source ../../.venv/bin/activate
export CUDA_VISIBLE_DEVICES=''
export TF_CPP_MIN_LOG_LEVEL=3
# Suppress chatty Keras warnings
python -W ignore -c "import absl.logging; absl.logging.set_verbosity(absl.logging.ERROR)" 2>/dev/null

DATASET_ROOT=/data/stevens/sowfa_windfarm/dataset
mkdir -p $DATASET_ROOT/train $DATASET_ROOT/valid $DATASET_ROOT/test
echo "=== TRAIN: 200 layouts x 10 inflows = 2000 graphs, 8 threads ==="
date
python -W ignore generate_graphs.py -c config.yml -nl 200 -ni 10 -d $DATASET_ROOT/train -t 8 2>&1 | grep -v -E "WARNING|absl|tensorflow|cudnn|cublas|cpu_feature_guard|^E0000|^W0000|computation_placer|UserWarning|warnings.warn" | tail -10
date
echo "=== VALID: 30 layouts x 10 inflows = 300 graphs ==="
python -W ignore generate_graphs.py -c config.yml -nl 30 -ni 10 -d $DATASET_ROOT/valid -t 8 2>&1 | grep -v -E "WARNING|absl|tensorflow|cudnn|cublas|cpu_feature_guard|^E0000|^W0000|computation_placer|UserWarning|warnings.warn" | tail -5
date
echo "=== TEST: 30 layouts x 10 inflows = 300 graphs ==="
python -W ignore generate_graphs.py -c config.yml -nl 30 -ni 10 -d $DATASET_ROOT/test -t 8 2>&1 | grep -v -E "WARNING|absl|tensorflow|cudnn|cublas|cpu_feature_guard|^E0000|^W0000|computation_placer|UserWarning|warnings.warn" | tail -5
date
echo "=== summary ==="
for d in train valid test; do
  echo "-- $d --"
  find $DATASET_ROOT/$d -type f -name '*.zip' | wc -l
  du -sh $DATASET_ROOT/$d
done

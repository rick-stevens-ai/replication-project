#!/bin/bash
# Launch hyperparameter sweep on cels-hcdgx2 (16x V100)
# Syncs code, then submits parallel jobs across GPUs

set -e

REMOTE="cels-hcdgx2"
REMOTE_DIR="/homes/stevens/pvmol-sweep"
LOCAL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "=== Syncing project to $REMOTE ==="
ssh $REMOTE "mkdir -p $REMOTE_DIR/{src,data,results/sweep}"
rsync -az --delete \
  $LOCAL_DIR/src/sweep_classifier.py \
  $REMOTE:$REMOTE_DIR/src/
rsync -az $LOCAL_DIR/data/T0.csv $REMOTE:$REMOTE_DIR/data/

echo "=== Generating sweep configs ==="
# Hyperparameter grid (focused on most impactful params)
# Total: 4*4*3*4*3*2*3 = 3456 configs — too many
# Use a focused grid: ~100 configs covering the most important axes

cat > /tmp/sweep_configs.py << 'PYEOF'
import json
import itertools

# Focused sweep
configs = []
job_id = 0

# Axis 1: Architecture (embed, lstm, tdense) — most important
architectures = [
    (64, 32, 32),
    (128, 64, 64),
    (256, 128, 128),
    (512, 128, 128),
    (512, 256, 256),
    (1024, 256, 256),
    (256, 256, 128),
    (128, 128, 128),
]

# Axis 2: Learning rate
lrs = [5e-4, 2e-4, 1.26e-4, 5e-5, 2e-5]

# Axis 3: Other params (fixed reasonable combos)
other_combos = [
    # (batch, patience, epochs, dense_depth, dropout, aug_factor, extra_features)
    (16, 25, 200, 0, 0.1, 10, True),
    (16, 25, 200, 0, 0.1, 10, False),
    (32, 25, 200, 0, 0.1, 10, True),
    (16, 15, 150, 1, 0.2, 10, True),
    (16, 25, 300, 0, 0.05, 20, True),
    (8, 30, 200, 0, 0.1, 10, True),
]

# Thresholds to test post-hoc
thresholds = [0.40, 0.45, 0.47, 0.50, 0.55]

for (embed, lstm, tdense), lr, (batch, patience, epochs, dd, drop, aug, extra) in \
    itertools.product(architectures, lrs, other_combos):
    # Only use threshold 0.47 during training; we'll sweep thresholds post-hoc
    configs.append({
        'id': job_id,
        'embed': embed, 'lstm': lstm, 'tdense': tdense,
        'lr': lr, 'batch': batch, 'patience': patience,
        'epochs': epochs, 'dense_depth': dd, 'dropout': drop,
        'aug_factor': aug, 'extra_features': extra,
        'threshold': 0.47,
    })
    job_id += 1

print(f"Generated {len(configs)} configs", flush=True)

with open('/tmp/sweep_configs.json', 'w') as f:
    json.dump(configs, f, indent=2)
PYEOF
python3 /tmp/sweep_configs.py

echo ""
echo "=== Total configs: $(python3 -c "import json; print(len(json.load(open('/tmp/sweep_configs.json'))))")"

# Copy configs to remote
scp /tmp/sweep_configs.json $REMOTE:$REMOTE_DIR/

echo ""
echo "=== Creating remote runner script ==="
ssh $REMOTE "cat > $REMOTE_DIR/run_sweep.sh" << 'RUNNER'
#!/bin/bash
# Run sweep jobs across available GPUs
# Usage: bash run_sweep.sh [start_idx] [end_idx] [max_parallel]

SWEEP_DIR="/homes/stevens/pvmol-sweep"
CONFIGS="$SWEEP_DIR/sweep_configs.json"
RESULTS="$SWEEP_DIR/results/sweep"
START=${1:-0}
END=${2:-999999}
MAX_PARALLEL=${3:-8}

mkdir -p $RESULTS

# Count total configs
TOTAL=$(python3 -c "import json; print(len(json.load(open('$CONFIGS'))))")
if [ $END -gt $TOTAL ]; then END=$TOTAL; fi

echo "Running configs $START to $END ($((END - START)) jobs, max $MAX_PARALLEL parallel)"

# Run jobs, distributing across GPUs
NUM_GPUS=$(nvidia-smi -L | wc -l)
echo "Available GPUs: $NUM_GPUS"

running=0
for i in $(seq $START $((END - 1))); do
    # Check if already done
    if [ -f "$RESULTS/config_${i}.json" ]; then
        continue
    fi
    
    # Wait if at max parallel
    while [ $(jobs -r | wc -l) -ge $MAX_PARALLEL ]; do
        sleep 2
    done
    
    GPU_ID=$((i % NUM_GPUS))
    
    # Extract params from config
    PARAMS=$(python3 -c "
import json
configs = json.load(open('$CONFIGS'))
c = configs[$i]
args = []
args.append(f'--embed {c[\"embed\"]}')
args.append(f'--lstm {c[\"lstm\"]}')
args.append(f'--tdense {c[\"tdense\"]}')
args.append(f'--lr {c[\"lr\"]}')
args.append(f'--batch {c[\"batch\"]}')
args.append(f'--epochs {c[\"epochs\"]}')
args.append(f'--patience {c[\"patience\"]}')
args.append(f'--dense-depth {c[\"dense_depth\"]}')
args.append(f'--dropout {c[\"dropout\"]}')
args.append(f'--aug-factor {c[\"aug_factor\"]}')
args.append(f'--threshold {c[\"threshold\"]}')
if c.get('extra_features'): args.append('--extra-features')
args.append(f'--output $RESULTS/config_{c[\"id\"]}.json')
args.append(f'--data $SWEEP_DIR/data/T0.csv')
print(' '.join(args))
")
    
    echo "[Job $i] GPU=$GPU_ID: $PARAMS"
    CUDA_VISIBLE_DEVICES=$GPU_ID python3 $SWEEP_DIR/src/sweep_classifier.py $PARAMS \
        > $RESULTS/config_${i}.log 2>&1 &
    
    running=$((running + 1))
done

# Wait for all jobs to finish
echo "Waiting for remaining jobs..."
wait
echo "All done! Results in $RESULTS/"

# Summarize
python3 << 'SUMMARY'
import json, glob, os

results = []
for f in sorted(glob.glob("/homes/stevens/pvmol-sweep/results/sweep/config_*.json")):
    try:
        d = json.load(open(f))
        results.append({
            'file': os.path.basename(f),
            'f1': d['mean_f1'],
            'auc': d['mean_auc'],
            'acc': d['mean_acc'],
            'time': d['total_time_s'],
            'embed': d['params']['embed'],
            'lstm': d['params']['lstm'],
            'tdense': d['params']['tdense'],
            'lr': d['params']['lr'],
        })
    except:
        pass

results.sort(key=lambda x: x['f1'], reverse=True)
print(f"\nTop 10 by F1:")
for r in results[:10]:
    print(f"  F1={r['f1']:.4f} AUC={r['auc']:.4f} | embed={r['embed']} lstm={r['lstm']} "
          f"tdense={r['tdense']} lr={r['lr']:.1e} | {r['file']}")

results.sort(key=lambda x: x['auc'], reverse=True)
print(f"\nTop 10 by AUC:")
for r in results[:10]:
    print(f"  AUC={r['auc']:.4f} F1={r['f1']:.4f} | embed={r['embed']} lstm={r['lstm']} "
          f"tdense={r['tdense']} lr={r['lr']:.1e} | {r['file']}")
SUMMARY
RUNNER
ssh $REMOTE "chmod +x $REMOTE_DIR/run_sweep.sh"

echo ""
echo "=== Ready! ==="
echo "To launch sweep on cels-hcdgx2:"
echo "  ssh cels-hcdgx2 'cd /homes/stevens/pvmol-sweep && nohup bash run_sweep.sh 0 240 8 > sweep.log 2>&1 &'"
echo ""
echo "To monitor:"
echo "  ssh cels-hcdgx2 'ls /homes/stevens/pvmol-sweep/results/sweep/*.json | wc -l'"
echo "  ssh cels-hcdgx2 'tail -20 /homes/stevens/pvmol-sweep/sweep.log'"

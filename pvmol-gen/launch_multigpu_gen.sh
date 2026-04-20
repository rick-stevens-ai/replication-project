#!/bin/bash
# Launch 8 independent generation processes, one per GPU.
# Each generates target/8 molecules.
#
# Usage: bash launch_multigpu_gen.sh <cycle> [target]

set -e

CYCLE=${1:-1}
TARGET=${2:-100000}
MODEL_PATH="models/gpt2_finetuned/cycle_${CYCLE}/model"
KNOWN_FILE="/tmp/known_smiles_cycle${CYCLE}.txt"
GEN_DIR="data/gen_cycles"
LOG_DIR="logs"
N_GPUS=8
PER_GPU=$(( (TARGET + N_GPUS - 1) / N_GPUS ))

export LD_LIBRARY_PATH=/gpustor/stevens/anaconda3/lib:$LD_LIBRARY_PATH

mkdir -p "$GEN_DIR" "$LOG_DIR"

echo "=== Multi-GPU Generation: Cycle $CYCLE ==="
echo "  Model: $MODEL_PATH"
echo "  Target: $TARGET total ($PER_GPU per GPU)"
echo "  GPUs: $N_GPUS"

# Build known SMILES file from T1 + any previous cycles
python3 -c "
import pandas as pd
known = set()
# T1
t1 = pd.read_csv('data/t1_class1.csv')
known.update(t1['smiles'].dropna().tolist())
# Previous cycles
import os
for c in range(1, $CYCLE):
    f = 'data/gen_cycles/cycle_{}_generated.csv'.format(c)
    if os.path.exists(f):
        df = pd.read_csv(f)
        known.update(df['smiles'].dropna().tolist())
with open('$KNOWN_FILE', 'w') as f:
    f.write('\n'.join(known))
print(f'Known SMILES: {len(known)}')
"

echo "Launching $N_GPUS workers..."
PIDS=""
for GPU in $(seq 0 $((N_GPUS - 1))); do
    OUT_FILE="${GEN_DIR}/cycle_${CYCLE}_gpu${GPU}.txt"
    LOG_FILE="${LOG_DIR}/gen_cycle${CYCLE}_gpu${GPU}.log"

    python3 generate_on_gpu.py \
        --gpu $GPU \
        --model-path "$MODEL_PATH" \
        --target $PER_GPU \
        --known-file "$KNOWN_FILE" \
        --output-file "$OUT_FILE" \
        --batch-size 48 \
        > "$LOG_FILE" 2>&1 &

    PIDS="$PIDS $!"
    echo "  GPU $GPU: PID $! -> $OUT_FILE"
done

echo ""
echo "All workers launched. PIDs:$PIDS"
echo "Monitor with: tail -f logs/gen_cycle${CYCLE}_gpu*.log"
echo "Check progress: for f in ${GEN_DIR}/cycle_${CYCLE}_gpu*.txt; do wc -l \$f 2>/dev/null; done"

# Wait for all
echo ""
echo "Waiting for completion..."
for PID in $PIDS; do
    wait $PID
    echo "  PID $PID finished (exit: $?)"
done

# Combine results
echo ""
echo "Combining results..."
python3 -c "
import os
combined = set()
for gpu in range($N_GPUS):
    f = '${GEN_DIR}/cycle_${CYCLE}_gpu{}.txt'.format(gpu)
    if os.path.exists(f):
        with open(f) as fh:
            for line in fh:
                s = line.strip()
                if s:
                    combined.add(s)
print(f'Total unique CUN molecules: {len(combined)}')

# Save combined
import pandas as pd
df = pd.DataFrame({'smiles': list(combined)})
df.to_csv('${GEN_DIR}/cycle_${CYCLE}_raw.csv', index=False)
print(f'Saved to ${GEN_DIR}/cycle_${CYCLE}_raw.csv')
"

# Cleanup
rm -f "$KNOWN_FILE"
echo "Done!"

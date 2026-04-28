#!/bin/bash
# Paper-faithful replication driver.
# Hyperparameters match NukeLM paper (Burchfield et al., OSTI 1861801):
#   DAPT:     max_len=512, MLM=0.15, effective batch 256, LR 5e-5, Gururangan2020
#   Finetune: max_len=512, LR=1e-5, batch=64, 5 epochs, warmup 0.06
#
# Models covered (RoBERTa-large "NukeLM" skipped due to compute budget):
#   roberta-base, roberta-base + OSTI-DAPT, scibert
set -euo pipefail
cd "$(dirname "$0")/.."
source venv/bin/activate
source ~/env.sh

N_GPU=${N_GPU:-4}
DATA=data/processed_paper
RES=results_paper
mkdir -p "$RES"

RAW_ALL=${RAW_ALL:-"data/osti_raw.jsonl data/osti_raw_large.jsonl"}
# Combine raw files for dataset prep
cat $RAW_ALL > data/osti_raw_combined.jsonl
echo "Combined raw file line count:"
wc -l data/osti_raw_combined.jsonl

echo "=== Preparing datasets (paper-scale subset) ==="
python scripts/prepare_datasets.py \
  --raw data/osti_raw_combined.jsonl --outdir "$DATA" --topk 10 \
  --max-binary 60000 --max-mc 40000 2>&1 | tee "$RES/prepare.log"

echo "=== Preparing DAPT text ==="
python scripts/prep_txt.py \
  --jsonl data/osti_raw_combined.jsonl \
  --out-train data/dapt/train.txt --out-val data/dapt/val.txt \
  --val-frac 0.02

echo "=== DAPT: RoBERTa-base on OSTI (paper hyperparameters, scaled steps) ==="
# Paper: 13K steps; we run 1500 steps due to compute budget (documented)
torchrun --standalone --nproc_per_node=$N_GPU scripts/dapt.py \
  --train-txt data/dapt/train.txt --val-txt data/dapt/val.txt \
  --out "$RES/dapt_roberta_base" \
  --model roberta-base --block-size 512 --mlm-prob 0.15 \
  --per-device-batch 16 --grad-accum 4 --max-steps 1500 \
  --lr 5e-5 --warmup-ratio 0.06 --weight-decay 0.01 --bf16 \
  --eval-steps 250 --save-steps 1500 2>&1 | tee "$RES/dapt_roberta_base.log"

# Models to fine-tune: name -> path
declare -A MODELS=(
  ["roberta-base"]="roberta-base"
  ["roberta-base+OSTI"]="$RES/dapt_roberta_base/final"
  ["scibert"]="allenai/scibert_scivocab_uncased"
)

EPOCHS=${EPOCHS:-5}
MAX_LEN=${MAX_LEN:-512}
LR=${LR:-1e-5}
# Paper effective batch 64; with 4 GPUs use 16/device x accum 1
PER_DEV=${PER_DEV:-16}

for name in "roberta-base" "roberta-base+OSTI" "scibert"; do
  path="${MODELS[$name]}"
  safe=$(echo "$name" | tr '+/' '_')
  for task in binary multiclass; do
    out="$RES/${safe}_${task}"
    if [[ -f "$out/result.json" ]]; then
      echo "=== SKIP ($out/result.json exists) ==="; continue
    fi
    echo "=== Fine-tune $name on $task -> $out ==="
    torchrun --standalone --nproc_per_node=$N_GPU scripts/finetune.py \
      --data-dir "$DATA/$task" --task "$task" \
      --model "$path" --out "$out" \
      --epochs "$EPOCHS" --max-len "$MAX_LEN" --lr "$LR" \
      --per-device-batch "$PER_DEV" --grad-accum 1 --bf16 \
      2>&1 | tee "$RES/${safe}_${task}.log"
  done
done

echo "=== Collecting results ==="
python scripts/collect_results.py --root "$RES" --out "$RES/summary.json" \
  2>&1 | tee "$RES/summary.log"
echo "=== DONE ==="

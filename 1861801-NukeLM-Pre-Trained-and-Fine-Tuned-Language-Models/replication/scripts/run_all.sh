#!/bin/bash
# Driver: prepare data, run fine-tuning for each model on binary + multiclass,
# run mini-DAPT (MLM) demo, and fine-tune a DAPT-adapted model.
set -euo pipefail
cd "$(dirname "$0")/.."
source venv/bin/activate
source ~/env.sh

RAW=${RAW:-data/osti_raw.jsonl}
DATA=data/processed
RES=results
mkdir -p "$RES"

echo "=== Preparing datasets ==="
python scripts/prepare_datasets.py --raw "$RAW" --outdir "$DATA" --topk 10 \
  --max-binary 30000 --max-mc 30000 | tee "$RES/prepare.log"

EPOCHS=${EPOCHS:-3}
BATCH=${BATCH:-32}
MAXLEN=${MAXLEN:-256}

MODELS_SHORT=(
  "distilbert-base-uncased"
  "distilroberta-base"
)

for M in "${MODELS_SHORT[@]}"; do
  name=$(echo "$M" | tr '/' '_')
  echo "=== Fine-tune $M on BINARY ==="
  python scripts/finetune.py --data-dir "$DATA/binary" --task binary \
    --model "$M" --out "$RES/${name}_binary" \
    --epochs "$EPOCHS" --batch "$BATCH" --max-len "$MAXLEN" --bf16 \
    2>&1 | tee "$RES/${name}_binary.log"
  echo "=== Fine-tune $M on MULTICLASS ==="
  python scripts/finetune.py --data-dir "$DATA/multiclass" --task multiclass \
    --model "$M" --out "$RES/${name}_multiclass" \
    --epochs "$EPOCHS" --batch "$BATCH" --max-len "$MAXLEN" --bf16 \
    2>&1 | tee "$RES/${name}_multiclass.log"
done

echo "=== Mini-DAPT on DistilBERT ==="
python scripts/mini_mlm.py --raw "$RAW" --out "$RES/dapt_distilbert" \
  --model distilbert-base-uncased --n-docs 8000 --epochs 2 --batch 32 --bf16 \
  2>&1 | tee "$RES/dapt_distilbert.log"

echo "=== Fine-tune DAPT checkpoint on BINARY & MULTICLASS ==="
python scripts/finetune.py --data-dir "$DATA/binary" --task binary \
  --model "$RES/dapt_distilbert/final" --out "$RES/dapt_distilbert_binary" \
  --epochs "$EPOCHS" --batch "$BATCH" --max-len "$MAXLEN" --bf16 \
  2>&1 | tee "$RES/dapt_distilbert_binary.log"
python scripts/finetune.py --data-dir "$DATA/multiclass" --task multiclass \
  --model "$RES/dapt_distilbert/final" --out "$RES/dapt_distilbert_multiclass" \
  --epochs "$EPOCHS" --batch "$BATCH" --max-len "$MAXLEN" --bf16 \
  2>&1 | tee "$RES/dapt_distilbert_multiclass.log"

echo "=== ALL DONE ==="

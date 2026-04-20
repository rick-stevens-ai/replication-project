#!/bin/bash
# Cycle 2: Fine-tune GPT-2 on T2 (78K molecules), then generate 100K on 8 GPUs
set -e
export LD_LIBRARY_PATH=/gpustor/stevens/anaconda3/lib:$LD_LIBRARY_PATH

echo "=== CYCLE 2: Fine-tuning GPT-2 on T2 ==="

# Fine-tune (on GPU 0, uses the cycle 1 model as starting point)
CUDA_VISIBLE_DEVICES=0 python3 -c "
import sys, os
sys.path.insert(0, 'src')
os.makedirs('models/gpt2_finetuned/cycle_2/model', exist_ok=True)

import pandas as pd
from pathlib import Path
from generate_alternatives import finetune_gpt2, DEVICE
from utils import augment_smiles
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# Load T2
df = pd.read_csv('data/gen_cycles/t2_training.csv')
smiles = df['smiles'].dropna().tolist()
logger.info(f'T2: {len(smiles)} molecules')

# Sample + augment (full T2 is too large to augment fully)
import random
random.seed(42)
sample = random.sample(smiles, min(20000, len(smiles)))
augmented = set(sample)
for smi in sample[:5000]:
    augmented.update(augment_smiles(smi, n=3))
augmented = list(augmented)
logger.info(f'Augmented training set: {len(augmented)}')

# Load from cycle 1 model
model_path = 'models/gpt2_finetuned/cycle_1/model'
tokenizer = GPT2Tokenizer.from_pretrained(model_path)
model = GPT2LMHeadModel.from_pretrained(model_path)

# Fine-tune
model = finetune_gpt2(augmented, tokenizer, model, epochs=30, patience=5)

# Save
out = 'models/gpt2_finetuned/cycle_2/model'
model.save_pretrained(out)
tokenizer.save_pretrained(out)
logger.info(f'Saved cycle 2 model to {out}')
" 2>&1 | tee logs/cycle2_finetune.log

echo "=== Fine-tuning complete. Launching 8-GPU generation ==="
bash launch_multigpu_gen.sh 2 100000 2>&1 | tee logs/launch_multigpu_cycle2.log

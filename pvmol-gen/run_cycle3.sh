#!/bin/bash
set -e
export LD_LIBRARY_PATH=/gpustor/stevens/anaconda3/lib:$LD_LIBRARY_PATH

echo "=== CYCLE 3: Fine-tuning GPT-2 on T3 ==="

CUDA_VISIBLE_DEVICES=0 python3 -c "
import sys, os, random
sys.path.insert(0, 'src')
os.makedirs('models/gpt2_finetuned/cycle_3/model', exist_ok=True)

import pandas as pd
from generate_alternatives import finetune_gpt2
from utils import augment_smiles
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

df = pd.read_csv('data/gen_cycles/t3_training.csv')
smiles = df['smiles'].dropna().tolist()
logger.info(f'T3: {len(smiles)} molecules')

random.seed(42)
sample = random.sample(smiles, min(20000, len(smiles)))
augmented = set(sample)
for smi in sample[:5000]:
    augmented.update(augment_smiles(smi, n=3))
augmented = list(augmented)
logger.info(f'Augmented training set: {len(augmented)}')

model_path = 'models/gpt2_finetuned/cycle_2/model'
tokenizer = GPT2Tokenizer.from_pretrained(model_path)
model = GPT2LMHeadModel.from_pretrained(model_path)
model = finetune_gpt2(augmented, tokenizer, model, epochs=30, patience=5)

out = 'models/gpt2_finetuned/cycle_3/model'
model.save_pretrained(out)
tokenizer.save_pretrained(out)
logger.info(f'Saved cycle 3 model to {out}')
" 2>&1 | tee logs/cycle3_finetune.log

echo "=== Fine-tuning complete. Launching 8-GPU generation ==="
bash launch_multigpu_gen.sh 3 100000 2>&1 | tee logs/launch_multigpu_cycle3.log

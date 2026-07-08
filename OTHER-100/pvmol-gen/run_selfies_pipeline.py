"""Complete SELFIES-based generative pipeline — 3 cycles on 8 GPUs.

Replaces SMILES with SELFIES for GPT-2 training and generation.
Classifier remains SMILES-based (convert back for classification).
"""

import json
import logging
import os
import pickle
import random
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader, random_split
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from rdkit import Chem, RDLogger
import selfies as sf

RDLogger.DisableLog("rdApp.*")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from config import (
    T1_FILE, RESULTS_DIR, CLASSIFIER_DIR,
    CLASSIFICATION_THRESHOLD, NUM_GEN_CYCLES, GEN_TARGET_PER_CYCLE,
)
from utils import validate_smiles, augment_smiles
from stage1_classifier import predict_class
from stage1b_pubchem_augment import _compute_extra_features

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/selfies_pipeline.log"),
    ],
)
logger = logging.getLogger(__name__)

N_GPUS = torch.cuda.device_count()
SELFIES_DIR = Path("models/gpt2_selfies")
GEN_DIR = Path("data/gen_selfies")
EPOCHS = 30
PATIENCE = 5
BATCH_TRAIN = 4
MAX_LENGTH = 128


def smiles_to_selfies(smiles_list):
    """Convert SMILES list to SELFIES, with augmentation."""
    selfies = set()
    failed = 0
    for smi in smiles_list:
        try:
            se = sf.encoder(smi)
            if se:
                selfies.add(se)
        except:
            failed += 1
        # Also augment: random SMILES → SELFIES for diversity
        for aug in augment_smiles(smi, n=3):
            try:
                se = sf.encoder(aug)
                if se:
                    selfies.add(se)
            except:
                pass
    logger.info(f"  Converted {len(smiles_list)} SMILES → {len(selfies)} unique SELFIES ({failed} failed)")
    return list(selfies)


def finetune_gpt2_selfies(selfies_list, cycle, prev_model_path=None):
    """Fine-tune GPT-2 on SELFIES strings."""
    logger.info(f"  Fine-tuning GPT-2 on {len(selfies_list)} SELFIES (cycle {cycle})...")

    device = torch.device("cuda:0")

    if prev_model_path and Path(prev_model_path).exists():
        tokenizer = GPT2Tokenizer.from_pretrained(prev_model_path)
        model = GPT2LMHeadModel.from_pretrained(prev_model_path)
        logger.info(f"  Loaded model from {prev_model_path}")
    else:
        local_cache = Path("models/gpt2_pretrained")
        if local_cache.exists():
            tokenizer = GPT2Tokenizer.from_pretrained(str(local_cache))
            model = GPT2LMHeadModel.from_pretrained(str(local_cache))
        else:
            tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
            model = GPT2LMHeadModel.from_pretrained("gpt2")

    if tokenizer.pad_token is None:
        tokenizer.add_special_tokens({"pad_token": "[PAD]"})
    tokenizer.padding_side = "left"
    model.resize_token_embeddings(len(tokenizer))

    # Cap training data for speed if very large
    if len(selfies_list) > 50000:
        random.seed(42 + cycle)
        selfies_list = random.sample(selfies_list, 50000)
        logger.info(f"  Sampled to {len(selfies_list)} for training")

    encoded = tokenizer(selfies_list, padding=True, truncation=True,
                        max_length=MAX_LENGTH, return_tensors="pt")

    class DS(Dataset):
        def __init__(self, enc):
            self.ids = enc["input_ids"]
            self.mask = enc["attention_mask"]
        def __len__(self): return len(self.ids)
        def __getitem__(self, i):
            return {"input_ids": self.ids[i], "attention_mask": self.mask[i], "labels": self.ids[i]}

    def collate(batch):
        return {k: torch.stack([b[k] for b in batch]) for k in batch[0]}

    dataset = DS(encoded)
    train_n = int(0.8 * len(dataset))
    train_ds, val_ds = random_split(dataset, [train_n, len(dataset) - train_n])
    train_loader = DataLoader(train_ds, batch_size=BATCH_TRAIN, shuffle=True, collate_fn=collate)
    val_loader = DataLoader(val_ds, batch_size=BATCH_TRAIN, collate_fn=collate)

    model = model.to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5, weight_decay=0.01)
    scaler = torch.amp.GradScaler("cuda")

    best_val = float("inf")
    best_state = None
    no_improve = 0

    for epoch in range(EPOCHS):
        model.train()
        total = 0
        for batch in train_loader:
            ids = batch["input_ids"].to(device)
            mask = batch["attention_mask"].to(device)
            optimizer.zero_grad()
            with torch.amp.autocast("cuda", dtype=torch.float16):
                out = model(input_ids=ids, attention_mask=mask, labels=ids)
            scaler.scale(out.loss).backward()
            scaler.step(optimizer)
            scaler.update()
            total += out.loss.item()

        model.eval()
        val_loss = 0
        with torch.no_grad():
            for batch in val_loader:
                ids = batch["input_ids"].to(device)
                mask = batch["attention_mask"].to(device)
                out = model(input_ids=ids, attention_mask=mask, labels=ids)
                val_loss += out.loss.item()
        val_loss /= max(len(val_loader), 1)

        if (epoch + 1) % 5 == 0:
            logger.info(f"    Epoch {epoch+1}: train={total/len(train_loader):.4f} val={val_loss:.4f}")

        if val_loss < best_val:
            best_val = val_loss
            best_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}
            no_improve = 0
        else:
            no_improve += 1
        if no_improve >= PATIENCE:
            logger.info(f"    Early stopping at epoch {epoch+1}")
            break

    if best_state:
        model.load_state_dict(best_state)

    # Save
    cycle_dir = SELFIES_DIR / f"cycle_{cycle}"
    cycle_dir.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(str(cycle_dir))
    tokenizer.save_pretrained(str(cycle_dir))
    logger.info(f"  Model saved to {cycle_dir}")

    del model, optimizer, scaler
    torch.cuda.empty_cache()
    return str(cycle_dir)


def generate_multigpu(model_path, target, known_smiles, cycle):
    """Launch 8 GPU workers for SELFIES generation."""
    per_gpu = target // N_GPUS + 1

    known_file = f"/tmp/known_selfies_cycle{cycle}.txt"
    with open(known_file, "w") as f:
        f.write("\n".join(known_smiles))

    GEN_DIR.mkdir(parents=True, exist_ok=True)
    procs = []
    output_files = []

    logger.info(f"  Generating {target} molecules across {N_GPUS} GPUs...")

    for gpu in range(N_GPUS):
        out_file = str(GEN_DIR / f"cycle_{cycle}_gpu{gpu}.txt")
        log_file = f"logs/selfies_cycle{cycle}_gpu{gpu}.log"
        output_files.append(out_file)

        env = os.environ.copy()
        env["LD_LIBRARY_PATH"] = f"/gpustor/stevens/anaconda3/lib:{env.get('LD_LIBRARY_PATH', '')}"

        p = subprocess.Popen(
            ["python3", "generate_selfies_gpu.py",
             "--gpu", str(gpu),
             "--model-path", model_path,
             "--target", str(per_gpu),
             "--known-file", known_file,
             "--output-file", out_file,
             "--batch-size", "64",
             "--temperature", "0.9",
             "--max-length", "128"],
            stdout=open(log_file, "w"),
            stderr=subprocess.STDOUT,
            env=env,
        )
        procs.append(p)
        logger.info(f"    GPU {gpu}: PID {p.pid}")

    # Monitor
    t0 = time.time()
    while any(p.poll() is None for p in procs):
        time.sleep(30)
        total = 0
        for f in output_files:
            if os.path.exists(f):
                with open(f) as fh:
                    total += sum(1 for _ in fh)
        elapsed = time.time() - t0
        rate = total / elapsed if elapsed > 0 else 0
        eta = (target - total) / rate / 60 if rate > 0 else 0
        logger.info(f"    Progress: {total}/{target} ({rate:.1f}/s, ETA {eta:.0f}min)")
        if total >= target:
            break

    for p in procs:
        p.wait(timeout=120)

    # Combine
    all_generated = set()
    for f in output_files:
        if os.path.exists(f):
            with open(f) as fh:
                for line in fh:
                    s = line.strip()
                    if s:
                        all_generated.add(s)

    novel = all_generated - known_smiles
    elapsed = time.time() - t0
    logger.info(f"  Generation complete: {len(novel)} CUN molecules in {elapsed/60:.1f}min")

    os.remove(known_file)
    return list(novel)


def classify_molecules(smiles_list, tokenizer):
    """Classify with SMILES-X classifier."""
    if not smiles_list:
        return [], []
    extra = [_compute_extra_features(s) for s in smiles_list]
    probs = predict_class(smiles_list, tokenizer, extra_features=extra)
    preds = (probs >= CLASSIFICATION_THRESHOLD).astype(int)
    return probs, preds


def main():
    GEN_DIR.mkdir(parents=True, exist_ok=True)
    SELFIES_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # Load classifier
    with open(CLASSIFIER_DIR / "tokenizer.pkl", "rb") as f:
        cls_tokenizer = pickle.load(f)

    # Load T1
    t1 = pd.read_csv(T1_FILE)["smiles"].dropna().tolist()
    training_smiles = set(t1)
    all_known = set(t1)
    logger.info(f"T1: {len(training_smiles)} SMILES")

    cycle_stats = []

    for cycle in range(1, NUM_GEN_CYCLES + 1):
        logger.info(f"\n{'='*60}")
        logger.info(f"SELFIES CYCLE {cycle}/{NUM_GEN_CYCLES}")
        logger.info(f"Training set: {len(training_smiles)} SMILES")
        logger.info(f"{'='*60}")
        t_start = time.time()

        # Convert to SELFIES
        selfies_list = smiles_to_selfies(list(training_smiles))

        # Fine-tune
        prev = str(SELFIES_DIR / f"cycle_{cycle-1}") if cycle > 1 else None
        model_path = finetune_gpt2_selfies(selfies_list, cycle, prev_model_path=prev)

        # Generate on all 8 GPUs
        new_molecules = generate_multigpu(model_path, GEN_TARGET_PER_CYCLE, all_known, cycle)
        logger.info(f"Cycle {cycle}: {len(new_molecules)} CUN molecules")

        # Classify
        probs, preds = classify_molecules(new_molecules, cls_tokenizer)
        class1 = [s for s, p in zip(new_molecules, preds) if p == 1]
        logger.info(f"Cycle {cycle}: {len(class1)} class 1 ({len(class1)/max(len(new_molecules),1)*100:.1f}%)")

        # Save
        pd.DataFrame({
            "smiles": new_molecules,
            "prob_class1": probs if len(new_molecules) > 0 else [],
            "pred_class1": preds if len(new_molecules) > 0 else [],
        }).to_csv(GEN_DIR / f"cycle_{cycle}_generated.csv", index=False)

        # Update training set
        training_smiles.update(class1)
        all_known.update(new_molecules)

        elapsed = time.time() - t_start
        cycle_stats.append({
            "cycle": cycle,
            "training_size": len(training_smiles),
            "generated": len(new_molecules),
            "class1": len(class1),
            "class1_pct": len(class1) / max(len(new_molecules), 1) * 100,
            "time_min": elapsed / 60,
        })
        logger.info(f"Cycle {cycle}: {elapsed/60:.1f} min")
        torch.cuda.empty_cache()

    # Combine all class 1
    all_class1 = set()
    for cycle in range(1, NUM_GEN_CYCLES + 1):
        cdf = pd.read_csv(GEN_DIR / f"cycle_{cycle}_generated.csv")
        all_class1.update(cdf[cdf["pred_class1"] == 1]["smiles"].tolist())

    pd.DataFrame({"smiles": list(all_class1)}).to_csv(
        GEN_DIR / "all_generated_class1.csv", index=False)

    # Save stats
    stats = pd.DataFrame(cycle_stats)
    stats.to_csv(RESULTS_DIR / "selfies_cycle_stats.csv", index=False)
    logger.info(f"\n{stats.to_string()}")
    logger.info(f"\nTotal class 1: {len(all_class1)}")
    logger.info(f"Saved to {GEN_DIR}/all_generated_class1.csv")


if __name__ == "__main__":
    main()

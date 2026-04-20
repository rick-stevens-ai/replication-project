"""Multi-GPU GPT-2 generation for Stage 2.

Splits generation target across all available GPUs. Each GPU runs an
independent generation loop with a shared known-SMILES set (via file).
Reuses the already fine-tuned model from cycle_1.

For subsequent cycles, retrains on the expanded dataset then generates again.
"""

import json
import logging
import os
import pickle
import sys
import time
from multiprocessing import Process, Queue, Value
from pathlib import Path
from ctypes import c_long

import numpy as np
import pandas as pd
import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from rdkit import Chem, RDLogger

RDLogger.DisableLog("rdApp.*")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from config import (
    T1_FILE, GEN_CYCLE_DIR, GPT2_DIR, RESULTS_DIR, CLASSIFIER_DIR,
    NUM_GEN_CYCLES, SMILES_AUGMENTATIONS,
    GEN_TARGET_PER_CYCLE, GEN_TEMPERATURE, GEN_MAX_LENGTH,
    GPT2_TRAIN_EPOCHS, GPT2_BATCH_SIZE,
    GPT2_WARMUP_STEPS, GPT2_WEIGHT_DECAY, GPT2_EARLY_STOPPING_PATIENCE,
    CLASSIFICATION_THRESHOLD,
)
from utils import validate_smiles, augment_smiles

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/stage2_multigpu.log"),
    ],
)
logger = logging.getLogger(__name__)

N_GPUS = torch.cuda.device_count()
logger.info(f"Available GPUs: {N_GPUS}")


def generate_on_gpu(gpu_id, model_path, target_count, known_smiles_file,
                    output_file, counter, gen_batch_size=48):
    """Generate molecules on a single GPU. Runs as a separate process."""
    device = torch.device(f"cuda:{gpu_id}")

    tokenizer = GPT2Tokenizer.from_pretrained(model_path)
    model = GPT2LMHeadModel.from_pretrained(model_path).to(device)
    model.eval()

    # Load known SMILES
    with open(known_smiles_file, "r") as f:
        known = set(f.read().strip().split("\n"))

    pad_id = tokenizer.encode("[PAD]", add_special_tokens=False)
    input_ids = torch.tensor([pad_id]).to(device)

    generated = set()
    attempts = 0
    max_attempts = target_count * 200  # allow more attempts given low valid rate
    t0 = time.time()

    while len(generated) < target_count and attempts < max_attempts:
        try:
            batch_input = input_ids.repeat(gen_batch_size, 1)
            attention_mask = torch.ones_like(batch_input)

            with torch.no_grad():
                outputs = model.generate(
                    batch_input,
                    attention_mask=attention_mask,
                    max_length=GEN_MAX_LENGTH,
                    num_return_sequences=gen_batch_size,
                    temperature=GEN_TEMPERATURE,
                    do_sample=True,
                    pad_token_id=tokenizer.pad_token_id,
                )

            for seq in outputs:
                smiles = tokenizer.decode(seq, skip_special_tokens=True).strip()
                canon = validate_smiles(smiles)
                if canon and canon not in generated and canon not in known:
                    generated.add(canon)
                    with counter.get_lock():
                        counter.value += 1
                attempts += 1

        except Exception as e:
            attempts += gen_batch_size

        # Progress every 60s
        elapsed = time.time() - t0
        if int(elapsed) % 60 < 2 and elapsed > 10:
            total = counter.value
            rate = total / elapsed if elapsed > 0 else 0
            valid_pct = total / max(attempts, 1) * 100
            print(f"  GPU {gpu_id}: {len(generated)} local, {total} global, "
                  f"{valid_pct:.1f}% valid, {rate:.1f}/s", flush=True)

    elapsed = time.time() - t0
    print(f"  GPU {gpu_id}: DONE — {len(generated)} molecules in {elapsed/60:.1f} min",
          flush=True)

    # Save results
    with open(output_file, "w") as f:
        for smi in generated:
            f.write(smi + "\n")


def generate_multigpu(model_path, target_count, known_smiles, cycle):
    """Distribute generation across all GPUs."""
    logger.info(f"Generating {target_count} molecules across {N_GPUS} GPUs")

    per_gpu = target_count // N_GPUS + 1

    # Write known SMILES to temp file for sharing
    known_file = f"/tmp/known_smiles_cycle{cycle}.txt"
    with open(known_file, "w") as f:
        f.write("\n".join(known_smiles))

    counter = Value(c_long, 0)
    processes = []
    output_files = []

    for gpu_id in range(N_GPUS):
        out_file = str(GEN_CYCLE_DIR / f"cycle_{cycle}_gpu{gpu_id}.txt")
        output_files.append(out_file)
        p = Process(
            target=generate_on_gpu,
            args=(gpu_id, str(model_path), per_gpu, known_file, out_file, counter),
        )
        processes.append(p)

    t0 = time.time()
    for p in processes:
        p.start()

    # Monitor progress
    while any(p.is_alive() for p in processes):
        time.sleep(30)
        total = counter.value
        elapsed = time.time() - t0
        rate = total / elapsed if elapsed > 0 else 0
        eta = (target_count - total) / rate / 60 if rate > 0 else 0
        logger.info(f"  Progress: {total}/{target_count} ({total/target_count*100:.1f}%) "
                    f"rate={rate:.1f}/s ETA={eta:.0f}min")
        if total >= target_count:
            break

    for p in processes:
        p.join(timeout=60)

    # Collect all results
    all_generated = set()
    for out_file in output_files:
        if os.path.exists(out_file):
            with open(out_file, "r") as f:
                for line in f:
                    smi = line.strip()
                    if smi:
                        all_generated.add(smi)

    # Deduplicate against known
    novel = all_generated - known_smiles
    elapsed = time.time() - t0
    logger.info(f"Generation complete: {len(novel)} CUN molecules in {elapsed/60:.1f} min")

    # Cleanup
    os.remove(known_file)
    for f in output_files:
        if os.path.exists(f):
            os.remove(f)

    return list(novel)


def finetune_gpt2(smiles_list, cycle, output_dir):
    """Fine-tune GPT-2 on SMILES (single GPU, training is fast)."""
    from torch.utils.data import Dataset, DataLoader, random_split

    logger.info(f"Cycle {cycle}: Fine-tuning GPT-2 on {len(smiles_list)} SMILES")

    # Augment
    augmented = set()
    for smi in smiles_list:
        augmented.update(augment_smiles(smi, n=SMILES_AUGMENTATIONS))
    augmented = list(augmented)
    logger.info(f"Augmented to {len(augmented)} unique SMILES")

    # Load model (from previous cycle or pretrained)
    prev_cycle = output_dir / f"cycle_{cycle-1}" / "model"
    if prev_cycle.exists() and cycle > 1:
        tokenizer = GPT2Tokenizer.from_pretrained(str(prev_cycle))
        model = GPT2LMHeadModel.from_pretrained(str(prev_cycle))
        logger.info(f"Loaded model from cycle {cycle-1}")
    else:
        local_cache = Path(__file__).resolve().parent / "models" / "gpt2_pretrained"
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

    encoded = tokenizer(augmented, padding=True, truncation=True,
                        max_length=GEN_MAX_LENGTH, return_tensors="pt")

    class SMIDataset(Dataset):
        def __init__(self, enc):
            self.ids = enc["input_ids"]
            self.mask = enc["attention_mask"]
        def __len__(self):
            return len(self.ids)
        def __getitem__(self, i):
            return {"input_ids": self.ids[i], "attention_mask": self.mask[i], "labels": self.ids[i]}

    dataset = SMIDataset(encoded)
    train_n = int(0.8 * len(dataset))
    train_ds, val_ds = random_split(dataset, [train_n, len(dataset) - train_n])

    device = torch.device("cuda:0")
    model = model.to(device)

    def collate(batch):
        return {k: torch.stack([b[k] for b in batch]) for k in batch[0]}

    train_loader = DataLoader(train_ds, batch_size=GPT2_BATCH_SIZE, shuffle=True, collate_fn=collate)
    val_loader = DataLoader(val_ds, batch_size=GPT2_BATCH_SIZE, collate_fn=collate)

    optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5, weight_decay=GPT2_WEIGHT_DECAY)
    scaler = torch.amp.GradScaler("cuda")

    cycle_dir = output_dir / f"cycle_{cycle}"
    cycle_dir.mkdir(parents=True, exist_ok=True)

    best_val_loss = float("inf")
    patience = 0

    for epoch in range(GPT2_TRAIN_EPOCHS):
        model.train()
        total_loss = 0
        for batch in train_loader:
            ids = batch["input_ids"].to(device)
            mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)
            optimizer.zero_grad()
            with torch.amp.autocast("cuda", dtype=torch.float16):
                out = model(input_ids=ids, attention_mask=mask, labels=labels)
            scaler.scale(out.loss).backward()
            scaler.step(optimizer)
            scaler.update()
            total_loss += out.loss.item()
        train_loss = total_loss / len(train_loader)

        model.eval()
        val_loss = 0
        with torch.no_grad():
            for batch in val_loader:
                ids = batch["input_ids"].to(device)
                mask = batch["attention_mask"].to(device)
                labels = batch["labels"].to(device)
                out = model(input_ids=ids, attention_mask=mask, labels=labels)
                val_loss += out.loss.item()
        val_loss /= len(val_loader)

        if (epoch + 1) % 5 == 0:
            logger.info(f"  Epoch {epoch+1}: train={train_loss:.4f} val={val_loss:.4f}")

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            patience = 0
            model.save_pretrained(str(cycle_dir / "model"))
            tokenizer.save_pretrained(str(cycle_dir / "model"))
        else:
            patience += 1

        if patience >= GPT2_EARLY_STOPPING_PATIENCE:
            logger.info(f"  Early stopping at epoch {epoch+1}")
            break

    del model, optimizer, scaler
    torch.cuda.empty_cache()
    logger.info(f"Cycle {cycle}: best val_loss={best_val_loss:.4f}")

    return cycle_dir / "model"


def main():
    GEN_CYCLE_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # Load classifier for prediction
    with open(CLASSIFIER_DIR / "tokenizer.pkl", "rb") as f:
        cls_tokenizer = pickle.load(f)

    sys.path.insert(0, str(Path(__file__).parent / "src"))
    from stage1_classifier import predict_class

    # Load T1
    t1_df = pd.read_csv(T1_FILE)
    smi_col = [c for c in t1_df.columns if "smiles" in c.lower()][0]
    training_smiles = set(t1_df[smi_col].dropna().tolist())
    all_known = set(training_smiles)
    logger.info(f"Initial T1: {len(training_smiles)} class 1 SMILES")

    cycle_stats = []

    for cycle in range(1, NUM_GEN_CYCLES + 1):
        logger.info(f"\n{'='*60}")
        logger.info(f"GENERATIVE CYCLE {cycle}/{NUM_GEN_CYCLES}")
        logger.info(f"Training set: {len(training_smiles)} SMILES")
        logger.info(f"{'='*60}")

        t_start = time.time()

        # Fine-tune (skip cycle 1 if model already exists)
        model_path = GPT2_DIR / f"cycle_{cycle}" / "model"
        if model_path.exists() and cycle == 1:
            logger.info(f"Cycle {cycle}: Reusing existing fine-tuned model")
        else:
            model_path = finetune_gpt2(list(training_smiles), cycle, GPT2_DIR)

        # Generate across all GPUs
        new_molecules = generate_multigpu(
            model_path, GEN_TARGET_PER_CYCLE, all_known, cycle
        )
        logger.info(f"Cycle {cycle}: {len(new_molecules)} CUN molecules generated")

        # Classify
        if new_molecules:
            # Compute extra features
            from stage1b_pubchem_augment import _compute_extra_features
            extra = [_compute_extra_features(s) for s in new_molecules]
            probs = predict_class(new_molecules, cls_tokenizer, extra_features=extra)
            preds = (probs >= CLASSIFICATION_THRESHOLD).astype(int)
            class1 = [s for s, p in zip(new_molecules, preds) if p == 1]
            logger.info(f"Cycle {cycle}: {len(class1)} class 1 ({len(class1)/len(new_molecules)*100:.1f}%)")
        else:
            class1 = []

        # Save cycle output
        cycle_df = pd.DataFrame({
            "smiles": new_molecules,
            "prob_class1": probs if new_molecules else [],
            "pred_class1": preds if new_molecules else [],
        })
        cycle_df.to_csv(GEN_CYCLE_DIR / f"cycle_{cycle}_generated.csv", index=False)

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
        logger.info(f"Cycle {cycle}: {elapsed/60:.1f} minutes")

        torch.cuda.empty_cache()

    # Save stats
    pd.DataFrame(cycle_stats).to_csv(RESULTS_DIR / "generative_cycle_stats.csv", index=False)

    # Combine all class 1
    all_class1 = []
    for cycle in range(1, NUM_GEN_CYCLES + 1):
        cdf = pd.read_csv(GEN_CYCLE_DIR / f"cycle_{cycle}_generated.csv")
        all_class1.extend(cdf[cdf["pred_class1"] == 1]["smiles"].tolist())
    all_class1 = list(set(all_class1))
    pd.DataFrame({"smiles": all_class1}).to_csv(
        GEN_CYCLE_DIR / "all_generated_class1.csv", index=False
    )
    logger.info(f"\nTotal generated class 1: {len(all_class1)}")


if __name__ == "__main__":
    main()

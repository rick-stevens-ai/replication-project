"""
Stage 2: Iterative GPT-2 molecular generation.
Pure PyTorch implementation (no HuggingFace Trainer — avoids tf-keras conflicts on Polaris).

Steps:
  1. Fine-tune GPT-2 on Data T1 (class 1 SMILES)
  2. Generate molecules, classify with SMILES-X
  3. Feed predicted class 1 back into training set
  4. Repeat for 3 cycles
  5. Track CUN metrics (Chemically valid, Unique, Novel)
"""
import logging
import math
import os
import pickle
import time
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader, random_split
from torch.amp import autocast, GradScaler
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from rdkit import Chem
from tqdm import tqdm

from config import (
    T1_FILE, GEN_CYCLE_DIR, GPT2_DIR, RESULTS_DIR, CLASSIFIER_DIR,
    GPT2_MODEL_NAME, NUM_GEN_CYCLES, SMILES_AUGMENTATIONS,
    GEN_TARGET_PER_CYCLE, GEN_TEMPERATURE, GEN_MAX_LENGTH,
    GPT2_TRAIN_EPOCHS, GPT2_BATCH_SIZE, GPT2_WARMUP_STEPS,
    GPT2_WEIGHT_DECAY, GPT2_EARLY_STOPPING_PATIENCE,
    CLASSIFICATION_THRESHOLD, DEVICE
)
from utils import validate_smiles, augment_smiles

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


# ─── SMILES Dataset for GPT-2 ───────────────────────────
class SmilesGPTDataset(Dataset):
    def __init__(self, encoded_inputs):
        self.input_ids = encoded_inputs["input_ids"]
        self.attention_mask = encoded_inputs["attention_mask"]

    def __len__(self):
        return len(self.input_ids)

    def __getitem__(self, idx):
        return {
            "input_ids": self.input_ids[idx],
            "attention_mask": self.attention_mask[idx],
            "labels": self.input_ids[idx],
        }


def _collate_fn(batch):
    return {
        "input_ids": torch.stack([b["input_ids"] for b in batch]),
        "attention_mask": torch.stack([b["attention_mask"] for b in batch]),
        "labels": torch.stack([b["labels"] for b in batch]),
    }


# ─── GPT-2 Training (pure PyTorch) ──────────────────────
def finetune_gpt2(smiles_list: list, cycle: int, output_dir: Path):
    """Fine-tune GPT-2 on a list of SMILES strings."""
    logger.info(f"Cycle {cycle}: Fine-tuning GPT-2 on {len(smiles_list)} SMILES")

    # Augment SMILES
    augmented = []
    for smi in tqdm(smiles_list, desc="Augmenting SMILES"):
        augmented.extend(augment_smiles(smi, n=SMILES_AUGMENTATIONS))
    augmented = list(set(augmented))
    logger.info(f"Augmented to {len(augmented)} SMILES")

    # Load from local cache (offline compute nodes)
    local_cache = Path(__file__).resolve().parent.parent / "models" / "gpt2_pretrained"
    if local_cache.exists():
        tokenizer = GPT2Tokenizer.from_pretrained(str(local_cache))
        model = GPT2LMHeadModel.from_pretrained(str(local_cache))
    else:
        tokenizer = GPT2Tokenizer.from_pretrained(GPT2_MODEL_NAME)
        model = GPT2LMHeadModel.from_pretrained(GPT2_MODEL_NAME)

    if tokenizer.pad_token is None:
        tokenizer.add_special_tokens({"pad_token": "[PAD]"})
    tokenizer.padding_side = "left"  # Required for decoder-only generation
    model.resize_token_embeddings(len(tokenizer))

    # Tokenize
    encoded = tokenizer(augmented, padding=True, truncation=True,
                        max_length=GEN_MAX_LENGTH, return_tensors="pt")

    dataset = SmilesGPTDataset(encoded)
    train_size = int(0.8 * len(dataset))
    test_size = len(dataset) - train_size
    train_ds, test_ds = random_split(dataset, [train_size, test_size])

    device = torch.device(DEVICE)
    model = model.to(device)

    train_loader = DataLoader(train_ds, batch_size=GPT2_BATCH_SIZE, shuffle=True,
                              collate_fn=_collate_fn, num_workers=4, pin_memory=True)
    test_loader = DataLoader(test_ds, batch_size=GPT2_BATCH_SIZE,
                             collate_fn=_collate_fn, num_workers=2, pin_memory=True)

    # Optimizer with weight decay
    no_decay = ["bias", "LayerNorm.weight"]
    optimizer_grouped = [
        {"params": [p for n, p in model.named_parameters()
                    if not any(nd in n for nd in no_decay)],
         "weight_decay": GPT2_WEIGHT_DECAY},
        {"params": [p for n, p in model.named_parameters()
                    if any(nd in n for nd in no_decay)],
         "weight_decay": 0.0},
    ]
    optimizer = torch.optim.AdamW(optimizer_grouped, lr=5e-5)

    # Warmup + linear decay scheduler
    total_steps = len(train_loader) * GPT2_TRAIN_EPOCHS
    warmup_steps = min(GPT2_WARMUP_STEPS, total_steps // 5)

    def lr_lambda(step):
        if step < warmup_steps:
            return step / max(1, warmup_steps)
        return max(0.0, (total_steps - step) / max(1, total_steps - warmup_steps))

    scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda)
    scaler = GradScaler("cuda") if device.type == "cuda" else None

    cycle_dir = output_dir / f"cycle_{cycle}"
    cycle_dir.mkdir(parents=True, exist_ok=True)

    best_val_loss = float("inf")
    patience_counter = 0

    for epoch in range(GPT2_TRAIN_EPOCHS):
        # Training
        model.train()
        total_train_loss = 0
        for batch in train_loader:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)

            optimizer.zero_grad()
            if scaler:
                with autocast("cuda", dtype=torch.float16):
                    outputs = model(input_ids=input_ids,
                                    attention_mask=attention_mask,
                                    labels=labels)
                    loss = outputs.loss
                scaler.scale(loss).backward()
                scaler.step(optimizer)
                scaler.update()
            else:
                outputs = model(input_ids=input_ids,
                                attention_mask=attention_mask,
                                labels=labels)
                loss = outputs.loss
                loss.backward()
                optimizer.step()

            scheduler.step()
            total_train_loss += loss.item()

        avg_train_loss = total_train_loss / len(train_loader)

        # Validation
        model.eval()
        total_val_loss = 0
        with torch.no_grad():
            for batch in test_loader:
                input_ids = batch["input_ids"].to(device)
                attention_mask = batch["attention_mask"].to(device)
                labels = batch["labels"].to(device)
                outputs = model(input_ids=input_ids,
                                attention_mask=attention_mask,
                                labels=labels)
                total_val_loss += outputs.loss.item()
        avg_val_loss = total_val_loss / len(test_loader)

        if (epoch + 1) % 5 == 0:
            logger.info(f"  Epoch {epoch+1}/{GPT2_TRAIN_EPOCHS}: "
                        f"train_loss={avg_train_loss:.4f} val_loss={avg_val_loss:.4f}")

        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            patience_counter = 0
            # Save best
            model.save_pretrained(str(cycle_dir / "model"))
            tokenizer.save_pretrained(str(cycle_dir / "model"))
        else:
            patience_counter += 1

        if patience_counter >= GPT2_EARLY_STOPPING_PATIENCE:
            logger.info(f"  Early stopping at epoch {epoch+1}")
            break

    # Free optimizer/scaler memory, then load best model fresh
    del optimizer, scheduler
    if scaler:
        del scaler
    del model
    torch.cuda.empty_cache()

    model = GPT2LMHeadModel.from_pretrained(str(cycle_dir / "model")).to(device)
    logger.info(f"Cycle {cycle}: Model saved to {cycle_dir / 'model'}")
    logger.info(f"  Best val_loss: {best_val_loss:.4f}")
    if device.type == "cuda":
        logger.info(f"  GPU memory after reload: {torch.cuda.memory_allocated()/1e9:.2f} GB")

    return model, tokenizer


# ─── Generation ──────────────────────────────────────────
def generate_molecules(model, tokenizer, target_count: int,
                       known_smiles: set, device: str = DEVICE) -> list:
    """Generate novel, valid, unique SMILES using the fine-tuned model."""
    model.to(device)
    model.eval()

    generated = set()
    attempts = 0
    max_attempts = target_count * 100
    batch_size = 32  # keep modest to avoid OOM during generation

    pad_id = tokenizer.encode("[PAD]", add_special_tokens=False)
    input_ids = torch.tensor([pad_id]).to(device)

    logger.info(f"Generating up to {target_count} molecules...")
    pbar = tqdm(total=target_count, desc="Generating")
    t0 = time.time()

    while len(generated) < target_count and attempts < max_attempts:
        try:
            batch_input = input_ids.repeat(batch_size, 1)
            attention_mask = torch.ones_like(batch_input)

            with torch.no_grad():
                outputs = model.generate(
                    batch_input,
                    attention_mask=attention_mask,
                    max_length=GEN_MAX_LENGTH,
                    num_return_sequences=batch_size,
                    temperature=GEN_TEMPERATURE,
                    do_sample=True,
                    pad_token_id=tokenizer.pad_token_id,
                )

            new_this_batch = 0
            for seq in outputs:
                smiles = tokenizer.decode(seq, skip_special_tokens=True).strip()
                canon = validate_smiles(smiles)
                if canon and canon not in generated and canon not in known_smiles:
                    generated.add(canon)
                    new_this_batch += 1
                attempts += 1

            pbar.update(new_this_batch)

            # Progress logging every 10K
            if len(generated) % 10000 < batch_size and len(generated) > 0:
                elapsed = time.time() - t0
                rate = len(generated) / elapsed
                eta = (target_count - len(generated)) / rate if rate > 0 else 0
                valid_pct = len(generated) / max(attempts, 1) * 100
                logger.info(f"  Progress: {len(generated)}/{target_count} "
                            f"({valid_pct:.1f}% valid, {rate:.0f}/s, ETA {eta/60:.0f}min)")

        except Exception as e:
            logger.warning(f"Generation error: {e}")
            attempts += batch_size

    pbar.close()
    elapsed = time.time() - t0
    valid_pct = len(generated) / max(attempts, 1) * 100
    logger.info(f"Generated {len(generated)} CUN molecules in {elapsed:.0f}s "
                f"({valid_pct:.1f}% valid rate)")

    return list(generated)


# ─── Iterative Cycle ─────────────────────────────────────
def run_generative_cycles():
    """Run the full iterative generative pipeline."""
    from stage1_classifier import predict_class

    GEN_CYCLE_DIR.mkdir(parents=True, exist_ok=True)

    # Load tokenizer for classifier
    with open(CLASSIFIER_DIR / "tokenizer.pkl", "rb") as f:
        cls_tokenizer = pickle.load(f)

    # Load initial T1 data
    t1_df = pd.read_csv(T1_FILE)
    smi_col = [c for c in t1_df.columns if "smiles" in c.lower()][0]
    training_smiles = set(t1_df[smi_col].dropna().tolist())
    all_known = set(training_smiles)

    logger.info(f"Initial T1: {len(training_smiles)} class 1 SMILES")

    cycle_stats = []

    for cycle in range(1, NUM_GEN_CYCLES + 1):
        logger.info(f"═══ Generative Cycle {cycle}/{NUM_GEN_CYCLES} ═══")
        logger.info(f"Training set size: {len(training_smiles)}")

        t_cycle_start = time.time()

        # Fine-tune
        model, gpt_tokenizer = finetune_gpt2(
            list(training_smiles), cycle, GPT2_DIR
        )

        # Generate
        new_molecules = generate_molecules(
            model, gpt_tokenizer, GEN_TARGET_PER_CYCLE, all_known
        )
        logger.info(f"Cycle {cycle}: Generated {len(new_molecules)} CUN molecules")

        # Classify
        if new_molecules:
            probs = predict_class(new_molecules, cls_tokenizer)
            preds = (probs >= CLASSIFICATION_THRESHOLD).astype(int)
            class1_new = [s for s, p in zip(new_molecules, preds) if p == 1]
            class1_pct = len(class1_new) / len(new_molecules) * 100
            logger.info(f"Cycle {cycle}: {len(class1_new)} predicted class 1 "
                        f"({class1_pct:.1f}%)")
        else:
            class1_new = []
            class1_pct = 0
            probs = np.array([])
            preds = np.array([])

        # Save cycle output
        cycle_df = pd.DataFrame({
            "smiles": new_molecules,
            "prob_class1": probs if len(new_molecules) > 0 else [],
            "pred_class1": preds if len(new_molecules) > 0 else [],
        })
        cycle_df.to_csv(GEN_CYCLE_DIR / f"cycle_{cycle}_generated.csv", index=False)

        # Update training set for next cycle
        training_smiles.update(class1_new)
        all_known.update(new_molecules)

        cycle_time = time.time() - t_cycle_start
        cycle_stats.append({
            "cycle": cycle,
            "training_size": len(training_smiles),
            "generated": len(new_molecules),
            "class1_new": len(class1_new),
            "class1_pct": class1_pct,
            "total_known": len(all_known),
            "cycle_time_min": cycle_time / 60,
        })

        logger.info(f"Cycle {cycle} took {cycle_time/60:.1f} minutes")

        # Free GPU memory
        del model
        torch.cuda.empty_cache()

    # Save summary
    stats_df = pd.DataFrame(cycle_stats)
    stats_df.to_csv(RESULTS_DIR / "generative_cycle_stats.csv", index=False)
    logger.info(f"\n{stats_df.to_string()}")

    # Combine all generated class 1 molecules
    all_gen_class1 = []
    for cycle in range(1, NUM_GEN_CYCLES + 1):
        cdf = pd.read_csv(GEN_CYCLE_DIR / f"cycle_{cycle}_generated.csv")
        class1 = cdf[cdf["pred_class1"] == 1]["smiles"].tolist()
        all_gen_class1.extend(class1)

    all_gen_class1 = list(set(all_gen_class1))
    pd.DataFrame({"smiles": all_gen_class1}).to_csv(
        GEN_CYCLE_DIR / "all_generated_class1.csv", index=False
    )
    logger.info(f"Total generated class 1 molecules: {len(all_gen_class1)}")

    return all_gen_class1


if __name__ == "__main__":
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    run_generative_cycles()

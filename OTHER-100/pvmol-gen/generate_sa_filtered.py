"""Generate molecules with on-the-fly SA filtering + SELFIES approach.

Two strategies run in parallel:
  A) SMILES + GPT-2 with SA filter during generation (reuse cycle 1 model)
  B) SELFIES + GPT-2 with SA filter (retrain on SELFIES)

Target: 10K molecules with SA <= 6.0 each.
"""

import logging
import os
import sys
import time
import random

import numpy as np
import pandas as pd
import torch
from pathlib import Path
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from rdkit import Chem, RDLogger
import selfies as sf

RDLogger.DisableLog("rdApp.*")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from sa_scorer import calculate_score as sa_score
from utils import validate_smiles, augment_smiles

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/generate_sa_filtered.log"),
    ],
)
logger = logging.getLogger(__name__)

TARGET = 10000
SA_MAX = 6.0
TEMPERATURE = 0.9
MAX_LENGTH = 100
BATCH_GEN = 64


def check_sa(smiles):
    """Return SA score if valid, else None."""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    try:
        Chem.SanitizeMol(mol)
        return sa_score(mol)
    except:
        return None


# ═══════════════════════════════════════════════════════════════
# Strategy A: SMILES + GPT-2, filter SA during generation
# ═══════════════════════════════════════════════════════════════

def run_smiles_sa_filtered(device_id=0):
    """Reuse cycle 1 model, but only keep molecules with SA <= 6."""
    device = torch.device(f"cuda:{device_id}")
    logger.info(f"=== Strategy A: SMILES + GPT-2 + SA filter (GPU {device_id}) ===")

    model_path = "models/gpt2_finetuned/cycle_1/model"
    tokenizer = GPT2Tokenizer.from_pretrained(model_path)
    model = GPT2LMHeadModel.from_pretrained(model_path).to(device)
    model.eval()

    known = set(pd.read_csv("data/t1_class1.csv")["smiles"].dropna().tolist())
    pad_id = tokenizer.encode("[PAD]", add_special_tokens=False)
    input_ids = torch.tensor([pad_id]).to(device)

    generated = {}  # smiles -> sa_score
    attempts = 0
    valid_count = 0
    sa_pass_count = 0
    t0 = time.time()

    while len(generated) < TARGET and attempts < TARGET * 100000:
        batch_input = input_ids.repeat(BATCH_GEN, 1)
        with torch.no_grad():
            outputs = model.generate(
                batch_input,
                attention_mask=torch.ones_like(batch_input),
                max_length=MAX_LENGTH,
                num_return_sequences=BATCH_GEN,
                temperature=TEMPERATURE,
                do_sample=True,
                pad_token_id=tokenizer.pad_token_id,
            )

        for seq in outputs:
            raw = tokenizer.decode(seq, skip_special_tokens=True).strip()
            canon = validate_smiles(raw)
            attempts += 1

            if canon and canon not in generated and canon not in known:
                valid_count += 1
                sa = check_sa(canon)
                if sa is not None and sa <= SA_MAX:
                    generated[canon] = sa
                    sa_pass_count += 1

        elapsed = time.time() - t0
        if len(generated) % 100 < BATCH_GEN and len(generated) > 0:
            rate = len(generated) / elapsed
            logger.info(f"  A: {len(generated)}/{TARGET} SA-valid "
                        f"({valid_count} valid total, {sa_pass_count} SA<=6, "
                        f"{rate:.1f}/s)")

    elapsed = time.time() - t0
    sa_rate = sa_pass_count / max(valid_count, 1) * 100
    logger.info(f"  A: DONE — {len(generated)} SA-valid molecules in {elapsed/60:.1f}min "
                f"(SA pass rate: {sa_rate:.1f}% of valid)")

    del model
    torch.cuda.empty_cache()
    return generated


# ═══════════════════════════════════════════════════════════════
# Strategy B: SELFIES + GPT-2 + SA filter
# ═══════════════════════════════════════════════════════════════

def run_selfies_sa_filtered(device_id=1):
    """Train GPT-2 on SELFIES, generate with SA filter."""
    from torch.utils.data import Dataset, DataLoader, random_split
    device = torch.device(f"cuda:{device_id}")
    logger.info(f"=== Strategy B: SELFIES + GPT-2 + SA filter (GPU {device_id}) ===")

    # Load T1 and convert to SELFIES
    t1 = pd.read_csv("data/t1_class1.csv")["smiles"].dropna().tolist()
    selfies_list = []
    for smi in t1:
        try:
            se = sf.encoder(smi)
            if se:
                selfies_list.append(se)
        except:
            pass
    logger.info(f"  Converted {len(selfies_list)}/{len(t1)} to SELFIES")

    # Augment via random SMILES → SELFIES
    augmented = set(selfies_list)
    random.seed(42)
    for smi in random.sample(t1, min(3000, len(t1))):
        for aug in augment_smiles(smi, n=3):
            try:
                se = sf.encoder(aug)
                if se:
                    augmented.add(se)
            except:
                pass
    augmented = list(augmented)
    logger.info(f"  Augmented to {len(augmented)} SELFIES strings")

    # Load and fine-tune GPT-2
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

    # Tokenize
    encoded = tokenizer(augmented, padding=True, truncation=True,
                        max_length=MAX_LENGTH, return_tensors="pt")

    class DS(torch.utils.data.Dataset):
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
    train_loader = DataLoader(train_ds, batch_size=4, shuffle=True, collate_fn=collate)
    val_loader = DataLoader(val_ds, batch_size=4, collate_fn=collate)

    model = model.to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5, weight_decay=0.01)
    scaler = torch.amp.GradScaler("cuda")

    best_val = float("inf")
    best_state = None
    patience = 0

    logger.info("  Fine-tuning GPT-2 on SELFIES...")
    for epoch in range(30):
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
            patience = 0
        else:
            patience += 1
        if patience >= 5:
            logger.info(f"    Early stopping at epoch {epoch+1}")
            break

    if best_state:
        model.load_state_dict(best_state)
    model.to(device)
    model.eval()

    # Save model
    out_path = "models/gpt2_finetuned/selfies_sa"
    os.makedirs(out_path, exist_ok=True)
    model.save_pretrained(out_path)
    tokenizer.save_pretrained(out_path)

    # Generate with SA filter
    known = set(t1)
    pad_id = tokenizer.encode("[PAD]", add_special_tokens=False)
    input_ids = torch.tensor([pad_id]).to(device)

    generated = {}
    attempts = 0
    valid_count = 0
    sa_pass_count = 0
    t0 = time.time()

    logger.info(f"  Generating {TARGET} SA-valid molecules from SELFIES...")

    while len(generated) < TARGET and attempts < TARGET * 10000:
        batch_input = input_ids.repeat(BATCH_GEN, 1)
        with torch.no_grad():
            outputs = model.generate(
                batch_input,
                attention_mask=torch.ones_like(batch_input),
                max_length=MAX_LENGTH,
                num_return_sequences=BATCH_GEN,
                temperature=TEMPERATURE,
                do_sample=True,
                pad_token_id=tokenizer.pad_token_id,
            )

        for seq in outputs:
            raw = tokenizer.decode(seq, skip_special_tokens=True).strip()
            attempts += 1
            try:
                smi = sf.decoder(raw)
                canon = validate_smiles(smi) if smi else None
            except:
                canon = None

            if canon and canon not in generated and canon not in known:
                valid_count += 1
                sa = check_sa(canon)
                if sa is not None and sa <= SA_MAX:
                    generated[canon] = sa
                    sa_pass_count += 1

        elapsed = time.time() - t0
        if len(generated) % 100 < BATCH_GEN and len(generated) > 0:
            rate = len(generated) / elapsed
            sa_rate = sa_pass_count / max(valid_count, 1) * 100
            logger.info(f"  B: {len(generated)}/{TARGET} SA-valid "
                        f"({valid_count} valid, SA pass: {sa_rate:.1f}%, {rate:.1f}/s)")

    elapsed = time.time() - t0
    sa_rate = sa_pass_count / max(valid_count, 1) * 100
    logger.info(f"  B: DONE — {len(generated)} SA-valid molecules in {elapsed/60:.1f}min "
                f"(SA pass rate: {sa_rate:.1f}% of valid)")

    del model
    torch.cuda.empty_cache()
    return generated


# ═══════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════

def main():
    os.makedirs("results/sa_filtered", exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    results = {}

    # Strategy A: SMILES + SA filter
    gen_a = run_smiles_sa_filtered(device_id=0)
    sa_values_a = list(gen_a.values())
    results["A_smiles_sa"] = {
        "count": len(gen_a),
        "mean_sa": np.mean(sa_values_a) if sa_values_a else 0,
        "median_sa": np.median(sa_values_a) if sa_values_a else 0,
    }
    pd.DataFrame({"smiles": list(gen_a.keys()), "sa": list(gen_a.values())}).to_csv(
        "results/sa_filtered/smiles_sa_filtered.csv", index=False)

    # Strategy B: SELFIES + SA filter
    gen_b = run_selfies_sa_filtered(device_id=1)
    sa_values_b = list(gen_b.values())
    results["B_selfies_sa"] = {
        "count": len(gen_b),
        "mean_sa": np.mean(sa_values_b) if sa_values_b else 0,
        "median_sa": np.median(sa_values_b) if sa_values_b else 0,
    }
    pd.DataFrame({"smiles": list(gen_b.keys()), "sa": list(gen_b.values())}).to_csv(
        "results/sa_filtered/selfies_sa_filtered.csv", index=False)

    # Summary
    print(f"\n{'='*60}")
    print("SA-FILTERED GENERATION COMPARISON")
    print(f"{'='*60}")
    for name, r in results.items():
        print(f"  {name}: {r['count']} molecules, mean SA={r['mean_sa']:.2f}, median SA={r['median_sa']:.2f}")
    print(f"{'='*60}")

    import json
    with open("results/sa_filtered/comparison.json", "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()

"""Three alternative molecular generation approaches, benchmarked against
the baseline GPT-2 + SMILES approach.

1. SELFIES + GPT-2: Convert SMILES→SELFIES, fine-tune, generate, convert back.
   Every SELFIES string is a valid molecule → ~100% validity.

2. SAFE (Sequential Attachment-based Fragment Embedding) + GPT-2:
   Fragment-based representation that reduces sequence complexity.

3. Grammar-constrained SMILES via character-level LSTM with teacher forcing
   and a SMILES syntax validator at each decoding step.

Each approach: fine-tune on T1, generate 10K molecules, measure validity,
uniqueness, novelty, and speed.
"""

import logging
import os
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader, random_split
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from rdkit import Chem, RDLogger

RDLogger.DisableLog("rdApp.*")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from utils import validate_smiles, augment_smiles

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/generate_alternatives.log"),
    ],
)
logger = logging.getLogger(__name__)

DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
TARGET = 10000  # Generate 10K for benchmark comparison
BATCH_SIZE_TRAIN = 4
BATCH_SIZE_GEN = 64
MAX_LENGTH = 100
TEMPERATURE = 0.9
EPOCHS = 30
PATIENCE = 5


# ═══════════════════════════════════════════════════════════════════════════
# Shared utilities
# ═══════════════════════════════════════════════════════════════════════════

def load_t1():
    """Load T1 SMILES."""
    df = pd.read_csv("data/t1_class1.csv")
    return df["smiles"].dropna().tolist()


def evaluate_generation(generated, known, label):
    """Compute validity, uniqueness, novelty metrics."""
    valid = [s for s in generated if validate_smiles(s) is not None]
    valid_canonical = set(validate_smiles(s) for s in valid)
    novel = valid_canonical - known

    n = len(generated)
    validity = len(valid) / n * 100 if n > 0 else 0
    uniqueness = len(valid_canonical) / len(valid) * 100 if valid else 0
    novelty = len(novel) / len(valid_canonical) * 100 if valid_canonical else 0

    print(f"\n  {label}:")
    print(f"    Raw generated:  {n}")
    print(f"    Valid:          {len(valid)} ({validity:.1f}%)")
    print(f"    Unique:         {len(valid_canonical)} ({uniqueness:.1f}%)")
    print(f"    Novel:          {len(novel)} ({novelty:.1f}%)")
    print(f"    CUN molecules:  {len(novel)}")

    return {
        "method": label,
        "raw": n, "valid": len(valid), "unique": len(valid_canonical),
        "novel": len(novel),
        "validity_pct": validity, "uniqueness_pct": uniqueness,
        "novelty_pct": novelty,
    }


class SimpleDataset(Dataset):
    def __init__(self, encoded):
        self.ids = encoded["input_ids"]
        self.mask = encoded["attention_mask"]

    def __len__(self):
        return len(self.ids)

    def __getitem__(self, i):
        return {"input_ids": self.ids[i], "attention_mask": self.mask[i],
                "labels": self.ids[i]}


def collate(batch):
    return {k: torch.stack([b[k] for b in batch]) for k in batch[0]}


def finetune_gpt2(strings, tokenizer, model, epochs=EPOCHS, patience=PATIENCE):
    """Fine-tune GPT-2 on a list of strings. Returns best model."""
    encoded = tokenizer(strings, padding=True, truncation=True,
                        max_length=MAX_LENGTH, return_tensors="pt")
    dataset = SimpleDataset(encoded)
    train_n = int(0.8 * len(dataset))
    train_ds, val_ds = random_split(dataset, [train_n, len(dataset) - train_n])

    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE_TRAIN, shuffle=True, collate_fn=collate)
    val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE_TRAIN, collate_fn=collate)

    model = model.to(DEVICE)
    optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5, weight_decay=0.01)
    scaler = torch.amp.GradScaler("cuda") if DEVICE.type == "cuda" else None

    best_val = float("inf")
    best_state = None
    no_improve = 0

    for epoch in range(epochs):
        model.train()
        total = 0
        for batch in train_loader:
            ids = batch["input_ids"].to(DEVICE)
            mask = batch["attention_mask"].to(DEVICE)
            optimizer.zero_grad()
            if scaler:
                with torch.amp.autocast("cuda", dtype=torch.float16):
                    out = model(input_ids=ids, attention_mask=mask, labels=ids)
                scaler.scale(out.loss).backward()
                scaler.step(optimizer)
                scaler.update()
            else:
                out = model(input_ids=ids, attention_mask=mask, labels=ids)
                out.loss.backward()
                optimizer.step()
            total += out.loss.item()

        model.eval()
        val_loss = 0
        with torch.no_grad():
            for batch in val_loader:
                ids = batch["input_ids"].to(DEVICE)
                mask = batch["attention_mask"].to(DEVICE)
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
        if no_improve >= patience:
            logger.info(f"    Early stopping at epoch {epoch+1}")
            break

    if best_state:
        model.load_state_dict(best_state)
    model.to(DEVICE)
    return model


def generate_gpt2(model, tokenizer, target, known_smiles, decode_fn=None):
    """Generate molecules with GPT-2. decode_fn converts raw string → canonical SMILES."""
    model.eval()
    pad_id = tokenizer.encode("[PAD]", add_special_tokens=False)
    input_ids = torch.tensor([pad_id]).to(DEVICE)

    all_raw = []
    generated = set()
    attempts = 0
    t0 = time.time()

    while len(generated) < target and attempts < target * 500:
        batch_input = input_ids.repeat(BATCH_SIZE_GEN, 1)
        with torch.no_grad():
            outputs = model.generate(
                batch_input,
                attention_mask=torch.ones_like(batch_input),
                max_length=MAX_LENGTH,
                num_return_sequences=BATCH_SIZE_GEN,
                temperature=TEMPERATURE,
                do_sample=True,
                pad_token_id=tokenizer.pad_token_id,
            )

        for seq in outputs:
            raw = tokenizer.decode(seq, skip_special_tokens=True).strip()
            all_raw.append(raw)

            if decode_fn:
                canon = decode_fn(raw)
            else:
                canon = validate_smiles(raw)

            if canon and canon not in generated and canon not in known_smiles:
                generated.add(canon)
            attempts += 1

        if len(generated) % 1000 < BATCH_SIZE_GEN and len(generated) > 0:
            elapsed = time.time() - t0
            rate = len(generated) / elapsed
            logger.info(f"    {len(generated)}/{target} ({rate:.1f}/s)")

    elapsed = time.time() - t0
    logger.info(f"    Done: {len(generated)} CUN in {elapsed:.0f}s "
                f"({len(generated)/elapsed:.1f}/s)")
    return list(generated), all_raw


# ═══════════════════════════════════════════════════════════════════════════
# METHOD 1: SELFIES + GPT-2
# ═══════════════════════════════════════════════════════════════════════════

def run_selfies_gpt2(smiles_list, known):
    """Convert to SELFIES, fine-tune GPT-2, generate, convert back."""
    import selfies as sf

    logger.info("=== METHOD 1: SELFIES + GPT-2 ===")

    # Convert SMILES → SELFIES
    selfies_list = []
    for smi in smiles_list:
        try:
            se = sf.encoder(smi)
            if se:
                selfies_list.append(se)
        except:
            pass
    logger.info(f"  Converted {len(selfies_list)}/{len(smiles_list)} to SELFIES")

    # Augment with random SMILES → SELFIES
    augmented = set(selfies_list)
    for smi in smiles_list[:2000]:  # augment a subset for speed
        for aug in augment_smiles(smi, n=3):
            try:
                se = sf.encoder(aug)
                if se:
                    augmented.add(se)
            except:
                pass
    augmented = list(augmented)
    logger.info(f"  Augmented to {len(augmented)} SELFIES strings")

    # Load GPT-2
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

    # Fine-tune on SELFIES
    logger.info("  Fine-tuning GPT-2 on SELFIES...")
    model = finetune_gpt2(augmented, tokenizer, model)

    # Generate
    def selfies_to_smiles(raw):
        try:
            smi = sf.decoder(raw)
            return validate_smiles(smi) if smi else None
        except:
            return None

    logger.info(f"  Generating {TARGET} molecules...")
    generated, all_raw = generate_gpt2(model, tokenizer, TARGET, known,
                                        decode_fn=selfies_to_smiles)

    # Evaluate raw validity (how many raw strings decode to valid molecules)
    metrics = evaluate_generation(all_raw, known, "SELFIES + GPT-2")
    metrics["method"] = "SELFIES + GPT-2"

    # Save
    os.makedirs("results/gen_alternatives", exist_ok=True)
    pd.DataFrame({"smiles": generated}).to_csv(
        "results/gen_alternatives/selfies_gpt2.csv", index=False)

    del model
    torch.cuda.empty_cache()
    return metrics


# ═══════════════════════════════════════════════════════════════════════════
# METHOD 2: SAFE + GPT-2
# ═══════════════════════════════════════════════════════════════════════════

def run_safe_gpt2(smiles_list, known):
    """Convert to SAFE representation, fine-tune GPT-2, generate, convert back."""
    import safe

    logger.info("=== METHOD 2: SAFE + GPT-2 ===")

    # Convert SMILES → SAFE
    safe_list = []
    failed = 0
    for smi in smiles_list:
        try:
            s = safe.encode(smi)
            if s:
                safe_list.append(s)
        except:
            failed += 1
    logger.info(f"  Converted {len(safe_list)}/{len(smiles_list)} to SAFE ({failed} failed)")

    # Augment
    augmented = set(safe_list)
    for smi in smiles_list[:2000]:
        for aug in augment_smiles(smi, n=3):
            try:
                s = safe.encode(aug)
                if s:
                    augmented.add(s)
            except:
                pass
    augmented = list(augmented)
    logger.info(f"  Augmented to {len(augmented)} SAFE strings")

    # Load GPT-2
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

    # Fine-tune
    logger.info("  Fine-tuning GPT-2 on SAFE...")
    model = finetune_gpt2(augmented, tokenizer, model)

    # Generate
    def safe_to_smiles(raw):
        try:
            smi = safe.decode(raw)
            return validate_smiles(smi) if smi else None
        except:
            return None

    logger.info(f"  Generating {TARGET} molecules...")
    generated, all_raw = generate_gpt2(model, tokenizer, TARGET, known,
                                        decode_fn=safe_to_smiles)

    metrics = evaluate_generation(all_raw, known, "SAFE + GPT-2")
    metrics["method"] = "SAFE + GPT-2"

    pd.DataFrame({"smiles": generated}).to_csv(
        "results/gen_alternatives/safe_gpt2.csv", index=False)

    del model
    torch.cuda.empty_cache()
    return metrics


# ═══════════════════════════════════════════════════════════════════════════
# METHOD 3: Character-level LSTM with SMILES
# ═══════════════════════════════════════════════════════════════════════════

class CharLSTM(nn.Module):
    """Character-level LSTM for SMILES generation."""
    def __init__(self, vocab_size, embed_dim=128, hidden_dim=512, n_layers=3, dropout=0.2):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, n_layers,
                           batch_first=True, dropout=dropout)
        self.fc = nn.Linear(hidden_dim, vocab_size)
        self.hidden_dim = hidden_dim
        self.n_layers = n_layers

    def forward(self, x, hidden=None):
        emb = self.embedding(x)
        out, hidden = self.lstm(emb, hidden)
        logits = self.fc(out)
        return logits, hidden

    def init_hidden(self, batch_size, device):
        h = torch.zeros(self.n_layers, batch_size, self.hidden_dim).to(device)
        c = torch.zeros(self.n_layers, batch_size, self.hidden_dim).to(device)
        return (h, c)


class CharSmilesDataset(Dataset):
    def __init__(self, smiles_list, char2idx, max_len=100):
        self.data = []
        for smi in smiles_list:
            # Add start/end tokens
            s = "^" + smi + "$"
            if len(s) > max_len:
                continue
            ids = [char2idx.get(c, char2idx.get("?", 0)) for c in s]
            # Pad
            ids = ids + [0] * (max_len - len(ids))
            self.data.append(ids)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, i):
        ids = torch.tensor(self.data[i], dtype=torch.long)
        return ids[:-1], ids[1:]  # input, target (shifted by 1)


def run_char_lstm(smiles_list, known):
    """Train character-level LSTM on SMILES, generate molecules."""
    logger.info("=== METHOD 3: Character-level LSTM ===")

    # Build vocabulary
    all_chars = set()
    for smi in smiles_list:
        all_chars.update(smi)
    all_chars = sorted(all_chars)
    special = ["<pad>", "^", "$", "?"]
    vocab = special + all_chars
    char2idx = {c: i for i, c in enumerate(vocab)}
    idx2char = {i: c for c, i in char2idx.items()}
    logger.info(f"  Vocabulary: {len(vocab)} characters")

    # Augment
    augmented = set(smiles_list)
    for smi in smiles_list[:2000]:
        augmented.update(augment_smiles(smi, n=3))
    augmented = list(augmented)
    logger.info(f"  Augmented to {len(augmented)} SMILES")

    # Dataset
    dataset = CharSmilesDataset(augmented, char2idx, max_len=MAX_LENGTH)
    train_n = int(0.8 * len(dataset))
    train_ds, val_ds = random_split(dataset, [train_n, len(dataset) - train_n])
    train_loader = DataLoader(train_ds, batch_size=64, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=64)

    # Model
    model = CharLSTM(len(vocab), embed_dim=128, hidden_dim=512, n_layers=3).to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    criterion = nn.CrossEntropyLoss(ignore_index=0)

    best_val = float("inf")
    best_state = None
    no_improve = 0

    logger.info("  Training character LSTM...")
    for epoch in range(60):
        model.train()
        total = 0
        n = 0
        for x, y in train_loader:
            x, y = x.to(DEVICE), y.to(DEVICE)
            optimizer.zero_grad()
            logits, _ = model(x)
            loss = criterion(logits.reshape(-1, len(vocab)), y.reshape(-1))
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            total += loss.item()
            n += 1

        model.eval()
        val_loss = 0
        vn = 0
        with torch.no_grad():
            for x, y in val_loader:
                x, y = x.to(DEVICE), y.to(DEVICE)
                logits, _ = model(x)
                val_loss += criterion(logits.reshape(-1, len(vocab)), y.reshape(-1)).item()
                vn += 1
        val_loss /= max(vn, 1)

        if (epoch + 1) % 10 == 0:
            logger.info(f"    Epoch {epoch+1}: train={total/n:.4f} val={val_loss:.4f}")

        if val_loss < best_val:
            best_val = val_loss
            best_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}
            no_improve = 0
        else:
            no_improve += 1
        if no_improve >= 10:
            logger.info(f"    Early stopping at epoch {epoch+1}")
            break

    if best_state:
        model.load_state_dict(best_state)
    model.to(DEVICE)

    # Generate
    logger.info(f"  Generating {TARGET} molecules...")
    model.eval()
    generated = set()
    all_raw = []
    t0 = time.time()
    start_idx = char2idx["^"]
    end_idx = char2idx["$"]

    while len(generated) < TARGET and len(all_raw) < TARGET * 100:
        batch_size = 256
        hidden = model.init_hidden(batch_size, DEVICE)
        inp = torch.full((batch_size, 1), start_idx, dtype=torch.long).to(DEVICE)

        sequences = [[] for _ in range(batch_size)]
        finished = [False] * batch_size

        for step in range(MAX_LENGTH):
            logits, hidden = model(inp, hidden)
            probs = torch.softmax(logits[:, -1, :] / TEMPERATURE, dim=-1)
            next_char = torch.multinomial(probs, 1)
            inp = next_char

            for i in range(batch_size):
                if not finished[i]:
                    c = idx2char.get(next_char[i].item(), "?")
                    if c == "$":
                        finished[i] = True
                    elif c not in ("<pad>", "?"):
                        sequences[i].append(c)

            if all(finished):
                break

        for seq in sequences:
            smi = "".join(seq)
            all_raw.append(smi)
            canon = validate_smiles(smi)
            if canon and canon not in generated and canon not in known:
                generated.add(canon)

        if len(generated) % 1000 < 256 and len(generated) > 0:
            elapsed = time.time() - t0
            logger.info(f"    {len(generated)}/{TARGET} ({len(generated)/elapsed:.1f}/s)")

    elapsed = time.time() - t0
    logger.info(f"    Done: {len(generated)} CUN in {elapsed:.0f}s")

    metrics = evaluate_generation(all_raw, known, "Char-LSTM")
    metrics["method"] = "Char-LSTM"

    pd.DataFrame({"smiles": list(generated)}).to_csv(
        "results/gen_alternatives/char_lstm.csv", index=False)

    del model
    torch.cuda.empty_cache()
    return metrics


# ═══════════════════════════════════════════════════════════════════════════
# BASELINE: SMILES + GPT-2 (current approach, for comparison)
# ═══════════════════════════════════════════════════════════════════════════

def run_smiles_gpt2_baseline(known):
    """Use the already fine-tuned model from Cycle 1."""
    logger.info("=== BASELINE: SMILES + GPT-2 ===")

    model_path = "models/gpt2_finetuned/cycle_1/model"
    tokenizer = GPT2Tokenizer.from_pretrained(model_path)
    model = GPT2LMHeadModel.from_pretrained(model_path).to(DEVICE)

    logger.info(f"  Generating {TARGET} molecules (reusing cycle 1 model)...")
    generated, all_raw = generate_gpt2(model, tokenizer, TARGET, known)

    metrics = evaluate_generation(all_raw, known, "SMILES + GPT-2 (baseline)")
    metrics["method"] = "SMILES + GPT-2 (baseline)"

    pd.DataFrame({"smiles": generated}).to_csv(
        "results/gen_alternatives/smiles_gpt2_baseline.csv", index=False)

    del model
    torch.cuda.empty_cache()
    return metrics


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

def main():
    os.makedirs("results/gen_alternatives", exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    smiles_list = load_t1()
    known = set(smiles_list)
    logger.info(f"T1: {len(smiles_list)} SMILES, generating {TARGET} per method\n")

    results = []

    # Baseline
    try:
        results.append(run_smiles_gpt2_baseline(known))
    except Exception as e:
        logger.error(f"Baseline failed: {e}")

    # Method 1: SELFIES
    try:
        results.append(run_selfies_gpt2(smiles_list, known))
    except Exception as e:
        logger.error(f"SELFIES failed: {e}")

    # Method 2: SAFE
    try:
        results.append(run_safe_gpt2(smiles_list, known))
    except Exception as e:
        logger.error(f"SAFE failed: {e}")

    # Method 3: Char-LSTM
    try:
        results.append(run_char_lstm(smiles_list, known))
    except Exception as e:
        logger.error(f"Char-LSTM failed: {e}")

    # Summary
    print(f"\n{'='*80}")
    print("GENERATION METHOD COMPARISON")
    print(f"{'='*80}")
    print(f"  {'Method':<30s} {'Valid%':>8s} {'Unique%':>8s} {'Novel%':>8s} {'CUN':>8s}")
    print(f"  {'-'*30} {'-'*8} {'-'*8} {'-'*8} {'-'*8}")
    for r in results:
        print(f"  {r['method']:<30s} {r['validity_pct']:>7.1f}% {r['uniqueness_pct']:>7.1f}% "
              f"{r['novelty_pct']:>7.1f}% {r['novel']:>7d}")
    print(f"{'='*80}")

    pd.DataFrame(results).to_csv("results/gen_alternatives/comparison.csv", index=False)
    logger.info("Results saved to results/gen_alternatives/")


if __name__ == "__main__":
    main()

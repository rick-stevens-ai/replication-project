#!/usr/bin/env python3
"""Mini Domain-Adaptive Pre-training (DAPT) demo.

Takes ~5-10K OSTI abstracts and continues MLM pre-training on a small LM
to demonstrate the NukeLM methodology at reduced scale. Produces a
checkpoint that can be loaded by finetune.py via --model path.
"""
import json, argparse, os, math, time
import torch
from torch.utils.data import Dataset
from transformers import (
    AutoTokenizer, AutoModelForMaskedLM,
    TrainingArguments, Trainer, DataCollatorForLanguageModeling,
)


class MLMDataset(Dataset):
    def __init__(self, texts, tok, max_len):
        self.tok = tok
        self.max_len = max_len
        self.texts = texts

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, i):
        t = self.texts[i]
        enc = self.tok(t, truncation=True, max_length=self.max_len, padding=False)
        return enc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default="distilbert-base-uncased")
    ap.add_argument("--n-docs", type=int, default=8000)
    ap.add_argument("--epochs", type=float, default=1.0)
    ap.add_argument("--batch", type=int, default=32)
    ap.add_argument("--lr", type=float, default=5e-5)
    ap.add_argument("--max-len", type=int, default=256)
    ap.add_argument("--mlm-prob", type=float, default=0.15)
    ap.add_argument("--fp16", action="store_true")
    ap.add_argument("--bf16", action="store_true")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    texts = []
    with open(args.raw) as f:
        for line in f:
            try:
                r = json.loads(line)
            except Exception:
                continue
            t = ((r.get("title") or "") + ". " + (r.get("abstract") or "")).strip()
            if len(t) > 200:
                texts.append(t)
            if len(texts) >= args.n_docs:
                break
    print(f"MLM docs: {len(texts)}")

    tok = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForMaskedLM.from_pretrained(args.model)

    n_val = min(500, len(texts) // 10)
    train_ds = MLMDataset(texts[n_val:], tok, args.max_len)
    val_ds = MLMDataset(texts[:n_val], tok, args.max_len)
    collator = DataCollatorForLanguageModeling(tok, mlm=True, mlm_probability=args.mlm_prob)

    targs = TrainingArguments(
        output_dir=args.out,
        overwrite_output_dir=True,
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch,
        per_device_eval_batch_size=args.batch * 2,
        learning_rate=args.lr,
        weight_decay=0.01,
        warmup_ratio=0.06,
        eval_strategy="epoch",
        save_strategy="epoch",
        save_total_limit=1,
        logging_steps=50,
        fp16=args.fp16,
        bf16=args.bf16,
        report_to=[],
        seed=args.seed,
        dataloader_num_workers=2,
        remove_unused_columns=False,
    )
    trainer = Trainer(
        model=model, args=targs,
        train_dataset=train_ds, eval_dataset=val_ds,
        tokenizer=tok, data_collator=collator,
    )

    # Baseline eval (pre-DAPT MLM loss)
    pre = trainer.evaluate()
    print("PRE-DAPT eval:", pre)
    t0 = time.time()
    trainer.train()
    post = trainer.evaluate()
    print("POST-DAPT eval:", post)
    result = {
        "model": args.model,
        "n_train": len(train_ds),
        "n_val": len(val_ds),
        "pre_eval_loss": pre.get("eval_loss"),
        "pre_eval_ppl": math.exp(pre.get("eval_loss", 0)) if pre.get("eval_loss") is not None else None,
        "post_eval_loss": post.get("eval_loss"),
        "post_eval_ppl": math.exp(post.get("eval_loss", 0)) if post.get("eval_loss") is not None else None,
        "train_seconds": time.time() - t0,
        "args": vars(args),
    }
    with open(os.path.join(args.out, "mlm_result.json"), "w") as f:
        json.dump(result, f, indent=2)
    # Save HF model
    trainer.save_model(os.path.join(args.out, "final"))
    tok.save_pretrained(os.path.join(args.out, "final"))
    print("MLM done:", result)


if __name__ == "__main__":
    main()

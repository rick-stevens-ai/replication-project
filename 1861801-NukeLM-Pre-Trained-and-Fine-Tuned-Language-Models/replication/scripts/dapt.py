#!/usr/bin/env python3
"""Domain-Adaptive Pre-Training (DAPT) on OSTI abstracts — paper-faithful.

NukeLM paper (Burchfield et al., OSTI 1861801) — pre-training recipe:
  * continued MLM on pretrained checkpoint (RoBERTa-base/large or SciBERT)
  * 13K steps, effective batch 256, max_len 512, MLM-prob 15%
  * remaining hyperparameters follow Gururangan et al. 2020 ("Don't Stop
    Pretraining"): AdamW, LR 5e-5, warmup_ratio 0.06, weight_decay 0.01,
    linear LR decay, no dropout change.

Our replication scales `--max-steps` down from 13K when compute-limited
(documented in report), but uses identical optimizer / seq-len / masking /
effective-batch settings.
"""
import argparse, json, math, os, time
import torch
from torch.utils.data import Dataset, IterableDataset
from transformers import (
    AutoTokenizer, AutoModelForMaskedLM,
    TrainingArguments, Trainer, DataCollatorForLanguageModeling,
)


class PackedTextDataset(Dataset):
    """Tokenize once, pack into fixed-size chunks of `block_size` tokens.

    Spans cross document boundaries (as done in the NukeLM paper).
    """

    def __init__(self, text_paths, tokenizer, block_size):
        self.tok = tokenizer
        self.block_size = block_size
        bos = [tokenizer.cls_token_id] if tokenizer.cls_token_id is not None else []
        eos = [tokenizer.sep_token_id] if tokenizer.sep_token_id is not None else []
        ids = []
        n_docs = 0
        for p in text_paths:
            with open(p) as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    toks = tokenizer(line, add_special_tokens=False, truncation=False)["input_ids"]
                    ids.extend(bos + toks + eos)
                    n_docs += 1
        # Drop tail
        total = (len(ids) // block_size) * block_size
        ids = ids[:total]
        self.examples = torch.tensor(ids, dtype=torch.long).view(-1, block_size)
        print(f"packed {n_docs} docs into {len(self.examples)} blocks of {block_size} tokens ({total/1e6:.2f}M tokens)")

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, i):
        x = self.examples[i]
        return {"input_ids": x, "attention_mask": torch.ones_like(x)}


def jsonl_to_txt(jsonl_path, txt_path, min_chars=200):
    n = 0
    with open(jsonl_path) as fin, open(txt_path, "w") as fout:
        for line in fin:
            try:
                r = json.loads(line)
            except Exception:
                continue
            t = ((r.get("title") or "") + ". " + (r.get("abstract") or "")).strip()
            if len(t) >= min_chars:
                # flatten newlines
                t = " ".join(t.split())
                fout.write(t + "\n")
                n += 1
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train-txt", required=True,
                    help="plain text file, one doc per line (produced by prep_txt.py)")
    ap.add_argument("--val-txt", default=None)
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default="roberta-base")
    ap.add_argument("--block-size", type=int, default=512)
    ap.add_argument("--mlm-prob", type=float, default=0.15)
    ap.add_argument("--per-device-batch", type=int, default=16)
    ap.add_argument("--grad-accum", type=int, default=4,
                    help="effective batch = per_device * n_gpu * grad_accum; paper=256")
    ap.add_argument("--max-steps", type=int, default=3000,
                    help="paper uses 13000; scale down if compute-limited")
    ap.add_argument("--lr", type=float, default=5e-5)
    ap.add_argument("--warmup-ratio", type=float, default=0.06)
    ap.add_argument("--weight-decay", type=float, default=0.01)
    ap.add_argument("--bf16", action="store_true")
    ap.add_argument("--fp16", action="store_true")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--eval-steps", type=int, default=300)
    ap.add_argument("--save-steps", type=int, default=1000)
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    txt_train = args.train_txt
    txt_val = args.val_txt or args.train_txt  # fallback but we expect val-txt

    tok = AutoTokenizer.from_pretrained(args.model, use_fast=True)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForMaskedLM.from_pretrained(args.model)

    train_ds = PackedTextDataset([txt_train], tok, args.block_size)
    val_ds = PackedTextDataset([txt_val], tok, args.block_size)
    collator = DataCollatorForLanguageModeling(tok, mlm=True, mlm_probability=args.mlm_prob)

    targs = TrainingArguments(
        output_dir=args.out,
        overwrite_output_dir=True,
        max_steps=args.max_steps,
        per_device_train_batch_size=args.per_device_batch,
        per_device_eval_batch_size=max(args.per_device_batch, 8),
        gradient_accumulation_steps=args.grad_accum,
        learning_rate=args.lr,
        weight_decay=args.weight_decay,
        warmup_ratio=args.warmup_ratio,
        lr_scheduler_type="linear",
        eval_strategy="steps",
        eval_steps=args.eval_steps,
        save_strategy="steps",
        save_steps=args.save_steps,
        save_total_limit=1,
        logging_steps=25,
        fp16=args.fp16,
        bf16=args.bf16,
        report_to=[],
        seed=args.seed,
        dataloader_num_workers=2,
        remove_unused_columns=False,
        ddp_find_unused_parameters=False,
    )
    trainer = Trainer(
        model=model, args=targs,
        train_dataset=train_ds, eval_dataset=val_ds,
        tokenizer=tok, data_collator=collator,
    )
    pre = trainer.evaluate()
    print("PRE-DAPT:", pre)
    t0 = time.time()
    trainer.train()
    post = trainer.evaluate()
    secs = time.time() - t0
    print("POST-DAPT:", post)
    result = {
        "model": args.model, "max_steps": args.max_steps,
        "block_size": args.block_size,
        "effective_batch": args.per_device_batch * args.grad_accum * max(1, torch.cuda.device_count()),
        "n_train_blocks": len(train_ds), "n_val_blocks": len(val_ds),
        "pre_eval_loss": pre.get("eval_loss"),
        "pre_ppl": math.exp(pre["eval_loss"]) if pre.get("eval_loss") is not None else None,
        "post_eval_loss": post.get("eval_loss"),
        "post_ppl": math.exp(post["eval_loss"]) if post.get("eval_loss") is not None else None,
        "train_seconds": secs,
    }
    with open(os.path.join(args.out, "dapt_result.json"), "w") as f:
        json.dump(result, f, indent=2)
    trainer.save_model(os.path.join(args.out, "final"))
    tok.save_pretrained(os.path.join(args.out, "final"))
    print("DAPT done:", result)


if __name__ == "__main__":
    main()

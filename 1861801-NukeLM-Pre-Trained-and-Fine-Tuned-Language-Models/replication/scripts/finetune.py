#!/usr/bin/env python3
"""Fine-tune a pre-trained LM on binary or multi-class OSTI classification.

Reproduces (scaled-down) the NukeLM fine-tuning setup: lr=1e-5, batch=64,
epochs=3-5 (default 3 for budget), max_seq_len=256 (paper uses 512).
"""
import json, os, argparse, time
import numpy as np
import torch
from torch.utils.data import Dataset
from transformers import (
    AutoTokenizer, AutoModelForSequenceClassification,
    TrainingArguments, Trainer, DataCollatorWithPadding,
)
from sklearn.metrics import (
    accuracy_score, precision_recall_fscore_support, classification_report,
)


def load_jsonl(path):
    with open(path) as f:
        return [json.loads(l) for l in f]


class TextDataset(Dataset):
    def __init__(self, records, tokenizer, max_len):
        self.records = records
        self.tok = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.records)

    def __getitem__(self, idx):
        r = self.records[idx]
        enc = self.tok(
            r["text"], truncation=True, max_length=self.max_len, padding=False
        )
        enc["labels"] = int(r["label"])
        return enc


def compute_metrics_binary(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    acc = accuracy_score(labels, preds)
    p, r, f1, _ = precision_recall_fscore_support(
        labels, preds, average="binary", zero_division=0
    )
    return {"accuracy": acc, "precision": p, "recall": r, "f1": f1}


def compute_metrics_multiclass(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    acc = accuracy_score(labels, preds)
    # Paper reports macro-weighted metrics (acc equal to weighted recall).
    p_w, r_w, f1_w, _ = precision_recall_fscore_support(
        labels, preds, average="weighted", zero_division=0
    )
    p_m, r_m, f1_m, _ = precision_recall_fscore_support(
        labels, preds, average="macro", zero_division=0
    )
    return {
        "accuracy": acc,
        "precision_weighted": p_w,
        "recall_weighted": r_w,
        "f1_weighted": f1_w,
        "precision_macro": p_m,
        "recall_macro": r_m,
        "f1_macro": f1_m,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", required=True)
    ap.add_argument("--task", required=True, choices=["binary", "multiclass"])
    ap.add_argument("--model", default="distilbert-base-uncased")
    ap.add_argument("--out", required=True)
    # NukeLM paper fine-tuning hyperparameters
    ap.add_argument("--epochs", type=float, default=5.0)
    ap.add_argument("--batch", type=int, default=64,
                    help="effective batch; paper uses 64 (from grid {16,64})")
    ap.add_argument("--per-device-batch", type=int, default=0,
                    help="if >0, overrides --batch -> per_device_train_batch_size and uses grad_accum")
    ap.add_argument("--grad-accum", type=int, default=1)
    ap.add_argument("--eval-batch", type=int, default=64)
    ap.add_argument("--lr", type=float, default=1e-5,
                    help="paper uses 1e-5 (from grid {1e-5,2e-5,5e-5})")
    ap.add_argument("--max-len", type=int, default=512,
                    help="paper uses 512")
    ap.add_argument("--warmup", type=float, default=0.06)
    ap.add_argument("--weight-decay", type=float, default=0.01)
    ap.add_argument("--fp16", action="store_true")
    ap.add_argument("--bf16", action="store_true")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    train = load_jsonl(os.path.join(args.data_dir, "train.jsonl"))
    val = load_jsonl(os.path.join(args.data_dir, "val.jsonl"))
    test = load_jsonl(os.path.join(args.data_dir, "test.jsonl"))
    num_labels = int(max(r["label"] for r in train + val + test)) + 1
    print(f"task={args.task} model={args.model} n_train={len(train)} n_val={len(val)} n_test={len(test)} num_labels={num_labels}")

    tok = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForSequenceClassification.from_pretrained(
        args.model, num_labels=num_labels
    )

    ds_train = TextDataset(train, tok, args.max_len)
    ds_val = TextDataset(val, tok, args.max_len)
    ds_test = TextDataset(test, tok, args.max_len)

    collator = DataCollatorWithPadding(tok)
    cm = compute_metrics_binary if args.task == "binary" else compute_metrics_multiclass
    metric_best = "f1" if args.task == "binary" else "f1_weighted"

    # Resolve batch settings: effective batch = per_device * n_gpu * grad_accum
    n_gpu = max(1, torch.cuda.device_count())
    if args.per_device_batch > 0:
        per_device = args.per_device_batch
        grad_accum = args.grad_accum
    else:
        per_device = max(1, args.batch // (n_gpu * max(1, args.grad_accum)))
        grad_accum = args.grad_accum
    eff_batch = per_device * n_gpu * grad_accum
    print(f"n_gpu={n_gpu} per_device={per_device} grad_accum={grad_accum} eff_batch={eff_batch}")

    targs = TrainingArguments(
        output_dir=args.out,
        overwrite_output_dir=True,
        num_train_epochs=args.epochs,
        per_device_train_batch_size=per_device,
        per_device_eval_batch_size=args.eval_batch,
        gradient_accumulation_steps=grad_accum,
        learning_rate=args.lr,
        weight_decay=args.weight_decay,
        warmup_ratio=args.warmup,
        lr_scheduler_type="linear",
        eval_strategy="epoch",
        save_strategy="no",
        logging_strategy="steps",
        logging_steps=50,
        fp16=args.fp16,
        bf16=args.bf16,
        report_to=[],
        seed=args.seed,
        dataloader_num_workers=2,
        remove_unused_columns=False,
        ddp_find_unused_parameters=False,
    )

    trainer = Trainer(
        model=model,
        args=targs,
        train_dataset=ds_train,
        eval_dataset=ds_val,
        tokenizer=tok,
        data_collator=collator,
        compute_metrics=cm,
    )
    t0 = time.time()
    trainer.train()
    train_secs = time.time() - t0
    val_metrics = trainer.evaluate(ds_val)
    test_metrics = trainer.evaluate(ds_test, metric_key_prefix="test")
    print("VAL:", json.dumps(val_metrics, indent=2))
    print("TEST:", json.dumps(test_metrics, indent=2))
    # Detailed test classification report
    preds = trainer.predict(ds_test)
    pred_labels = np.argmax(preds.predictions, axis=-1)
    true_labels = preds.label_ids
    report = classification_report(true_labels, pred_labels, zero_division=0, output_dict=True)
    result = {
        "task": args.task,
        "model": args.model,
        "args": vars(args),
        "n_train": len(train),
        "n_val": len(val),
        "n_test": len(test),
        "num_labels": num_labels,
        "train_seconds": train_secs,
        "val": val_metrics,
        "test": test_metrics,
        "classification_report": report,
    }
    with open(os.path.join(args.out, "result.json"), "w") as f:
        json.dump(result, f, indent=2)
    print(f"saved {args.out}/result.json  train_secs={train_secs:.0f}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Prepare binary & multi-class classification datasets from OSTI raw JSONL.

Binary (Task A): NFC-related (positive) vs Other (negative).
NFC-related primary codes (per NukeLM paper) correspond to OSTI subject
categories for Nuclear Fuels / Radiation Sources / Fuel Cycle / Waste /
Nuclear Reactors / Nuclear/Radiation Physics / Radiation Chemistry /
Instrumentation for Nuclear Science. Approximate mapping by leading codes:
  07  Isotope and Radiation Sources  (aka "ISOTOPES AND RADIATION SOURCES")
  11  Nuclear Fuel Cycle and Fuel Materials
  12  Management of Radioactive Wastes
  21  Specific Nuclear Reactors and Associated Plants
  22  General Studies of Nuclear Reactors
  37  Inorganic, Organic, Physical, and Analytical Chemistry (broad, excluded)
  38  Radiation Chemistry, Radiochemistry, and Nuclear Chemistry
  46  Instrumentation Related to Nuclear Science and Technology
  73  Nuclear Physics and Radiation Physics  (historical)
  77  Nuclear Physics and Radiation Physics  (current)

Multi-class (Task B): top-K most frequent primary codes (K=10 by default).
"""
import json, argparse, random, os
from collections import Counter

NFC_CODES = {7, 11, 12, 21, 22, 38, 46, 73, 77}

def load(path):
    with open(path) as f:
        for line in f:
            try:
                yield json.loads(line)
            except Exception:
                continue

def write_jsonl(path, records):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", required=True)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--topk", type=int, default=10)
    ap.add_argument("--max-binary", type=int, default=30000)
    ap.add_argument("--max-mc", type=int, default=30000)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    rng = random.Random(args.seed)
    records = list(load(args.raw))
    rng.shuffle(records)
    print(f"loaded {len(records)} raw records")
    code_counts = Counter(r["primary_code"] for r in records)
    print("top 20 codes:", code_counts.most_common(20))

    # ---- Binary ----
    pos = [r for r in records if r["primary_code"] in NFC_CODES]
    neg = [r for r in records if r["primary_code"] not in NFC_CODES]
    # Keep class imbalance roughly matching paper (~12% pos in fine-tune set).
    target_pos = min(len(pos), int(args.max_binary * 0.15))
    target_neg = min(len(neg), args.max_binary - target_pos)
    bin_recs = [
        {"text": (r["title"] + ". " + r["abstract"]).strip(), "label": 1}
        for r in pos[:target_pos]
    ] + [
        {"text": (r["title"] + ". " + r["abstract"]).strip(), "label": 0}
        for r in neg[:target_neg]
    ]
    rng.shuffle(bin_recs)
    n = len(bin_recs)
    tr = bin_recs[: int(0.8 * n)]
    vl = bin_recs[int(0.8 * n): int(0.9 * n)]
    te = bin_recs[int(0.9 * n):]
    write_jsonl(os.path.join(args.outdir, "binary", "train.jsonl"), tr)
    write_jsonl(os.path.join(args.outdir, "binary", "val.jsonl"), vl)
    write_jsonl(os.path.join(args.outdir, "binary", "test.jsonl"), te)
    print(f"binary: train={len(tr)} val={len(vl)} test={len(te)} pos_frac={sum(r['label'] for r in bin_recs)/n:.3f}")

    # ---- Multi-class ----
    top_codes = [c for c, _ in code_counts.most_common(args.topk)]
    code2idx = {c: i for i, c in enumerate(top_codes)}
    mc_pool = [r for r in records if r["primary_code"] in code2idx]
    rng.shuffle(mc_pool)
    mc_pool = mc_pool[: args.max_mc]
    mc_recs = [
        {
            "text": (r["title"] + ". " + r["abstract"]).strip(),
            "label": code2idx[r["primary_code"]],
            "primary_code": r["primary_code"],
            "primary_name": r["primary_name"],
        }
        for r in mc_pool
    ]
    n = len(mc_recs)
    tr = mc_recs[: int(0.8 * n)]
    vl = mc_recs[int(0.8 * n): int(0.9 * n)]
    te = mc_recs[int(0.9 * n):]
    write_jsonl(os.path.join(args.outdir, "multiclass", "train.jsonl"), tr)
    write_jsonl(os.path.join(args.outdir, "multiclass", "val.jsonl"), vl)
    write_jsonl(os.path.join(args.outdir, "multiclass", "test.jsonl"), te)
    # Save label map
    with open(os.path.join(args.outdir, "multiclass", "labels.json"), "w") as f:
        json.dump({"codes": top_codes, "code2idx": {str(k): v for k, v in code2idx.items()},
                   "names": {str(c): next((r["primary_name"] for r in records if r["primary_code"] == c), "") for c in top_codes}}, f, indent=2)
    print(f"multiclass: train={len(tr)} val={len(vl)} test={len(te)} classes={len(top_codes)}")
    print("label codes:", top_codes)

if __name__ == "__main__":
    main()

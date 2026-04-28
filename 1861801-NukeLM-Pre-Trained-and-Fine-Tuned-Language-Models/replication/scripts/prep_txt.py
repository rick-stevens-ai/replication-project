#!/usr/bin/env python3
"""Convert OSTI jsonl(s) into train/val plain-text files (one doc per line)."""
import argparse, json, os, random

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jsonl", nargs="+", required=True)
    ap.add_argument("--out-train", required=True)
    ap.add_argument("--out-val", required=True)
    ap.add_argument("--val-frac", type=float, default=0.02)
    ap.add_argument("--min-chars", type=int, default=200)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    rng = random.Random(args.seed)
    rows = []
    for p in args.jsonl:
        with open(p) as f:
            for line in f:
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                t = ((r.get("title") or "") + ". " + (r.get("abstract") or "")).strip()
                if len(t) < args.min_chars:
                    continue
                t = " ".join(t.split())
                rows.append(t)
    rng.shuffle(rows)
    n_val = max(500, int(len(rows) * args.val_frac))
    os.makedirs(os.path.dirname(args.out_train), exist_ok=True)
    os.makedirs(os.path.dirname(args.out_val), exist_ok=True)
    with open(args.out_train, "w") as f:
        for r in rows[n_val:]:
            f.write(r + "\n")
    with open(args.out_val, "w") as f:
        for r in rows[:n_val]:
            f.write(r + "\n")
    print(f"train={len(rows) - n_val} val={n_val} total={len(rows)}")

if __name__ == "__main__":
    main()

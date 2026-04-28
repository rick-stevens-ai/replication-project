#!/usr/bin/env python3
"""Collect all result.json / dapt_result.json under a root into a summary."""
import argparse, json, os, glob

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    summary = {"finetune": [], "dapt": []}
    for p in sorted(glob.glob(os.path.join(args.root, "**", "result.json"), recursive=True)):
        with open(p) as f:
            txt = f.read()
        try:
            r = json.loads(txt)
        except json.JSONDecodeError:
            # DDP may have written concatenated copies; keep first.
            dec = json.JSONDecoder()
            r, _ = dec.raw_decode(txt)
        r["_path"] = p
        summary["finetune"].append({
            "path": p,
            "task": r.get("task"),
            "model": r.get("model"),
            "n_train": r.get("n_train"),
            "n_test": r.get("n_test"),
            "train_seconds": r.get("train_seconds"),
            "test": r.get("test"),
            "val": r.get("val"),
        })
    for p in sorted(glob.glob(os.path.join(args.root, "**", "dapt_result.json"), recursive=True)):
        with open(p) as f:
            r = json.load(f)
        summary["dapt"].append({"path": p, **r})
    with open(args.out, "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()

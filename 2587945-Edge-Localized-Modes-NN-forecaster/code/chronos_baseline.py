"""Chronos-T5 baseline for ELM forecasting.

Applies amazon/chronos-t5-small per-pixel to each test-window's 30-step
history -> 30-step forecast, on the SAME synthetic dataset / split as
the FNO and ConvLSTM evaluations.

Usage:
    python chronos_baseline.py --out results --model amazon/chronos-t5-small

Notes
-----
Chronos is a generic zero-shot time-series forecaster (no fine-tuning).
Each of the 64 pixel channels is treated as an independent univariate
time series of length delta=30, and we ask Chronos for H=30 steps. We
take the median of the predictive samples as the point forecast (the
recommended default). This is honest about Chronos' role as a baseline:
it has never seen plasma data, and it's being asked to forecast a
high-frequency 1 us BES-like signal from only 30 us of context.
"""
from __future__ import annotations
import argparse
import json
import os
import time
import sys
from pathlib import Path

import numpy as np
import torch
from torch.utils.data import DataLoader

sys.path.insert(0, os.path.dirname(__file__))
from data import build_datasets
from train import metrics  # reuse metrics function

from chronos import ChronosPipeline


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="results")
    ap.add_argument("--model", default="amazon/chronos-t5-small")
    ap.add_argument("--n_train", type=int, default=32)
    ap.add_argument("--n_val", type=int, default=4)
    ap.add_argument("--n_test", type=int, default=4)
    ap.add_argument("--T", type=int, default=80_000)
    ap.add_argument("--delta", type=int, default=30)
    ap.add_argument("--H", type=int, default=30)
    ap.add_argument("--stride", type=int, default=80)
    ap.add_argument("--max_per_shot", type=int, default=200)
    ap.add_argument("--num_samples", type=int, default=10)
    ap.add_argument("--max_windows", type=int, default=200,
                    help="Cap test windows for compute budget; <=0 for all.")
    ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    args = ap.parse_args()
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)

    print(f"[chronos] device={args.device}, model={args.model}")
    print("[chronos] building datasets (same seeds as main run)...")
    t0 = time.time()
    _, _, test, _ = build_datasets(
        n_train=args.n_train, n_val=args.n_val, n_test=args.n_test,
        T=args.T, delta=args.delta, H=args.H, stride=args.stride,
        max_per_shot=args.max_per_shot,
    )
    print(f"  test windows={len(test)}  [{time.time()-t0:.1f}s]")

    # Collect all test (hist, targ) pairs deterministically
    hists = []; targs = []
    for i in range(len(test)):
        h, tg = test[i]
        hists.append(h.numpy()); targs.append(tg.numpy())
    hists = np.stack(hists)   # (N, delta, 8, 8)
    targs = np.stack(targs)   # (N, H, 8, 8)
    last_hist = hists[:, -1]  # (N, 8, 8)
    N = hists.shape[0]
    if args.max_windows > 0 and N > args.max_windows:
        # Use evenly-spaced subset (deterministic) so we match metric definitions
        idx = np.linspace(0, N - 1, args.max_windows).astype(int)
        hists = hists[idx]; targs = targs[idx]; last_hist = last_hist[idx]
        N = hists.shape[0]
        print(f"[chronos] subsampled to {N} windows for compute budget")

    # Per-pixel univariate series: (N*64, delta)
    P = hists.reshape(N, args.delta, 64).transpose(0, 2, 1).reshape(N * 64, args.delta)
    print(f"[chronos] forecasting {P.shape[0]} pixel series, len={args.delta} -> H={args.H}")

    pipe = ChronosPipeline.from_pretrained(
        args.model,
        device_map=args.device,
        torch_dtype=torch.bfloat16 if args.device == "cuda" else torch.float32,
    )

    # Chronos works best on un-normalized scale; our data is already normalized
    # to ~unit std. Add a constant offset to keep values strictly positive-ish?
    # Chronos handles arbitrary scalars fine via its internal scaling.
    BATCH = 64
    preds = np.zeros((N * 64, args.H), dtype=np.float32)
    t1 = time.time()
    for i in range(0, P.shape[0], BATCH):
        ctx = torch.from_numpy(P[i:i+BATCH]).float()
        # predict returns (B, num_samples, H)
        out_t = pipe.predict(inputs=ctx, prediction_length=args.H,
                             num_samples=args.num_samples)
        # Median over samples
        med = out_t.median(dim=1).values.cpu().numpy()  # (B, H)
        preds[i:i+BATCH] = med
        if (i // BATCH) % 25 == 0:
            print(f"  batch {i//BATCH+1}/{(P.shape[0]+BATCH-1)//BATCH}  "
                  f"{(time.time()-t1):.1f}s elapsed")
    print(f"[chronos] inference done in {time.time()-t1:.1f}s")

    # Reshape back to (N, H, 8, 8)
    preds = preds.reshape(N, 64, args.H).transpose(0, 2, 1).reshape(N, args.H, 8, 8)

    res = metrics(preds, targs, last_hist) | {
        "params": 0,            # zero-shot pretrained
        "model": args.model,
        "n_test_windows": int(N),
        "note": "zero-shot; per-pixel univariate; median of samples",
    }
    print(json.dumps({k: v for k, v in res.items() if k != "mse_per_step"}, indent=2))

    out_json = out / "chronos_metrics.json"
    with open(out_json, "w") as f:
        json.dump(res, f, indent=2)
    print(f"[chronos] saved {out_json}")


if __name__ == "__main__":
    main()

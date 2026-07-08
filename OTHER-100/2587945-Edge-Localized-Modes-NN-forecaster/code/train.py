"""Train and evaluate ELM forecasters.

Usage:
    python train.py --out results/

Pipeline:
  1) Generate synthetic shots & windows.
  2) Train FNO and ConvLSTM (pretrain direct + finetune autoregressive).
  3) Evaluate constant / FNO / ConvLSTM on test set.
  4) Compute per-event prediction & residual correlation, MSE-vs-lead-time,
     and a derived ROC for ELM-onset-in-next-H-steps using forecast.
  5) Save metrics JSON + plots.
"""
from __future__ import annotations
import argparse
import json
import os
import time
from pathlib import Path
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader

import sys
sys.path.insert(0, os.path.dirname(__file__))
from data import build_datasets
from models import ConstantBaseline, FNO2DForecaster, ConvLSTMSeq2Seq, count_params


def pearson(a: np.ndarray, b: np.ndarray) -> float:
    a = a.reshape(-1); b = b.reshape(-1)
    a = a - a.mean(); b = b - b.mean()
    den = (np.linalg.norm(a) * np.linalg.norm(b))
    return float((a @ b) / den) if den > 1e-9 else 0.0


def train_model(model: nn.Module, train_loader, val_loader, device,
                epochs_pre: int = 6, epochs_ft: int = 6, lr: float = 1e-3,
                tag: str = ""):
    model = model.to(device)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    log = []
    # ---- Stage 1: direct one-step MSE pretraining ----
    print(f"[{tag}] Stage 1: direct 1-step pretraining ({epochs_pre} ep)")
    for ep in range(epochs_pre):
        model.train(); tloss = 0.0; n = 0
        for hist, targ in train_loader:
            hist = hist.to(device); targ = targ.to(device)
            # one-step prediction: predict only first horizon step
            pred = model(hist, H=1)
            loss = F.mse_loss(pred, targ[:, :1])
            opt.zero_grad(); loss.backward(); opt.step()
            tloss += loss.item() * hist.size(0); n += hist.size(0)
        vloss = eval_loss(model, val_loader, device, H=1)
        msg = f"[{tag}] pre ep{ep+1} train_mse={tloss/n:.5f} val_mse_1step={vloss:.5f}"
        print(msg); log.append(msg)
    # ---- Stage 2: autoregressive H-step MSE finetuning ----
    print(f"[{tag}] Stage 2: autoregressive H-step finetuning ({epochs_ft} ep)")
    for ep in range(epochs_ft):
        model.train(); tloss = 0.0; n = 0
        for hist, targ in train_loader:
            hist = hist.to(device); targ = targ.to(device)
            pred = model(hist)  # full H
            loss = F.mse_loss(pred, targ)
            opt.zero_grad(); loss.backward(); opt.step()
            tloss += loss.item() * hist.size(0); n += hist.size(0)
        vloss = eval_loss(model, val_loader, device, H=None)
        msg = f"[{tag}] ft  ep{ep+1} train_mse={tloss/n:.5f} val_mse_H={vloss:.5f}"
        print(msg); log.append(msg)
    return log


def eval_loss(model, loader, device, H=None):
    model.eval(); tot=0.0; n=0
    with torch.no_grad():
        for hist, targ in loader:
            hist=hist.to(device); targ=targ.to(device)
            pred = model(hist, H=H) if H is not None else model(hist)
            t = targ[:, :pred.size(1)]
            tot += F.mse_loss(pred, t, reduction="sum").item()
            n += t.numel()
    return tot/max(n,1)


def collect_predictions(model, loader, device):
    """Return arrays preds (N, H, 8, 8) and targets (N, H, 8, 8) and last_hist (N,8,8)."""
    model.eval(); P=[]; T=[]; L=[]
    with torch.no_grad():
        for hist, targ in loader:
            hist=hist.to(device); targ=targ.to(device)
            pred = model(hist)
            P.append(pred.cpu().numpy()); T.append(targ.cpu().numpy()); L.append(hist[:,-1].cpu().numpy())
    return np.concatenate(P), np.concatenate(T), np.concatenate(L)


def metrics(preds, targs, last_hist):
    """Compute paper-style metrics + onset ROC."""
    N, H, _, _ = preds.shape
    # Per-event prediction correlation: each window treated as an "event slice"
    rho_pred = []
    for i in range(N):
        rho_pred.append(pearson(preds[i], targs[i]))
    rho_pred = np.array(rho_pred)
    # Constant baseline preds
    const = np.broadcast_to(last_hist[:, None], targs.shape)
    rho_const = np.array([pearson(const[i], targs[i]) for i in range(N)])
    # Residual correlation
    res_pred = preds - const
    res_targ = targs - const
    rho_resid = np.array([pearson(res_pred[i], res_targ[i]) for i in range(N)])
    # MSE per lead step (mean over events & 8x8)
    mse_per_step = ((preds - targs)**2).mean(axis=(0,2,3))
    # Onset classification: label = max gradient of mean-channel signal in next H exceeds threshold
    chan_mean_target = targs.mean(axis=(2,3))   # (N,H)
    chan_mean_pred   = preds.mean(axis=(2,3))   # (N,H)
    grad_t = np.diff(chan_mean_target, axis=1).max(axis=1)
    grad_p = np.diff(chan_mean_pred,   axis=1).max(axis=1)
    thr = np.quantile(grad_t, 0.7)             # top-30% as positive class
    y = (grad_t > thr).astype(int)
    s = grad_p
    auc = roc_auc(y, s)
    return {
        "rho_pred_mean": float(rho_pred.mean()),
        "rho_pred_median": float(np.median(rho_pred)),
        "rho_const_mean": float(rho_const.mean()),
        "rho_resid_mean": float(rho_resid.mean()),
        "mse_total": float(((preds-targs)**2).mean()),
        "mse_per_step": mse_per_step.tolist(),
        "onset_roc_auc": float(auc),
        "onset_pos_frac": float(y.mean()),
    }


def roc_auc(y, s):
    """Mann-Whitney U based AUC."""
    y = np.asarray(y); s = np.asarray(s)
    pos = s[y==1]; neg = s[y==0]
    if len(pos)==0 or len(neg)==0: return 0.5
    # rank-based
    order = np.argsort(s)
    ranks = np.empty_like(order, dtype=float)
    ranks[order] = np.arange(1, len(s)+1)
    sum_r_pos = ranks[y==1].sum()
    n1 = len(pos); n0 = len(neg)
    U = sum_r_pos - n1*(n1+1)/2.0
    return U/(n1*n0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="results")
    ap.add_argument("--n_train", type=int, default=32)
    ap.add_argument("--n_val", type=int, default=4)
    ap.add_argument("--n_test", type=int, default=4)
    ap.add_argument("--T", type=int, default=80_000)
    ap.add_argument("--delta", type=int, default=30)
    ap.add_argument("--H", type=int, default=30)
    ap.add_argument("--stride", type=int, default=80)
    ap.add_argument("--max_per_shot", type=int, default=200)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--epochs_pre", type=int, default=6)
    ap.add_argument("--epochs_ft", type=int, default=6)
    ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    args = ap.parse_args()
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    print("device:", args.device)

    print("Building datasets...")
    t0 = time.time()
    train, val, test, norm = build_datasets(
        n_train=args.n_train, n_val=args.n_val, n_test=args.n_test,
        T=args.T, delta=args.delta, H=args.H, stride=args.stride,
        max_per_shot=args.max_per_shot,
    )
    print(f"  train={len(train)} val={len(val)} test={len(test)} norm=(m={norm[0]:.3f},sd={norm[1]:.3f}) [{time.time()-t0:.1f}s]")

    train_loader = DataLoader(train, batch_size=args.batch, shuffle=True, num_workers=2, drop_last=True)
    val_loader   = DataLoader(val,   batch_size=args.batch, shuffle=False, num_workers=1)
    test_loader  = DataLoader(test,  batch_size=args.batch, shuffle=False, num_workers=1)

    results = {}

    # ---- Constant baseline ----
    print("\n=== Constant baseline ===")
    const = ConstantBaseline(args.H).to(args.device)
    p, t, l = collect_predictions(const, test_loader, args.device)
    results["constant"] = metrics(p, t, l) | {"params": 0}
    print(json.dumps(results["constant"], indent=2))

    # ---- FNO ----
    print("\n=== FNO 2D ===")
    fno = FNO2DForecaster(args.delta, args.H, hidden=32, modes=4, n_layers=4)
    print(f"  params: {count_params(fno):,}")
    log_fno = train_model(fno, train_loader, val_loader, args.device,
                          epochs_pre=args.epochs_pre, epochs_ft=args.epochs_ft, tag="FNO")
    p, t, l = collect_predictions(fno, test_loader, args.device)
    results["fno"] = metrics(p, t, l) | {"params": count_params(fno), "train_log": log_fno}
    print(json.dumps({k:v for k,v in results["fno"].items() if k!="train_log" and k!="mse_per_step"}, indent=2))
    torch.save(fno.state_dict(), out/"fno.pt")

    # ---- ConvLSTM ----
    print("\n=== ConvLSTM seq2seq ===")
    clstm = ConvLSTMSeq2Seq(args.delta, args.H, hidden=32, use_attention=True, use_smoothing=True)
    print(f"  params: {count_params(clstm):,}")
    log_cl = train_model(clstm, train_loader, val_loader, args.device,
                         epochs_pre=args.epochs_pre, epochs_ft=args.epochs_ft, tag="CLSTM")
    p, t, l = collect_predictions(clstm, test_loader, args.device)
    results["convlstm"] = metrics(p, t, l) | {"params": count_params(clstm), "train_log": log_cl}
    print(json.dumps({k:v for k,v in results["convlstm"].items() if k!="train_log" and k!="mse_per_step"}, indent=2))
    torch.save(clstm.state_dict(), out/"convlstm.pt")

    with open(out/"metrics.json","w") as f:
        json.dump(results, f, indent=2)
    print("\nSaved", out/"metrics.json")


if __name__ == "__main__":
    main()

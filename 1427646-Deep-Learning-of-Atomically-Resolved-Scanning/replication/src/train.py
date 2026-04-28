"""Train U-Net on synthetic STEM data for atomic-column pixelwise classification."""
import argparse, json, os, time
from pathlib import Path
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset

from synth_stem import generate_dataset, CLASS_NAMES, NUM_CLASSES, SimConfig
from unet import UNet


def rand_augment(x, y, rng):
    # x: (B,1,H,W), y: (B,H,W). Apply random flips and 90-deg rotations.
    B = x.size(0)
    for i in range(B):
        if rng.random() < 0.5:
            x[i] = torch.flip(x[i], dims=[-1])
            y[i] = torch.flip(y[i], dims=[-1])
        if rng.random() < 0.5:
            x[i] = torch.flip(x[i], dims=[-2])
            y[i] = torch.flip(y[i], dims=[-2])
        k = int(rng.integers(0, 4))
        if k:
            x[i] = torch.rot90(x[i], k, dims=[-2, -1])
            y[i] = torch.rot90(y[i], k, dims=[-2, -1])
        # brightness/contrast
        a = 1.0 + float(rng.normal(0, 0.1))
        b = float(rng.normal(0, 0.05))
        x[i] = torch.clamp(x[i] * a + b, 0, 1)
    return x, y


def compute_metrics(logits, y, n_classes=NUM_CLASSES):
    """Return dict with pixel-acc and per-class precision/recall (ignore defect = class5 for summary)."""
    pred = logits.argmax(1)
    acc = (pred == y).float().mean().item()
    pr = {}
    for c in range(n_classes):
        tp = ((pred == c) & (y == c)).sum().item()
        fp = ((pred == c) & (y != c)).sum().item()
        fn = ((pred != c) & (y == c)).sum().item()
        precision = tp / (tp + fp + 1e-9)
        recall = tp / (tp + fn + 1e-9)
        pr[CLASS_NAMES[c]] = {"precision": precision, "recall": recall,
                               "f1": 2 * precision * recall / (precision + recall + 1e-9),
                               "support": int((y == c).sum().item())}
    return {"pixel_acc": acc, "per_class": pr}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--n-train", type=int, default=512)
    p.add_argument("--n-val", type=int, default=64)
    p.add_argument("--n-test", type=int, default=64)
    p.add_argument("--img-size", type=int, default=256)
    p.add_argument("--epochs", type=int, default=30)
    p.add_argument("--batch-size", type=int, default=16)
    p.add_argument("--lr", type=float, default=2e-3)
    p.add_argument("--base-ch", type=int, default=32)
    p.add_argument("--gpu", type=int, default=0)
    p.add_argument("--out", type=str, default="./runs/unet")
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()

    os.makedirs(args.out, exist_ok=True)
    device = torch.device(f"cuda:{args.gpu}" if torch.cuda.is_available() else "cpu")
    print(f"[train] device={device} gpus={torch.cuda.device_count()}")

    t0 = time.time()
    cfg = SimConfig(img_size=args.img_size)
    print("[data] generating synthetic train/val/test ...")
    Xtr, Ytr = generate_dataset(args.n_train, cfg, seed=args.seed)
    Xva, Yva = generate_dataset(args.n_val, cfg, seed=args.seed + 1000)
    Xte, Yte = generate_dataset(args.n_test, cfg, seed=args.seed + 2000)
    print(f"[data] done in {time.time()-t0:.1f}s  train={Xtr.shape} val={Xva.shape} test={Xte.shape}")

    # save a quick preview
    np.save(os.path.join(args.out, "test_X.npy"), Xte)
    np.save(os.path.join(args.out, "test_Y.npy"), Yte)

    ds_tr = TensorDataset(torch.from_numpy(Xtr), torch.from_numpy(Ytr))
    ds_va = TensorDataset(torch.from_numpy(Xva), torch.from_numpy(Yva))
    dl_tr = DataLoader(ds_tr, batch_size=args.batch_size, shuffle=True, num_workers=2, drop_last=True)
    dl_va = DataLoader(ds_va, batch_size=args.batch_size, shuffle=False, num_workers=2)

    model = UNet(in_ch=1, n_classes=NUM_CLASSES, base=args.base_ch).to(device)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"[model] UNet base={args.base_ch}  params={n_params/1e6:.2f}M")

    # Class weights (defect class is rare)
    flat = torch.from_numpy(Ytr).flatten()
    counts = torch.bincount(flat, minlength=NUM_CLASSES).float()
    weights = (counts.sum() / (NUM_CLASSES * (counts + 1))).to(device)
    # Cap weights so defect class (very rare) doesn't explode
    weights = torch.clamp(weights, 0.2, 20.0)
    print(f"[train] class counts={counts.tolist()} weights={weights.tolist()}")

    crit = nn.CrossEntropyLoss(weight=weights)
    opt = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=1e-4)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=args.epochs)

    rng = np.random.default_rng(args.seed)
    history = []
    best_f1 = -1.0
    for epoch in range(args.epochs):
        model.train()
        tr_loss = 0.0
        n_seen = 0
        for xb, yb in dl_tr:
            xb = xb.to(device, non_blocking=True)
            yb = yb.to(device, non_blocking=True)
            xb, yb = rand_augment(xb, yb, rng)
            logits = model(xb)
            loss = crit(logits, yb)
            opt.zero_grad()
            loss.backward()
            opt.step()
            tr_loss += loss.item() * xb.size(0)
            n_seen += xb.size(0)
        sched.step()
        tr_loss /= max(n_seen, 1)

        # validation
        model.eval()
        with torch.no_grad():
            vloss = 0.0
            vcount = 0
            all_logits = []
            all_y = []
            for xb, yb in dl_va:
                xb = xb.to(device, non_blocking=True)
                yb = yb.to(device, non_blocking=True)
                logits = model(xb)
                vloss += crit(logits, yb).item() * xb.size(0)
                vcount += xb.size(0)
                all_logits.append(logits.cpu())
                all_y.append(yb.cpu())
            vloss /= max(vcount, 1)
            logits_cat = torch.cat(all_logits, 0)
            y_cat = torch.cat(all_y, 0)
            metrics = compute_metrics(logits_cat, y_cat)

        # Mean F1 across non-vacuum classes
        f1s = [metrics["per_class"][c]["f1"] for c in ["Sr","Ti","LaSr","Mn"]]
        mean_f1 = float(np.mean(f1s))
        history.append({"epoch": epoch, "train_loss": tr_loss, "val_loss": vloss,
                        "val_pixel_acc": metrics["pixel_acc"], "val_mean_f1_atoms": mean_f1})
        print(f"[epoch {epoch:02d}] train_loss={tr_loss:.4f} val_loss={vloss:.4f} "
              f"val_acc={metrics['pixel_acc']:.4f} mean_f1_atoms={mean_f1:.4f}")

        if mean_f1 > best_f1:
            best_f1 = mean_f1
            torch.save({"model": model.state_dict(), "args": vars(args), "metrics": metrics},
                       os.path.join(args.out, "best.pt"))

    # Final test
    print("[test] evaluating best model on held-out test set ...")
    ckpt = torch.load(os.path.join(args.out, "best.pt"), map_location=device)
    model.load_state_dict(ckpt["model"])
    model.eval()
    with torch.no_grad():
        dl_te = DataLoader(TensorDataset(torch.from_numpy(Xte), torch.from_numpy(Yte)),
                           batch_size=args.batch_size)
        all_logits = []; all_y = []
        for xb, yb in dl_te:
            xb = xb.to(device, non_blocking=True)
            logits = model(xb)
            all_logits.append(logits.cpu())
            all_y.append(yb)
        logits_cat = torch.cat(all_logits, 0)
        y_cat = torch.cat(all_y, 0)
        test_metrics = compute_metrics(logits_cat, y_cat)
    print("[test] metrics:", json.dumps(test_metrics, indent=2))

    # Save preds for a handful of samples for figures
    with torch.no_grad():
        xb = torch.from_numpy(Xte[:8]).to(device)
        pred = model(xb).argmax(1).cpu().numpy()
    np.save(os.path.join(args.out, "test_pred_sample.npy"), pred)

    with open(os.path.join(args.out, "history.json"), "w") as f:
        json.dump(history, f, indent=2)
    with open(os.path.join(args.out, "test_metrics.json"), "w") as f:
        json.dump(test_metrics, f, indent=2)
    print("[done] total time:", f"{(time.time()-t0):.1f}s")


if __name__ == "__main__":
    main()

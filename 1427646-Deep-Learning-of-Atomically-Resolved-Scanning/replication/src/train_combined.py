"""Train U-Net using BOTH the synthetic surrogate and a multislice subset.

Loads:
  - synthetic train via synth_stem.generate_dataset
  - multislice images/labels saved by multislice_gen.py

Evaluates on a held-out multislice subset to mimic 'real' physics.
"""
import argparse, json, os, time, sys
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset

from synth_stem import generate_dataset, CLASS_NAMES, NUM_CLASSES, SimConfig
from unet import UNet


def crop_or_pad(img, size):
    """Center-crop/pad img (H,W) to (size,size). Pad with 0."""
    H, W = img.shape
    out = np.zeros((size, size), dtype=img.dtype)
    h = min(H, size); w = min(W, size)
    sy = (size-h)//2; sx = (size-w)//2
    iy = (H-h)//2; ix = (W-w)//2
    out[sy:sy+h, sx:sx+w] = img[iy:iy+h, ix:ix+w]
    return out


def load_multislice(d, size):
    imgs = np.load(os.path.join(d, "images.npy"))
    lbls = np.load(os.path.join(d, "labels.npy"))
    n = imgs.shape[0]
    X = np.zeros((n, 1, size, size), dtype=np.float32)
    Y = np.zeros((n, size, size), dtype=np.int64)
    for i in range(n):
        X[i,0] = crop_or_pad(imgs[i], size)
        Y[i] = crop_or_pad(lbls[i], size)
    return X, Y


def rand_augment(x, y, rng):
    B = x.size(0)
    for i in range(B):
        if rng.random() < 0.5:
            x[i] = torch.flip(x[i], dims=[-1]); y[i] = torch.flip(y[i], dims=[-1])
        if rng.random() < 0.5:
            x[i] = torch.flip(x[i], dims=[-2]); y[i] = torch.flip(y[i], dims=[-2])
        k = int(rng.integers(0,4))
        if k:
            x[i] = torch.rot90(x[i], k, dims=[-2,-1])
            y[i] = torch.rot90(y[i], k, dims=[-2,-1])
        a = 1.0 + float(rng.normal(0,0.1)); b = float(rng.normal(0,0.05))
        x[i] = torch.clamp(x[i]*a+b, 0, 1)
    return x, y


def metrics(logits, y, names=None):
    pred = logits.argmax(1)
    acc = (pred==y).float().mean().item()
    out = {}
    n = logits.shape[1]
    for c in range(n):
        tp=((pred==c)&(y==c)).sum().item()
        fp=((pred==c)&(y!=c)).sum().item()
        fn=((pred!=c)&(y==c)).sum().item()
        p=tp/max(tp+fp,1e-9); r=tp/max(tp+fn,1e-9)
        f1=2*p*r/(p+r+1e-9)
        nm = (names or CLASS_NAMES)[c]
        out[nm]={"precision":p,"recall":r,"f1":f1,"support":int((y==c).sum().item())}
    return {"pixel_acc":acc,"per_class":out}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ms-dir", default="multislice_data")
    ap.add_argument("--n-synth", type=int, default=384)
    ap.add_argument("--img-size", type=int, default=64)
    ap.add_argument("--epochs", type=int, default=20)
    ap.add_argument("--batch", type=int, default=16)
    ap.add_argument("--lr", type=float, default=2e-3)
    ap.add_argument("--out", default="runs/combined")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    device = torch.device("mps" if torch.backends.mps.is_available()
                          else ("cuda" if torch.cuda.is_available() else "cpu"))
    print(f"[device] {device}")

    rng = np.random.default_rng(args.seed)

    # multislice
    print(f"[ms] loading {args.ms_dir}")
    Xms, Yms = load_multislice(args.ms_dir, args.img_size)
    print(f"[ms] X={Xms.shape} Y={Yms.shape}")
    n = Xms.shape[0]
    perm = rng.permutation(n)
    n_test = max(8, n//4)
    test_idx = perm[:n_test]; train_idx = perm[n_test:]
    Xms_te, Yms_te = Xms[test_idx], Yms[test_idx]
    Xms_tr, Yms_tr = Xms[train_idx], Yms[train_idx]
    print(f"[ms] split: train={len(Xms_tr)} test={len(Xms_te)}")

    # synthetic train
    cfg = SimConfig(img_size=args.img_size)
    print(f"[synth] generating {args.n_synth} synthetic samples ...")
    Xs_tr, Ys_tr = generate_dataset(args.n_synth, cfg, seed=args.seed)
    print(f"[synth] X={Xs_tr.shape}")

    # combine train sets
    Xtr = np.concatenate([Xs_tr, Xms_tr], axis=0)
    Ytr = np.concatenate([Ys_tr, Yms_tr], axis=0)
    print(f"[combined] train X={Xtr.shape}")

    ds_tr = TensorDataset(torch.from_numpy(Xtr), torch.from_numpy(Ytr))
    dl_tr = DataLoader(ds_tr, batch_size=args.batch, shuffle=True, drop_last=True)

    Xte_t = torch.from_numpy(Xms_te); Yte_t = torch.from_numpy(Yms_te)

    model = UNet(in_ch=1, n_classes=NUM_CLASSES, base=32).to(device)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"[model] params={n_params/1e6:.2f}M")

    flat = torch.from_numpy(Ytr).flatten()
    counts = torch.bincount(flat, minlength=NUM_CLASSES).float()
    w = torch.clamp(counts.sum()/(NUM_CLASSES*(counts+1)), 0.2, 20.0).to(device)
    crit = nn.CrossEntropyLoss(weight=w)
    opt = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=1e-4)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=args.epochs)

    history = []
    for epoch in range(args.epochs):
        model.train()
        tloss=0; ns=0
        for xb,yb in dl_tr:
            xb=xb.to(device); yb=yb.to(device)
            xb,yb = rand_augment(xb,yb,rng)
            logits = model(xb)
            loss = crit(logits, yb)
            opt.zero_grad(); loss.backward(); opt.step()
            tloss += loss.item()*xb.size(0); ns += xb.size(0)
        sched.step()
        # eval on multislice held-out
        model.eval()
        with torch.no_grad():
            xb = Xte_t.to(device); yb = Yte_t.to(device)
            logits = model(xb)
            m = metrics(logits.cpu(), yb.cpu())
        f1s = [m["per_class"][c]["f1"] for c in ["Sr","Ti","LaSr","Mn"]]
        history.append({"epoch":epoch, "train_loss":tloss/ns, "ms_acc":m["pixel_acc"], "ms_mean_f1":float(np.mean(f1s))})
        print(f"[ep {epoch:02d}] tr_loss={tloss/ns:.4f} ms_acc={m['pixel_acc']:.4f} mean_f1={np.mean(f1s):.4f}")
    
    # final test metrics
    print("[final] multislice held-out:")
    print(json.dumps(m, indent=2))
    json.dump(m, open(os.path.join(args.out,"ms_test_metrics.json"),"w"), indent=2)
    json.dump(history, open(os.path.join(args.out,"history.json"),"w"), indent=2)
    torch.save({"model":model.state_dict(),"args":vars(args)}, os.path.join(args.out,"best.pt"))
    np.save(os.path.join(args.out,"ms_test_X.npy"), Xms_te)
    np.save(os.path.join(args.out,"ms_test_Y.npy"), Yms_te)
    with torch.no_grad():
        pred = model(Xte_t.to(device)).argmax(1).cpu().numpy()
    np.save(os.path.join(args.out,"ms_test_pred.npy"), pred)
    print(f"[done] saved → {args.out}")

if __name__ == "__main__":
    main()

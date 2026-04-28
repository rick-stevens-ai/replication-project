"""Produce report figures from trained model + cached test arrays.

Figures:
  fig_data.png     : sample images with ground-truth label overlay
  fig_pred.png     : input | GT | prediction side-by-side (4 examples)
  fig_history.png  : training curves
  fig_confmat.png  : confusion matrix + per-class F1 bar
  fig_peaks.png    : peak-finding atomic positions & RMSE to ground truth
"""
import json, os, sys
from pathlib import Path
import numpy as np
import torch
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from scipy.ndimage import maximum_filter, label as nd_label, center_of_mass

sys.path.insert(0, os.path.dirname(__file__))
from unet import UNet
from synth_stem import CLASS_NAMES, NUM_CLASSES

RUN_DIR = Path(os.environ.get("RUN_DIR", "../runs/unet"))
OUT_DIR = Path(os.environ.get("FIG_DIR", "../figures"))
OUT_DIR.mkdir(parents=True, exist_ok=True)

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# Load data and model
Xte = np.load(RUN_DIR / "test_X.npy")
Yte = np.load(RUN_DIR / "test_Y.npy")
hist = json.loads((RUN_DIR / "history.json").read_text())
tm = json.loads((RUN_DIR / "test_metrics.json").read_text())
ckpt = torch.load(RUN_DIR / "best.pt", map_location=device, weights_only=False)
args = ckpt["args"]
model = UNet(in_ch=1, n_classes=NUM_CLASSES, base=args["base_ch"]).to(device)
model.load_state_dict(ckpt["model"])
model.eval()

with torch.no_grad():
    xb = torch.from_numpy(Xte).to(device)
    preds = []
    for i in range(0, len(xb), 16):
        preds.append(model(xb[i:i+16]).argmax(1).cpu().numpy())
    pred = np.concatenate(preds, 0)

# Color map: vacuum black, Sr cyan, Ti blue, LaSr orange, Mn red, defect yellow
cmap = ListedColormap(["#000000", "#00d0d0", "#2050ff", "#ff8800", "#e02020", "#ffee00"])

# --- fig_data: samples with GT ---
fig, ax = plt.subplots(2, 4, figsize=(13, 6.5))
for i in range(4):
    ax[0, i].imshow(Xte[i, 0], cmap="gray")
    ax[0, i].set_title(f"Synth. HAADF-STEM #{i}")
    ax[0, i].axis("off")
    ax[1, i].imshow(Yte[i], cmap=cmap, vmin=0, vmax=5, interpolation="nearest")
    ax[1, i].set_title("Ground-truth labels")
    ax[1, i].axis("off")
plt.tight_layout()
plt.savefig(OUT_DIR / "fig_data.png", dpi=130)
plt.close()

# --- fig_pred: input | GT | pred | error ---
fig, ax = plt.subplots(4, 4, figsize=(13, 13))
for i in range(4):
    err = (pred[i] != Yte[i]).astype(np.float32)
    ax[i, 0].imshow(Xte[i, 0], cmap="gray");       ax[i, 0].set_title("input"); ax[i, 0].axis("off")
    ax[i, 1].imshow(Yte[i], cmap=cmap, vmin=0, vmax=5); ax[i, 1].set_title("GT"); ax[i, 1].axis("off")
    ax[i, 2].imshow(pred[i], cmap=cmap, vmin=0, vmax=5); ax[i, 2].set_title("U-Net pred"); ax[i, 2].axis("off")
    ax[i, 3].imshow(err, cmap="hot", vmin=0, vmax=1);   ax[i, 3].set_title("error map"); ax[i, 3].axis("off")
plt.tight_layout()
plt.savefig(OUT_DIR / "fig_pred.png", dpi=130)
plt.close()

# --- fig_history: training curves ---
ep = [h["epoch"] for h in hist]
fig, ax = plt.subplots(1, 2, figsize=(10, 3.8))
ax[0].plot(ep, [h["train_loss"] for h in hist], label="train")
ax[0].plot(ep, [h["val_loss"] for h in hist], label="val")
ax[0].set_xlabel("epoch"); ax[0].set_ylabel("cross-entropy loss"); ax[0].legend(); ax[0].set_title("loss")
ax[1].plot(ep, [h["val_pixel_acc"] for h in hist], label="pixel acc")
ax[1].plot(ep, [h["val_mean_f1_atoms"] for h in hist], label="mean-F1 (Sr,Ti,LaSr,Mn)")
ax[1].set_xlabel("epoch"); ax[1].legend(); ax[1].set_title("val metrics"); ax[1].set_ylim(0.4, 1.02)
plt.tight_layout()
plt.savefig(OUT_DIR / "fig_history.png", dpi=130)
plt.close()

# --- fig_confmat + bar ---
yf = Yte.flatten(); pf = pred.flatten()
K = NUM_CLASSES
cm = np.zeros((K, K), dtype=np.int64)
for t in range(K):
    for p in range(K):
        cm[t, p] = int(((yf == t) & (pf == p)).sum())
# normalize rows
cmn = cm / (cm.sum(axis=1, keepdims=True) + 1e-9)

fig, ax = plt.subplots(1, 2, figsize=(11, 4.5))
im = ax[0].imshow(cmn, cmap="Blues", vmin=0, vmax=1)
ax[0].set_xticks(range(K)); ax[0].set_yticks(range(K))
ax[0].set_xticklabels(CLASS_NAMES, rotation=30); ax[0].set_yticklabels(CLASS_NAMES)
ax[0].set_xlabel("pred"); ax[0].set_ylabel("true"); ax[0].set_title("row-normalized confusion matrix")
for i in range(K):
    for j in range(K):
        if cm[i, :].sum() > 0:
            ax[0].text(j, i, f"{cmn[i,j]:.2f}", ha="center", va="center",
                        color="white" if cmn[i, j] > 0.5 else "black", fontsize=8)
plt.colorbar(im, ax=ax[0], fraction=0.046)

f1 = [tm["per_class"][c]["f1"] for c in CLASS_NAMES]
p = [tm["per_class"][c]["precision"] for c in CLASS_NAMES]
r = [tm["per_class"][c]["recall"] for c in CLASS_NAMES]
x = np.arange(K); w = 0.28
ax[1].bar(x - w, p, w, label="precision")
ax[1].bar(x,     r, w, label="recall")
ax[1].bar(x + w, f1, w, label="F1")
ax[1].set_xticks(x); ax[1].set_xticklabels(CLASS_NAMES, rotation=30)
ax[1].set_ylim(0, 1.02); ax[1].legend(); ax[1].set_title("per-class test metrics")
plt.tight_layout()
plt.savefig(OUT_DIR / "fig_confmat.png", dpi=130)
plt.close()

# --- Peak finding: predicted atomic positions vs. GT ---
def find_peaks(mask: np.ndarray, neigh: int = 5):
    """Return (y,x) centroids of connected components of mask."""
    if mask.sum() == 0:
        return np.zeros((0, 2))
    labels, n = nd_label(mask)
    if n == 0:
        return np.zeros((0, 2))
    coms = center_of_mass(mask, labels, range(1, n + 1))
    return np.array(coms)  # (N, 2) row, col

def match_rmse(a: np.ndarray, b: np.ndarray, tol: float = 8.0):
    """Greedy nearest-neighbour match; return (rmse, matched, total_a, total_b)."""
    if len(a) == 0 or len(b) == 0:
        return float("nan"), 0, len(a), len(b)
    from scipy.spatial import cKDTree
    tree = cKDTree(b)
    d, idx = tree.query(a, k=1)
    keep = d < tol
    rmse = float(np.sqrt(np.mean(d[keep] ** 2))) if keep.sum() else float("nan")
    return rmse, int(keep.sum()), len(a), len(b)

# Accumulate over test set for each atomic class (1..4)
peak_stats = {}
for cls, name in enumerate(CLASS_NAMES):
    if name in ("vacuum", "defect"):
        continue
    rmses = []
    matched = 0; total_gt = 0; total_pr = 0
    for i in range(len(Yte)):
        gt_pk = find_peaks(Yte[i] == cls)
        pr_pk = find_peaks(pred[i] == cls)
        rmse, m, ta, tb = match_rmse(pr_pk, gt_pk)
        if not np.isnan(rmse):
            rmses.append(rmse)
        matched += m; total_pr += ta; total_gt += tb
    peak_stats[name] = {
        "mean_rmse_px": float(np.mean(rmses)) if rmses else float("nan"),
        "matched": matched,
        "total_gt": total_gt,
        "total_pred": total_pr,
        "detect_recall": matched / max(total_gt, 1),
        "detect_precision": matched / max(total_pr, 1),
    }

# Plot one example with peaks overlaid
i0 = 0
fig, ax = plt.subplots(1, 2, figsize=(11, 5))
ax[0].imshow(Xte[i0, 0], cmap="gray")
for cls, color in [(1, "#00ffff"), (2, "#66aaff"), (3, "#ffaa00"), (4, "#ff6060")]:
    gt_pk = find_peaks(Yte[i0] == cls)
    pr_pk = find_peaks(pred[i0] == cls)
    if len(gt_pk):
        ax[0].scatter(gt_pk[:, 1], gt_pk[:, 0], s=24, facecolors="none",
                      edgecolors=color, linewidths=1.2, label=f"GT {CLASS_NAMES[cls]}")
    if len(pr_pk):
        ax[0].scatter(pr_pk[:, 1], pr_pk[:, 0], s=6, c=color, label=f"pred {CLASS_NAMES[cls]}")
ax[0].legend(fontsize=7, ncol=2, loc="upper right")
ax[0].set_title(f"Peak detection overlay (example {i0})"); ax[0].axis("off")

names = [n for n in CLASS_NAMES if n not in ("vacuum", "defect")]
rmses = [peak_stats[n]["mean_rmse_px"] for n in names]
recs  = [peak_stats[n]["detect_recall"] for n in names]
precs = [peak_stats[n]["detect_precision"] for n in names]
x = np.arange(len(names)); w = 0.35
ax[1].bar(x - w/2, recs, w, label="recall")
ax[1].bar(x + w/2, precs, w, label="precision")
for xi, rm in zip(x, rmses):
    ax[1].text(xi, 0.05, f"RMSE={rm:.2f}px", ha="center", fontsize=9, color="black")
ax[1].set_xticks(x); ax[1].set_xticklabels(names)
ax[1].set_ylim(0, 1.05); ax[1].legend(); ax[1].set_title("atomic-column detection")
plt.tight_layout()
plt.savefig(OUT_DIR / "fig_peaks.png", dpi=130)
plt.close()

with open(OUT_DIR / "peak_stats.json", "w") as f:
    json.dump(peak_stats, f, indent=2)

print("wrote figures to", OUT_DIR.resolve())
print(json.dumps(peak_stats, indent=2))

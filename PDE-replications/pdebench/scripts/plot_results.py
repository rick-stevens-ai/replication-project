"""Plot training history + sample rollouts + comparison to persistence baseline."""
from __future__ import annotations
import json
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import torch
import sys

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT / "repo"
sys.path.insert(0, str(REPO / "pdebench" / "models"))
from metrics import metric_func   # type: ignore  # noqa: E402

RES = ROOT / "results"
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)


def main():
    summary = json.loads((RES / "fno_advection_summary.json").read_text())
    pred = np.load(RES / "fno_advection_test_pred.npy")  # (b, x, t, ch)
    tgt = np.load(RES / "fno_advection_test_tgt.npy")
    init_step = summary["initial_step"]
    print("pred", pred.shape, "tgt", tgt.shape, "init_step", init_step)

    # Persistence baseline: prediction = repeat last context frame
    persist = tgt.copy()
    for t in range(init_step - 1, persist.shape[2] - 1):
        persist[:, :, t + 1, :] = persist[:, :, init_step - 1, :]

    rmse_p, nrmse_p, *_ = metric_func(
        torch.from_numpy(persist), torch.from_numpy(tgt), if_mean=True, Lx=1.0, initial_step=init_step
    )
    nrmse_persist = float(nrmse_p.mean())
    print(f"Persistence baseline nRMSE = {nrmse_persist:.4e}")
    print(f"FNO trained         nRMSE = {summary['final_test_nRMSE']:.4e}")

    summary["persistence_test_nRMSE"] = nrmse_persist
    summary["persistence_test_RMSE"] = float(rmse_p.mean())
    (RES / "fno_advection_summary.json").write_text(json.dumps(summary, indent=2))

    # Figure 1: training curve
    h = summary["history"]
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    ax[0].plot(h["train_loss"], label="train MSE")
    ax[0].set_yscale("log"); ax[0].grid(alpha=0.3); ax[0].set_xlabel("epoch")
    ax[0].set_title("Training loss")
    ax[0].legend()
    ax[1].plot(h["val_nrmse"], label="val nRMSE (autoreg rollout)")
    ax[1].axhline(nrmse_persist, ls="--", c="red", label=f"persistence={nrmse_persist:.3f}")
    ax[1].axhline(summary["final_test_nRMSE"], ls=":", c="green", label=f"FNO test={summary['final_test_nRMSE']:.3f}")
    ax[1].set_yscale("log"); ax[1].grid(alpha=0.3); ax[1].set_xlabel("epoch")
    ax[1].set_title("Validation nRMSE")
    ax[1].legend(fontsize=8)
    fig.suptitle("PDEBench replication — FNO1d on 1D Advection β=1.0 (small subset)")
    fig.tight_layout()
    fig.savefig(FIG / "training_curve.png", dpi=120)
    print("wrote", FIG / "training_curve.png")

    # Figure 2: sample trajectory comparison (x-t image)
    sample = 0
    fig, axs = plt.subplots(1, 3, figsize=(12, 4), sharey=True)
    extent = [0, summary["data_shape_bxtc"][2], 0, 1]  # t, x
    for a, arr, ttl in zip(axs, (tgt, pred, np.abs(pred - tgt)), ("ground truth", "FNO prediction", "|error|")):
        im = a.imshow(arr[sample, :, :, 0], aspect="auto", origin="lower", extent=extent, cmap="RdBu_r" if ttl != "|error|" else "magma")
        a.set_title(ttl); a.set_xlabel("t index"); a.set_ylabel("x" if a is axs[0] else "")
        plt.colorbar(im, ax=a, fraction=0.04)
    fig.suptitle(f"Test sample {sample} — initial_step={init_step}, rest autoregressive")
    fig.tight_layout()
    fig.savefig(FIG / "sample_rollout.png", dpi=120)
    print("wrote", FIG / "sample_rollout.png")


if __name__ == "__main__":
    main()

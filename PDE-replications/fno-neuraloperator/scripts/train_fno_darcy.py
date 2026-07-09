"""
FNO on small Darcy-Flow — replication script.

Adapted from neuraloperator/neuraloperator examples/models/plot_FNO_darcy.py
(MIT, NeuralOperator developers, 2023).

Modifications:
  * Non-interactive: writes figures to ./figures/, metrics JSON to ./results/.
  * Adds explicit final relative-L2 evaluation at both train and super-resolution test sets.
  * Seeded for reproducibility.
"""

import os, sys, json, time, argparse
import numpy as np
import torch
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from neuralop.models import FNO
from neuralop import Trainer, LpLoss, H1Loss
from neuralop.training import AdamW
from neuralop.data.datasets import load_darcy_flow_small
from neuralop.utils import count_model_params


def set_seed(seed: int) -> None:
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def relative_l2(pred: torch.Tensor, target: torch.Tensor) -> float:
    """Mean over batch of ||pred-y||_2 / ||y||_2 (per-sample, flattened)."""
    p = pred.reshape(pred.shape[0], -1)
    t = target.reshape(target.shape[0], -1)
    num = torch.linalg.vector_norm(p - t, dim=1)
    den = torch.linalg.vector_norm(t, dim=1).clamp_min(1e-12)
    return (num / den).mean().item()


def evaluate(model, loader, data_processor, device):
    model.eval()
    rels, h1s, n = [], [], 0
    h1 = H1Loss(d=2)
    with torch.no_grad():
        for batch in loader:
            batch = data_processor.preprocess(batch, batched=True)
            x = batch["x"].to(device)
            y = batch["y"].to(device)
            out = model(x)
            # Match shapes
            if out.shape != y.shape:
                # Some processors keep extra channel dim; squeeze if needed
                out = out.reshape(y.shape)
            rels.append(relative_l2(out, y) * x.shape[0])
            h1s.append(h1(out, y).item() * x.shape[0])
            n += x.shape[0]
    return {"rel_l2": float(sum(rels) / n), "h1": float(sum(h1s) / n), "n": int(n)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--epochs", type=int, default=20)
    ap.add_argument("--n-train", type=int, default=1000)
    ap.add_argument("--batch-size", type=int, default=64)
    ap.add_argument("--n-modes", type=int, default=8)
    ap.add_argument("--hidden-channels", type=int, default=24)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--out-dir", default=os.path.join(os.path.dirname(__file__), ".."))
    args = ap.parse_args()

    set_seed(args.seed)
    device = args.device

    out_dir = os.path.abspath(args.out_dir)
    fig_dir = os.path.join(out_dir, "figures")
    res_dir = os.path.join(out_dir, "results")
    log_dir = os.path.join(out_dir, "logs")
    os.makedirs(fig_dir, exist_ok=True)
    os.makedirs(res_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)

    print(f"[setup] device={device}  epochs={args.epochs}  n_train={args.n_train}  "
          f"modes={args.n_modes}  hidden={args.hidden_channels}  seed={args.seed}", flush=True)

    t0 = time.time()

    # ----- Data -----
    train_loader, test_loaders, data_processor = load_darcy_flow_small(
        n_train=args.n_train,
        batch_size=args.batch_size,
        n_tests=[100, 50],
        test_resolutions=[16, 32],
        test_batch_sizes=[32, 32],
    )
    data_processor = data_processor.to(device)
    print(f"[data] train batches={len(train_loader)}  "
          f"test resolutions={list(test_loaders.keys())}", flush=True)

    # ----- Model -----
    model = FNO(
        n_modes=(args.n_modes, args.n_modes),
        in_channels=1,
        out_channels=1,
        hidden_channels=args.hidden_channels,
        projection_channel_ratio=2,
    ).to(device)
    n_params = count_model_params(model)
    print(f"[model] FNO params={n_params}", flush=True)

    # ----- Optim -----
    optimizer = AdamW(model.parameters(), lr=1e-2, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs)

    l2loss = LpLoss(d=2, p=2)
    h1loss = H1Loss(d=2)
    train_loss = h1loss
    eval_losses = {"h1": h1loss, "l2": l2loss}

    trainer = Trainer(
        model=model,
        n_epochs=args.epochs,
        device=device,
        data_processor=data_processor,
        wandb_log=False,
        eval_interval=5,
        use_distributed=False,
        verbose=True,
    )

    # ----- Pre-training eval (sanity baseline = untrained model) -----
    pre_train_eval = {
        f"res_{r}": evaluate(model, test_loaders[r], data_processor, device)
        for r in test_loaders
    }
    print(f"[pre-train] {pre_train_eval}", flush=True)

    # ----- Train -----
    trainer.train(
        train_loader=train_loader,
        test_loaders=test_loaders,
        optimizer=optimizer,
        scheduler=scheduler,
        regularizer=False,
        training_loss=train_loss,
        eval_losses=eval_losses,
    )

    # ----- Post-training eval (custom rel-L2) -----
    post_eval = {
        f"res_{r}": evaluate(model, test_loaders[r], data_processor, device)
        for r in test_loaders
    }
    print(f"[post-train] {post_eval}", flush=True)

    elapsed = time.time() - t0
    metrics = {
        "config": vars(args),
        "n_params": int(n_params),
        "elapsed_seconds": elapsed,
        "torch_version": torch.__version__,
        "numpy_version": np.__version__,
        "device": device,
        "pre_train": pre_train_eval,
        "post_train": post_eval,
    }
    res_path = os.path.join(res_dir, "metrics.json")
    with open(res_path, "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"[done] wrote {res_path}  elapsed={elapsed:.1f}s", flush=True)

    # ----- Figures: train-res (16) and zero-shot super-res (32) -----
    def make_panel(res, title, fname):
        ds = test_loaders[res].dataset
        fig = plt.figure(figsize=(7, 7))
        for idx in range(3):
            data = ds[idx]
            data = data_processor.preprocess(data, batched=False)
            x = data["x"]
            y = data["y"]
            with torch.no_grad():
                out = model(x.unsqueeze(0))
            ax = fig.add_subplot(3, 3, idx * 3 + 1)
            ax.imshow(x[0].cpu(), cmap="gray")
            if idx == 0:
                ax.set_title(f"Input ({res}x{res})")
            ax.set_xticks([]); ax.set_yticks([])
            ax = fig.add_subplot(3, 3, idx * 3 + 2)
            ax.imshow(y.squeeze().cpu())
            if idx == 0:
                ax.set_title("Ground truth")
            ax.set_xticks([]); ax.set_yticks([])
            ax = fig.add_subplot(3, 3, idx * 3 + 3)
            ax.imshow(out.squeeze().cpu().numpy())
            if idx == 0:
                ax.set_title("FNO prediction")
            ax.set_xticks([]); ax.set_yticks([])
        fig.suptitle(title, y=0.98)
        plt.tight_layout()
        fig_path = os.path.join(fig_dir, fname)
        fig.savefig(fig_path, dpi=120)
        plt.close(fig)
        print(f"[fig] wrote {fig_path}", flush=True)

    make_panel(16, "FNO predictions on 16x16 Darcy-Flow", "darcy_16.png")
    make_panel(32, "Zero-shot super-resolution: trained on 16, tested at 32",
               "darcy_32_zeroshot.png")


if __name__ == "__main__":
    main()

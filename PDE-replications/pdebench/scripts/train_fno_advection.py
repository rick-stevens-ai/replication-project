"""Train PDEBench's FNO1d baseline on a small locally-generated 1D Advection
dataset (β=1.0), matching the PDEBench autoregressive protocol with
initial_step=10. Reports RMSE and nRMSE (PDEBench metrics) on the held-out
test split. Pure CPU, kept tiny so it runs on a laptop in a few minutes.
"""
from __future__ import annotations
import argparse
import json
import sys
import time
from pathlib import Path

import h5py
import numpy as np
import torch
from torch.utils.data import DataLoader, TensorDataset

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT / "repo"
sys.path.insert(0, str(REPO / "pdebench" / "models"))

# Official PDEBench modules
from fno.fno import FNO1d                       # type: ignore  # noqa: E402
from metrics import metric_func                 # type: ignore  # noqa: E402


def load_dataset(hdf5_path: Path, reduced_resolution: int = 1, reduced_resolution_t: int = 1):
    with h5py.File(hdf5_path, "r") as f:
        u = f["tensor"][:].astype(np.float32)                # (b, t, x)
        x = f["x-coordinate"][:].astype(np.float32)         # (x,)
    u = u[:, ::reduced_resolution_t, ::reduced_resolution]
    x = x[::reduced_resolution]
    # PDEBench FNO expects (b, x, t, ch) layout
    u = np.transpose(u, (0, 2, 1))[..., None]               # (b, x, t, 1)
    return torch.from_numpy(u), torch.from_numpy(x).unsqueeze(-1)  # grid: (x, 1)


def split(data: torch.Tensor, n_train: int, n_val: int):
    n_test = data.shape[0] - n_train - n_val
    assert n_test > 0, f"need n_test>0; got {n_test}"
    return data[:n_train], data[n_train:n_train + n_val], data[n_train + n_val:]


def make_loader(data: torch.Tensor, batch_size: int, shuffle: bool):
    return DataLoader(TensorDataset(data), batch_size=batch_size, shuffle=shuffle, num_workers=0)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=str(ROOT / "data" / "1D_Advection_Sols_beta1.0.hdf5"))
    ap.add_argument("--initial-step", type=int, default=10, help="PDEBench default = 10")
    ap.add_argument("--modes", type=int, default=12)
    ap.add_argument("--width", type=int, default=20)
    ap.add_argument("--batch-size", type=int, default=16)
    ap.add_argument("--epochs", type=int, default=40)
    ap.add_argument("--lr", type=float, default=1e-3)
    ap.add_argument("--n-train", type=int, default=96)
    ap.add_argument("--n-val", type=int, default=16)
    ap.add_argument("--reduced-resolution", type=int, default=1)
    ap.add_argument("--reduced-resolution-t", type=int, default=1)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--out-dir", default=str(ROOT / "results"))
    args = ap.parse_args()

    torch.manual_seed(args.seed)
    np.random.seed(args.seed)

    data, grid = load_dataset(Path(args.data), args.reduced_resolution, args.reduced_resolution_t)
    print(f"data shape (b, x, t, ch) = {tuple(data.shape)}; grid {tuple(grid.shape)}")
    b, nx, nt, nc = data.shape

    train, val, test = split(data, args.n_train, args.n_val)
    print(f"train {train.shape[0]}, val {val.shape[0]}, test {test.shape[0]}")

    initial_step = args.initial_step
    assert nt > initial_step + 1, "need at least initial_step + 1 frames"

    device = torch.device(args.device)
    model = FNO1d(num_channels=nc, modes=args.modes, width=args.width, initial_step=initial_step).to(device)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"FNO1d params = {n_params}  (modes={args.modes}, width={args.width})")

    opt = torch.optim.Adam(model.parameters(), lr=args.lr)
    sched = torch.optim.lr_scheduler.StepLR(opt, step_size=max(1, args.epochs // 5), gamma=0.5)
    loss_fn = torch.nn.MSELoss()

    grid_dev = grid.to(device)

    def teacher_forced_loss(batch_data):
        """One-step prediction loss across all valid (t-step) transitions."""
        # batch_data: (b, x, t, ch)
        bsz = batch_data.shape[0]
        # Predict y_{t+1} given last initial_step frames ending at t
        # PDEBench layout: x_input = concat of last `initial_step` frames -> shape (b, x, initial_step * ch)
        losses = []
        # randomly choose a step per batch for speed (akin to pushforward sampling)
        for _ in range(4):  # 4 random anchor steps per batch
            t = torch.randint(initial_step - 1, nt - 1, (1,)).item()
            ctx = batch_data[:, :, t - initial_step + 1: t + 1, :]   # (b, x, initial_step, ch)
            ctx = ctx.reshape(bsz, nx, initial_step * nc)
            grid_b = grid_dev.unsqueeze(0).expand(bsz, -1, -1)
            pred = model(ctx, grid_b)                                # (b, x, 1, ch)
            target = batch_data[:, :, t + 1:t + 2, :]
            losses.append(loss_fn(pred, target))
        return sum(losses) / len(losses)

    def autoregressive_rollout(batch_data):
        """Roll out full trajectory from initial_step context; return prediction tensor."""
        bsz = batch_data.shape[0]
        pred_full = batch_data.clone()
        grid_b = grid_dev.unsqueeze(0).expand(bsz, -1, -1)
        with torch.no_grad():
            for t in range(initial_step - 1, nt - 1):
                ctx = pred_full[:, :, t - initial_step + 1: t + 1, :]
                ctx = ctx.reshape(bsz, nx, initial_step * nc)
                step = model(ctx, grid_b)                            # (b, x, 1, ch)
                pred_full[:, :, t + 1:t + 2, :] = step
        return pred_full

    @torch.no_grad()
    def eval_set(data_set):
        model.eval()
        loader = make_loader(data_set, args.batch_size, shuffle=False)
        all_pred, all_tgt = [], []
        for (batch_data,) in loader:
            batch_data = batch_data.to(device)
            pred = autoregressive_rollout(batch_data)
            all_pred.append(pred.cpu())
            all_tgt.append(batch_data.cpu())
        pred = torch.cat(all_pred, dim=0)
        tgt = torch.cat(all_tgt, dim=0)
        rmse, nrmse, csv_err, mx, bd, fer = metric_func(
            pred, tgt, if_mean=True, Lx=1.0, initial_step=initial_step
        )
        # rmse shape: (nc, nt-initial_step); take time-mean for single number
        rmse_scalar = float(rmse.mean().cpu())
        nrmse_scalar = float(nrmse.mean().cpu())
        return rmse_scalar, nrmse_scalar, pred, tgt

    history = {"train_loss": [], "val_rmse": [], "val_nrmse": [], "time_s": []}
    train_loader = make_loader(train, args.batch_size, shuffle=True)

    t0 = time.time()
    for ep in range(args.epochs):
        model.train()
        ep_loss = 0.0
        nb_batches = 0
        for (batch_data,) in train_loader:
            batch_data = batch_data.to(device)
            opt.zero_grad()
            loss = teacher_forced_loss(batch_data)
            loss.backward()
            opt.step()
            ep_loss += float(loss.detach())
            nb_batches += 1
        sched.step()
        ep_loss /= max(1, nb_batches)

        val_rmse, val_nrmse, *_ = eval_set(val)
        history["train_loss"].append(ep_loss)
        history["val_rmse"].append(val_rmse)
        history["val_nrmse"].append(val_nrmse)
        history["time_s"].append(time.time() - t0)
        print(f"ep {ep+1:3d}/{args.epochs}  train_loss={ep_loss:.4e}  val_RMSE={val_rmse:.4e}  val_nRMSE={val_nrmse:.4e}  t={history['time_s'][-1]:.1f}s")

    # Final test evaluation
    test_rmse, test_nrmse, test_pred, test_tgt = eval_set(test)
    print(f"\nFINAL TEST  RMSE={test_rmse:.4e}  nRMSE={test_nrmse:.4e}")

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    summary = {
        "data_file": args.data,
        "data_shape_bxtc": list(data.shape),
        "n_train": args.n_train, "n_val": args.n_val, "n_test": int(test.shape[0]),
        "initial_step": initial_step, "modes": args.modes, "width": args.width,
        "epochs": args.epochs, "batch_size": args.batch_size, "lr": args.lr,
        "model_params": int(n_params),
        "final_test_RMSE": test_rmse, "final_test_nRMSE": test_nrmse,
        "history": history,
        "device": str(device),
    }
    with open(out / "fno_advection_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    np.save(out / "fno_advection_test_pred.npy", test_pred.numpy())
    np.save(out / "fno_advection_test_tgt.npy", test_tgt.numpy())
    print(f"wrote {out/'fno_advection_summary.json'}")


if __name__ == "__main__":
    main()

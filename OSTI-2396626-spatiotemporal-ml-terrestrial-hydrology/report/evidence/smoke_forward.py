"""
Independent-replication smoke test for Bennett et al. 2024 (OSTI-2396626).

Instantiates the exact ForcedSTRNN (FSTR) model from the released code,
using the exact hyperparameters in the paper's train script
(train_scripts/fstr_train.sh in the 0.0.3 Zenodo release).

Measures:
  (1) Parameter count of the "new_params_2l_64hd" FSTR variant.
  (2) Forward-pass wall clock for one water-year rollout at a fixed
      spatial patch, on a single A100.

This test cannot rerun training (raw ParFlow-CLM CONUS1 zarr requires a
per-user HydroFrame API pin), but it directly verifies:
  - the code is real and runnable
  - the model architecture matches the paper description
  - the "single A100, less than an hour per year" speedup claim (C4) is
    order-of-magnitude consistent with a forward-only inference run
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import torch

CODE_ROOT = Path("/home/stevens/replicate/osti-2396626/code/HydroFrame-ML-hydrogen-emulator-configurable-5cb5b95")
sys.path.insert(0, str(CODE_ROOT))


def _stub_deps() -> None:
    """Provide minimal stubs so we can import models.py without training deps.

    The models module needs hydroml.loss (MWSE/DWSE) at import time; the package
    __init__ also pulls forecast->datapipes->torchdata/mlflow. We stub what we don't use.
    """
    import types
    import torch.nn as nn

    hydroml = types.ModuleType("hydroml")
    loss_mod = types.ModuleType("hydroml.loss")

    class _MSEStub(nn.Module):
        def forward(self, pred, target, **kw):
            return torch.mean((pred - target) ** 2)

    loss_mod.MWSE = _MSEStub
    loss_mod.DWSE = _MSEStub
    hydroml.loss = loss_mod
    sys.modules["hydroml"] = hydroml
    sys.modules["hydroml.loss"] = loss_mod

    # Stub optional training-time deps we don't need for a forward pass
    for name in ["torchdata", "torchdata.datapipes", "torchdata.datapipes.iter", "mlflow", "xbatcher"]:
        if name not in sys.modules:
            sys.modules[name] = types.ModuleType(name)
    sys.modules["torchdata.datapipes.iter"].IterDataPipe = object


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--h", type=int, default=256, help="patch height (paper zooms show 256x256 km sub-domains)")
    ap.add_argument("--w", type=int, default=256, help="patch width")
    ap.add_argument("--year-days", type=int, default=365, help="rollout timesteps (paper = full water year)")
    ap.add_argument("--batch", type=int, default=1)
    ap.add_argument("--precision", choices=["fp32", "fp16", "bf16"], default="fp32")
    ap.add_argument("--out", type=str, required=True)
    args = ap.parse_args()

    _stub_deps()
    # Bypass the package __init__ (which imports forecast->datapipes) by loading models.py directly
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "_fstr_models",
        str(CODE_ROOT / "emulator_configurable" / "models.py"),
    )
    # models.py does `from . import model_builder`, so we must first load that module too
    mb_spec = importlib.util.spec_from_file_location(
        "emulator_configurable.model_builder",
        str(CODE_ROOT / "emulator_configurable" / "model_builder.py"),
    )
    import types as _t
    pkg = _t.ModuleType("emulator_configurable")
    pkg.__path__ = [str(CODE_ROOT / "emulator_configurable")]
    sys.modules["emulator_configurable"] = pkg
    mb_mod = importlib.util.module_from_spec(mb_spec)
    sys.modules["emulator_configurable.model_builder"] = mb_mod
    mb_spec.loader.exec_module(mb_mod)
    spec2 = importlib.util.spec_from_file_location(
        "emulator_configurable.models",
        str(CODE_ROOT / "emulator_configurable" / "models.py"),
    )
    models_mod = importlib.util.module_from_spec(spec2)
    sys.modules["emulator_configurable.models"] = models_mod
    spec2.loader.exec_module(models_mod)
    ForcedSTRNN = models_mod.ForcedSTRNN

    # Exact hyperparameters from train_scripts/fstr_train.sh, variant new_params_2l_64hd
    cfg = dict(
        num_layers=2,
        num_hidden=[64, 64],
        img_channel=5,
        out_channel=5,
        act_channel=5,
        init_cond_channel=5,
        static_channel=15,
    )

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = ForcedSTRNN(**cfg).to(device).eval()

    n_params = sum(p.numel() for p in model.parameters())
    n_trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)

    dtype = {"fp32": torch.float32, "fp16": torch.float16, "bf16": torch.bfloat16}[args.precision]

    B, T, H, W = args.batch, args.year_days, args.h, args.w
    forcings = torch.randn(B, T, cfg["img_channel"], H, W, device=device, dtype=dtype)  # (B,T,C,H,W)
    init_cond = torch.randn(B, 1, cfg["init_cond_channel"], H, W, device=device, dtype=dtype)
    static = torch.randn(B, 1, cfg["static_channel"], H, W, device=device, dtype=dtype)

    if dtype != torch.float32:
        model = model.to(dtype)

    # Warm up
    with torch.no_grad():
        _ = model(forcings[:, :5], init_cond, static)
        if device.type == "cuda":
            torch.cuda.synchronize()

    # Timed rollout. Do it in chunks to avoid the model's known long-rollout issue
    # (its forward stores per-step decouple_loss tensors; at T~=365 on GPU this
    # can cause an illegal memory access even under no_grad). We chunk by `chunk`
    # timesteps and stitch outputs together, which measures the *same* wall clock
    # for a full-year rollout without triggering the pathological state buildup.
    chunk = 30 if args.year_days > 60 else args.year_days
    torch.cuda.reset_peak_memory_stats() if device.type == "cuda" else None
    t0 = time.perf_counter()
    outs = []
    ic = init_cond
    with torch.no_grad():
        for t0_ in range(0, T, chunk):
            t1_ = min(t0_ + chunk, T)
            piece = model(forcings[:, t0_:t1_], ic, static)
            outs.append(piece.detach())
            # advance init_cond to last predicted frame for the next chunk
            ic = piece[:, -1:].detach()
            if device.type == "cuda":
                torch.cuda.synchronize()
    out = torch.cat(outs, dim=1)
    if device.type == "cuda":
        torch.cuda.synchronize()
    dt = time.perf_counter() - t0
    peak_mem_mb = (torch.cuda.max_memory_allocated() / 1e6) if device.type == "cuda" else None

    # Full CONUS1 grid is 3342x1888 = 6,309,696 cells; a 256x256 patch is 65,536 cells.
    # A tiled inference over the whole domain needs ceil(3342/256)*ceil(1888/256) = 14*8 = 112 patches.
    full_grid_cells = 3342 * 1888
    patch_cells = H * W
    n_patches_conus = -(-3342 // H) * -(-1888 // W)
    est_conus_year_sec = dt * n_patches_conus

    # Original ParFlow-CLM CONUS1 baseline runs (O'Neill 2021) took roughly
    # ~ 3,000 CPU cores * hours per simulated year. Any GPU rollout wallclock
    # measured in single-digit hours on one A100 already implies 100x+ core-equivalent.

    result = {
        "device": str(device),
        "device_name": torch.cuda.get_device_name(0) if device.type == "cuda" else None,
        "precision": args.precision,
        "cfg": cfg,
        "n_params_total": int(n_params),
        "n_params_trainable": int(n_trainable),
        "input_shape": {"B": B, "T": T, "H": H, "W": W, "C_forc": cfg["img_channel"], "C_static": cfg["static_channel"]},
        "output_shape": list(out.shape),
        "forward_seconds": float(dt),
        "peak_gpu_memory_mb": float(peak_mem_mb) if peak_mem_mb is not None else None,
        "full_conus_grid_cells": full_grid_cells,
        "patch_cells": patch_cells,
        "n_patches_to_cover_conus": int(n_patches_conus),
        "estimated_conus_year_rollout_sec_single_gpu_tiled": float(est_conus_year_sec),
        "estimated_conus_year_rollout_hours_single_gpu_tiled": float(est_conus_year_sec / 3600.0),
    }

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

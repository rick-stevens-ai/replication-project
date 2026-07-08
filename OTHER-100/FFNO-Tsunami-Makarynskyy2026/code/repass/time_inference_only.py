#!/usr/bin/env python
"""
Compute-only inference timing for the F-FNO Selected checkpoint.

Loosely mirrors Table 4 of Kim et al. 2026: file I/O excluded, autoregressive
rollout times averaged over post-warm-up repetitions.

Procedure:
    1. Load Selected_10L_cont10_dc100.pt once (one-time cost not counted).
    2. For each of K = 3 cases, preload the NetCDF history & bathymetry to CPU,
       move tensors to GPU (one-time per case), and time ONLY the autoregressive
       rollout loop (200 forward_step calls) — wrapped in torch.cuda.synchronize
       before and after.
    3. Repeat each case 3 times, discard the first (warm-up), report mean ± std
       across the remaining 2 × K = 6 runs.

Run on uicgpu:
    CUDA_VISIBLE_DEVICES=2 /data/stevens/CAMELS/.venv/bin/python \
        /data/stevens/tsunami/code/repass/time_inference_only.py \
        --ckpt /data/stevens/tsunami/code/weights/Selected_10L_cont10_dc100.pt \
        --cases /data/stevens/tsunami/data/Test-EM/Case6T1D1L1M4ML10.nc \
                /data/stevens/tsunami/data/Test-EM/Case6T3D2L2M4ML10.nc \
                /data/stevens/tsunami/data/Test-EM/Case6T5D1L1M4ML10.nc \
        --reps 3 \
        --out /data/stevens/tsunami/results_reference/timing_inference_only.json
"""
import argparse
import json
import os
import statistics
import sys
import time

import numpy as np
import torch
import xarray as xr

# Make the authors' inference module importable
sys.path.insert(0, "/data/stevens/tsunami/code")
import inference as INF  # type: ignore


def time_one_case(model, normalizer, depth_mean, depth_std, ckpt_cfg, device,
                  nc_path, seq_len=10, horizon=200, amp=True, reps=3):
    """Return per-rep wall-clock seconds for the autoregressive rollout only."""
    # --- Preload (NOT timed) ---
    ds = xr.open_dataset(nc_path, engine="netcdf4")
    eta = INF._read_3d_tyx(ds, "eta").astype(np.float32)
    u   = INF._read_3d_tyx(ds, "u").astype(np.float32)
    v   = INF._read_3d_tyx(ds, "v").astype(np.float32)
    primary = str(ckpt_cfg.get("DEPTH_VAR_NAME", "h"))
    fallbacks = ckpt_cfg.get("DEPTH_VAR_FALLBACKS", ("depth", "bathymetry", "bathy"))
    if isinstance(fallbacks, list): fallbacks = tuple(fallbacks)
    depth_var = INF._find_var_with_fallbacks(ds, primary=primary, fallbacks=fallbacks)
    h_da = ds[depth_var]
    if h_da.ndim == 3:
        h_da = h_da.isel(time=0) if "time" in h_da.dims else h_da.isel({h_da.dims[0]: 0})
    depth = h_da.transpose("y", "x").to_numpy().astype(np.float32)
    x_1d = np.asarray(ds["x"].to_numpy(), dtype=np.float64).ravel()
    y_1d = np.asarray(ds["y"].to_numpy(), dtype=np.float64).ravel()
    ds.close()

    T, H, W = eta.shape
    HW = int(H * W)
    eta0_2d = eta[0].astype(np.float32)
    wet_mask2d = np.isfinite(eta0_2d)
    # No depth_min applied here (matches default CLI of pass-1 run)
    mask_flat = INF.mask_flat_from_wet(wet_mask2d)
    lon2d_full, lat2d_full = INF.build_lonlat_2d_from_xy_1d(x_1d, y_1d)

    t0 = 0
    # Build initial history
    x_seq = np.zeros((seq_len, 3, HW), dtype=np.float32)
    for t in range(seq_len):
        a3 = np.stack([eta[t0 + t], u[t0 + t], v[t0 + t]], axis=0).astype(np.float32)
        x_seq[t] = INF.pack_3ch_full_flat(a3, mask_flat)
    x_seq_t = torch.from_numpy(x_seq).unsqueeze(0).to(device)  # (1,seq_len,3,HW)

    d2d = depth.astype(np.float32)
    if depth_mean is not None and depth_std is not None:
        d2d = (d2d - float(depth_mean)) / float(depth_std)
    depth_t = torch.from_numpy(d2d).to(device)
    lat_t = torch.from_numpy(lat2d_full.astype(np.float32)).to(device)
    lon_t = torch.from_numpy(lon2d_full.astype(np.float32)).to(device)
    mask_flat_t = torch.from_numpy(mask_flat).to(device).bool()
    hw = (int(H), int(W))

    if normalizer is not None:
        x_seq_tn = normalizer.encode_seq_flat(x_seq_t)
    else:
        x_seq_tn = x_seq_t

    amp_enabled = bool(amp and device.type == "cuda")
    amp_dtype = INF._select_amp_dtype(ckpt_cfg=ckpt_cfg)

    rep_times = []
    for r in range(reps):
        # Rebuild hidden state per rep (Selected is FFNO-only -> no hidden state needed,
        # but keep symmetry with paper protocol of fresh rollouts).
        hcs = None
        is_recurrent = hasattr(model, "lstm") and (getattr(model, "lstm") is not None)
        if is_recurrent:
            for t in range(seq_len):
                x_step = x_seq_tn[:, t]
                with INF.autocast_ctx(device, enabled=amp_enabled, dtype=amp_dtype):
                    _, hcs = model.forward_step(
                        x_step_flat=x_step, mask_flat=mask_flat_t, hw=hw,
                        hcs=hcs, depth_2d=depth_t, lat_2d=lat_t, lon_2d=lon_t,
                    )
        x_last = x_seq_tn[:, seq_len - 1].clone()

        # ---- TIMED REGION (rollout only) ----
        torch.cuda.synchronize() if device.type == "cuda" else None
        t_start = time.perf_counter()
        with torch.inference_mode():
            for k in range(horizon):
                with INF.autocast_ctx(device, enabled=amp_enabled, dtype=amp_dtype):
                    y_step, hcs = model.forward_step(
                        x_step_flat=x_last, mask_flat=mask_flat_t, hw=hw,
                        hcs=hcs, depth_2d=depth_t, lat_2d=lat_t, lon_2d=lon_t,
                    )
                x_last = y_step
        torch.cuda.synchronize() if device.type == "cuda" else None
        t_end = time.perf_counter()
        # ---- END TIMED REGION ----
        rep_times.append(t_end - t_start)
        print(f"  {os.path.basename(nc_path)}  rep {r}: {t_end - t_start:.3f}s", flush=True)
    return rep_times


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--cases", nargs="+", required=True)
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[INFO] device={device}, gpu={torch.cuda.get_device_name(0) if device.type=='cuda' else 'cpu'}")

    # Load checkpoint via the authors' helpers
    ckpt = INF.torch_load_ckpt_safe(args.ckpt, map_location=device, allow_unsafe_full_load=True)
    model, ckpt_cfg = INF.build_model_from_ckpt(ckpt, device)
    normalizer, depth_mean, depth_std = INF.build_normalizer_from_ckpt(ckpt, ckpt_cfg, device)
    model.eval()

    results = {
        "device": str(device),
        "gpu_name": torch.cuda.get_device_name(0) if device.type == "cuda" else None,
        "ckpt": args.ckpt,
        "horizon": 200,
        "seq_len": 10,
        "amp": True,
        "per_case": {},
    }
    all_post_warmup = []
    for case in args.cases:
        rep_times = time_one_case(
            model, normalizer, depth_mean, depth_std, ckpt_cfg, device,
            case, seq_len=10, horizon=200, amp=True, reps=args.reps,
        )
        post_warmup = rep_times[1:]  # discard first as warm-up
        results["per_case"][os.path.basename(case)] = {
            "all_reps_sec": rep_times,
            "warmup_discarded": rep_times[0],
            "post_warmup_sec": post_warmup,
            "post_warmup_mean": statistics.mean(post_warmup) if post_warmup else None,
        }
        all_post_warmup.extend(post_warmup)

    results["summary"] = {
        "n_post_warmup_runs": len(all_post_warmup),
        "mean_sec": statistics.mean(all_post_warmup),
        "std_sec":  statistics.pstdev(all_post_warmup),
        "min_sec":  min(all_post_warmup),
        "max_sec":  max(all_post_warmup),
    }

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print("\n=== SUMMARY ===")
    print(json.dumps(results["summary"], indent=2))
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()

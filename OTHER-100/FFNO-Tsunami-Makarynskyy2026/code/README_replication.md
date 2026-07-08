# F-FNO Tsunami Replication — Code Notes

## Source

All code comes from the official Zenodo archive:
- https://zenodo.org/records/19198928

Files in `/data/stevens/tsunami/code/` on uicgpu:
- `inference.py` — full autoregressive rollout inference + metric computation
- `train.py` — training pipeline (not used; pretrained weights used)
- `weights/Selected_10L_cont10_dc100.pt` — pretrained Selected model (10 layers, λcont=10, λdc=100)
- `weights/Reference_8L_cont05_dc100.pt` — pretrained Reference model
- `splits/split_testEM_case6_onlyM4.txt` — 54 Test-EM filenames

## Inference Command Used

```bash
/data/stevens/CAMELS/.venv/bin/python inference.py \
    --ckpt weights/Selected_10L_cont10_dc100.pt \
    --test_list_txt splits/split_testEM_case6_onlyM4.txt \
    --data_root /data/stevens/tsunami/data/Test-EM/ffno-tsunami-Test-EM-data \
    --outdir /data/stevens/tsunami/results \
    --device cuda \
    --amp \
    --seq_len 10 \
    --horizon 200 \
    --make_fig1_all_buoys \
    --fig1_aggregated \
    --buoy_mode fixed \
    --buoy_epicenters '40.9,138.9;40.2,138.7;39.0,138.0;38.3,137.7' \
    --buoy_target_lat 37.1 \
    --buoy_target_lon 129.39 \
    --buoy_fixed_dists_km 80 160 240 320 400 480 560 640 720 \
    --snapshot_n_frames 6
```

## Environment

- Python 3.11.15 (CAMELS venv)
- PyTorch 2.5.1+cu121
- CUDA 12.1, 8× A100 80GB (uicgpu)
- xarray 2026.4.0, numpy 2.4.6, scipy, matplotlib, netCDF4

## Model Architecture (from checkpoint config)

- F-FNO: 10 FNO layers, width=64, modes=(256,256)
- Input: η (sea-surface elevation) + u, v (depth-averaged velocity) + h (bathymetry)
- Coordinate channels: sin/cos encoding (4 channels)
- Total encoder channels: 8 (3 state + 1 bathymetry + 4 coord)
- Grid: 695×556 (East Sea / Sea of Japan)
- DT: 60 s/step

## Metrics Computed

- **RMSEη**: Root mean square error of sea-surface elevation over wet cells, all time steps
- **ATE**: Absolute arrival time error at virtual buoys (minutes)
- **BEE**: Band energy fraction error (spectral metric)
- **RMSEavg**: Mean RMSE over η, u, v channels
